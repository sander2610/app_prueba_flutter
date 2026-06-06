import json
import os
import sys
import time
import subprocess
import threading
import hashlib
from datetime import datetime
from pathlib import Path
import webbrowser

# ============================================
# CONFIGURACIÓN AUTO-SINCRONIZACIÓN
# ============================================

REPO_URL = "https://github.com/sander2610/app_prueba_flutter.git"
BRANCH = "master"
SYNC_INTERVAL = 30  # segundos entre sincronizaciones
AUTO_COMMIT = True
AUTO_PUSH = True

# ============================================
# SISTEMA DE AUTO-SINCRONIZACIÓN
# ============================================

class AutoSync:
    def __init__(self):
        self.repo_path = Path.cwd()
        self.ultimo_hash = None
        self.cambios_locales = 0
        self.cambios_remotos = 0
        self.sync_activa = True
        self._inicializar_git()
        
    def _inicializar_git(self):
        """Inicializa git si no existe"""
        if not (self.repo_path / ".git").exists():
            print("📁 Inicializando repositorio git...")
            subprocess.run(["git", "init"], cwd=self.repo_path, capture_output=True)
            subprocess.run(["git", "remote", "add", "origin", REPO_URL], cwd=self.repo_path, capture_output=True)
            print("   ✅ Repositorio inicializado")
    
    def obtener_hash_actual(self) -> str:
        """Obtiene el hash del último commit"""
        try:
            result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo_path, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def detectar_cambios_locales(self) -> bool:
        """Detecta cambios en archivos locales"""
        result = subprocess.run(["git", "status", "--porcelain"], cwd=self.repo_path, capture_output=True, text=True)
        cambios = result.stdout.strip()
        if cambios:
            self.cambios_locales += 1
            print(f"   📝 Cambios locales detectados ({self.cambios_locales})")
            return True
        return False
    
    def detectar_cambios_remotos(self) -> bool:
        """Detecta cambios en el repositorio remoto"""
        subprocess.run(["git", "fetch", "origin", BRANCH], cwd=self.repo_path, capture_output=True)
        
        result = subprocess.run(["git", "rev-list", f"HEAD..origin/{BRANCH}", "--count"], cwd=self.repo_path, capture_output=True, text=True)
        try:
            count = int(result.stdout.strip())
            if count > 0:
                self.cambios_remotos += count
                print(f"   🌐 {count} cambios remotos detectados ({self.cambios_remotos} total)")
                return True
        except:
            pass
        return False
    
    def commit_auto(self, mensaje: str = None):
        """Auto-commit de cambios locales"""
        if mensaje is None:
            mensaje = f"Auto-sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        subprocess.run(["git", "add", "."], cwd=self.repo_path, capture_output=True)
        result = subprocess.run(["git", "commit", "-m", mensaje], cwd=self.repo_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ Auto-commit realizado: {mensaje[:50]}")
            return True
        return False
    
    def pull_auto(self):
        """Auto-pull de cambios remotos"""
        result = subprocess.run(["git", "pull", "origin", BRANCH], cwd=self.repo_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            if "Already up to date" in result.stdout:
                print("   ✅ Ya está actualizado")
            else:
                print(f"   📥 Pull realizado: {len(result.stdout)} bytes")
            return True
        else:
            # Intentar con rebase si hay conflicto
            subprocess.run(["git", "pull", "--rebase", "origin", BRANCH], cwd=self.repo_path, capture_output=True)
            return True
    
    def push_auto(self):
        """Auto-push de cambios locales"""
        result = subprocess.run(["git", "push", "origin", BRANCH], cwd=self.repo_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   📤 Auto-push realizado")
            return True
        return False
    
    def sincronizar(self):
        """Ciclo completo de sincronización"""
        print(f"\n🔄 CICLO DE SINCRONIZACIÓN - {datetime.now().strftime('%H:%M:%S')}")
        
        # 1. Detectar cambios locales
        if self.detectar_cambios_locales() and AUTO_COMMIT:
            self.commit_auto()
            if AUTO_PUSH:
                self.push_auto()
        
        # 2. Detectar cambios remotos
        if self.detectar_cambios_remotos():
            self.pull_auto()
        
        # 3. Verificar hash actual
        nuevo_hash = self.obtener_hash_actual()
        if nuevo_hash and nuevo_hash != self.ultimo_hash:
            print(f"   🔑 Nuevo hash: {nuevo_hash[:8]}")
            self.ultimo_hash = nuevo_hash
    
    def ejecutar(self):
        """Ejecuta la sincronización en bucle"""
        print("\n" + "=" * 60)
        print("🔄 AUTO-SINCRONIZACIÓN EN TIEMPO REAL")
        print("=" * 60)
        print(f"📁 Repositorio: {REPO_URL}")
        print(f"🌿 Rama: {BRANCH}")
        print(f"⏱️ Intervalo: {SYNC_INTERVAL} segundos")
        print("=" * 60)
        
        while self.sync_activa:
            try:
                self.sincronizar()
                time.sleep(SYNC_INTERVAL)
            except KeyboardInterrupt:
                print("\n\n🛑 Sincronización detenida")
                break
            except Exception as e:
                print(f"⚠️ Error: {e}")
                time.sleep(5)

# ============================================
# MONITOR DE ARCHIVOS EN TIEMPO REAL
# ============================================

class FileWatcher:
    """Monitorea cambios en archivos y auto-actualiza"""
    
    def __init__(self):
        self.archivos_ultima_modificacion = {}
        self.cambios_detectados = []
        self.watching = True
        
    def escanear_archivos(self):
        """Escanea archivos en busca de cambios"""
        patrones = ["*.py", "*.md", "*.yaml", "*.json", "*.sh"]
        
        for patron in patrones:
            for archivo in Path.cwd().glob(patron):
                try:
                    mtime = archivo.stat().st_mtime
                    if str(archivo) in self.archivos_ultima_modificacion:
                        if self.archivos_ultima_modificacion[str(archivo)] != mtime:
                            print(f"\n📄 ARCHIVO MODIFICADO: {archivo.name}")
                            self.cambios_detectados.append({
                                "archivo": str(archivo),
                                "tiempo": datetime.now().isoformat()
                            })
                            self.archivos_ultima_modificacion[str(archivo)] = mtime
                    else:
                        self.archivos_ultima_modificacion[str(archivo)] = mtime
                except:
                    pass
    
    def ejecutar(self):
        """Ejecuta el monitoreo en bucle"""
        print("\n👁️ MONITOREO DE ARCHIVOS ACTIVADO")
        print("   Detectando cambios en tiempo real...")
        
        while self.watching:
            self.escanear_archivos()
            time.sleep(2)

# ============================================
# SISTEMA AUTO-ACTUALIZABLE
# ============================================

class AutoUpdatableSystem:
    def __init__(self):
        self.version = "23.0"
        self.auto_sync = AutoSync()
        self.file_watcher = FileWatcher()
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🔄 FLUTTERFIX v23 - AUTO-SINCRONIZACIÓN EN TIEMPO REAL    ║
║                                                              ║
║   ✅ Sincronización automática con GitHub                    ║
║   ✅ Monitoreo de archivos en tiempo real                   ║
║   ✅ Auto-commit y auto-push                                ║
║   ✅ Auto-pull de cambios remotos                           ║
║   ✅ Actualización en vivo del sistema                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        print(f"📦 Versión: {self.version}")
        print(f"📁 Repositorio: {REPO_URL}")
        print(f"🔄 Sincronizando cada {SYNC_INTERVAL} segundos")
        
    def iniciar(self):
        """Inicia todos los servicios"""
        print("\n🚀 INICIANDO SERVICIOS DE AUTO-SINCRONIZACIÓN")
        
        # Hilo para sincronización con GitHub
        hilo_sync = threading.Thread(target=self.auto_sync.ejecutar, daemon=True)
        hilo_sync.start()
        
        # Hilo para monitoreo de archivos
        hilo_watcher = threading.Thread(target=self.file_watcher.ejecutar, daemon=True)
        hilo_watcher.start()
        
        print("\n✅ TODOS LOS SERVICIOS ACTIVOS")
        print("   • GitHub sincronizado automáticamente")
        print("   • Cambios detectados en tiempo real")
        print("   • Auto-commit y auto-push activos")
        print("\n   Presiona Ctrl+C para detener\n")
        
        try:
            while True:
                time.sleep(1)
                # Mostrar estadísticas cada 30 segundos
                if int(time.time()) % 30 == 0:
                    print(f"\n📊 ESTADO: {datetime.now().strftime('%H:%M:%S')}")
                    print(f"   Cambios locales: {self.auto_sync.cambios_locales}")
                    print(f"   Cambios remotos: {self.auto_sync.cambios_remotos}")
                    print(f"   Archivos monitoreados: {len(self.file_watcher.archivos_ultima_modificacion)}")
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n\n🛑 Sistema detenido")
            print(f"📊 Resumen final:")
            print(f"   Cambios locales: {self.auto_sync.cambios_locales}")
            print(f"   Cambios remotos: {self.auto_sync.cambios_remotos}")
            print("   ✅ Última sincronización completada")

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    sistema = AutoUpdatableSystem()
    sistema.iniciar()
