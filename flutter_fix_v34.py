import json
import random
import time
from datetime import datetime
from typing import Dict, List, Any

# ============================================
# CONFIGURACIÓN DEL SISTEMA
# ============================================

VERSION = "34.0"
NOMBRE_SISTEMA = "FLUTTERFIX - Sistema Unificado Total con DEGC"

# ============================================
# CONOCIMIENTO (BASE)
# ============================================

class Conocimiento:
    def __init__(self, nombre: str, descripcion: str, area: str, prioridad_base: int = 50):
        self.id = f"C_{random.randint(1000, 9999)}"
        self.nombre = nombre
        self.descripcion = descripcion
        self.area = area
        self.prioridad_base = prioridad_base
        self.estado = "experimentacion"
        self.productividad_inicial = 0
        self.productividad_final = 0
        self.mejora_productividad = 0
        self.experimentos = []
        self.prioridad_final = 0
        self.fecha_creacion = datetime.now().isoformat()
        
    def registrar_experimento(self, exito: bool, mejora: float):
        self.experimentos.append({"mejora": mejora, "exito": exito})
        if len(self.experimentos) >= 3:
            self.productividad_final = sum(e["mejora"] for e in self.experimentos) / len(self.experimentos)
            self.mejora_productividad = self.productividad_final - self.productividad_inicial
            self.prioridad_final = self.prioridad_base + self.mejora_productividad
            self.estado = "validacion"
    
    def validar(self) -> bool:
        if self.mejora_productividad >= 10:
            self.estado = "aceptado"
            return True
        self.estado = "rechazado"
        return False

# ============================================
# DEPARTAMENTO DE ENSEÑANZA (DEGC)
# ============================================

class DEGC:
    def __init__(self):
        self.conocimientos = []
        self.aceptados = []
        self.rechazados = []
        
    def proponer(self, nombre, descripcion, area, productividad_base=50, prioridad=50):
        c = Conocimiento(nombre, descripcion, area, prioridad)
        c.productividad_inicial = productividad_base
        self.conocimientos.append(c)
        return c
    
    def experimentar(self, conocimiento):
        print(f"\n🧪 Experimentando: {conocimiento.nombre}")
        for i in range(3):
            exito = random.random() > 0.3
            mejora = random.uniform(5, 25) if exito else random.uniform(-10, 5)
            conocimiento.registrar_experimento(exito, mejora)
            print(f"   Test {i+1}: {'EXITO' if exito else 'FRACASO'} (mejora {mejora:+.1f}%)")
            time.sleep(0.3)
        print(f"   Mejora promedio: {conocimiento.mejora_productividad:+.1f}%")
    
    def validar_todos(self):
        for c in self.conocimientos:
            if c.estado == "validacion":
                if c.validar():
                    self.aceptados.append(c)
                    print(f"\n✅ ACEPTADO: {c.nombre} (+{c.mejora_productividad:.1f}%)")
                else:
                    self.rechazados.append(c)
                    print(f"\n❌ RECHAZADO: {c.nombre} (+{c.mejora_productividad:.1f}% < 10)")
    
    def ensenar_a_todos(self, sociedades):
        for c in self.aceptados:
            print(f"\n📢 Enseñando {c.nombre} a {len(sociedades)} sociedades...")
            for s in sociedades:
                s.recibir_conocimiento(c)
    
    def reporte(self):
        print(f"\n📊 DEGC: {len(self.aceptados)} aceptados, {len(self.rechazados)} rechazados")

# ============================================
# SOCIEDAD BASE
# ============================================

class Sociedad:
    def __init__(self, nombre, especialidad):
        self.nombre = nombre
        self.especialidad = especialidad
        self.productividad = 50.0
        self.conocimientos = []
        self.proyectos = []
        
    def recibir_conocimiento(self, conocimiento):
        self.conocimientos.append(conocimiento)
        self.productividad += conocimiento.mejora_productividad
        print(f"   {self.nombre} aprendió {conocimiento.nombre} (+{conocimiento.mejora_productividad:.1f}%)")
    
    def generar_proyecto(self, tipo):
        proyecto = {"nombre": f"Proyecto de {self.nombre}", "tipo": tipo, "estado": "creado"}
        self.proyectos.append(proyecto)
        return proyecto

# ============================================
# SISTEMA DE DECISIÓN AUTÓNOMA
# ============================================

