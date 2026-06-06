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
# CONFIGURACIÓN DE CALIDAD SUPERIOR
# ============================================

OBJETIVO_CALIDAD = 95.0  # Nuevo objetivo mínimo
REDUCCION_DEUDA_POR_CICLO = 5  # % de reducción por ciclo
EXPANSION_ACTIVA = True  # Permitir más departamentos

# ============================================
# DEPARTAMENTO DE SALUD DEL CÓDIGO (MEJORADO)
# ============================================

class DepartamentoSaludCodigo:
    def __init__(self):
        self.deuda_tecnica = 100.0
        self.deuda_historica = [100.0]
        self.metricas_salud = {
            "complejidad_ciclomatica": 25.0,
            "duplicacion_codigo": 15.0,
            "cobertura_tests": 65.0,
            "documentacion_faltante": 30.0,
            "codigo_muerto": 10.0,
            "dependencias_obsoletas": 5.0
        }
        
    def analizar_salud(self) -> dict:
        """Analiza la salud actual del código"""
        
        # Calcular deuda técnica basada en métricas reales
        deuda = 0.0
        deuda += self.metricas_salud["complejidad_ciclomatica"] * 1.5
        deuda += self.metricas_salud["duplicacion_codigo"] * 2.0
        deuda += (100 - self.metricas_salud["cobertura_tests"]) * 0.8
        deuda += self.metricas_salud["documentacion_faltante"] * 0.5
        deuda += self.metricas_salud["codigo_muerto"] * 1.2
        deuda += self.metricas_salud["dependencias_obsoletas"] * 2.0
        
        self.deuda_tecnica = min(100.0, deuda)
        self.deuda_historica.append(self.deuda_tecnica)
        
        print(f"\n🏥 DIAGNÓSTICO DE SALUD:")
        print(f"   Deuda técnica: {self.deuda_tecnica:.1f}/100")
        print(f"   Complejidad: {self.metricas_salud['complejidad_ciclomatica']:.1f}")
        print(f"   Duplicación: {self.metricas_salud['duplicacion_codigo']:.1f}%")
        print(f"   Cobertura tests: {self.metricas_salud['cobertura_tests']:.1f}%")
        print(f"   Documentación: {100 - self.metricas_salud['documentacion_faltante']:.1f}%")
        print(f"   Código muerto: {self.metricas_salud['codigo_muerto']:.1f}%")
        
        return {"deuda": self.deuda_tecnica, "salud": 100 - self.deuda_tecnica}
    
    def reducir_deuda(self, esfuerzo: float):
        """Reduce la deuda técnica según el esfuerzo aplicado"""
        reduccion = esfuerzo * REDUCCION_DEUDA_POR_CICLO
        
        # Reducir métricas específicas
        self.metricas_salud["complejidad_ciclomatica"] = max(5, self.metricas_salud["complejidad_ciclomatica"] - reduccion * 0.2)
        self.metricas_salud["duplicacion_codigo"] = max(2, self.metricas_salud["duplicacion_codigo"] - reduccion * 0.15)
        self.metricas_salud["cobertura_tests"] = min(100, self.metricas_salud["cobertura_tests"] + reduccion * 0.3)
        self.metricas_salud["documentacion_faltante"] = max(5, self.metricas_salud["documentacion_faltante"] - reduccion * 0.1)
        self.metricas_salud["codigo_muerto"] = max(0, self.metricas_salud["codigo_muerto"] - reduccion * 0.25)
        self.metricas_salud["dependencias_obsoletas"] = max(0, self.metricas_salud["dependencias_obsoletas"] - reduccion * 0.3)
        
        nueva_deuda = self.analizar_salud()
        mejora = self.deuda_historica[-2] - nueva_deuda["deuda"] if len(self.deuda_historica) > 1 else 0
        
        print(f"\n🔧 TRABAJO DE REFACTORIZACIÓN:")
        print(f"   Esfuerzo aplicado: {esfuerzo:.1f}%")
        print(f"   Reducción de deuda: {mejora:.1f} puntos")
        
        return mejora
    
    def recomendar_tratamiento(self) -> List[str]:
        """Recomienda acciones específicas para reducir deuda"""
        tratamientos = []
        
        if self.metricas_salud["complejidad_ciclomatica"] > 20:
            tratamientos.append("🔧 Reducir complejidad ciclomática (extraer métodos)")
        if self.metricas_salud["duplicacion_codigo"] > 10:
            tratamientos.append("📦 Eliminar código duplicado (DRY)")
        if self.metricas_salud["cobertura_tests"] < 80:
            tratamientos.append("🧪 Aumentar cobertura de tests unitarios")
        if self.metricas_salud["documentacion_faltante"] > 15:
            tratamientos.append("📝 Mejorar documentación de APIs")
        if self.metricas_salud["codigo_muerto"] > 5:
            tratamientos.append("🗑️ Eliminar código muerto y comentado")
        if self.metricas_salud["dependencias_obsoletas"] > 2:
            tratamientos.append("📦 Actualizar dependencias obsoletas")
        
        return tratamientos if tratamientos else ["✅ Código saludable - Mantenimiento preventivo"]

