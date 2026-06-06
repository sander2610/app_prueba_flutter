import json
import re
import os
import sqlite3
import subprocess
import threading
import time
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import defaultdict
import math

# ============================================
# CONFIGURACIÓN DE RECURSOS LIMITADOS
# ============================================

class Recurso:
    CPU = "cpu"
    MEMORIA = "memoria"
    DISCO = "disco"

# ============================================
# DEPARTAMENTO DE ECONOMÍA (PRESUPUESTOS)
# ============================================

class DepartamentoEconomia:
    def __init__(self):
        self.presupuesto_total = 1000
        self.presupuesto_usado = 0
        self.costos_operativos = {
            "patrullaje": 10,
            "departamento_nuevo": 200,
            "expansion_agentes": 50,
            "investigacion": 30,
            "calidad_mejora": 40
        }
        self.historial_gastos = []
        
    def asignar_presupuesto(self, actividad: str) -> bool:
        """Asigna presupuesto para una actividad"""
        costo = self.costos_operativos.get(actividad, 0)
        
        if self.presupuesto_total - self.presupuesto_usado >= costo:
            self.presupuesto_usado += costo
            self.historial_gastos.append({
                "actividad": actividad,
                "costo": costo,
                "timestamp": datetime.now().isoformat()
            })
            print(f"   💰 Presupuesto asignado: {costo} ({actividad})")
            return True
        else:
            print(f"   ⚠️ Presupuesto insuficiente para: {actividad}")
            return False
    
    def reportar_ahorro(self, cantidad: int, motivo: str):
        """Reporta ahorro de recursos"""
        self.presupuesto_usado -= cantidad
        print(f"   💰 Ahorro: {cantidad} ({motivo})")
    
    def estado_financiero(self) -> dict:
        return {
            "total": self.presupuesto_total,
            "usado": self.presupuesto_usado,
            "disponible": self.presupuesto_total - self.presupuesto_usado
        }

# ============================================
# DEPARTAMENTO DE SALUD DEL CÓDIGO
# ============================================

class DepartamentoSaludCodigo:
    def __init__(self):
        self.deuda_tecnica = 100  # 0-100, 100 es peor
        self.metricas_salud = {
            "complejidad_ciclomatica": 0,
            "duplicacion_codigo": 0,
            "cobertura_tests": 0,
            "documentacion_faltante": 0
        }
        
    def analizar_salud(self, metricas: Dict) -> dict:
        """Analiza la salud del código base"""
        # Calcular deuda técnica basada en métricas
        deuda = 0
        deuda += metricas.get("complejidad_ciclomatica", 0) * 2
        deuda += metricas.get("duplicacion_codigo", 0) * 5
        deuda += (100 - metricas.get("test_coverage", 0)) * 0.5
        deuda += metricas.get("documentacion_faltante", 0) * 3
        
        self.deuda_tecnica = min(100, deuda)
        self.metricas_salud = metricas
        
        print(f"\n🏥 SALUD DEL CÓDIGO:")
        print(f"   Deuda técnica: {self.deuda_tecnica:.1f}/100")
        print(f"   Complejidad: {metricas.get('complejidad_ciclomatica', 0):.1f}")
        print(f"   Duplicación: {metricas.get('duplicacion_codigo', 0):.1f}%")
        print(f"   Cobertura tests: {metricas.get('test_coverage', 0):.1f}%")
        
        return {"deuda": self.deuda_tecnica, "salud": 100 - self.deuda_tecnica}
    
    def recomendar_tratamiento(self) -> List[str]:
        """Recomienda acciones para mejorar la salud"""
        tratamientos = []
        
        if self.deuda_tecnica > 80:
            tratamientos = ["🔴 REFACTORIZACIÓN URGENTE", "Eliminar código duplicado", "Aumentar cobertura de tests"]
        elif self.deuda_tecnica > 60:
            tratamientos = ["🟡 Refactorización prioritaria", "Reducir complejidad ciclomática", "Mejorar documentación"]
        elif self.deuda_tecnica > 40:
            tratamientos = ["🟢 Optimización incremental", "Pagar deuda pequeña", "Revisar código crítico"]
        else:
            tratamientos = ["🔵 Mantenimiento preventivo", "Documentar mejores prácticas", "Auditoría regular"]
        
        return tratamientos

