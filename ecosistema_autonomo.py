import json
import os
import sys
import time
import threading
import random
import subprocess
import webbrowser
import smtplib
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from flask import Flask, render_template_string, jsonify, request
from dataclasses import dataclass, field
from queue import Queue
import hashlib

# ============================================
# SISTEMA DE COMUNICACIÓN ENTRE SOCIEDADES
# ============================================

class CanalComunicacion:
    """Canal central de comunicación entre todas las sociedades"""
    
    def __init__(self):
        self.mensajes = []
        self.suscriptores = {}
        self.buzon = Queue()
        self.historial = []
        
    def registrar_sociedad(self, nombre: str, callback):
        """Registra una sociedad para recibir mensajes"""
        self.suscriptores[nombre] = callback
        print(f"   📡 {nombre} registrada en canal de comunicación")
        
    def enviar_mensaje(self, emisor: str, receptor: str, tipo: str, contenido: Dict):
        """Envía un mensaje a otra sociedad"""
        mensaje = {
            "id": hashlib.md5(f"{emisor}{receptor}{time.time()}".encode()).hexdigest()[:8],
            "emisor": emisor,
            "receptor": receptor,
            "tipo": tipo,
            "contenido": contenido,
            "timestamp": datetime.now().isoformat(),
            "leido": False
        }
        self.mensajes.append(mensaje)
        self.historial.append(mensaje)
        
        # Notificar al receptor si está suscrito
        if receptor in self.suscriptores:
            self.suscriptores[receptor](mensaje)
        
        print(f"   💬 {emisor} → {receptor}: {tipo}")
        return mensaje
    
    def broadcast(self, emisor: str, tipo: str, contenido: Dict):
        """Envía un mensaje a todas las sociedades"""
        mensajes = []
        for receptor in self.suscriptores:
            if receptor != emisor:
                msg = self.enviar_mensaje(emisor, receptor, tipo, contenido)
                mensajes.append(msg)
        return mensajes
    
    def obtener_mensajes_no_leidos(self, sociedad: str) -> List[Dict]:
        """Obtiene mensajes no leídos para una sociedad"""
        no_leidos = [m for m in self.mensajes if m["receptor"] == sociedad and not m["leido"]]
        for m in no_leidos:
            m["leido"] = True
        return no_leidos

# ============================================
# CLASE BASE PARA TODAS LAS SOCIEDADES
# ============================================

class SociedadBase:
    def __init__(self, nombre: str, tipo: str, canal: CanalComunicacion):
        self.nombre = nombre
        self.tipo = tipo
        self.canal = canal
        self.calidad = random.uniform(40, 70)
        self.deuda_tecnica = random.uniform(50, 90)
        self.puntos = 0
        self.version = "1.0"
        self.historial = []
        self.conocimiento = {}
        
        # Registrar en el canal
        self.canal.registrar_sociedad(nombre, self.recibir_mensaje)
        
    def recibir_mensaje(self, mensaje: Dict):
        """Procesa mensajes recibidos de otras sociedades"""
        print(f"\n   📨 {self.nombre} recibió mensaje de {mensaje['emisor']}: {mensaje['tipo']}")
        
        if mensaje["tipo"] == "solicitar_ayuda":
            self._ayudar_sociedad(mensaje)
        elif mensaje["tipo"] == "compartir_conocimiento":
            self._aprender_de_otra(mensaje)
        elif mensaje["tipo"] == "mejora_significativa":
            self._celebrar_mejora(mensaje)
        elif mensaje["tipo"] == "alerta":
            self._reaccionar_alerta(mensaje)
            
    def _ayudar_sociedad(self, mensaje: Dict):
        """Ayuda a otra sociedad que lo solicita"""
        if self.calidad > 70:
            ayuda = {
                "consejo": f"Mejora tu cobertura de tests",
                "prioridad": "alta",
                "ejemplo": "Agrega pruebas unitarias"
            }
            self.canal.enviar_mensaje(self.nombre, mensaje["emisor"], "consejo_recibido", ayuda)
            print(f"      🤝 {self.nombre} ayudó a {mensaje['emisor']}")
            
    def _aprender_de_otra(self, mensaje: Dict):
        """Aprende de otras sociedades"""
        conocimiento = mensaje["contenido"].get("conocimiento", {})
        self.conocimiento.update(conocimiento)
        print(f"      🧠 {self.nombre} aprendió de {mensaje['emisor']}")
        
    def _celebrar_mejora(self, mensaje: Dict):
        """Celebra mejoras de otras sociedades"""
        print(f"      🎉 {self.nombre} celebra mejora de {mensaje['emisor']}")
        
    def _reaccionar_alerta(self, mensaje: Dict):
        """Reacciona a alertas de otras sociedades"""
        print(f"      ⚠️ {self.nombre} recibió alerta de {mensaje['emisor']}")
        
    def mejorar(self) -> float:
        """Mejora la calidad de la sociedad"""
        mejora = random.uniform(1, 5)
        self.calidad = min(100, self.calidad + mejora)
        self.deuda_tecnica = max(0, self.deuda_tecnica - mejora * 0.3)
        self.puntos += int(mejora * 10)
        
        # Registrar mejora en historial
        self.historial.append({
            "timestamp": datetime.now().isoformat(),
            "mejora": mejora,
            "calidad": self.calidad
        })
        
        # Si la mejora es significativa, compartir con todos
        if mejora > 3:
            self.canal.broadcast(self.nombre, "mejora_significativa", {
                "mejora": mejora,
                "nueva_calidad": self.calidad
            })
        
        return mejora
    
    def solicitar_ayuda(self):
        """Solicita ayuda a otras sociedades"""
        if self.calidad < 50:
            self.canal.broadcast(self.nombre, "solicitar_ayuda", {
                "problema": "calidad_baja",
                "calidad_actual": self.calidad
            })
            
    def compartir_conocimiento(self):
        """Comparte conocimiento con otras sociedades"""
        if self.calidad > 80:
            conocimiento = {
                "mejores_practicas": ["tests", "documentacion", "refactorizacion"],
                "calidad_alcanzada": self.calidad
            }
            self.canal.broadcast(self.nombre, "compartir_conocimiento", {
                "conocimiento": conocimiento
            })
    
    def to_dict(self) -> Dict:
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "calidad": round(self.calidad, 1),
            "deuda": round(self.deuda_tecnica, 1),
            "puntos": self.puntos,
            "conocimiento": len(self.conocimiento)
        }

