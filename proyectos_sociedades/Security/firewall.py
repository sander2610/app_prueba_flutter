import time
import random

class QuantumFirewall:
    def __init__(self):
        self.amenazas_bloqueadas = 0
        self.nivel_seguridad = 100
        self.alertas = []
        
    def escanear_paquete(self, paquete):
        riesgo = random.randint(0, 100)
        if riesgo > 80:
            self.amenazas_bloqueadas += 1
            self.alertas.append(f"Amenaza bloqueada: {paquete}")
            return False
        return True
    
    def analizar_trafico(self):
        print("🔍 Analizando tráfico de red...")
        paquetes = ["HTTP", "HTTPS", "DNS", "SSH", "FTP", "MALWARE", "SQL"]
        
        for paquete in paquetes:
            if self.escanear_paquete(paquete):
                print(f"   ✅ {paquete}: Permitido")
            else:
                print(f"   🛑 {paquete}: BLOQUEADO")
            time.sleep(0.3)
    
    def reporte_seguridad(self):
        print(f"\n📊 REPORTE DE SEGURIDAD:")
        print(f"   🛡️ Nivel: {self.nivel_seguridad}%")
        print(f"   🚫 Amenazas bloqueadas: {self.amenazas_bloqueadas}")
        print(f"   ⚠️ Alertas generadas: {len(self.alertas)}")

if __name__ == "__main__":
    print("="*50)
    print("🔒 Security Society - Quantum Firewall")
    print("="*50)
    
    firewall = QuantumFirewall()
    
    print("\n🛡️ Iniciando protección cuántica...")
    firewall.analizar_trafico()
    firewall.reporte_seguridad()
    
    print("\n✅ Firewall activo - Sistema protegido")
