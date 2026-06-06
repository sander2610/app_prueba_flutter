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

# ============================================
# CONFIGURACIÓN DE NOTIFICACIONES
# ============================================

EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email": os.environ.get("NOTIFY_EMAIL", ""),
    "password": os.environ.get("NOTIFY_PASSWORD", "")
}

SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK", "")

# ============================================
# INTELIGENCIA ARTIFICIAL PARA DECISIONES AUTÓNOMAS
# ============================================

class IASociety:
    """IA que toma decisiones autónomas para mejorar las sociedades"""
    
    def __init__(self):
        self.decisiones = []
        self.aprendizaje = {}
        
    def analizar_metricas(self, sociedades: Dict) -> Dict:
        """Analiza métricas y sugiere mejoras"""
        sugerencias = {}
        
        for nombre, sociedad in sociedades.items():
            if sociedad.calidad < 80:
                sugerencias[nombre] = {
                    "accion": "mejorar_calidad",
                    "prioridad": "alta",
                    "esfuerzo": random.randint(1, 5)
                }
            elif sociedad.deuda_tecnica > 50:
                sugerencias[nombre] = {
                    "accion": "reducir_deuda",
                    "prioridad": "media",
                    "esfuerzo": random.randint(1, 3)
                }
            else:
                sugerencias[nombre] = {
                    "accion": "mantenimiento",
                    "prioridad": "baja",
                    "esfuerzo": random.randint(1, 2)
                }
        
        self.decisiones.append({
            "timestamp": datetime.now().isoformat(),
            "sugerencias": sugerencias
        })
        
        return sugerencias
    
    def aprender(self, resultado: Dict):
        """Aprende de resultados pasados"""
        self.aprendizaje[datetime.now().isoformat()] = resultado

# ============================================
# SOCIEDADES EXISTENTES + NUEVAS
# ============================================

class FlutterFixSociety:
    def __init__(self):
        self.nombre = "FlutterFix Society"
        self.tipo = "mobile"
        self.calidad = 96.0
        self.deuda_tecnica = 14.0
        self.puntos = 8553
        self.version = "23.0"
        
    def mejorar(self):
        mejora = random.uniform(0.5, 2)
        self.calidad = min(100, self.calidad + mejora)
        self.deuda_tecnica = max(0, self.deuda_tecnica - mejora * 0.3)
        return mejora
    
    def to_dict(self):
        return {"nombre": self.nombre, "tipo": self.tipo, "calidad": round(self.calidad, 1), 
                "deuda": round(self.deuda_tecnica, 1), "puntos": self.puntos}

class WebSociety:
    def __init__(self):
        self.nombre = "Web Society"
        self.tipo = "web"
        self.calidad = 91.2
        self.deuda_tecnica = 87.0
        self.puntos = 256
        
    def mejorar(self):
        mejora = random.uniform(0.5, 3)
        self.calidad = min(100, self.calidad + mejora)
        self.deuda_tecnica = max(0, self.deuda_tecnica - mejora * 0.2)
        return mejora
    
    def to_dict(self):
        return {"nombre": self.nombre, "tipo": self.tipo, "calidad": round(self.calidad, 1), 
                "deuda": round(self.deuda_tecnica, 1), "puntos": self.puntos}

class DevOpsSociety:
    def __init__(self):
        self.nombre = "DevOps Society"
        self.tipo = "infraestructura"
        self.calidad = 70.0
        self.deuda_tecnica = 60.0
        self.puntos = 0
        
    def mejorar(self):
        mejora = random.uniform(1, 4)
        self.calidad = min(100, self.calidad + mejora)
        self.deuda_tecnica = max(0, self.deuda_tecnica - mejora * 0.25)
        return mejora
    
    def to_dict(self):
        return {"nombre": self.nombre, "tipo": self.tipo, "calidad": round(self.calidad, 1), 
                "deuda": round(self.deuda_tecnica, 1), "puntos": self.puntos}

