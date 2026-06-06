import random
import time

class CosmicGameEngine:
    def __init__(self):
        self.version = "Cosmic Engine v1.0"
        self.fps = 60
        self.escenas = 0
        self.entidades = 0
        
    def crear_escena(self, nombre):
        self.escenas += 1
        print(f"🎮 Creando escena: {nombre}")
        return {"nombre": nombre, "id": self.escenas}
    
    def crear_entidad(self, tipo):
        self.entidades += 1
        print(f"   ✨ Entidad creada: {tipo}")
        return {"tipo": tipo, "id": self.entidades}
    
    def renderizar(self):
        print(f"🎨 Renderizando - FPS: {self.fps}")
        
    def simular_fisica(self):
        print("⚡ Simulando física en tiempo real")

if __name__ == "__main__":
    print("="*50)
    print("🎮 GameDev Society - Cosmic Game Engine")
    print("="*50)
    
    engine = CosmicGameEngine()
    
    print("\n🏗️ Construyendo Mundo...")
    mundo = engine.crear_escena("Mundo Principal")
    engine.crear_entidad("Jugador")
    engine.crear_entidad("Enemigo")
    engine.crear_entidad("NPC")
    
    print("\n🎮 Iniciando Game Loop...")
    for i in range(5):
        print(f"\n--- Frame {i+1} ---")
        engine.renderizar()
        engine.simular_fisica()
        time.sleep(0.5)
    
    print(f"\n✅ Motor listo: {engine.version}")
    print(f"📊 Estadísticas: {engine.escenas} escenas, {engine.entidades} entidades")