# ============================================
# DEPARTAMENTO DE CALIDAD SUPERIOR
# ============================================

class DepartamentoCalidadSuperior:
    def __init__(self, salud: DepartamentoSaludCodigo):
        self.salud = salud
        self.calidad_actual = 60.0
        self.calidad_exigida = OBJETIVO_CALIDAD
        self.historial_calidad = [60.0]
        self.meta_alcanzada = False
        
    def evaluar_calidad(self) -> float:
        """Evalúa la calidad actual basada en salud del código"""
        calidad = 100.0 - self.salud.deuda_tecnica
        
        # Bonus por cobertura de tests
        calidad += self.salud.metricas_salud["cobertura_tests"] * 0.1
        
        # Penalización por código muerto
        calidad -= self.salud.metricas_salud["codigo_muerto"] * 0.5
        
        self.calidad_actual = min(100.0, max(0, calidad))
        self.historial_calidad.append(self.calidad_actual)
        
        print(f"\n🎯 CALIDAD DEL SISTEMA:")
        print(f"   Actual: {self.calidad_actual:.1f}%")
        print(f"   Exigida: {self.calidad_exigida:.1f}%")
        print(f"   Brecha: {self.calidad_exigida - self.calidad_actual:.1f} puntos")
        
        if self.calidad_actual >= self.calidad_exigida and not self.meta_alcanzada:
            self.meta_alcanzada = True
            print(f"\n🎉 ¡META DE CALIDAD ALCANZADA! ({self.calidad_exigida}%)")
        
        return self.calidad_actual
    
    def calcular_esfuerzo_necesario(self) -> float:
        """Calcula el esfuerzo necesario para alcanzar la meta"""
        brecha = self.calidad_exigida - self.calidad_actual
        if brecha <= 0:
            return 0
        # Cada punto de calidad requiere ~0.5 de esfuerzo
        return brecha * 0.5

# ============================================
# DEPARTAMENTO DE EXPANSIÓN ACELERADA
# ============================================