class DataScienceSociety:
    def __init__(self):
        self.nombre = "Data Science Society"
        self.tipo = "ia_datos"
        self.calidad = 65.0
        self.deuda_tecnica = 70.0
        self.puntos = 0
        
    def mejorar(self):
        mejora = random.uniform(1, 3.5)
        self.calidad = min(100, self.calidad + mejora)
        self.deuda_tecnica = max(0, self.deuda_tecnica - mejora * 0.3)
        return mejora
    
    def to_dict(self):
        return {"nombre": self.nombre, "tipo": self.tipo, "calidad": round(self.calidad, 1), 
                "deuda": round(self.deuda_tecnica, 1), "puntos": self.puntos}

# NUEVAS SOCIEDADES
class MobileWebSociety:
    def __init__(self):
        self.nombre = "Mobile Web Society"
        self.tipo = "mobile_web"
        self.calidad = 55.0
        self.deuda_tecnica = 80.0
        self.puntos = 0
        print("   📱 Mobile Web Society creada")
        
    def mejorar(self):
        mejora = random.uniform(1, 4)
        self.calidad = min(100, self.calidad + mejora)
        self.deuda_tecnica = max(0, self.deuda_tecnica - mejora * 0.2)
        return mejora
    
    def to_dict(self):
        return {"nombre": self.nombre, "tipo": self.tipo, "calidad": round(self.calidad, 1), 
                "deuda": round(self.deuda_tecnica, 1), "puntos": self.puntos}

class GameDevSociety:
    def __init__(self):
        self.nombre = "Game Dev Society"
        self.tipo = "gamedev"
        self.calidad = 50.0
        self.deuda_tecnica = 85.0
        self.puntos = 0
        print("   🎮 Game Dev Society creada")
        
    def mejorar(self):
        mejora = random.uniform(1, 5)
        self.calidad = min(100, self.calidad + mejora)
        self.deuda_tecnica = max(0, self.deuda_tecnica - mejora * 0.15)
        return mejora
    
    def to_dict(self):
        return {"nombre": self.nombre, "tipo": self.tipo, "calidad": round(self.calidad, 1), 
                "deuda": round(self.deuda_tecnica, 1), "puntos": self.puntos}

class QASociety:
    def __init__(self):
        self.nombre = "QA Society"
        self.tipo = "testing"
        self.calidad = 60.0
        self.deuda_tecnica = 75.0
        self.puntos = 0
        print("   🧪 QA Society creada")
        
    def mejorar(self):
        mejora = random.uniform(1, 3)
        self.calidad = min(100, self.calidad + mejora)
        self.deuda_tecnica = max(0, self.deuda_tecnica - mejora * 0.35)
        return mejora
    
    def to_dict(self):
        return {"nombre": self.nombre, "tipo": self.tipo, "calidad": round(self.calidad, 1), 
                "deuda": round(self.deuda_tecnica, 1), "puntos": self.puntos}

class SecuritySociety:
    def __init__(self):
        self.nombre = "Security Society"
        self.tipo = "security"
        self.calidad = 55.0
        self.deuda_tecnica = 78.0
        self.puntos = 0
        print("   🔒 Security Society creada")
        
    def mejorar(self):
        mejora = random.uniform(1, 4)
        self.calidad = min(100, self.calidad + mejora)
        self.deuda_tecnica = max(0, self.deuda_tecnica - mejora * 0.3)
        return mejora
    
    def to_dict(self):
        return {"nombre": self.nombre, "tipo": self.tipo, "calidad": round(self.calidad, 1), 
                "deuda": round(self.deuda_tecnica, 1), "puntos": self.puntos}

# ============================================
# SISTEMA DE NOTIFICACIONES
# ============================================

