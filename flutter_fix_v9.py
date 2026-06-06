import json
import re
import os
import sqlite3
import subprocess
import shutil
import threading
import time
import queue
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pathlib import Path
import hashlib
import urllib.request
import urllib.error

# ============================================
# CONFIGURACIÓN
# ============================================

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
AUTO_FIX = True
MONITOR_REAL_TIME = True

# ============================================
# MONITOREO EN TIEMPO REAL
# ============================================

class MonitorTiempoReal:
    def __init__(self):
        self.proceso = None
        self.cola_logs = queue.Queue()
        self.corriendo = False
        self.errores_detectados = []
        self.auto_corrector = None
        
    def verificar_dispositivos(self) -> List[str]:
        """Verifica dispositivos Android conectados"""
        try:
            resultado = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
            lineas = resultado.stdout.split('\n')[1:]
            dispositivos = []
            for linea in lineas:
                if 'device' in linea and 'offline' not in linea:
                    dispositivo = linea.split('\t')[0].strip()
                    if dispositivo:
                        dispositivos.append(dispositivo)
            return dispositivos
        except:
            return []
    
    def capturar_logs(self):
        """Captura logs en tiempo real del dispositivo"""
        try:
            # Limpiar logs anteriores
            subprocess.run("adb logcat -c", shell=True, capture_output=True)
            
            # Iniciar captura de logs
            proceso_logs = subprocess.Popen(
                "adb logcat -v time *:E",  # Solo errores
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            while self.corriendo:
                linea = proceso_logs.stdout.readline()
                if linea:
                    self.cola_logs.put(linea)
                    if self._es_error_relevante(linea):
                        self.errores_detectados.append({
                            "timestamp": datetime.now().isoformat(),
                            "error": linea.strip(),
                            "procesado": False
                        })
                        print(f"⚠️ Error detectado: {linea[:100]}...")
                        
        except Exception as e:
            print(f"Error en captura de logs: {e}")
    
    def _es_error_relevante(self, linea: str) -> bool:
        """Filtra errores relevantes"""
        patrones_error = [
            r"FATAL EXCEPTION",
            r"AndroidRuntime",
            r"NullPointerException",
            r"RangeError",
            r"SQLiteException",
            r"MissingPluginException",
            r"setState.*called after dispose"
        ]
        return any(re.search(p, linea, re.IGNORECASE) for p in patrones_error)
    
    def iniciar_app(self, auto_corrector) -> bool:
        """Inicia la app Flutter en el dispositivo"""
        self.auto_corrector = auto_corrector
        dispositivos = self.verificar_dispositivos()
        
        if not dispositivos:
            print("❌ No hay dispositivos conectados")
            print("   Conecta un celular por USB y activa depuración USB")
            return False
        
        print(f"✅ Dispositivo conectado: {dispositivos[0]}")
        print("🚀 Iniciando app...")
        
        # Iniciar la app
        self.proceso = subprocess.Popen(
            "flutter run",
            shell=True,
            cwd=Path.cwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Iniciar captura de logs
        self.corriendo = True
        hilo_logs = threading.Thread(target=self.capturar_logs, daemon=True)
        hilo_logs.start()
        
        # Hilo para procesar errores en tiempo real
        hilo_procesador = threading.Thread(target=self.procesar_errores_tiempo_real, daemon=True)
        hilo_procesador.start()
        
        return True
    
    def procesar_errores_tiempo_real(self):
        """Procesa errores automáticamente cuando aparecen"""
        while self.corriendo:
            if self.errores_detectados:
                for error in self.errores_detectados:
                    if not error["procesado"]:
                        print(f"\n🔧 Procesando error en tiempo real...")
                        # Analizar error
                        from ParserEntrada import ParserEntrada
                        parser = ParserEntrada()
                        entrada = parser.parsear(error["error"])
                        
                        # Auto-corregir
                        if self.auto_corrector and AUTO_FIX:
                            resultado = self.auto_corrector.auto_fix_por_categoria(entrada["categoria"])
                            if resultado:
                                print("✅ Error corregido automáticamente")
                                print("🔄 Reiniciando app...")
                                self.reiniciar_app()
                        
                        error["procesado"] = True
            time.sleep(2)
    
    def reiniciar_app(self):
        """Reinicia la app después de una corrección"""
        if self.proceso:
            self.proceso.terminate()
            time.sleep(2)
        
        # Recompilar
        subprocess.run("flutter clean", shell=True, capture_output=True)
        subprocess.run("flutter pub get", shell=True, capture_output=True)
        
        # Reiniciar
        self.iniciar_app(self.auto_corrector)
    
    def detener(self):
        """Detiene el monitoreo"""
        self.corriendo = False
        if self.proceso:
            self.proceso.terminate()

# ============================================
# AUTO-CORRECTOR MEJORADO
# ============================================

class AutoCorrector:
    def __init__(self):
        self.backup_dir = Path.cwd() / ".flutterfix_backups"
        self.backup_dir.mkdir(exist_ok=True)
        self.cambios_realizados = []
    
    def hacer_backup(self, archivo: str) -> Path:
        archivo_path = Path(archivo)
        if not archivo_path.exists():
            return None
        backup_path = self.backup_dir / f"{archivo_path.name}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
        shutil.copy2(archivo_path, backup_path)
        return backup_path
    
    def auto_fix_por_categoria(self, categoria: str) -> bool:
        """Aplica auto-corrección según la categoría del error"""
        if categoria == "gradle_agp_incompatibilidad":
            return self.auto_fix_gradle_incompatibilidad()
        elif categoria == "null_pointer":
            return self.auto_fix_null_pointer()
        elif categoria == "plugin_incompatible":
            return self.auto_fix_plugin()
        elif categoria == "error_compilacion_gradle":
            return self.auto_fix_gradle_clean()
        else:
            print(f"⚠️ No hay auto-corrección para {categoria}")
            return False
    
    def auto_fix_gradle_incompatibilidad(self) -> bool:
        print("🔧 Auto-corrigiendo error de Gradle...")
        self.cambios_realizados = []
        
        # 1. Actualizar app_links
        if self.modificar_pubspec("app_links", "^8.0.2"):
            self.cambios_realizados.append("app_links actualizado")
        
        # 2. Actualizar AGP
        viejo_agp = 'com.android.tools.build:gradle:7'
        nuevo_agp = 'com.android.tools.build:gradle:8.1.0'
        if self.modificar_gradle(viejo_agp, nuevo_agp):
            self.cambios_realizados.append("AGP actualizado")
        
        # 3. Limpiar y reconstruir
        subprocess.run("flutter clean", shell=True, capture_output=True)
        subprocess.run("flutter pub get", shell=True, capture_output=True)
        
        print(f"✅ Realizados {len(self.cambios_realizados)} cambios")
        return len(self.cambios_realizados) > 0
    
    def auto_fix_null_pointer(self) -> bool:
        print("🔧 Auto-corrigiendo Null Pointer...")
        # Buscar archivos con ! y sugerir cambio
        archivos_dart = list(Path.cwd().rglob("*.dart"))
        for archivo in archivos_dart[:5]:  # Limitar a 5 archivos
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            if re.search(r'\w+\!\.', contenido):
                self.hacer_backup(archivo)
                # Reemplazar !. por ?.
                nuevo_contenido = re.sub(r'(\w+)\!\.', r'\1?.', contenido)
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(nuevo_contenido)
                self.cambios_realizados.append(f"Corregido null safety en {archivo.name}")
        return len(self.cambios_realizados) > 0
    
    def auto_fix_plugin(self) -> bool:
        print("🔧 Actualizando plugins...")
        subprocess.run("flutter pub upgrade", shell=True, capture_output=True)
        self.cambios_realizados.append("Plugins actualizados")
        return True
    
    def auto_fix_gradle_clean(self) -> bool:
        print("🔧 Limpiando Gradle...")
        subprocess.run("cd android && gradlew clean", shell=True, capture_output=True)
        subprocess.run("flutter clean", shell=True, capture_output=True)
        self.cambios_realizados.append("Cache de Gradle limpiado")
        return True
    
    def modificar_pubspec(self, paquete: str, nueva_version: str) -> bool:
        pubspec_path = Path.cwd() / "pubspec.yaml"
        if not pubspec_path.exists():
            return False
        self.hacer_backup(pubspec_path)
        with open(pubspec_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
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

# ============================================
# INTEGRACIÓN IA (simplificada)
# ============================================

class IAIntegracion:
    @staticmethod
    def sugerir_solucion(error: str, categoria: str) -> str:
        sugerencias = {
            "gradle_agp_incompatibilidad": "Actualizar app_links a ^8.0.2 y AGP a 8.1.0",
            "null_pointer": "Reemplazar '!' con '?.' o '??'",
            "plugin_incompatible": "Ejecutar 'flutter pub upgrade'",
            "error_compilacion_gradle": "Ejecutar 'flutter clean' y 'cd android && gradlew clean'"
        }
        return sugerencias.get(categoria, "Revisar documentación del error")

# ============================================
# PARSER
# ============================================

class ParserEntrada:
    @staticmethod
    def parsear(entrada: str) -> Dict:
        entrada_lower = entrada.lower()
        
        if "error" in entrada_lower or "exception" in entrada_lower or "crash" in entrada_lower:
            tipo = "error"
        elif "warning" in entrada_lower:
            tipo = "warning"
        else:
            tipo = "consulta"
        
        patrones = {
            r"defaultandroidsourceset.*cannot be cast": "gradle_agp_incompatibilidad",
            r"app_links.*incompatible": "plugin_incompatible",
            r"build failed|gradle task": "error_compilacion_gradle",
            r"null check|null value|null pointer": "null_pointer",
            r"rangeerror|index out": "indice_fuera_rango"
        }
        
        categoria = "general"
        for patron, cat in patrones.items():
            if re.search(patron, entrada_lower):
                categoria = cat
                break
        
        return {"tipo": tipo, "mensaje_original": entrada, "categoria": categoria}

# ============================================
# SISTEMA PRINCIPAL CON MONITOREO
# ============================================

class FlutterFixCascade:
    def __init__(self):
        self.parser = ParserEntrada()
        self.auto_corrector = AutoCorrector()
        self.monitor = MonitorTiempoReal()
        self.modo_monitoreo = False
    
    def iniciar_monitoreo(self):
        """Inicia el monitoreo en tiempo real"""
        print("=" * 60)
        print("🔍 FLUTTERFIX v9 - MODO MONITOREO EN TIEMPO REAL")
        print("=" * 60)
        
        if not self.monitor.iniciar_app(self.auto_corrector):
            print("❌ No se pudo iniciar la app")
            return
        
        self.modo_monitoreo = True
        print("\n✅ App ejecutándose...")
        print("📡 Monitoreando errores en tiempo real")
        print("   - Los errores se corregirán automáticamente")
        print("   - Presiona Ctrl+C para detener\n")
        
        try:
            while self.modo_monitoreo:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo monitoreo...")
            self.monitor.detener()
            print("✅ Monitoreo detenido")
    
    def procesar_entrada_manual(self, entrada_usuario: str) -> str:
        """Procesa errores manuales"""
        entrada = self.parser.parsear(entrada_usuario)
        
        # Auto-corregir si es posible
        if AUTO_FIX and entrada["categoria"] != "general":
            print(f"🔧 Auto-corrigiendo {entrada['categoria']}...")
            self.auto_corrector.auto_fix_por_categoria(entrada["categoria"])
        
        sugerencia = IAIntegracion.sugerir_solucion(entrada["mensaje_original"], entrada["categoria"])
        
        return f"""
{'='*60}
🤖 FLUTTERFIX v9 - RESULTADO
{'='*60}
📥 Error: {entrada['mensaje_original'][:100]}
📋 Categoría: {entrada['categoria']}

🤖 Solución sugerida:
   {sugerencia}

{'✅' if AUTO_FIX else '⚠️'} Modo auto-corrección: {'Activado' if AUTO_FIX else 'Desactivado'}
{'='*60}
"""

def main():
    print("=" * 60)
    print("🚀 FLUTTERFIX CASCADE v9 - MONITOREO EN TIEMPO REAL")
    print("=" * 60)
    print("\n¿Qué deseas hacer?")
    print("1. 🔍 Monitorear app en tiempo real (conecta tu celular)")
    print("2. 📝 Analizar errores manualmente")
    print("3. ❌ Salir")
    
    opcion = input("\n💡 Elige una opción (1, 2 o 3): ").strip()
    
    sistema = FlutterFixCascade()
    
    if opcion == "1":
        sistema.iniciar_monitoreo()
    elif opcion == "2":
        print("\n📝 Modo manual - Ingresa los errores que quieras analizar")
        print("   Escribe 'salir' para terminar\n")
        while True:
            error = input("💬 > ")
            if error.lower() == "salir":
                break
            print(sistema.procesar_entrada_manual(error))
    else:
        print("👋 Hasta luego!")

if __name__ == "__main__":
    main()