class DepartamentoExpansionAcelerada:
    def __init__(self):
        self.departamentos_creados = []
        self.proximos_departamentos = [
            {"tipo": "Optimización", "especialidad": "Rendimiento", "agentes": 5, "costo": 150},
            {"tipo": "IA", "especialidad": "Machine Learning", "agentes": 8, "costo": 250},
            {"tipo": "DevOps", "especialidad": "CI/CD", "agentes": 6, "costo": 180},
            {"tipo": "UX", "especialidad": "Experiencia Usuario", "agentes": 4, "costo": 120},
            {"tipo": "Seguridad", "especialidad": "Auditoría", "agentes": 7, "costo": 200}
        ]
        
    def evaluar_necesidad_expansion(self, calidad_actual: float, deuda_tecnica: float) -> bool:
        """Evalúa si se necesita un nuevo departamento"""
        if len(self.departamentos_creados) >= 5:
            return False
        
        if calidad_actual < 70 and deuda_tecnica > 80:
            return True
        elif calidad_actual < 85 and deuda_tecnica > 60:
            return len(self.departamentos_creados) < 3
        elif calidad_actual < 95 and deuda_tecnica > 40:
            return len(self.departamentos_creados) < 5
        
        return False
    
    def crear_departamento(self, presupuesto: int, ciclo: int) -> dict:
        """Crea un nuevo departamento especializado"""
        if not self.proximos_departamentos:
            return None
        
        nuevo = self.proximos_departamentos.pop(0)
        nuevo["id"] = len(self.departamentos_creados) + 1
        nuevo["ciclo_creacion"] = ciclo
        
        self.departamentos_creados.append(nuevo)
        
        print(f"\n🚀 NUEVO DEPARTAMENTO CREADO:")
        print(f"   Nombre: {nuevo['tipo']} Department")
        print(f"   Especialidad: {nuevo['especialidad']}")
        print(f"   Agentes asignados: {nuevo['agentes']}")
        print(f"   Costo: {nuevo['costo']} unidades")
        
        return nuevo

# ============================================
# SISTEMA DE RECOMPENSAS (MEJORADO)
# ============================================

class SistemaRecompensas:
    def __init__(self):
        self.puntos = 0
        self.logros = []
        self.metas_cumplidas = []
        
    def celebrar_mejora(self, mejora_calidad: float, reduccion_deuda: float):
        """Celebra mejoras significativas"""
        puntos_ganados = 0
        
        if mejora_calidad >= 2:
            puntos = int(mejora_calidad * 15)
            puntos_ganados += puntos
            print(f"\n🎉 ¡MEJORA DE CALIDAD! +{mejora_calidad:.1f}% → +{puntos} puntos")
        
        if reduccion_deuda >= 5:
            puntos = int(reduccion_deuda * 10)
            puntos_ganados += puntos
            print(f"🔧 ¡REDUCCIÓN DE DEUDA! -{reduccion_deuda:.1f}% → +{puntos} puntos")
        
        self.puntos += puntos_ganados
        return puntos_ganados
    
    def celebrar_meta(self, meta: str):
        """Celebra el cumplimiento de una meta"""
        puntos = 100
        self.puntos += puntos
        self.metas_cumplidas.append(meta)
        print(f"\n🏆 ¡META CUMPLIDA! {meta} → +{puntos} puntos")
    
    def ver_logros(self) -> List[str]:
        """Retorna los logros alcanzados"""
        if self.puntos >= 500:
            self.logros.append("💎 MAESTROS DE RECOMPENSAS")
        if self.puntos >= 1000:
            self.logros.append("🏆 LEYENDAS DE CALIDAD")
        if len(self.metas_cumplidas) >= 3:
            self.logros.append("🎯 CAZADORES DE METAS")
        
        return self.logros

# ============================================
# DEPARTAMENTO DE POLICÍA (OPTIMIZADO)
# ============================================

class DepartamentoPoliciaOptimizado:
    def __init__(self):
        self.patrullas = 0
        self.infracciones = 0
        self.patrullas_activas = 8
        
    def patrullar(self) -> int:
        """Realiza patrullaje y retorna infracciones encontradas"""
        self.patrullas += 1
        
        # Simular detección de infracciones
        if self.patrullas % 3 == 0:
            infracciones = random.randint(1, 3)
            self.infracciones += infracciones
            print(f"\n👮 PATRULLA #{self.patrullas}: 🚨 {infracciones} infracciones encontradas")
            return infracciones
        else:
            print(f"\n👮 PATRULLA #{self.patrullas}: ✅ Sin infracciones")
            return 0

# ============================================
# SOCIEDAD PRINCIPAL
# ============================================