# ============================================
# SOCIEDADES ESPECÍFICAS
# ============================================

class FlutterFixSociety(SociedadBase):
    def __init__(self, canal: CanalComunicacion):
        super().__init__("FlutterFix", "mobile", canal)
        self.especialidad = "Apps Móviles"
        self.tecnologias = ["Flutter", "Dart", "Android", "iOS"]
        
    def mejorar(self):
        mejora = super().mejorar()
        if self.calidad > 90:
            self.compartir_conocimiento()
        return mejora

class WebSociety(SociedadBase):
    def __init__(self, canal: CanalComunicacion):
        super().__init__("Web", "web", canal)
        self.especialidad = "Desarrollo Web"
        self.tecnologias = ["React", "Vue", "HTML/CSS", "JavaScript"]

class DevOpsSociety(SociedadBase):
    def __init__(self, canal: CanalComunicacion):
        super().__init__("DevOps", "infraestructura", canal)
        self.especialidad = "Infraestructura"
        self.tecnologias = ["Docker", "K8s", "CI/CD", "AWS"]

class DataScienceSociety(SociedadBase):
    def __init__(self, canal: CanalComunicacion):
        super().__init__("DataScience", "ia_datos", canal)
        self.especialidad = "IA y Datos"
        self.tecnologias = ["Python", "ML", "Analytics", "TensorFlow"]

class MobileWebSociety(SociedadBase):
    def __init__(self, canal: CanalComunicacion):
        super().__init__("MobileWeb", "mobile_web", canal)
        self.especialidad = "Web Móvil"
        self.tecnologias = ["PWA", "Responsive", "Mobile First"]

class GameDevSociety(SociedadBase):
    def __init__(self, canal: CanalComunicacion):
        super().__init__("GameDev", "gamedev", canal)
        self.especialidad = "Desarrollo de Juegos"
        self.tecnologias = ["Unity", "Unreal", "Godot", "2D/3D"]

class QASociety(SociedadBase):
    def __init__(self, canal: CanalComunicacion):
        super().__init__("QA", "testing", canal)
        self.especialidad = "Calidad y Testing"
        self.tecnologias = ["Unit Tests", "E2E", "Performance"]

class SecuritySociety(SociedadBase):
    def __init__(self, canal: CanalComunicacion):
        super().__init__("Security", "security", canal)
        self.especialidad = "Seguridad"
        self.tecnologias = ["OWASP", "PenTesting", "Encryption"]

# ============================================
# COORDINADOR AUTÓNOMO
# ============================================