class SistemaDecision:
    def __init__(self, degc, sociedades):
        self.degc = degc
        self.sociedades = sociedades
        self.prioridades = {}
        self.historial = []
        
    def evaluar_prioridades(self):
        print("\n🎯 EVALUANDO PRIORIDADES DEL SISTEMA")
        print("="*40)
        
        # Calcular prioridad por área
        areas = {}
        for s in self.sociedades:
            areas[s.especialidad] = areas.get(s.especialidad, 0) + 1
        
        self.prioridades = {
            "devops": areas.get("infraestructura", 0) * 10,
            "qa": areas.get("testing", 0) * 10,
            "gamedev": areas.get("gamedev", 0) * 10,
            "frontend": (areas.get("mobile_flutter", 0) + areas.get("mobile_web", 0) + areas.get("web_react", 0)) * 8,
            "ia": areas.get("ia_datos", 0) * 8,
            "seguridad": areas.get("seguridad", 0) * 10,
            "archivos": areas.get("control_archivos", 0) * 5
        }
        
        for area, prioridad in sorted(self.prioridades.items(), key=lambda x: x[1], reverse=True):
            print(f"   {area}: {prioridad:.0f}")
        
        return self.prioridades
    
    def decidir_proximas_acciones(self):
        print("\n🧠 SISTEMA DECIDIENDO PRÓXIMAS ACCIONES")
        print("="*40)
        
        acciones = []
        
        # Prioridad alta = crear nuevos conocimientos
        for area, prioridad in self.prioridades.items():
            if prioridad > 30:
                acciones.append({"tipo": "crear_conocimiento", "area": area, "prioridad": prioridad})
        
        # Ordenar por prioridad
        acciones.sort(key=lambda x: x["prioridad"], reverse=True)
        
        for a in acciones[:3]:
            print(f"   → Crear conocimiento en {a['area']} (prioridad {a['prioridad']:.0f})")
        
        return acciones
    
    def ejecutar_ciclo(self):
        print("\n" + "="*60)
        print(f"🔄 CICLO DE DECISIÓN - {datetime.now().strftime('%H:%M:%S')}")
        print("="*60)
        
        # 1. Evaluar prioridades
        prioridades = self.evaluar_prioridades()
        
        # 2. Decidir acciones
        acciones = self.decidir_proximas_acciones()
        
        # 3. Ejecutar acciones prioritarias
        for accion in acciones[:2]:
            if accion["tipo"] == "crear_conocimiento":
                conocimiento = self.degc.proponer(
                    nombre=f"Optimización de {accion['area']}",
                    descripcion=f"Mejora continua para el área de {accion['area']}",
                    area=accion["area"],
                    productividad_base=50,
                    prioridad=accion["prioridad"]
                )
                self.degc.experimentar(conocimiento)
        
        # 4. Validar conocimientos
        self.degc.validar_todos()
        
        # 5. Enseñar conocimientos aceptados
        self.degc.ensenar_a_todos(self.sociedades)
        
        # 6. Registrar en historial
        self.historial.append({
            "fecha": datetime.now().isoformat(),
            "aceptados": len(self.degc.aceptados),
            "productividad_promedio": sum(s.productividad for s in self.sociedades) / len(self.sociedades)
        })
        
        return self.historial[-1]

# ============================================
# SISTEMA UNIFICADO TOTAL
# ============================================

class SistemaUnificadoTotal:
    def __init__(self):
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🏛️ {NOMBRE_SISTEMA} v{VERSION}                                             ║
║                                                                               ║
║   El sistema decide autónomamente qué hacer, cuándo y con qué prioridad     ║
║                                                                               ║
║   Módulos integrados:                                                        ║
║   • 9 Sociedades                                                             ║
║   • DEGC (Enseñanza y Gestión del Conocimiento)                              ║
║   • Sistema de Decisión Autónoma                                             ║
║                                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
        
        # Crear sociedades
        self.sociedades = [
            Sociedad("FlutterFix", "mobile_flutter"),
            Sociedad("Web", "web_react"),
            Sociedad("GameDev", "gamedev"),
            Sociedad("DataScience", "ia_datos"),
            Sociedad("QA", "testing"),
            Sociedad("DevOps", "infraestructura"),
            Sociedad("Security", "seguridad"),
            Sociedad("MobileWeb", "mobile_web"),
            Sociedad("SCAS", "control_archivos")
        ]
        
        # Crear DEGC
        self.degc = DEGC()
        
        # Crear sistema de decisión
        self.decision = SistemaDecision(self.degc, self.sociedades)
        
        self.ciclo = 0
        
    def ejecutar(self, ciclos: int = 5):
        print(f"\n🚀 INICIANDO SISTEMA UNIFICADO TOTAL")
        print(f"🎯 El sistema decidirá autónomamente qué conocimientos priorizar")
        print(f"📚 Solo conocimientos con mejora >10% serán aceptados")
        print(f"🔄 {ciclos} ciclos de decisión autónoma\n")
        
        for _ in range(ciclos):
            self.ciclo += 1
            resultado = self.decision.ejecutar_ciclo()
            time.sleep(2)
        
        self.reporte_final()
    
    def reporte_final(self):
        print("\n" + "="*60)
        print("📊 REPORTE FINAL DEL SISTEMA UNIFICADO")
        print("="*60)
        
        print(f"\n🏛️ SOCIEDADES:")
        for s in self.sociedades:
            print(f"   {s.nombre}: Productividad {s.productividad:.1f}% | Conocimientos: {len(s.conocimientos)}")
        
        print(f"\n📚 DEPARTAMENTO DE ENSEÑANZA (DEGC):")
        print(f"   Conocimientos aceptados: {len(self.degc.aceptados)}")
        print(f"   Conocimientos rechazados: {len(self.degc.rechazados)}")
        
        if self.degc.aceptados:
            print(f"\n🏆 CONOCIMIENTOS ACEPTADOS:")
            for c in self.degc.aceptados:
                print(f"   • {c.nombre} (+{c.mejora_productividad:.1f}%) - Prioridad {c.prioridad_final:.0f}")
        
        print(f"\n🔄 HISTORIAL DE DECISIONES: {len(self.decision.historial)}")
        print(f"   Productividad promedio final: {sum(s.productividad for s in self.sociedades) / len(self.sociedades):.1f}%")
        
        print("\n" + "="*60)
        print("🎯 EL SISTEMA DECIDIÓ AUTÓNOMAMENTE")
        print("📚 EL CONOCIMIENTO SE PROPAGÓ A TODOS LOS NODOS")
        print("✅ SOLO MEJORAS >10% FUERON ACEPTADAS")
        print("="*60)

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    sistema = SistemaUnificadoTotal()
    sistema.ejecutar(ciclos=5)