class SociedadFlutterFix:
    def __init__(self):
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🏛️ FLUTTERFIX v19 - ENFOQUE EN CALIDAD 95%+               ║
║                                                              ║
║   🎯 Objetivo: Reducir deuda técnica al mínimo              ║
║   💰 Presupuesto inicial: 2000 unidades                     ║
║   🚀 Expansión acelerada según necesidad                    ║
║   🏥 Monitoreo intensivo de salud del código                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        self.salud = DepartamentoSaludCodigo()
        self.calidad = DepartamentoCalidadSuperior(self.salud)
        self.expansion = DepartamentoExpansionAcelerada()
        self.recompensas = SistemaRecompensas()
        self.policia = DepartamentoPoliciaOptimizado()
        
        self.presupuesto = 2000
        self.gastos = 0
        self.ciclo = 0
        self.historial = []
        
    def ciclo_refactorizacion(self):
        """Ciclo dedicado a reducir deuda técnica"""
        print("\n" + "=" * 70)
        self.ciclo += 1
        print(f"🔄 CICLO DE REFACTORIZACIÓN #{self.ciclo}")
        print("=" * 70)
        
        # 1. Análisis de salud actual
        salud_actual = self.salud.analizar_salud()
        
        # 2. Evaluar calidad
        calidad_actual = self.calidad.evaluar_calidad()
        
        # 3. Calcular esfuerzo necesario
        esfuerzo_necesario = self.calidad.calcular_esfuerzo_necesario()
        
        # 4. Aplicar refactorización
        if esfuerzo_necesario > 0:
            esfuerzo = min(100, esfuerzo_necesario * 1.2)  # Esfuerzo adicional
            mejora_deuda = self.salud.reducir_deuda(esfuerzo)
            
            # 5. Verificar mejora de calidad
            nueva_calidad = self.calidad.evaluar_calidad()
            mejora_calidad = nueva_calidad - calidad_actual
            
            # 6. Recompensas
            puntos = self.recompensas.celebrar_mejora(mejora_calidad, mejora_deuda)
            
            # 7. Reportar avance
            print(f"\n📈 AVANCE DEL CICLO:")
            print(f"   Esfuerzo invertido: {esfuerzo:.1f}%")
            print(f"   Mejora de calidad: +{mejora_calidad:.1f}%")
            print(f"   Reducción de deuda: -{mejora_deuda:.1f} puntos")
            print(f"   Puntos ganados: {puntos}")
        
        # 8. Recomendaciones de tratamiento
        tratamiento = self.salud.recomendar_tratamiento()
        if tratamiento:
            print(f"\n📋 TRATAMIENTO RECOMENDADO:")
            for item in tratamiento:
                print(f"   • {item}")
        
        # 9. Patrullaje de policía
        infracciones = self.policia.patrullar()
        
        # 10. Evaluar necesidad de expansión
        if self.expansion.evaluar_necesidad_expansion(calidad_actual, salud_actual["deuda"]):
            nuevo_depto = self.expansion.crear_departamento(self.presupuesto, self.ciclo)
            if nuevo_depto:
                self.presupuesto -= nuevo_depto["costo"]
                self.gastos += nuevo_depto["costo"]
                print(f"   💰 Presupuesto restante: {self.presupuesto}")
                
                # Celebración especial por expansión
                self.recompensas.celebrar_meta(f"Nuevo departamento: {nuevo_depto['tipo']}")
        
        # 11. Verificar metas de calidad
        if calidad_actual >= OBJETIVO_CALIDAD and not self.calidad.meta_alcanzada:
            self.recompensas.celebrar_meta(f"Alcanzar {OBJETIVO_CALIDAD}% de calidad")
        
        # 12. Estado financiero
        print(f"\n💰 ESTADO FINANCIERO:")
        print(f"   Presupuesto disponible: {self.presupuesto}/{2000 - self.gastos}")
        print(f"   Puntos de recompensa: {self.recompensas.puntos}")
        
        # Guardar historial
        self.historial.append({
            "ciclo": self.ciclo,
            "calidad": calidad_actual,
            "deuda": salud_actual["deuda"],
            "puntos": self.recompensas.puntos
        })
        
        return mejora_calidad if esfuerzo_necesario > 0 else 0
    
    def reporte_final(self):
        """Reporte completo de la evolución"""
        print("\n" + "=" * 70)
        print("📊 REPORTE FINAL - EVOLUCIÓN DE LA SOCIEDAD")
        print("=" * 70)
        
        # Estadísticas generales
        calidad_inicial = self.historial[0]["calidad"] if self.historial else 0
        calidad_final = self.historial[-1]["calidad"] if self.historial else 0
        deuda_inicial = self.historial[0]["deuda"] if self.historial else 0
        deuda_final = self.historial[-1]["deuda"] if self.historial else 0
        
        print(f"\n📈 EVOLUCIÓN DE CALIDAD:")
        print(f"   Inicial: {calidad_inicial:.1f}%")
        print(f"   Final: {calidad_final:.1f}%")
        print(f"   Mejora total: +{calidad_final - calidad_inicial:.1f}%")
        
        print(f"\n🔧 EVOLUCIÓN DE DEUDA TÉCNICA:")
        print(f"   Inicial: {deuda_inicial:.1f}/100")
        print(f"   Final: {deuda_final:.1f}/100")
        print(f"   Reducción total: -{deuda_inicial - deuda_final:.1f} puntos")
        
        print(f"\n🏆 LOGROS ALCANZADOS:")
        logros = self.recompensas.ver_logros()
        for logro in logros:
            print(f"   {logro}")
        
        if not logros:
            print("   ⏳ En progreso...")
        
        print(f"\n📊 ESTADÍSTICAS FINALES:")
        print(f"   Ciclos ejecutados: {self.ciclo}")
        print(f"   Departamentos creados: {len(self.expansion.departamentos_creados)}")
        print(f"   Patrullajes realizados: {self.policia.patrullas}")
        print(f"   Infracciones detectadas: {self.policia.infracciones}")
        print(f"   Puntos totales: {self.recompensas.puntos}")
        print(f"   Presupuesto restante: {self.presupuesto}")
        
        print("\n" + "=" * 70)
        
        # Mensaje final
        if calidad_final >= 95:
            print("\n🎉 ¡OBJETIVO ALCANZADO! La sociedad ha logrado calidad superior al 95%")
        elif calidad_final >= 90:
            print("\n🌟 ¡EXCELENTE TRABAJO! Muy cerca del objetivo del 95%")
        else:
            print("\n💪 CONTINUAMOS TRABAJANDO! La búsqueda de la calidad perfecta continúa")
        
        print("=" * 70)
    
    def ejecutar(self, ciclos: int = 30):
        """Ejecuta la sociedad por N ciclos"""
        print(f"\n🚀 INICIANDO SOCIEDAD - OBJETIVO: {OBJETIVO_CALIDAD}% DE CALIDAD")
        print(f"🎯 Meta: Reducir deuda técnica y mejorar calidad sosteniblemente\n")
        
        try:
            for ciclo in range(ciclos):
                mejora = self.ciclo_refactorizacion()
                time.sleep(1)  # Pausa para visualización
                
                # Reporte cada 10 ciclos
                if (ciclo + 1) % 10 == 0:
                    print("\n" + "📊" * 35)
                    print(f"📊 REPORTE PARCIAL - CICLO {ciclo + 1}")
                    print(f"   Calidad: {self.calidad.calidad_actual:.1f}%")
                    print(f"   Deuda: {self.salud.deuda_tecnica:.1f}")
                    print(f"   Puntos: {self.recompensas.puntos}")
                    print("📊" * 35)
                    
        except KeyboardInterrupt:
            print("\n\n🛑 Ejecución interrumpida por el usuario")
        
        self.reporte_final()
        
        print("\n🎯 LA SOCIEDAD CONTINÚA TRABAJANDO PARA ALCANZAR LA CALIDAD INFINITA")

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    sociedad = SociedadFlutterFix()
    sociedad.ejecutar(ciclos=30)  # 30 ciclos enfocados en mejora