class SistemaNotificaciones:
    def __init__(self):
        self.notificaciones = []
        
    def enviar_email(self, asunto: str, mensaje: str):
        if not EMAIL_CONFIG["email"]:
            return
        try:
            server = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
            server.starttls()
            server.login(EMAIL_CONFIG["email"], EMAIL_CONFIG["password"])
            email_msg = f"Subject: {asunto}\n\n{mensaje}"
            server.sendmail(EMAIL_CONFIG["email"], EMAIL_CONFIG["email"], email_msg)
            server.quit()
            print(f"   📧 Email enviado: {asunto}")
        except Exception as e:
            print(f"   ⚠️ Error email: {e}")
    
    def enviar_slack(self, mensaje: str):
        if not SLACK_WEBHOOK:
            return
        try:
            requests.post(SLACK_WEBHOOK, json={"text": mensaje})
            print(f"   💬 Slack notificación enviada")
        except:
            pass
    
    def notificar_mejora(self, sociedad: str, mejora: float):
        mensaje = f"🌟 {sociedad} mejoró en +{mejora:.1f}%"
        self.notificaciones.append(mensaje)
        print(f"   🔔 {mensaje}")
        if len(self.notificaciones) % 5 == 0:
            self.enviar_email("Mejora en el ecosistema", "\n".join(self.notificaciones[-5:]))

# ============================================
# INTERFAZ GRÁFICA DESKTOP (Tkinter)
# ============================================

class InterfazDesktop:
    def __init__(self, ecosistema):
        self.ecosistema = ecosistema
        self.ventana = None
        
    def iniciar(self):
        try:
            import tkinter as tk
            from tkinter import ttk
            
            self.ventana = tk.Tk()
            self.ventana.title("FlutterFix - Ecosistema de Sociedades")
            self.ventana.geometry("800x600")
            self.ventana.configure(bg="#1a1a2e")
            
            # Título
            titulo = tk.Label(self.ventana, text="🏛️ ECOSISTEMA DE SOCIEDADES", 
                              font=("Arial", 18, "bold"), bg="#1a1a2e", fg="white")
            titulo.pack(pady=10)
            
            # Frame para las sociedades
            frame = tk.Frame(self.ventana, bg="#1a1a2e")
            frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Grid de sociedades
            self.labels = {}
            for i, (nombre, sociedad) in enumerate(self.ecosistema.sociedades.items()):
                card = tk.Frame(frame, bg="#2d2d44", relief=tk.RAISED, bd=2)
                card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
                
                tk.Label(card, text=nombre, font=("Arial", 12, "bold"), 
                        bg="#2d2d44", fg="#667eea").pack(pady=5)
                
                self.labels[nombre] = {}
                self.labels[nombre]["calidad"] = tk.Label(card, text=f"Calidad: {sociedad.calidad}%", 
                                                          bg="#2d2d44", fg="white")
                self.labels[nombre]["calidad"].pack()
                
                self.labels[nombre]["deuda"] = tk.Label(card, text=f"Deuda: {sociedad.deuda_tecnica}/100", 
                                                        bg="#2d2d44", fg="white")
                self.labels[nombre]["deuda"].pack()
                
                self.labels[nombre]["puntos"] = tk.Label(card, text=f"Puntos: {sociedad.puntos}", 
                                                         bg="#2d2d44", fg="#f59e0b")
                self.labels[nombre]["puntos"].pack()
            
            # Botón de actualización manual
            def actualizar():
                self.ecosistema.ciclo_mejora()
                self.actualizar_ui()
            
            btn = tk.Button(self.ventana, text="🔄 Mejorar Ahora", command=actualizar,
                           bg="#667eea", fg="white", font=("Arial", 12), padx=20, pady=10)
            btn.pack(pady=10)
            
            # Actualizar automáticamente
            def auto_update():
                self.ecosistema.ciclo_mejora()
                self.actualizar_ui()
                self.ventana.after(10000, auto_update)
            
            self.ventana.after(5000, auto_update)
            self.ventana.mainloop()
            
        except ImportError:
            print("⚠️ Tkinter no disponible. Instala python-tk para la interfaz gráfica")
    
    def actualizar_ui(self):
        for nombre, sociedad in self.ecosistema.sociedades.items():
            if nombre in self.labels:
                self.labels[nombre]["calidad"].config(text=f"Calidad: {sociedad.calidad:.1f}%")
                self.labels[nombre]["deuda"].config(text=f"Deuda: {sociedad.deuda_tecnica:.1f}/100")
                self.labels[nombre]["puntos"].config(text=f"Puntos: {sociedad.puntos}")