# ============================================
# DEPARTAMENTO DE RELACIONES EXTERNAS
# ============================================

class DepartamentoRelacionesExternas:
    def __init__(self):
        self.apis_integradas = []
        self.integraciones_activas = []
        
    def verificar_apis(self) -> List[str]:
        """Verifica el estado de las APIs externas"""
        apis_sugeridas = ["GitHub API", "Flutter Pub API", "Firebase API", "Google Play API"]
        print(f"\n📡 RELACIONES EXTERNAS:")
        print(f"   APIs monitoreadas: {len(apis_sugeridas)}")
        
        for api in apis_sugeridas:
            if api not in self.apis_integradas:
                print(f"   🌐 API disponible: {api}")
                self.apis_integradas.append(api)
        
        return self.apis_integradas
    
    def sincronizar_con_github(self, repo_path: str) -> bool:
        """Sincroniza con GitHub automáticamente"""
        print(f"\n   📤 Sincronizando con GitHub...")
        try:
            subprocess.run(f"cd {repo_path} && git add . && git commit -m 'Auto-corrección por Sociedad'", 
                          shell=True, capture_output=True)
            subprocess.run(f"cd {repo_path} && git push", shell=True, capture_output=True)
            print("   ✅ Sincronización exitosa")
            return True
        except:
            print("   ⚠️ Error en sincronización")
            return False

# ============================================
# SISTEMA DE RECOMPENSAS
# ============================================

class SistemaRecompensas:
    def __init__(self):
        self.puntos = 0
        self.logros = []
        self.festejos = [
            "🎉 ¡Excelente trabajo!",
            "🏆 Logro desbloqueado!",
            "🌟 ¡Calidad mejorada!",
            "💪 La sociedad está más fuerte!",
            "🎯 Objetivo superado!",
            "✨ ¡Evolución exitosa!"
        ]
        
    def celebrar_mejora(self, mejora: float, tipo: str):
        """Celebra cuando hay mejora de calidad"""
        puntos_ganados = int(mejora * 10)
        self.puntos += puntos_ganados
        
        festejo = random.choice(self.festejos)
        print(f"\n{festejo}")
        print(f"   {tipo}: +{mejora:.1f}% de mejora")
        print(f"   🎁 Puntos ganados: +{puntos_ganados}")
        
        if mejora > 5:
            print("   🔥 ¡MEJORA SIGNIFICATIVA! 🔥")
    
    def celebrar_creacion_departamento(self, nombre: str):
        """Celebra la creación de un nuevo departamento"""
        puntos_ganados = 100
        self.puntos += puntos_ganados
        
        print(f"\n🎊 ¡NUEVO DEPARTAMENTO CREADO! 🎊")
        print(f"   {nombre}")
        print(f"   🎁 Puntos bonus: +{puntos_ganados}")
    
    def obtener_recompensas(self) -> dict:
        return {"puntos": self.puntos, "logros": self.logros}

# ============================================
# DEPARTAMENTO DE OPTIMIZACIÓN DE RECURSOS
# ============================================

