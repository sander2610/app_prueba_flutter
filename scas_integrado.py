import json
import os
import sys
import time
import threading
import random
import shutil
import hashlib
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from queue import Queue
import stat

# ============================================
# SISTEMA DE PROTECCIÓN DE ARCHIVOS CRÍTICOS
# ============================================

class ArchivosProtegidos:
    """Define archivos y carpetas que NO pueden ser tocados"""
    
    CARPETAS_PROTEGIDAS = [
        "Windows", "System32", "Program Files", "Program Files (x86)",
        "Boot", "Recovery", "System Volume Information", "$Recycle.Bin",
        "Config.Msi", "MSOCache", "PerfLogs", "WindowsApps"
    ]
    
    ARCHIVOS_PROTEGIDOS = [
        "ntldr", "bootmgr", "boot.ini", "pagefile.sys", "swapfile.sys",
        "hiberfil.sys", "winload.exe", "winresume.exe", "kernel32.dll",
        "ntoskrnl.exe", "hal.dll", "config", "sam", "security", "software", "system"
    ]
    
    @staticmethod
    def es_protegido(ruta: Path) -> bool:
        """Verifica si un archivo o carpeta está protegido"""
        ruta_str = str(ruta).lower()
        
        for carpeta in ArchivosProtegidos.CARPETAS_PROTEGIDAS:
            if carpeta.lower() in ruta_str:
                return True
        
        for archivo in ArchivosProtegidos.ARCHIVOS_PROTEGIDOS:
            if archivo.lower() == ruta.name.lower():
                return True
        
        return False

# ============================================
# SOCIEDAD DE CONTROL DE ARCHIVOS
# ============================================

