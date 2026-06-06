import json
import random
import time
from datetime import datetime
from typing import Dict, List, Any

# ============================================
# DEPARTAMENTO DE ENSEÑANZA Y GESTIÓN DEL CONOCIMIENTO
# ============================================

class Conocimiento:
    def __init__(self, nombre: str, descripcion: str, area: str):
        self.id = f"CONOCIMIENTO_{random.randint(1000, 9999)}"
        self.nombre = nombre
        self.descripcion = descripcion
        self.area = area
        self.estado = "experimentacion"  # experimentacion, validacion, aceptado, rechazado
        self.productividad_inicial = 0
        self.productividad_final = 0
        self.mejora_productividad = 0
        self.experimentos = []
        self.fecha_creacion = datetime.now().isoformat()
        self.fecha_validacion = None
        
    def registrar_experimento(self, exito: bool, mejora: float):
        self.experimentos.append({
            "fecha": datetime.now().isoformat(),
            "exito": exito,
            "mejora_productividad": mejora
        })
        if len(self.experimentos) >= 3:
            self.productividad_final = sum(e["mejora_productividad"] for e in self.experimentos) / len(self.experimentos)
            self.mejora_productividad = self.productividad_final - self.productividad_inicial
            self.estado = "validacion"
            
    def validar(self, umbral: float = 10) -> bool:
        if self.mejora_productividad >= umbral:
            self.estado = "aceptado"
            self.fecha_validacion = datetime.now().isoformat()
            return True
        else:
            self.estado = "rechazado"
            return False
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "area": self.area,
            "estado": self.estado,
            "mejora_productividad": round(self.mejora_productividad, 2),
            "experimentos": len(self.experimentos),
            "fecha_creacion": self.fecha_creacion[:10]
        }

class DepartamentoEnsenanza:
    def __init__(self):
        self.nombre = "DEGC - Departamento de Ensenanza y Gestion del Conocimiento"
        self.conocimientos = []
        self.conocimientos_aceptados = []
        self.conocimientos_rechazados = []
        self.historial_actualizaciones = []
        
    def proponer_conocimiento(self, nombre: str, descripcion: str, area: str, productividad_base: float = 50) -> Conocimiento:
        """Propone un nuevo conocimiento para experimentación"""
        nuevo = Conocimiento(nombre, descripcion, area)
        nuevo.productividad_inicial = productividad_base
        self.conocimientos.append(nuevo)
        print(f"\n📚 NUEVO CONOCIMIENTO PROPUESTO: {nombre}")
        print(f"   Area: {area}")
        print(f"   ID: {nuevo.id}")
        return nuevo
    
    def experimentar(self, conocimiento: Conocimiento, intentos: int = 3) -> Conocimiento:
        """Realiza experimentos de prueba y error"""
        print(f"\n🧪 EXPERIMENTANDO: {conocimiento.nombre}")
        print(f"   Intentos: {intentos}")
        
        for i in range(intentos):
            exito = random.random() > 0.3
            mejora = random.uniform(5, 25) if exito else random.uniform(-10, 5)
            conocimiento.registrar_experimento(exito, mejora)
            status = "EXITO" if exito else "FRACASO"
            print(f"   Experimento {i+1}: {status} (Mejora: {mejora:+.1f}%)")
            time.sleep(0.5)
        
        print(f"\n   Mejora promedio: {conocimiento.mejora_productividad:+.1f}%")
        return conocimiento
    
    def validar_todo(self, umbral: float = 10):
        """Valida todos los conocimientos en estado de validación"""
        for c in self.conocimientos:
            if c.estado == "validacion":
                if c.validar(umbral):
                    self.conocimientos_aceptados.append(c)
                    print(f"\n✅ CONOCIMIENTO ACEPTADO: {c.nombre}")
                    print(f"   Mejora productividad: +{c.mejora_productividad:.1f}%")
                else:
                    self.conocimientos_rechazados.append(c)
                    print(f"\n❌ CONOCIMIENTO RECHAZADO: {c.nombre}")
                    print(f"   Mejora insuficiente: {c.mejora_productividad:+.1f}% (umbral: {umbral}%)")
    
    def enseñar(self, conocimiento: Conocimiento, sociedades: List) -> int:
        """Enseña el conocimiento aceptado a todas las sociedades"""
        if conocimiento.estado != "aceptado":
            print(f"⚠️ {conocimiento.nombre} no está aceptado. No se puede enseñar.")
            return 0
        
        enseñados = 0
        print(f"\n📢 ENSEÑANDO: {conocimiento.nombre}")
        print(f"   Descripción: {conocimiento.descripcion}")
        
        for sociedad in sociedades:
            sociedad.aplicar_conocimiento(conocimiento)
            enseñados += 1
            print(f"   → {sociedad.nombre} aprendió {conocimiento.nombre}")
        
        self.historial_actualizaciones.append({
            "fecha": datetime.now().isoformat(),
            "conocimiento": conocimiento.nombre,
            "sociedades_enseñadas": enseñados
        })
        return enseñados
    
    def actualizar_todos_los_nodos(self, sociedades: List):
        """Actualiza todos los nodos/agentes con conocimientos aceptados"""
        print(f"\n🔄 ACTUALIZANDO TODOS LOS NODOS/AGENTES")
        print("="*50)
        
        for conocimiento in self.conocimientos_aceptados:
            self.enseñar(conocimiento, sociedades)
    
    def reporte_estado(self):
        """Genera reporte del departamento"""
        print("\n" + "="*60)
        print("📊 DEPARTAMENTO DE ENSEÑANZA - REPORTE DE ESTADO")
        print("="*60)
        
        print(f"\n📚 CONOCIMIENTOS TOTALES: {len(self.conocimientos)}")
        print(f"   ✅ Aceptados: {len(self.conocimientos_aceptados)}")
        print(f"   ❌ Rechazados: {len(self.conocimientos_rechazados)}")
        print(f"   🔬 En experimentación: {len([c for c in self.conocimientos if c.estado == 'experimentacion'])}")
        
        print(f"\n🏆 TOP CONOCIMIENTOS ACEPTADOS (por mejora):")
        top = sorted(self.conocimientos_aceptados, key=lambda x: x.mejora_productividad, reverse=True)[:3]
        for i, c in enumerate(top, 1):
            print(f"   {i}. {c.nombre} (+{c.mejora_productividad:.1f}%) - {c.area}")
        
        print(f"\n🔄 HISTORIAL DE ACTUALIZACIONES: {len(self.historial_actualizaciones)}")
        for h in self.historial_actualizaciones[-3:]:
            print(f"   • {h['fecha'][:16]} - {h['conocimiento']} → {h['sociedades_enseñadas']} sociedades")
        print("="*60)

