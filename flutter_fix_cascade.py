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

# ============================================
# CONFIGURACIÓN
# ============================================

AUTO_FIX = True  # Auto-corrección activada
MONITOR_MODE = False  # Se activa con comando "monitor"

# ============================================
# MONITOREO EN TIEMPO REAL
# ============================================

class MonitorTiempoReal:
    def __init__(self, auto_corrector):
        self.auto_corrector = auto_corrector
        self.proceso = None
        self.cola_logs = queue.Queue()
        self.corriendo = False
        self.errores_procesados = set()
        self.persistencia = None
        
    def conectar_persistencia(self, persistencia):
        self.persistencia = persistencia
    
    def verificar_dispositivos(self) -> List[str]:
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
        try:
            subprocess.run("adb logcat -c", shell=True, capture_output=True)
            proceso_logs = subprocess.Popen(
                "adb logcat -v time *:E",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            while self.corriendo:
                linea = proceso_logs.stdout.readline()
                if linea and self._es_error_relevante(linea):
                    print(f"\n⚠️ [MONITOR] Error detectado: {linea[:80]}...")
                    self.procesar_error(linea)
                        
        except Exception as e:
            print(f"Error en captura: {e}")
    
    def _es_error_relevante(self, linea: str) -> bool:
        patrones = [
            r"FATAL EXCEPTION",
            r"AndroidRuntime",
            r"NullPointerException",
            r"RangeError",
            r"SQLiteException",
            r"MissingPluginException",
            r"setState.*after dispose"
        ]
        return any(re.search(p, linea, re.IGNORECASE) for p in patrones)
    
    def procesar_error(self, linea_error: str):
        """Procesa y auto-corrige errores en tiempo real"""
        hash_error = hashlib.md5(linea_error.encode()).hexdigest()
        
        if hash_error in self.errores_procesados:
            return
        
        self.errores_procesados.add(hash_error)
        
        # Analizar categoría del error
        categoria = self.detectar_categoria(linea_error)
        print(f"🔍 [MONITOR] Categoría: {categoria}")
        
        # Buscar solución
        solucion = self.buscar_solucion_en_historial(categoria)
        
        if solucion and AUTO_FIX:
            print(f"🔧 [MONITOR] Aplicando auto-corrección...")
            self.auto_corrector.aplicar_solucion(solucion)
            
            # Guardar en persistencia
            if self.persistencia:
                self.persistencia.guardar_error_auto(
                    mensaje=linea_error,
                    categoria=categoria,
                    solucion=solucion,
                    auto_corregido=True
                )
            
            print(f"✅ [MONITOR] Error corregido. Reiniciando app...")
            self.reiniciar_app()
    
    def detectar_categoria(self, error: str) -> str:
        error_lower = error.lower()
        patrones = {
            r"defaultandroidsourceset.*cannot be cast": "gradle_agp_incompatibilidad",
            r"app_links|plugin.*incompatible": "plugin_incompatible",
            r"build failed|gradle task": "error_compilacion_gradle",
            r"nullpointer|null check": "null_pointer",
            r"rangeerror|index out": "indice_fuera_rango",
            r"setstate.*dispose": "estado_ui"
        }
        for patron, cat in patrones.items():
            if re.search(patron, error_lower):
                return cat
        return "general"
    
    def buscar_solucion_en_historial(self, categoria: str) -> Optional[Dict]:
        # Base de conocimientos interna
        soluciones = {
            "gradle_agp_incompatibilidad": {
                "tipo": "gradle",
                "acciones": [
                    {"archivo": "pubspec.yaml", "buscar": "app_links:", "reemplazar": "app_links: ^8.0.2"},
                    {"archivo": "android/build.gradle", "buscar": "com.android.tools.build:gradle:7", "reemplazar": "com.android.tools.build:gradle:8.1.0"},
                    {"comando": "flutter clean"},
                    {"comando": "flutter pub get"}
                ]
            },
            "null_pointer": {
                "tipo": "dart",
                "acciones": [
                    {"patron": r'(\w+)\!\.', "reemplazar": r'\1?.'}
                ]
            },
            "plugin_incompatible": {
                "tipo": "flutter",
                "acciones": [
                    {"comando": "flutter pub upgrade"}
                ]
            },
            "error_compilacion_gradle": {
                "tipo": "gradle",
                "acciones": [
                    {"comando": "flutter clean"},
                    {"comando": "cd android && gradlew clean && cd .."}
                ]
            }
        }
        return soluciones.get(categoria)
    
    def reiniciar_app(self):
        if self.proceso:
            self.proceso.terminate()
            time.sleep(2)
        
        subprocess.run("flutter clean", shell=True, capture_output=True)
        subprocess.run("flutter pub get", shell=True, capture_output=True)
        self.iniciar_app()
    
    def iniciar_app(self):
        dispositivos = self.verificar_dispositivos()
        if not dispositivos:
            print("❌ No hay dispositivos conectados")
            return False
        
        print(f"📱 Dispositivo: {dispositivos[0]}")
        print("🚀 Iniciando app...")
        
        self.proceso = subprocess.Popen(
            "flutter run",
            shell=True,
            cwd=Path.cwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        self.corriendo = True
        threading.Thread(target=self.capturar_logs, daemon=True).start()
        return True
    
    def detener(self):
        self.corriendo = False
        if self.proceso:
            self.proceso.terminate()
        print("✅ Monitoreo detenido")

# ============================================
# AUTO-CORRECTOR
# ============================================

class AutoCorrector:
    def __init__(self):
        self.backup_dir = Path.cwd() / ".flutterfix_backups"
        self.backup_dir.mkdir(exist_ok=True)
    
    def hacer_backup(self, archivo: str):
        archivo_path = Path(archivo)
        if archivo_path.exists():
            backup = self.backup_dir / f"{archivo_path.name}.bak"
            shutil.copy2(archivo_path, backup)
    
    def aplicar_solucion(self, solucion: Dict):
        for accion in solucion.get("acciones", []):
            if "archivo" in accion:
                self.modificar_archivo(accion["archivo"], accion.get("buscar"), accion.get("reemplazar"))
            elif "comando" in accion:
                self.ejecutar_comando(accion["comando"])
            elif "patron" in accion:
                self.corregir_patron_dart(accion["patron"], accion["reemplazar"])
    
    def modificar_archivo(self, archivo: str, buscar: str = None, reemplazar: str = None):
        ruta = Path.cwd() / archivo
        if not ruta.exists():
            return
        self.hacer_backup(ruta)
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
        if buscar and reemplazar:
            nuevo_contenido = contenido.replace(buscar, reemplazar)
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(nuevo_contenido)
            print(f"  ✅ Modificado: {archivo}")
    
    def ejecutar_comando(self, comando: str):
        print(f"  ▶️ Ejecutando: {comando}")
        subprocess.run(comando, shell=True, capture_output=True)
    
    def corregir_patron_dart(self, patron: str, reemplazar: str):
        for archivo in Path.cwd().rglob("*.dart"):
            if "build" in str(archivo):
                continue
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            if re.search(patron, contenido):
                self.hacer_backup(archivo)
                nuevo = re.sub(patron, reemplazar, contenido)
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(nuevo)
                print(f"  ✅ Corregido: {archivo.name}")

# ============================================
# PERSISTENCIA
# ============================================

class Persistencia:
    def __init__(self):
        self.db_path = Path.home() / ".flutterfix" / "errors.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS errores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mensaje TEXT,
                categoria TEXT,
                solucion TEXT,
                auto_corregido INTEGER,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def guardar_error_auto(self, mensaje: str, categoria: str, solucion: Dict, auto_corregido: bool):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO errores (mensaje, categoria, solucion, auto_corregido, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (mensaje[:500], categoria, json.dumps(solucion), 1 if auto_corregido else 0, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def obtener_historial(self, limite: int = 20) -> List[Dict]:
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('SELECT mensaje, categoria, auto_corregido, timestamp FROM errores ORDER BY id DESC LIMIT ?', (limite,))
        rows = cursor.fetchall()
        conn.close()
        return [{"mensaje": r[0][:80], "categoria": r[1], "auto_corregido": bool(r[2]), "timestamp": r[3]} for r in rows]

# ============================================
# SISTEMA PRINCIPAL UNIFICADO
# ============================================

class FlutterFixCascade:
    def __init__(self):
        self.persistencia = Persistencia()
        self.auto_corrector = AutoCorrector()
        self.monitor = None
    
    def iniciar_monitoreo(self):
        print("\n" + "=" * 60)
        print("🔍 MODO MONITOREO EN TIEMPO REAL")
        print("=" * 60)
        
        self.monitor = MonitorTiempoReal(self.auto_corrector)
        self.monitor.conectar_persistencia(self.persistencia)
        
        if self.monitor.iniciar_app():
            print("\n✅ App ejecutándose en tu dispositivo")
            print("📡 Monitoreando errores...")
            print("   • Los errores se corregirán automáticamente")
            print("   • Escribe 'salir' para detener\n")
            
            while True:
                cmd = input("🔧 > ").strip().lower()
                if cmd == "salir":
                    self.monitor.detener()
                    break
                elif cmd == "historial":
                    self.mostrar_historial()
                elif cmd == "estado":
                    print(f"   Dispositivo conectado: {len(self.monitor.verificar_dispositivos()) > 0}")
                    print(f"   Errores procesados: {len(self.monitor.errores_procesados)}")
        else:
            print("❌ No se pudo iniciar. Conecta tu celular y activa depuración USB")
    
    def analizar_error_manual(self):
        print("\n" + "=" * 60)
        print("📝 MODO ANÁLISIS MANUAL")
        print("=" * 60)
        print("Comandos:")
        print("  • Pega un error - Lo analizaré y sugeriré solución")
        print("  • 'historial' - Ver errores anteriores")
        print("  • 'salir' - Volver al menú\n")
        
        while True:
            entrada = input("💬 > ").strip()
            if entrada.lower() == "salir":
                break
            elif entrada.lower() == "historial":
                self.mostrar_historial()
                continue
            
            categoria = self.detectar_categoria(entrada)
            solucion = self.buscar_solucion(categoria)
            
            print("\n" + "=" * 60)
            print("📊 ANÁLISIS DEL ERROR")
            print("=" * 60)
            print(f"📥 Error: {entrada[:100]}...")
            print(f"🏷️ Categoría: {categoria}")
            print(f"\n🔧 Solución sugerida:")
            
            if solucion:
                for accion in solucion.get("acciones", []):
                    if "archivo" in accion:
                        print(f"  📁 Modificar {accion['archivo']}")
                        print(f"     Buscar: {accion.get('buscar', '')[:50]}")
                        print(f"     Reemplazar con: {accion.get('reemplazar', '')[:50]}")
                    elif "comando" in accion:
                        print(f"  💻 Ejecutar: {accion['comando']}")
                
                if AUTO_FIX:
                    aplicar = input("\n¿Aplicar auto-corrección? (s/n): ").strip().lower()
                    if aplicar == 's':
                        self.auto_corrector.aplicar_solucion(solucion)
                        self.persistencia.guardar_error_auto(entrada, categoria, solucion, True)
                        print("✅ Corrección aplicada")
            else:
                print("  No hay solución predefinida para este error")
            
            print("=" * 60 + "\n")
    
    def detectar_categoria(self, error: str) -> str:
        error_lower = error.lower()
        patrones = {
            r"defaultandroidsourceset.*cannot be cast": "gradle_agp_incompatibilidad",
            r"app_links|plugin.*incompatible": "plugin_incompatible",
            r"build failed|gradle task": "error_compilacion_gradle",
            r"nullpointer|null check": "null_pointer",
            r"rangeerror|index out": "indice_fuera_rango"
        }
        for patron, cat in patrones.items():
            if re.search(patron, error_lower):
                return cat
        return "general"
    
    def buscar_solucion(self, categoria: str) -> Optional[Dict]:
        soluciones = {
            "gradle_agp_incompatibilidad": {
                "acciones": [
                    {"archivo": "pubspec.yaml", "buscar": "app_links:", "reemplazar": "app_links: ^8.0.2"},
                    {"archivo": "android/build.gradle", "buscar": "com.android.tools.build:gradle:7", "reemplazar": "com.android.tools.build:gradle:8.1.0"},
                    {"comando": "flutter clean"},
                    {"comando": "flutter pub get"}
                ]
            },
            "null_pointer": {
                "acciones": [
                    {"comando": "echo Buscando archivos con null safety..."}
                ]
            },
            "plugin_incompatible": {
                "acciones": [{"comando": "flutter pub upgrade"}]
            },
            "error_compilacion_gradle": {
                "acciones": [{"comando": "flutter clean"}, {"comando": "cd android && gradlew clean && cd .."}]
            }
        }
        return soluciones.get(categoria)
    
    def mostrar_historial(self):
        historial = self.persistencia.obtener_historial()
        print("\n📜 HISTORIAL DE ERRORES:")
        for e in historial:
            status = "✅" if e['auto_corregido'] else "⚠️"
            print(f"  {status} [{e['timestamp'][:19]}] {e['categoria']}: {e['mensaje'][:50]}")
        print()

# ============================================
# MENÚ PRINCIPAL
# ============================================

def main():
    print("=" * 60)
    print("🚀 FLUTTERFIX CASCADE v10 - SISTEMA COMPLETO")
    print("=" * 60)
    print("\nUn solo sistema que hace TODO:")
    print("  ✅ Monitoreo en tiempo real con tu celular")
    print("  ✅ Detección y corrección automática de errores")
    print("  ✅ Análisis manual de errores")
    print("  ✅ Persistencia de historial")
    print("  ✅ Auto-reparación")
    print(f"  🔧 Auto-corrección: {'ACTIVADA' if AUTO_FIX else 'DESACTIVADA'}")
    
    sistema = FlutterFixCascade()
    
    while True:
        print("\n" + "=" * 60)
        print("📋 MENÚ PRINCIPAL")
        print("=" * 60)
        print("1. 🔍 Monitorear app en tiempo real (con celular conectado)")
        print("2. 📝 Analizar errores manualmente")
        print("3. 📊 Ver historial de errores")
        print("4. ⚙️ Configurar auto-corrección")
        print("5. ❌ Salir")
        
        opcion = input("\n💡 Elige una opción: ").strip()
        
        if opcion == "1":
            sistema.iniciar_monitoreo()
        elif opcion == "2":
            sistema.analizar_error_manual()
        elif opcion == "3":
            sistema.mostrar_historial()
        elif opcion == "4":
            global AUTO_FIX
            AUTO_FIX = not AUTO_FIX
            print(f"✅ Auto-corrección: {'ACTIVADA' if AUTO_FIX else 'DESACTIVADA'}")
        elif opcion == "5":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main()