class SociedadControlArchivos:
    """Sociedad especializada en gestionar archivos del sistema"""
    
    def __init__(self, canal_comunicacion):
        self.nombre = "SCAS - Sociedad de Control de Archivos"
        self.canal = canal_comunicacion
        self.calidad = 85.0
        self.complejidad = 2.5
        self.conocimiento = 50
        self.archivos_gestionados = 0
        self.espacio_liberado = 0  # MB
        self.archivos_eliminados = 0
        self.archivos_organizados = 0
        
        # Registrar en canal de comunicación
        self.canal.registrar(self.nombre, self.recibir_mensaje)
        
    def recibir_mensaje(self, mensaje: Dict):
        """Recibe mensajes de otras sociedades"""
        print(f"\n   📨 [{self.nombre}] Recibió: {mensaje['tipo']} de {mensaje['emisor']}")
        
        if mensaje["tipo"] == "solicitar_limpieza":
            self.limpiar_archivos_temporales()
        elif mensaje["tipo"] == "solicitar_organizacion":
            self.organizar_descargas()
        elif mensaje["tipo"] == "solicitar_analisis":
            self.analizar_espacio()
    
    # ==========================================
    # FUNCIONES DE CONTROL DE ARCHIVOS
    # ==========================================
    
    def limpiar_archivos_temporales(self) -> Dict:
        """Limpia archivos temporales de forma segura"""
        print(f"\n🧹 [{self.nombre}] Limpiando archivos temporales...")
        
        carpetas_temporales = [
            Path(os.environ.get("TEMP", "C:\\Temp")),
            Path(os.environ.get("TMP", "C:\\Temp")),
            Path.home() / "AppData" / "Local" / "Temp",
            Path.home() / "Downloads" / "Temp"
        ]
        
        liberado = 0
        eliminados = 0
        
        for carpeta in carpetas_temporales:
            if carpeta.exists() and not ArchivosProtegidos.es_protegido(carpeta):
                try:
                    for archivo in carpeta.iterdir():
                        if not ArchivosProtegidos.es_protegido(archivo):
                            try:
                                if archivo.is_file():
                                    tamanio = archivo.stat().st_size / (1024 * 1024)
                                    liberado += tamanio
                                    archivo.unlink()
                                    eliminados += 1
                            except:
                                pass
                except:
                    pass
        
        self.espacio_liberado += liberado
        self.archivos_eliminados += eliminados
        
        print(f"   ✅ Eliminados {eliminados} archivos temporales")
        print(f"   💾 Espacio liberado: {liberado:.2f} MB")
        
        return {"eliminados": eliminados, "liberado_mb": liberado}
    
    def organizar_descargas(self) -> Dict:
        """Organiza la carpeta de descargas por tipo de archivo"""
        print(f"\n📁 [{self.nombre}] Organizando carpeta de descargas...")
        
        descargas = Path.home() / "Downloads"
        if not descargas.exists():
            return {"organizados": 0}
        
        tipos = {
            "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
            "Documentos": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
            "Instaladores": [".exe", ".msi", ".deb", ".rpm", ".dmg"],
            "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
            "Musica": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
            "Codigo": [".py", ".java", ".cpp", ".c", ".js", ".html", ".css", ".dart", ".json", ".xml", ".yaml"],
            "Ejecutables": [".bat", ".cmd", ".ps1", ".sh"]
        }
        
        organizados = 0
        
        for archivo in descargas.iterdir():
            if archivo.is_file() and not ArchivosProtegidos.es_protegido(archivo):
                extension = archivo.suffix.lower()
                destino = None
                
                for tipo, exts in tipos.items():
                    if extension in exts:
                        destino = descargas / tipo
                        break
                
                if destino:
                    destino.mkdir(exist_ok=True)
                    try:
                        shutil.move(str(archivo), str(destino / archivo.name))
                        organizados += 1
                    except:
                        pass
        
        self.archivos_organizados += organizados
        
        print(f"   ✅ Organizados {organizados} archivos en la carpeta de descargas")
        
        return {"organizados": organizados}
    
    def analizar_espacio(self) -> Dict:
        """Analiza el espacio en disco y reporta"""
        print(f"\n💾 [{self.nombre}] Analizando espacio en disco...")
        
        try:
            uso_disco = shutil.disk_usage("/")
            total_gb = uso_disco.total / (1024**3)
            usado_gb = uso_disco.used / (1024**3)
            libre_gb = uso_disco.free / (1024**3)
            
            porcentaje_libre = (libre_gb / total_gb) * 100
            
            print(f"   💿 Total: {total_gb:.1f} GB")
            print(f"   📀 Usado: {usado_gb:.1f} GB")
            print(f"   💾 Libre: {libre_gb:.1f} GB ({porcentaje_libre:.1f}%)")
            
            if porcentaje_libre < 10:
                print(f"   ⚠️ ALERTA: Espacio libre crítico!")
                self.canal.broadcast(self.nombre, "alerta_espacio_critico", {
                    "libre_gb": libre_gb,
                    "porcentaje": porcentaje_libre
                })
            
            return {
                "total_gb": total_gb,
                "usado_gb": usado_gb,
                "libre_gb": libre_gb,
                "porcentaje_libre": porcentaje_libre
            }
            
        except Exception as e:
            print(f"   ❌ Error analizando disco: {e}")
            return {"error": str(e)}
    
    def buscar_archivos_duplicados(self, ruta: Path = None) -> List[Dict]:
        """Busca archivos duplicados en una ruta"""
        if ruta is None:
            ruta = Path.home() / "Desktop"
        
        print(f"\n🔍 [{self.nombre}] Buscando archivos duplicados en {ruta}...")
        
        if ArchivosProtegidos.es_protegido(ruta):
            print(f"   ⛔ Ruta protegida, no se puede escanear")
            return []
        
        archivos_por_hash = {}
        duplicados = []
        
        try:
            for archivo in ruta.rglob("*"):
                if archivo.is_file() and not ArchivosProtegidos.es_protegido(archivo):
                    if archivo.stat().st_size < 100 * 1024 * 1024:  # Solo archivos < 100MB
                        try:
                            with open(archivo, 'rb') as f:
                                hash_valor = hashlib.md5(f.read(8192)).hexdigest()
                            
                            if hash_valor in archivos_por_hash:
                                duplicados.append({
                                    "original": str(archivos_por_hash[hash_valor]),
                                    "duplicado": str(archivo),
                                    "tamanio_mb": archivo.stat().st_size / (1024 * 1024)
                                })
                            else:
                                archivos_por_hash[hash_valor] = archivo
                        except:
                            pass
        except:
            pass
        
        print(f"   ✅ Encontrados {len(duplicados)} archivos duplicados")
        
        return duplicados
    
    def eliminar_archivos_vacios(self) -> int:
        """Elimina carpetas vacías"""
        print(f"\n🗑️ [{self.nombre}] Buscando y eliminando carpetas vacías...")
        
        eliminadas = 0
        rutas_escaneadas = [Path.home() / "Desktop", Path.home() / "Documents"]
        
        for ruta in rutas_escaneadas:
            if ruta.exists() and not ArchivosProtegidos.es_protegido(ruta):
                try:
                    for carpeta in ruta.rglob("*"):
                        if carpeta.is_dir() and not ArchivosProtegidos.es_protegido(carpeta):
                            try:
                                if not any(carpeta.iterdir()):
                                    carpeta.rmdir()
                                    eliminadas += 1
                            except:
                                pass
                except:
                    pass
        
        print(f"   ✅ Eliminadas {eliminadas} carpetas vacías")
        
        return eliminadas
    
    # ==========================================
    # MEJORA Y EVOLUCIÓN
    # ==========================================
    
    def mejorar(self):
        """La sociedad mejora sus capacidades"""
        mejora = random.uniform(1, 4)
        self.calidad = min(99.9, self.calidad + mejora * 0.3)
        self.complejidad += random.uniform(0.05, 0.1)
        self.conocimiento += int(mejora)
        return mejora
    
    def reporte_estado(self) -> Dict:
        """Reporta el estado de la sociedad"""
        return {
            "nombre": self.nombre,
            "calidad": round(self.calidad, 1),
            "complejidad": round(self.complejidad, 2),
            "conocimiento": self.conocimiento,
            "archivos_gestionados": self.archivos_gestionados,
            "espacio_liberado_mb": round(self.espacio_liberado, 2),
            "archivos_eliminados": self.archivos_eliminados,
            "archivos_organizados": self.archivos_organizados
        }

