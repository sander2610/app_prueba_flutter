class OrganismoExpansionDinamica:
    def __init__(self):
        self.complejidad_actual = 1.0
        self.expansiones_realizadas = []
        self.departamentos_creados = []
        self.departamento_plantilla = {
            "nombre": "",
            "especialidad": "",
            "agentes_base": 0,
            "agentes_actuales": 0
        }
        self.ultima_expansion_ciclo = 0
        
    def evaluar_complejidad(self, metricas: Dict) -> float:
        """Evalúa la complejidad del sistema"""
        complejidad = 1.0
        
        # Factores que aumentan complejidad (ajustados)
        complejidad += min(3.0, metricas.get("errores_por_hora", 0) * 0.05)
        complejidad += min(2.0, metricas.get("lineas_codigo", 0) / 50000)
        complejidad += min(2.0, metricas.get("dependencias", 0) * 0.02)
        complejidad += min(2.0, metricas.get("usuarios_activos", 0) * 0.005)
        complejidad += min(3.0, metricas.get("vulnerabilidades", 0) * 0.15)
        
        self.complejidad_actual = min(10.0, max(1.0, complejidad))
        return self.complejidad_actual
    
    def necesita_expansion(self, ciclo_actual: int) -> bool:
        """Determina si se necesita crear nuevos departamentos"""
        # Evitar crear demasiados departamentos muy rápido
        if ciclo_actual - self.ultima_expansion_ciclo < 5:
            return False
            
        if self.complejidad_actual >= 8.0 and len(self.departamentos_creados) < 3:
            return True
        elif self.complejidad_actual >= 6.0 and len(self.departamentos_creados) < 2:
            return True
        return False
    
    def crear_departamento(self, tipo: str, especialidad: str, agentes_base: int) -> Dict:
        """Crea un nuevo departamento según la necesidad"""
        from datetime import datetime
        nuevo_depto = {
            "id": f"DEPT_{len(self.departamentos_creados) + 1:03d}",
            "nombre": f"Departamento de {tipo}",
            "especialidad": especialidad,
            "agentes_base": agentes_base,
            "agentes_actuales": agentes_base,
            "fecha_creacion": datetime.now().isoformat()
        }
        
        self.departamentos_creados.append(nuevo_depto)
        self.expansiones_realizadas.append(nuevo_depto)
        self.ultima_expansion_ciclo = ciclo_actual
        
        print(f"\n🚀 NUEVO DEPARTAMENTO CREADO: {nuevo_depto['nombre']}")
        print(f"   Especialidad: {especialidad}")
        print(f"   Agentes: {agentes_base}")
        return nuevo_depto