class DepartamentoOptimizacionRecursos:
    def __init__(self, economia: DepartamentoEconomia):
        self.economia = economia
        self.cpu_limite = 80.0
        self.memoria_limite = 70.0
        self.disco_limite = 85.0
        self.cpu_actual = 0.0
        self.memoria_actual = 0.0
        self.disco_actual = 0.0
        self.patrullas_activas = 10
        self.max_patrullas = 20
        self.min_patrullas = 5
        self.ajustes_realizados = []
        
    def medir_recursos(self):
        """Simula la medición de recursos"""
        self.cpu_actual = random.uniform(10, 60)
        self.memoria_actual = random.uniform(30, 70)
        self.disco_actual = random.uniform(20, 50)
    
    def monitorear(self):
        """Monitorea el uso de recursos y ajusta"""
        self.medir_recursos()
        
        print(f"\n💰 RECURSOS ACTUALES:")
        print(f"   CPU: {self.cpu_actual:.1f}% (límite: {self.cpu_limite}%)")
        print(f"   Memoria: {self.memoria_actual:.1f}% (límite: {self.memoria_limite}%)")
        print(f"   Disco: {self.disco_actual:.1f}% (límite: {self.disco_limite}%)")
        
        # Verificar sobrecarga
        if self.cpu_actual > self.cpu_limite:
            self._reducir_carga("CPU")
            return False
        return True
    
    def _reducir_carga(self, recurso: str):
        print(f"\n⚠️ SOBRECARGA DETECTADA en {recurso}")
        if self.patrullas_activas > self.min_patrullas:
            self.patrullas_activas -= 2
            print(f"   🔧 Patrullajes reducidos a {self.patrullas_activas}")
            self.economia.reportar_ahorro(50, f"Reducción por sobrecarga de {recurso}")
    
    def ajustar_patrullajes(self, fallas_detectadas: int, patrullas_realizadas: int):
        """Ajusta la frecuencia de patrullajes según efectividad"""
        if patrullas_realizadas == 0:
            return
        
        tasa_fallas = fallas_detectadas / patrullas_realizadas
        
        if tasa_fallas < 0.05 and self.patrullas_activas > self.min_patrullas:
            self.patrullas_activas -= 1
            print(f"\n🔧 Optimizando: Patrullajes reducidos a {self.patrullas_activas}")
            self.economia.reportar_ahorro(30, "Optimización de patrullajes")
        
        elif tasa_fallas > 0.3 and self.patrullas_activas < self.max_patrullas:
            if self.economia.asignar_presupuesto("patrullaje"):
                self.patrullas_activas += 1
                print(f"\n🔧 Detectadas fallas: Patrullajes aumentados a {self.patrullas_activas}")

# ============================================
# ORGANISMO DE EXPANSIÓN DINÁMICA
# ============================================

class OrganismoExpansionDinamica:
    def __init__(self, economia: DepartamentoEconomia, recompensas: SistemaRecompensas):
        self.economia = economia
        self.recompensas = recompensas
        self.complejidad_actual = 1.0
        self.departamentos_creados = []
        self.expansiones_realizadas = []
        self.ultima_expansion = 0
        
    def evaluar_complejidad(self, metricas: Dict) -> float:
        """Evalúa la complejidad del sistema"""
        complejidad = 1.0
        complejidad += min(3.0, metricas.get("errores", 0) * 0.1)
        complejidad += min(2.0, metricas.get("lineas_codigo", 0) / 100000)
        complejidad += min(2.0, metricas.get("dependencias", 0) * 0.05)
        complejidad += min(3.0, metricas.get("vulnerabilidades", 0) * 0.2)
        
        self.complejidad_actual = min(10.0, max(1.0, complejidad))
        return self.complejidad_actual
    
    def necesita_expansion(self, ciclo_actual: int) -> bool:
        """Determina si se necesita crear nuevos departamentos"""
        if ciclo_actual - self.ultima_expansion < 8:
            return False
            
        if self.complejidad_actual >= 9.0 and len(self.departamentos_creados) < 5:
            return True
        elif self.complejidad_actual >= 7.0 and len(self.departamentos_creados) < 3:
            return True
        elif self.complejidad_actual >= 5.0 and len(self.departamentos_creados) < 1:
            return True
        return False
    
    def crear_departamento(self, tipo: str, especialidad: str, agentes: int, ciclo: int):
        """Crea un nuevo departamento"""
        if not self.economia.asignar_presupuesto("departamento_nuevo"):
            return None
            
        nuevo = {
            "id": len(self.departamentos_creados) + 1,
            "nombre": f"Departamento de {tipo}",
            "especialidad": especialidad,
            "agentes": agentes,
            "ciclo_creacion": ciclo
        }
        self.departamentos_creados.append(nuevo)
        self.expansiones_realizadas.append(nuevo)
        self.ultima_expansion = ciclo
        
        self.recompensas.celebrar_creacion_departamento(nuevo['nombre'])
        
        print(f"\n🚀 NUEVO DEPARTAMENTO: {nuevo['nombre']}")
        print(f"   Especialidad: {especialidad}")
        print(f"   Agentes asignados: {agentes}")
        return nuevo