# ============================================
# INTEGRACIÓN CON EL SISTEMA UNIFICADO
# ============================================

class SistemaUnificadoConSCAS:
    def __init__(self):
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🏛️ FLUTTERFIX v32 - SOCIEDAD DE CONTROL DE ARCHIVOS (SCAS)                  ║
║                                                                               ║
║   Nueva sociedad especializada en:                                           ║
║   • Limpieza de archivos temporales                                          ║
║   • Organización de descargas                                                ║
║   • Búsqueda y eliminación de duplicados                                     ║
║   • Análisis de espacio en disco                                             ║
║   • Eliminación de carpetas vacías                                           ║
║                                                                               ║
║   🔒 PROTECCIÓN: Archivos de Windows NO pueden ser tocados                   ║
║                                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
        
        # Crear canal de comunicación
        self.canal = CanalComunicacion()
        
        # Crear SCAS
        self.scas = SociedadControlArchivos(self.canal)
        
        # Crear otras sociedades (simuladas para demostración)
        self.sociedades = {
            "SCAS": self.scas,
            "FlutterFix": self._crear_sociedad_demo("FlutterFix"),
            "WebSociety": self._crear_sociedad_demo("WebSociety"),
            "DevOpsSociety": self._crear_sociedad_demo("DevOpsSociety")
        }
        
        self.ciclo = 0
        
    def _crear_sociedad_demo(self, nombre: str):
        """Crea una sociedad demo para comunicación"""
        class DemoSociedad:
            def __init__(self, n, canal):
                self.nombre = n
                self.canal = canal
                self.calidad = random.uniform(70, 95)
                canal.registrar(n, self.recibir)
            def recibir(self, msg):
                print(f"   📨 [{self.nombre}] Recibió alerta de {msg['emisor']}")
        return DemoSociedad(nombre, self.canal)
    
    def ejecutar_ciclo(self):
        """Ejecuta un ciclo completo con SCAS"""
        self.ciclo += 1
        
        print(f"\n{'='*70}")
        print(f"🔄 CICLO #{self.ciclo} - SCAS ACTIVA")
        print(f"{'='*70}")
        
        # 1. SCAS mejora
        mejora = self.scas.mejorar()
        print(f"\n📈 SCAS mejora: +{mejora:.1f}% → Calidad {self.scas.calidad:.1f}%")
        
        # 2. SCAS ejecuta sus funciones
        self.scas.analizar_espacio()
        self.scas.limpiar_archivos_temporales()
        self.scas.organizar_descargas()
        
        # 3. Buscar duplicados (opcional)
        duplicados = self.scas.buscar_archivos_duplicados()
        if duplicados:
            print(f"\n📋 Archivos duplicados encontrados:")
            for d in duplicados[:3]:
                print(f"   • {d['duplicado']} (copia de {d['original']})")
        
        # 4. SCAS se comunica con otras sociedades
        if self.ciclo % 3 == 0:
            print(f"\n📡 SCAS se comunica con otras sociedades:")
            self.canal.broadcast("SCAS", "reporte_estado", self.scas.reporte_estado())
        
        # 5. Mostrar resumen
        reporte = self.scas.reporte_estado()
        print(f"\n📊 RESUMEN SCAS:")
        print(f"   Calidad: {reporte['calidad']}%")
        print(f"   Complejidad: {reporte['complejidad']}")
        print(f"   Espacio liberado: {reporte['espacio_liberado_mb']:.2f} MB")
        print(f"   Archivos eliminados: {reporte['archivos_eliminados']}")
        print(f"   Archivos organizados: {reporte['archivos_organizados']}")
    
    def ejecutar(self, ciclos: int = 5):
        """Ejecuta el sistema completo"""
        print("\n🚀 INICIANDO SOCIEDAD DE CONTROL DE ARCHIVOS")
        print("🔒 Archivos de Windows protegidos")
        print("=" * 70)
        
        try:
            for _ in range(ciclos):
                self.ejecutar_ciclo()
                time.sleep(3)
        except KeyboardInterrupt:
            print("\n\n🛑 Sistema detenido")
        
        self.reporte_final()
    
    def reporte_final(self):
        """Reporte final de SCAS"""
        reporte = self.scas.reporte_estado()
        
        print("\n" + "=" * 70)
        print("📊 REPORTE FINAL - SCAS")
        print("=" * 70)
        print(f"\n🏛️ SOCIEDAD: {reporte['nombre']}")
        print(f"   Calidad final: {reporte['calidad']}%")
        print(f"   Complejidad: {reporte['complejidad']}")
        print(f"   Conocimiento: {reporte['conocimiento']}")
        print(f"\n📈 ESTADÍSTICAS DE CONTROL:")
        print(f"   Espacio liberado: {reporte['espacio_liberado_mb']:.2f} MB")
        print(f"   Archivos eliminados: {reporte['archivos_eliminados']}")
        print(f"   Archivos organizados: {reporte['archivos_organizados']}")
        
        print("\n" + "=" * 70)
        print("🎯 SCAS sigue monitoreando y limpiando el sistema")
        print("🔒 Archivos críticos de Windows permanecen protegidos")
        print("=" * 70)

# ============================================
# CANAL DE COMUNICACIÓN (SINGLETON)
# ============================================

class CanalComunicacion:
    _instancia = None
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia
    
    def _inicializar(self):
        self.suscriptores = {}
        self.historial = []
    
    def registrar(self, nombre: str, callback):
        self.suscriptores[nombre] = callback
    
    def enviar(self, emisor: str, receptor: str, tipo: str, contenido: Dict):
        mensaje = {
            "emisor": emisor,
            "receptor": receptor,
            "tipo": tipo,
            "contenido": contenido,
            "timestamp": datetime.now().isoformat()
        }
        self.historial.append(mensaje)
        if receptor in self.suscriptores:
            self.suscriptores[receptor](mensaje)
    
    def broadcast(self, emisor: str, tipo: str, contenido: Dict):
        for receptor in self.suscriptores:
            if receptor != emisor:
                self.enviar(emisor, receptor, tipo, contenido)

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    sistema = SistemaUnificadoConSCAS()
    sistema.ejecutar(ciclos=5)