# ============================================
# DEPLOY EN LA NUBE (Railway/Heroku)
# ============================================

class DeployNube:
    @staticmethod
    def generar_railway_json():
        config = {
            "build": {"builder": "nixpacks"},
            "environments": {
                "production": {
                    "variables": {
                        "FLASK_ENV": "production",
                        "PYTHON_VERSION": "3.11"
                    }
                }
            }
        }
        with open("railway.json", "w") as f:
            json.dump(config, f, indent=2)
        print("📦 railway.json generado para deploy en Railway")
    
    @staticmethod
    def generar_dockerfile():
        dockerfile = '''
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "ecosistema_completo.py"]
'''
        with open("Dockerfile", "w") as f:
            f.write(dockerfile)
        print("🐳 Dockerfile generado")
    
    @staticmethod
    def generar_requirements():
        reqs = ["flask", "requests", "psutil"]
        with open("requirements.txt", "w") as f:
            f.write("\n".join(reqs))
        print("📋 requirements.txt generado")

# ============================================
# COORDINADOR PRINCIPAL
# ============================================

class CoordinadorEcosistema:
    def __init__(self):
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🏛️ FLUTTERFIX v26 - ECOSISTEMA SUPREMO                                      ║
║                                                                               ║
║   🤖 7 SOCIEDADES HERMANAS INTEGRADAS:                                        ║
║   1. FlutterFix Society     - Apps Móviles                                   ║
║   2. Web Society            - Desarrollo Web                                 ║
║   3. DevOps Society         - Infraestructura                                ║
║   4. Data Science Society   - IA/Datos                                       ║
║   5. Mobile Web Society     - Web Móvil (NUEVA)                              ║
║   6. Game Dev Society       - Desarrollo de Juegos (NUEVA)                   ║
║   7. QA Society             - Calidad/Testing (NUEVA)                        ║
║   8. Security Society       - Seguridad (NUEVA)                              ║
║                                                                               ║
║   ✅ IA para decisiones autónomas                                            ║
║   ✅ Interfaz gráfica desktop (Tkinter)                                     ║
║   ✅ Notificaciones por Email/Slack                                         ║
║   ✅ Despliegue en la nube (Railway/Docker)                                 ║
║   ✅ Panel web unificado                                                     ║
║                                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
        
        # Todas las sociedades
        self.sociedades = {
            "FlutterFix": FlutterFixSociety(),
            "Web": WebSociety(),
            "DevOps": DevOpsSociety(),
            "DataScience": DataScienceSociety(),
            "MobileWeb": MobileWebSociety(),
            "GameDev": GameDevSociety(),
            "QA": QASociety(),
            "Security": SecuritySociety()
        }
        
        self.ia = IASociety()
        self.notificaciones = SistemaNotificaciones()
        self.ciclo_activo = True
        
        # Preparar deploy
        DeployNube.generar_railway_json()
        DeployNube.generar_dockerfile()
        DeployNube.generar_requirements()
        
    def ciclo_mejora(self):
        mejora_total = 0
        mejoras = {}
        
        # IA analiza y sugiere
        sugerencias = self.ia.analizar_metricas(self.sociedades)
        
        for nombre, sociedad in self.sociedades.items():
            mejora = sociedad.mejorar()
            mejoras[nombre] = mejora
            mejora_total += mejora
            
            # Notificar mejoras significativas
            if mejora > 2:
                self.notificaciones.notificar_mejora(nombre, mejora)
        
        # Mostrar resumen
        print(f"\n🔄 MEJORAS - {datetime.now().strftime('%H:%M:%S')}")
        for nombre, mejora in mejoras.items():
            sociedad = self.sociedades[nombre]
            print(f"   {nombre}: +{mejora:.1f}% → {sociedad.calidad:.1f}%")
        
        return mejora_total
    
    def ejecutar(self):
        print("\n🚀 INICIANDO ECOSISTEMA SUPREMO")
        print("=" * 60)
        
        # Elegir modo de ejecución
        print("\n📋 SELECCIONA MODO DE EJECUCIÓN:")
        print("1. 🌐 Panel Web (http://localhost:5000)")
        print("2. 🖥️ Interfaz Gráfica Desktop (Tkinter)")
        print("3. 🔄 Ambos (Web + Mejora automática)")
        
        opcion = input("\n💡 Elige (1-3): ").strip()
        
        if opcion in ["1", "3"]:
            # Iniciar panel web
            from flask import Flask, render_template_string
            app = Flask(__name__)
            
            @app.route('/')
            def dashboard():
                return render_template_string(HTML_TEMPLATE, 
                    sociedades=self.sociedades,
                    actualizado=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
            
            @app.route('/api/estado')
            def api_estado():
                return jsonify({k: v.to_dict() for k, v in self.sociedades.items()})
            
            hilo_web = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False), daemon=True)
            hilo_web.start()
            print("\n🌐 Panel web en http://localhost:5000")
            webbrowser.open("http://localhost:5000")
        
        if opcion in ["2", "3"]:
            # Interfaz gráfica
            hilo_gui = threading.Thread(target=lambda: InterfazDesktop(self).iniciar(), daemon=True)
            hilo_gui.start()
            print("🖥️ Interfaz gráfica iniciada")
        
        if opcion == "3":
            # Ciclo de mejora automático
            print("\n🔄 Ciclo de mejora automática cada 10 segundos")
            try:
                while self.ciclo_activo:
                    self.ciclo_mejora()
                    time.sleep(10)
            except KeyboardInterrupt:
                print("\n\n🛑 Ecosistema detenido")