# ============================================
# SISTEMA DE CALIDAD INFINITA
# ============================================

class SistemaCalidadInfinita:
    def __init__(self, economia: DepartamentoEconomia, recompensas: SistemaRecompensas):
        self.economia = economia
        self.recompensas = recompensas
        self.calidad_actual = 60.0
        self.calidad_exigida = 100.0
        self.historial_calidad = []
        self.ultima_calidad = 60.0
        
    def evaluar_calidad(self, metricas: Dict, ciclo: int) -> float:
        """Evalúa la calidad actual"""
        calidad = 50.0
        calidad += min(30, metricas.get("test_coverage", 0) * 0.3)
        calidad += min(20, 20 - metricas.get("vulnerabilidades", 10))
        calidad -= metricas.get("deuda_tecnica", 0) * 0.1
        
        self.ultima_calidad = self.calidad_actual
        self.calidad_actual = min(100.0, max(0, calidad))
        self.historial_calidad.append(self.calidad_actual)
        
        # Detectar mejora
        mejora = self.calidad_actual - self.ultima_calidad
        if mejora > 0:
            self.recompensas.celebrar_mejora(mejora, "Calidad mejorada")
            if mejora > 3:
                self.economia.reportar_ahorro(20, f"Mejora de calidad de {mejora:.1f}%")
        
        brecha = self.calidad_exigida - self.calidad_actual
        
        print(f"\n🎯 CALIDAD ACTUAL: {self.calidad_actual:.1f}%")
        print(f"   Exigida: {self.calidad_exigida:.0f}%")
        print(f"   Brecha: {brecha:.1f} puntos")
        
        return self.calidad_actual
    
    def generar_plan_mejora(self) -> List[str]:
        """Genera plan de mejora basado en la brecha"""
        brecha = self.calidad_exigida - self.calidad_actual
        plan = []
        
        if brecha > 40:
            plan = ["🔴 REESTRUCTURACIÓN COMPLETA", "Implementar tests masivos", "Revisión arquitectónica"]
        elif brecha > 20:
            plan = ["🟡 Optimización de algoritmos", "Mejorar cobertura de tests", "Refactorización módulos"]
        elif brecha > 10:
            plan = ["🟢 Refinar UI/UX", "Optimizar consultas", "Mejorar documentación"]
        else:
            plan = ["🔵 Pulir detalles finales", "Optimizaciones micro", "Auditoría de calidad"]
        
        return plan

# ============================================
# DEPARTAMENTO DE POLICÍA OPTIMIZADO
# ============================================

