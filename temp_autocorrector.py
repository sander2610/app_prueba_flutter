class AutoCorrector:
    def __init__(self):
        self.backup_dir = Path.cwd() / ".flutterfix_backups"
        self.backup_dir.mkdir(exist_ok=True)
    
    def hacer_backup(self, archivo: str) -> Path:
        archivo_path = Path(archivo)
        if not archivo_path.exists():
            return None
        backup_path = self.backup_dir / f"{archivo_path.name}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
        shutil.copy2(archivo_path, backup_path)
        return backup_path
    
    def modificar_pubspec(self, paquete: str, nueva_version: str) -> bool:
        pubspec_path = Path.cwd() / "pubspec.yaml"
        if not pubspec_path.exists():
            return False
        self.hacer_backup(pubspec_path)
        with open(pubspec_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        # Buscar línea con el paquete (más flexible)
        lineas = contenido.split('\n')
        nuevas_lineas = []
        modificado = False
        for linea in lineas:
            if paquete in linea and ':' in linea and not linea.strip().startswith('#'):
                nueva_linea = f"  {paquete}: {nueva_version}"
                nuevas_lineas.append(nueva_linea)
                modificado = True
            else:
                nuevas_lineas.append(linea)
        if modificado:
            with open(pubspec_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(nuevas_lineas))
        return modificado
    
    def modificar_gradle(self, viejo_texto: str, nuevo_texto: str) -> bool:
        gradle_path = Path.cwd() / "android" / "build.gradle"
        gradle_kts_path = Path.cwd() / "android" / "build.gradle.kts"
        archivo_gradle = gradle_kts_path if gradle_kts_path.exists() else gradle_path if gradle_path.exists() else None
        if not archivo_gradle:
            return False
        self.hacer_backup(archivo_gradle)
        with open(archivo_gradle, 'r', encoding='utf-8') as f:
            contenido = f.read()
        if viejo_texto in contenido:
            nuevo_contenido = contenido.replace(viejo_texto, nuevo_texto)
            with open(archivo_gradle, 'w', encoding='utf-8') as f:
                f.write(nuevo_contenido)
            return True
        return False
    
    def ejecutar_comando(self, comando: str, cwd: str = None) -> Dict:
        try:
            resultado = subprocess.run(
                comando,
                shell=True,
                cwd=cwd or Path.cwd(),
                capture_output=True,
                text=True,
                timeout=60
            )
            return {"exito": resultado.returncode == 0, "salida": resultado.stdout, "error": resultado.stderr}
        except Exception as e:
            return {"exito": False, "error": str(e)}
    
    def auto_fix_gradle_incompatibilidad(self) -> bool:
        print("🔧 Auto-corrigiendo error de Gradle...")
        cambios_realizados = []
        
        # 1. Actualizar app_links en pubspec.yaml
        print("  📝 Actualizando pubspec.yaml...")
        if self.modificar_pubspec("app_links", "^8.0.2"):
            cambios_realizados.append("app_links actualizado a ^8.0.2")
            print("     ✅ app_links actualizado")
        else:
            print("     ⚠️ No se encontró app_links en pubspec.yaml")
        
        # 2. Actualizar AGP en build.gradle
        print("  📝 Actualizando build.gradle...")
        viejo_agp = 'com.android.tools.build:gradle:7'
        nuevo_agp = 'com.android.tools.build:gradle:8.1.0'
        if self.modificar_gradle(viejo_agp, nuevo_agp):
            cambios_realizados.append("AGP actualizado a 8.1.0")
            print("     ✅ AGP actualizado")
        else:
            print("     ⚠️ No se encontró AGP versión 7.x")
        
        # 3. Ejecutar flutter clean
        print("  🧹 Ejecutando flutter clean...")
        clean = self.ejecutar_comando("flutter clean")
        if clean["exito"]:
            cambios_realizados.append("flutter clean ejecutado")
            print("     ✅ flutter clean completado")
        else:
            print(f"     ⚠️ Error: {clean['error'][:100]}")
        
        # 4. Ejecutar flutter pub get
        print("  📦 Ejecutando flutter pub get...")
        pubget = self.ejecutar_comando("flutter pub get")
        if pubget["exito"]:
            cambios_realizados.append("flutter pub get ejecutado")
            print("     ✅ flutter pub get completado")
        else:
            print(f"     ⚠️ Error: {pubget['error'][:100]}")
        
        # 5. Verificar si se resolvió
        print("  🔍 Verificando corrección...")
        test = self.ejecutar_comando("flutter build apk --dry-run")
        if test["exito"]:
            print("     ✅ ¡Error corregido exitosamente!")
            return True
        else:
            print(f"     ⚠️ Aún hay errores: {test['error'][:200]}")
            return False