# ============================================
# HTML TEMPLATE ACTUALIZADO
# ============================================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FlutterFix - Ecosistema Supremo</title>
    <meta http-equiv="refresh" content="5">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { text-align: center; color: white; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); transition: transform 0.3s; }
        .card:hover { transform: translateY(-5px); }
        .card h3 { color: #667eea; margin-bottom: 15px; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
        .metric { font-size: 2em; font-weight: bold; color: #764ba2; }
        .progress-bar { background: #e0e0e0; border-radius: 10px; height: 20px; overflow: hidden; margin: 10px 0; }
        .progress-fill { background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; border-radius: 10px; transition: width 0.5s; }
        .badge { display: inline-block; padding: 5px 10px; border-radius: 20px; font-size: 0.8em; margin: 2px; }
        .success { background: #10b981; color: white; }
        .warning { background: #f59e0b; color: white; }
        .footer { text-align: center; color: white; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏛️ ECOSISTEMA SUPREMO</h1>
            <p>8 Sociedades Hermanas | Actualizado: {{ actualizado }}</p>
        </div>
        <div class="grid">
            {% for nombre, sociedad in sociedades.items() %}
            <div class="card">
                <h3>{% if sociedad.tipo == 'mobile' %}🤖{% elif sociedad.tipo == 'web' %}🌐{% elif sociedad.tipo == 'infraestructura' %}⚙️{% elif sociedad.tipo == 'ia_datos' %}🧠{% elif sociedad.tipo == 'mobile_web' %}📱{% elif sociedad.tipo == 'gamedev' %}🎮{% elif sociedad.tipo == 'testing' %}🧪{% else %}🔒{% endif %} {{ nombre }}</h3>
                <div class="metric">{{ sociedad.calidad }}%</div>
                <div class="progress-bar"><div class="progress-fill" style="width: {{ sociedad.calidad }}%"></div></div>
                <p>🔧 Deuda: {{ sociedad.deuda }}/100</p>
                <p>🏆 Puntos: {{ sociedad.puntos }}</p>
                <span class="badge success">{{ sociedad.tipo }}</span>
            </div>
            {% endfor %}
        </div>
        <div class="footer">
            <p>🤖 + 🌐 + ⚙️ + 🧠 + 📱 + 🎮 + 🧪 + 🔒 = 🏆 EXCELENCIA</p>
        </div>
    </div>
</body>
</html>
'''

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    ecosistema = CoordinadorEcosistema()
    ecosistema.ejecutar()