class DepartamentoPoliciaOptimizado:
    def __init__(self, dor: DepartamentoOptimizacionRecursos, economia: DepartamentoEconomia):
        self.dor = dor
        self.economia = economia
        self.patrullas_realizadas = 0
        self.infracciones = 0
        self.fallas_detectadas = 0
        
    def patrullar(self):
        """Realiza patrullajes según disponibilidad de recursos"""
        self.patrullas_realizadas += 1
        
        frecuencia = max(1, 20 // self.dor.patrullas_activas)
        
        if self.patrullas_realizadas % frecuencia == 0:
            print(f"\n👮 PATRULLA #{self.patrullas_realizadas}")
            
            fallas = random.randint(0, 3)
            self.fallas_detectadas += fallas
            
            if fallas > 0:
                print(f"   🚨 Detectadas {fallas} infracciones")
            else:
                print(f"   ✅ Sin fallas detectadas")
            
            self.dor.ajustar_patrullajes(self.fallas_detectadas, self.patrullas_realizadas)
            return fallas
        return 0

# ============================================
# SOCIEDAD PRINCIPAL
# ============================================

class SociedadFlutterFix:
    def __init__(self):
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🏛️ FLUTTERFIX v18 - SOCIEDAD COMPLETA                     ║
║                                                              ║
║   Departamentos activos:                                    ║
║   • Economía 💰       • Salud del Código 🏥                 ║
║   • Relaciones Ext. 📡  • Optimización 💰                    ║
║   • Expansión 🚀        • Policía 👮                        ║
║   • Calidad Infinita 🎯  • Recompensas 🎁                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # Sistema de recompensas (primero)
        self.recompensas = SistemaRecompensas()
        
        # Departamento de economía (segundo)
        self.economia = DepartamentoEconomia()
        
        # Demás departamentos
        self.dor = DepartamentoOptimizacionRecursos(self.economia)
        self.oed = OrganismoExpansionDinamica(self.economia, self.recompensas)
        self.calidad = SistemaCalidadInfinita(self.economia, self.recompensas)
        self.policia = DepartamentoPoliciaOptimizado(self.dor, self.economia)
        self.salud = DepartamentoSaludCodigo()
        self.relaciones = DepartamentoRelacionesExternas()
        
        self.ciclo = 0
        self.metricas = {
            "errores": 5,
            "lineas_codigo": 50000,
            "dependencias": 45,
            "vulnerabilidades": 3,
            "test_coverage": 65,
            "complejidad_ciclomatica": 25,
            "duplicacion_codigo": 15,
            "documentacion_faltante": 30
        }
        
    def actualizar_metricas(self):
        """Actualiza métricas aleatoriamente con tendencia a mejora"""
        self.metricas["errores"] = max(0, int(random.gauss(5, 2)))
        self.metricas["vulnerabilidades"] = max(0, int(random.gauss(3, 1)))
        self.metricas["test_coverage"] = min(100, self.metricas["test_coverage"] + random.uniform(-1, 3))
        self.metricas["deuda_tecnica"] = max(0, self.metricas.get("deuda_tecnica", 50) + random.uniform(-3, 2))
        
    def ciclo_principal(self):
        """Ejecuta un ciclo de la sociedad"""
        self.ciclo += 1
        
        print("\n" + "=" * 70)
        print(f"🔄 CICLO #{self.ciclo} - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 70)
        
        # 1. Relaciones Externas
        self.relaciones.verificar_apis()
        
        # 2. Optimizar recursos
        recursos_ok = self.dor.monitorear()
        
        # 3. Actualizar métricas
        self.actualizar_metricas()
        
        # 4. Salud del código
        salud = self.salud.analizar_salud(self.metricas)
        self.metricas["deuda_tecnica"] = salud["deuda"]
        
        # 5. Evaluar complejidad
        complejidad = self.oed.evaluar_complejidad(self.metricas)
        print(f"\n📊 COMPLEJIDAD: {complejidad:.2f}/10")
        
        # 6. Expansión si es necesario
        if self.oed.necesita_expansion(self.ciclo):
            if complejidad >= 9.0:
                self.oed.crear_departamento("Élite", "Alta Especialización", 10, self.ciclo)
            elif complejidad >= 7.0:
                self.oed.crear_departamento("Especializado", "Optimización Avanzada", 7, self.ciclo)
            elif complejidad >= 5.0:
                self.oed.crear_departamento("Base", "Fundacional", 5, self.ciclo)
        
        # 7. Patrullar
        if recursos_ok:
            self.policia.patrullar()
        
        # 8. Evaluar calidad
        calidad = self.calidad.evaluar_calidad(self.metricas, self.ciclo)
        
        # 9. Plan de mejora
        plan = self.calidad.generar_plan_mejora()
        if plan:
            print(f"\n📋 PLAN DE MEJORA:")
            for item in plan:
                print(f"   • {item}")
        
        # 10. Tratamiento de salud
        tratamiento = self.salud.recomendar_tratamiento()
        if tratamiento:
            print(f"\n🏥 TRATAMIENTO RECOMENDADO:")
            for item in tratamiento:
                print(f"   • {item}")
        
        # 11. Estado financiero
        finanzas = self.economia.estado_financiero()
        print(f"\n💰 ESTADO FINANCIERO:")
        print(f"   Presupuesto disponible: {finanzas['disponible']}/{finanzas['total']}")
        print(f"   Puntos de recompensa: {self.recompensas.puntos}")
    
    def reporte_final(self):
        """Reporte completo de la sociedad"""
        print("\n" + "=" * 70)
        print("📊 REPORTE FINAL DE LA SOCIEDAD")
        print("=" * 70)
        
        finanzas = self.economia.estado_financiero()
        
        print(f"\n📈 ESTADÍSTICAS GENERALES:")
        print(f"   Ciclos ejecutados: {self.ciclo}")
        print(f"   Calidad final: {self.calidad.calidad_actual:.1f}% (objetivo: 100%)")
        print(f"   Deuda técnica: {self.salud.deuda_tecnica:.1f}/100")
        print(f"   Puntos recompensa: {self.recompensas.puntos}")
        
        print(f"\n💰 FINANZAS:")
        print(f"   Presupuesto usado: {finanzas['usado']}/{finanzas['total']}")
        print(f"   Gastos registrados: {len(self.economia.historial_gastos)}")
        
        print(f"\n👮 SEGURIDAD:")
        print(f"   Patrullajes: {self.policia.patrullas_realizadas}")
        print(f"   Infracciones detectadas: {self.policia.fallas_detectadas}")
        
        print(f"\n🚀 EXPANSIÓN:")
        print(f"   Departamentos creados: {len(self.oed.departamentos_creados)}")
        if self.oed.departamentos_creados:
            for depto in self.oed.departamentos_creados:
                print(f"   • {depto['nombre']} ({depto['agentes']} agentes)")
        
        print(f"\n📡 RELACIONES EXTERNAS:")
        print(f"   APIs integradas: {len(self.relaciones.apis_integradas)}")
        
        print("\n🏆 LOGROS:")
        if self.calidad.calidad_actual > 90:
            print("   🌟 EXCELENCIA EN CALIDAD")
        if len(self.oed.departamentos_creados) >= 2:
            print("   🚀 SOCIEDAD EN EXPANSIÓN")
        if self.recompensas.puntos > 500:
            print("   💎 MAESTROS DE RECOMPENSAS")
        if self.salud.deuda_tecnica < 30:
            print("   💪 CÓDIGO SALUDABLE")
        
        print("=" * 70)
        
    def ejecutar(self):
        """Ejecuta la sociedad por 50 ciclos"""
        print("\n🚀 INICIANDO SOCIEDAD COMPLETA")
        print("🎯 Objetivo: Calidad infinita (siempre exigiendo 100%)")
        print("💰 Recursos limitados y optimizados")
        print("🏥 Monitoreo de salud del código")
        print("🎁 Sistema de recompensas activado")
        print("\n" + "=" * 70)
        
        try:
            # 50 ciclos como solicitaste
            for ciclo in range(50):
                self.ciclo_principal()
                time.sleep(2)  # Pausa entre ciclos
                
                # Reporte cada 10 ciclos
                if self.ciclo % 10 == 0:
                    print("\n" + "🎯" * 35)
                    print(f"📊 REPORTE PARCIAL - CICLO {self.ciclo}")
                    print(f"   Calidad: {self.calidad.calidad_actual:.1f}%")
                    print(f"   Deuda técnica: {self.salud.deuda_tecnica:.1f}")
                    print(f"   Puntos: {self.recompensas.puntos}")
                    print("🎯" * 35)
                    
        except KeyboardInterrupt:
            print("\n\n🛑 Sociedad detenida por el usuario")
        
        self.reporte_final()
        
        # Mensaje final inspirador
        print("\n" + "=" * 70)
        print("🎯 LA SOCIEDAD DESCANSAR PERO LA BÚSQUEDA DE LA PERFECCIÓN CONTINÚA")
        print(f"   Calidad alcanzada: {self.calidad.calidad_actual:.1f}%")
        print(f"   Meta: 100% - La calidad infinita nos espera")
        print("=" * 70)

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    sociedad = SociedadFlutterFix()
    sociedad.ejecutar()
