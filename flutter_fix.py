import json
import re
import os
import sqlite3
import subprocess
import shutil
import threading
import time
import queue
import sys
from datetime import datetime
from pathlib import Path
import hashlib

# ============================================
# CONFIGURACIÓN - SIN INTERVENCIÓN HUMANA
# ============================================

AUTO_FIX = True
MODO_AUTONOMO = True  # El usuario NO interviene
SILENT_MODE = False   # False para mostrar progreso

# ============================================
# SISTEMA DE LOGS INTERNO
# ============================================

class Logger:
    def __init__(self):
        self.logs = []
        self.log_file = Path.home() / ".flutterfix" / "autonomous.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log(self, mensaje, nivel="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        linea = f"[{timestamp}] [{nivel}] {mensaje}"
        self.logs.append(linea)
        if not SILENT_MODE:
            print(f"  {linea}")
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(linea + "\n")
    
    def error(self, mensaje):
        self.log(mensaje, "ERROR")
    
    def exito(self, mensaje):
        self.log(mensaje, "✅ EXITO")
    
    def proceso(self, mensaje):
        self.log(mensaje, "🔄 PROCESO")

logger = Logger()

# ============================================
# MONITOR Y CORRECTOR AUTÓNOMO
# ============================================

class DiosFlutterFix:
    def __init__(self):
        self.proyecto_path = Path.cwd()
        self.backup_dir = self.proyecto_path / ".flutterfix_backups"
        self.backup_dir.mkdir(exist_ok=True)
        self.db_path = Path.home() / ".flutterfix" / "errors.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        
        self.proceso_app = None
        self.monitoreando = False
        self.errores_procesados = set()
        self.ciclo_correcciones = 0
        
        logger.log("🤖 FLUTTERFIX v11 - MODO AUTÓNOMO INICIADO")
        logger.log(f"📁 Proyecto: {self.proyecto_path}")
    
    def _init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS correcciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error TEXT,
                categoria TEXT,
                solucion_aplicada TEXT,
                timestamp TEXT,
                ciclo INTEGER
            )
        ''')
        conn.commit()
        conn.close()
    
    def guardar_correccion(self, error: str, categoria: str, solucion: str):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO correcciones (error, categoria, solucion_aplicada, timestamp, ciclo)
            VALUES (?, ?, ?, ?, ?)
        ''', (error[:500], categoria, solucion, datetime.now().isoformat(), self.ciclo_correcciones))
        conn.commit()
        conn.close()
    
    def verificar_dispositivos(self):
        """Detecta celular automáticamente"""
        try:
            resultado = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
            for linea in resultado.stdout.split('\n')[1:]:
                if 'device' in linea and 'offline' not in linea:
                    dispositivo = linea.split('\t')[0].strip()
                    if dispositivo:
                        logger.exito(f"Dispositivo detectado: {dispositivo}")
                        return dispositivo
        except:
            pass
        return None
    
    def detectar_categoria_error(self, error: str) -> str:
        error_lower = error.lower()
        patrones = {
            r"defaultandroidsourceset.*cannot be cast": "gradle_agp_incompatibilidad",
            r"app_links": "plugin_incompatible",
            r"build failed|gradle task": "error_compilacion_gradle",
            r"nullpointer|null check": "null_pointer",
            r"rangeerror|index out": "indice_fuera_rango",
            r"setstate.*dispose": "estado_ui",
            r"missingplugin": "plugin_nativo",
            r"permission denied": "permiso_android"
        }
        for patron, cat in patrones.items():
            if re.search(patron, error_lower):
                return cat
        return "general"
    
    def obtener_solucion(self, categoria: str) -> dict:
        """Base de conocimientos de soluciones"""
        soluciones = {
            "gradle_agp_incompatibilidad": {
                "acciones": [
                    {"tipo": "modificar", "archivo": "pubspec.yaml", "buscar": r"app_links:\s*[\^]?[\d\.]+", "reemplazar": "app_links: ^8.0.2"},
                    {"tipo": "modificar", "archivo": "android/build.gradle", "buscar": r"com.android.tools.build:gradle:7[\d\.]*", "reemplazar": "com.android.tools.build:gradle:8.1.0"},
                    {"tipo": "comando", "comando": "flutter clean"},
                    {"tipo": "comando", "comando": "flutter pub get"}
                ],
                "mensaje": "Actualizando Gradle/AGP para compatibilidad"
            },
            "null_pointer": {
                "acciones": [
                    {"tipo": "buscar_reemplazar", "extension": ".dart", "buscar": r'(\w+)\!\.', "reemplazar": r'\1?.'}
                ],
                "mensaje": "Corrigiendo null safety en archivos Dart"
            },
            "plugin_incompatible": {
                "acciones": [
                    {"tipo": "comando", "comando": "flutter pub upgrade"}
                ],
                "mensaje": "Actualizando plugins incompatibles"
            },
            "error_compilacion_gradle": {
                "acciones": [
                    {"tipo": "comando", "comando": "flutter clean"},
                    {"tipo": "comando", "comando": "cd android && gradlew clean && cd .."}
                ],
                "mensaje": "Limpiando caché de Gradle"
            }
        }
        return soluciones.get(categoria, {"acciones": [], "mensaje": "No hay solución automática"})
    
    def aplicar_correccion(self, solucion: dict):
        """Aplica correcciones automáticamente"""
        for accion in solucion.get("acciones", []):
            if accion["tipo"] == "modificar":
                self.modificar_archivo(
                    Path.cwd() / accion["archivo"],
                    accion["buscar"],
                    accion["reemplazar"]
                )
            elif accion["tipo"] == "comando":
                self.ejecutar_comando(accion["comando"])
            elif accion["tipo"] == "buscar_reemplazar":
                self.buscar_reemplazar_en_dart(accion["buscar"], accion["reemplazar"])
    
    def modificar_archivo(self, ruta: Path, patron_buscar: str, reemplazar: str):
        if not ruta.exists():
            return
        
        # Backup automático
        backup = self.backup_dir / f"{ruta.name}.{int(time.time())}.bak"
        shutil.copy2(ruta, backup)
        
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        nuevo_contenido = re.sub(patron_buscar, reemplazar, contenido)
        
        if nuevo_contenido != contenido:
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(nuevo_contenido)
            logger.exito(f"Modificado: {ruta.name}")
    
    def buscar_reemplazar_en_dart(self, patron: str, reemplazar: str):
        for archivo in self.proyecto_path.rglob("*.dart"):
            if "build" in str(archivo) or "generated" in str(archivo):
                continue
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            if re.search(patron, contenido):
                backup = self.backup_dir / f"{archivo.name}.{int(time.time())}.bak"
                shutil.copy2(archivo, backup)
                nuevo = re.sub(patron, reemplazar, contenido)
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(nuevo)
                logger.exito(f"Corregido null safety en: {archivo.name}")
    
    def ejecutar_comando(self, comando: str):
        logger.proceso(f"Ejecutando: {comando}")
        try:
            resultado = subprocess.run(comando, shell=True, cwd=self.proyecto_path, capture_output=True, text=True, timeout=60)
            if resultado.returncode == 0:
                logger.exito(f"Comando exitoso: {comando[:50]}")
            else:
                logger.error(f"Comando falló: {comando[:50]} - {resultado.stderr[:100]}")
        except Exception as e:
            logger.error(f"Error ejecutando {comando}: {e}")
    
    def monitorear_logs(self):
        """Captura logs en tiempo real"""
        subprocess.run("adb logcat -c", shell=True, capture_output=True)
        
        proceso_logs = subprocess.Popen(
            "adb logcat -v time *:E",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        while self.monitoreando:
            linea = proceso_logs.stdout.readline()
            if linea and self.es_error_relevante(linea):
                self.manejar_error(linea)
    
    def es_error_relevante(self, linea: str) -> bool:
        patrones = [
            r"FATAL EXCEPTION",
            r"AndroidRuntime",
            r"NullPointerException",
            r"RangeError",
            r"SQLiteException",
            r"MissingPluginException"
        ]
        return any(re.search(p, linea, re.IGNORECASE) for p in patrones)
    
    def manejar_error(self, error: str):
        hash_error = hashlib.md5(error.encode()).hexdigest()
        if hash_error in self.errores_procesados:
            return
        
        self.errores_procesados.add(hash_error)
        self.ciclo_correcciones += 1
        
        logger.log(f"🔴 ERROR DETECTADO: {error[:100]}")
        
        categoria = self.detectar_categoria_error(error)
        logger.log(f"🏷️ Categoría: {categoria}")
        
        solucion = self.obtener_solucion(categoria)
        
        if solucion["acciones"]:
            logger.proceso(f"Aplicando corrección: {solucion['mensaje']}")
            self.aplicar_correccion(solucion)
            self.guardar_correccion(error, categoria, solucion["mensaje"])
            logger.exito(f"CORRECCIÓN APLICADA - Ciclo #{self.ciclo_correcciones}")
            self.reiniciar_app()
    
    def reiniciar_app(self):
        """Reinicia la app automáticamente"""
        if self.proceso_app:
            self.proceso_app.terminate()
            time.sleep(3)
        
        self.iniciar_app()
    
    def iniciar_app(self):
        """Inicia la app automáticamente"""
        dispositivo = self.verificar_dispositivos()
        
        if not dispositivo:
            logger.error("No hay dispositivo conectado. Esperando...")
            return False
        
        logger.proceso("Iniciando aplicación...")
        
        self.proceso_app = subprocess.Popen(
            "flutter run",
            shell=True,
            cwd=self.proyecto_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        return True
    
    def ejecutar(self):
        """Bucle principal autónomo"""
        logger.log("=" * 60)
        logger.log("🚀 INICIANDO MODO AUTÓNOMO")
        logger.log("=" * 60)
        
        # Paso 1: Verificar/Iniciar app
        if not self.iniciar_app():
            logger.log("Esperando conexión USB...")
            while not self.verificar_dispositivos():
                time.sleep(5)
            self.iniciar_app()
        
        # Paso 2: Iniciar monitoreo
        self.monitoreando = True
        hilo_monitoreo = threading.Thread(target=self.monitorear_logs, daemon=True)
        hilo_monitoreo.start()
        
        logger.log("✅ SISTEMA ACTIVO - MONITOREANDO EN TIEMPO REAL")
        logger.log("   • Detectando errores automáticamente")
        logger.log("   • Corrigiendo sin intervención")
        logger.log("   • Reiniciando app cuando sea necesario")
        logger.log("")
        logger.log("Presiona Ctrl+C para detener")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.log("\n🛑 Deteniendo sistema autónomo...")
            self.monitoreando = False
            if self.proceso_app:
                self.proceso_app.terminate()
            logger.exito("Sistema detenido correctamente")
            
            # Mostrar resumen
            logger.log("")
            logger.log("=" * 60)
            logger.log("📊 RESUMEN DE CORRECCIONES")
            logger.log("=" * 60)
            logger.log(f"   Ciclos de corrección: {self.ciclo_correcciones}")
            logger.log(f"   Errores únicos procesados: {len(self.errores_procesados)}")
            logger.log(f"   Logs guardados en: {logger.log_file}")
            logger.log(f"   Backups en: {self.backup_dir}")

# ============================================
# EJECUCIÓN PRINCIPAL - SIN INTERVENCIÓN
# ============================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ███████╗██╗     ██╗   ██╗████████╗████████╗███████╗██████╗ ║
║   ██╔════╝██║     ██║   ██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗║
║   █████╗  ██║     ██║   ██║   ██║      ██║   █████╗  ██████╔╝║
║   ██╔══╝  ██║     ██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗║
║   ██║     ███████╗╚██████╔╝   ██║      ██║   ███████╗██║  ██║║
║   ╚═╝     ╚══════╝ ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝║
║                                                              ║
║                   MODO AUTÓNOMO ACTIVADO                     ║
║                                                              ║
║   El sistema está en control total.                          ║
║   No necesita intervención humana.                          ║
║                                                              ║
║   🔍 Monitoreando errores...                                ║
║   🔧 Corrigiendo automáticamente...                         ║
║   🔄 Reiniciando cuando es necesario...                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    dios = DiosFlutterFix()
    dios.ejecutar()