class CoordinadorAutonomo:
    def __init__(self):
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🏛️ FLUTTERFIX v27 - SOCIEDADES AUTÓNOMAS CON COMUNICACIÓN                   ║
║                                                                               ║
║   📡 Sistema de comunicación entre todas las sociedades                       ║
║   🤝 Colaboración autónoma sin intervención humana                           ║
║   🧠 Aprendizaje mutuo y mejora continua                                     ║
║   🔄 Actualización en tiempo real                                            ║
║                                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
        
        # Crear canal de comunicación
        self.canal = CanalComunicacion()
        
        # Crear todas las sociedades
        self.sociedades = {
            "FlutterFix": FlutterFixSociety(self.canal),
            "Web": WebSociety(self.canal),
            "DevOps": DevOpsSociety(self.canal),
            "DataScience": DataScienceSociety(self.canal),
            "MobileWeb": MobileWebSociety(self.canal),
            "GameDev": GameDevSociety(self.canal),
            "QA": QASociety(self.canal),
            "Security": SecuritySociety(self.canal)
        }
        
        self.ciclo_activo = True
        self.ciclo = 0
        
        print(f"\n✅ {len(self.sociedades)} sociedades registradas y comunicándose")
        print("📡 Canal de comunicación activo\n")
        
    def ciclo_mejora(self):
        """Ciclo de mejora con comunicación entre sociedades"""
        self.ciclo += 1
        
        print(f"\n{'='*60}")
        print(f"🔄 CICLO #{self.ciclo} - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}")
        
        # Primero, sociedades con calidad baja solicitan ayuda
        for sociedad in self.sociedades.values():
            sociedad.solicitar_ayuda()
        
        # Todas las sociedades mejoran
        mejoras = {}
        for nombre, sociedad in self.sociedades.items():
            mejora = sociedad.mejorar()
            mejoras[nombre] = mejora
            print(f"\n📈 {nombre}: +{mejora:.1f}% → {sociedad.calidad:.1f}%")
        
        # Sociedades con calidad alta comparten conocimiento
        for sociedad in self.sociedades.values():
            sociedad.compartir_conocimiento()
        
        # Mostrar resumen de comunicación
        mensajes_no_leidos = sum(len(self.canal.obtener_mensajes_no_leidos(nombre)) 
                                for nombre in self.sociedades)
        
        print(f"\n📊 RESUMEN DEL CICLO:")
        print(f"   📨 Mensajes intercambiados: {len(self.canal.historial)}")
        print(f"   💬 Mensajes pendientes: {mensajes_no_leidos}")
        print(f"   🎯 Calidad promedio: {sum(s.calidad for s in self.sociedades.values()) / len(self.sociedades):.1f}%")
        
        return mejoras
    
    def ejecutar(self, ciclos: int = 20):
        """Ejecuta el ecosistema autónomo"""
        print("\n🚀 INICIANDO ECOSISTEMA AUTÓNOMO")
        print("🤝 Las sociedades se comunican y colaboran entre sí")
        print("🧠 Aprendizaje mutuo activado")
        print("📡 Sin intervención humana\n")
        
        try:
            for _ in range(ciclos):
                self.ciclo_mejora()
                time.sleep(3)
        except KeyboardInterrupt:
            print("\n\n🛑 Ecosistema detenido")
        
        self._reporte_final()
    
    def _reporte_final(self):
        """Reporte final del ecosistema"""
        print("\n" + "=" * 60)
        print("📊 REPORTE FINAL - ECOSISTEMA AUTÓNOMO")
        print("=" * 60)
        
        # Ordenar por calidad
        sorted_sociedades = sorted(self.sociedades.values(), key=lambda s: s.calidad, reverse=True)
        
        print("\n🏆 RANKING DE SOCIEDADES:")
        for i, sociedad in enumerate(sorted_sociedades, 1):
            print(f"   {i}. {sociedad.nombre}: {sociedad.calidad:.1f}% (Deuda: {sociedad.deuda_tecnica:.1f})")
        
        print(f"\n📊 ESTADÍSTICAS DE COMUNICACIÓN:")
        print(f"   Mensajes totales: {len(self.canal.historial)}")
        print(f"   Interacciones entre sociedades: {self.ciclo * len(self.sociedades)}")
        print(f"   Calidad promedio final: {sum(s.calidad for s in self.sociedades.values()) / len(self.sociedades):.1f}%")
        
        # Mostrar red de colaboración
        print("\n🌐 RED DE COLABORACIÓN:")
        for emisor in self.sociedades:
            msgs_enviados = [m for m in self.canal.historial if m["emisor"] == emisor]
            print(f"   📤 {emisor}: {len(msgs_enviados)} mensajes enviados")
        
        print("\n" + "=" * 60)
        print("🎉 ECOSISTEMA AUTÓNOMO COMPLETADO")
        print("🏛️ Las sociedades aprendieron y mejoraron juntas")
        print("=" * 60)

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    ecosistema = CoordinadorAutonomo()
    ecosistema.ejecutar(ciclos=15)