# ============================================
# SOCIEDAD BASE (NODO/AGENTE)
# ============================================

class SociedadNodo:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.conocimientos_adquiridos = []
        self.productividad = 50.0
        self.historial_productividad = [50.0]
        
    def aplicar_conocimiento(self, conocimiento: Conocimiento):
        """Aplica un conocimiento aprendido"""
        if conocimiento.estado == "aceptado":
            self.conocimientos_adquiridos.append(conocimiento)
            mejora = conocimiento.mejora_productividad
            self.productividad += mejora
            self.historial_productividad.append(self.productividad)
            return mejora
        return 0
    
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "productividad": round(self.productividad, 1),
            "conocimientos": len(self.conocimientos_adquiridos),
            "mejora_total": round(self.productividad - 50, 1)
        }

# ============================================
# DEMOSTRACIÓN DEL SISTEMA
# ============================================

def demostracion():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🧠 DEPARTAMENTO DE ENSEÑANZA Y GESTIÓN DEL CONOCIMIENTO (DEGC)               ║
║                                                                               ║
║   Funciones:                                                                 ║
║   1. Investigar nuevo conocimiento mediante experimentación                  ║
║   2. Validar que el conocimiento aumente la productividad                   ║
║   3. Enseñar a todas las sociedades (nodos/agentes)                         ║
║   4. Actualizar el conocimiento validado en todo el ecosistema              ║
║                                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Crear departamento
    degc = DepartamentoEnsenanza()
    
    # Crear sociedades (nodos)
    sociedades = [
        SociedadNodo("FlutterFix"),
        SociedadNodo("Web"),
        SociedadNodo("GameDev"),
        SociedadNodo("DataScience"),
        SociedadNodo("QA"),
        SociedadNodo("DevOps"),
        SociedadNodo("Security"),
        SociedadNodo("MobileWeb"),
        SociedadNodo("SCAS")
    ]
    
    # Proponer nuevos conocimientos
    conocimientos = [
        degc.proponer_conocimiento(
            "CI/CD Automatizado",
            "Pipeline de integración y despliegue continuo automático",
            "DevOps",
            productividad_base=50
        ),
        degc.proponer_conocimiento(
            "Testing Autónomo",
            "Pruebas automáticas con IA que detectan errores antes de producción",
            "QA",
            productividad_base=45
        ),
        degc.proponer_conocimiento(
            "Animaciones Optimizadas",
            "Uso de GPU para animaciones fluidas sin pérdida de rendimiento",
            "GameDev",
            productividad_base=55
        ),
        degc.proponer_conocimiento(
            "UI Component Library",
            "Biblioteca de componentes UI reutilizables con diseño consistente",
            "Frontend",
            productividad_base=48
        )
    ]
    
    # Experimentar con cada conocimiento
    print("\n" + "="*60)
    print("🔬 FASE 1: EXPERIMENTACIÓN")
    print("="*60)
    
    for c in conocimientos:
        degc.experimentar(c, intentos=3)
        time.sleep(1)
    
    # Validar conocimientos
    print("\n" + "="*60)
    print("⚖️ FASE 2: VALIDACIÓN")
    print("="*60)
    
    degc.validar_todo(umbral=10)  # Solo acepta mejoras >10%
    
    # Enseñar y actualizar nodos
    print("\n" + "="*60)
    print("📢 FASE 3: ENSEÑANZA Y ACTUALIZACIÓN")
    print("="*60)
    
    degc.actualizar_todos_los_nodos(sociedades)
    
    # Mostrar estado final de las sociedades
    print("\n" + "="*60)
    print("🏛️ ESTADO FINAL DE LAS SOCIEDADES (NODOS)")
    print("="*60)
    
    for s in sociedades:
        print(f"\n{s.nombre}:")
        print(f"   Productividad: {s.productividad:.1f}%")
        print(f"   Conocimientos adquiridos: {len(s.conocimientos_adquiridos)}")
        if s.conocimientos_adquiridos:
            print(f"   Mejora total: +{s.productividad - 50:.1f}%")
    
    # Reporte final
    degc.reporte_estado()
    
    print("\n" + "="*60)
    print("🎯 EL CONOCIMIENTO SE PROPAGA POR TODOS LOS NODOS")
    print("📚 Solo el conocimiento validado (mejora >10%) es aceptado")
    print("🔄 El sistema se actualiza automáticamente")
    print("="*60)

if __name__ == "__main__":
    demostracion()
