import pygame
import random
from abc import ABC, abstractmethod

pygame.init()

WIDTH = 600
HEIGHT = 407
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)

# Cargar imágenes
tortuga_imagen = pygame.image.load('p1.png')  
hoja_imagen = pygame.image.load('p2.png')        
camarones_imagen = pygame.image.load('p3.png')
algas_imagen = pygame.image.load('p4.png')        
roca_imagen = pygame.image.load('p5.png')       
medusa_imagen = pygame.image.load('p6.png')    
fondo_imagen = pygame.image.load('fondo3.jpg')   


tortuga_imagen = pygame.transform.scale(tortuga_imagen, (100, 100))
hoja_imagen = pygame.transform.scale(hoja_imagen, (80, 80))
camarones_imagen = pygame.transform.scale(camarones_imagen, (80, 80))
algas_imagen = pygame.transform.scale(algas_imagen, (80, 80))
roca_imagen = pygame.transform.scale(roca_imagen, (80, 80))
medusa_imagen = pygame.transform.scale(medusa_imagen, (80, 80))
fondo_imagen = pygame.transform.scale(fondo_imagen, (WIDTH, HEIGHT))  

class Figura(ABC):
    def __init__(self, velocidad):
        self.tamano = random.randint(30, 50)
        self.x = random.randint(0, WIDTH - self.tamano)
        self.y = random.randint(-90, -self.tamano)
        self.velocidad = velocidad

    @abstractmethod
    def dibujar(self, superficie):
        pass

    def caer(self):
        self.y += self.velocidad

class Hoja(Figura):
    def dibujar(self, superficie):
        superficie.blit(hoja_imagen, (self.x, self.y))

class Camarones(Figura):
    def dibujar(self, superficie):
        superficie.blit(camarones_imagen, (self.x, self.y))

class Algas(Figura):
    def dibujar(self, superficie):
        superficie.blit(algas_imagen, (self.x, self.y))

class Roca(Figura):
    def dibujar(self, superficie):
        superficie.blit(roca_imagen, (self.x, self.y))

class Medusa(Figura):
    def dibujar(self, superficie):
        superficie.blit(medusa_imagen, (self.x, self.y))

class Jugador:
    def __init__(self):
        self.imagen = tortuga_imagen 
        self.rect = self.imagen.get_rect(center=(WIDTH // 2, HEIGHT - 60))

    def mover(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)

class Colision:
    @staticmethod
    def verificar_colisiones(jugador, alimentos, peligros):
        colision_alimentos = []
        for alimento in alimentos:
            if jugador.rect.colliderect(pygame.Rect(alimento.x, alimento.y, alimento.tamano, alimento.tamano)):
                colision_alimentos.append(alimento)  

        
        for alimento in colision_alimentos:
            alimentos.remove(alimento)

        
        for peligro in peligros:
            if jugador.rect.colliderect(pygame.Rect(peligro.x, peligro.y, peligro.tamano, peligro.tamano)):
                return True  

        return False  

def menu():
    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Selecciona Dificultad")
    
    fuente = pygame.font.Font(None, 74)
    texto_facil = fuente.render("1: Fácil", True, VERDE)
    texto_medio = fuente.render("2: Medio", True, VERDE)
    texto_dificil = fuente.render("3: Difícil", True, VERDE)

    while True:
        pantalla.fill(NEGRO) 
        pantalla.blit(texto_facil, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
        pantalla.blit(texto_medio, (WIDTH // 2 - 100, HEIGHT // 2))
        pantalla.blit(texto_dificil, (WIDTH // 2 - 100, HEIGHT // 2 + 60))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return 1  
                if evento.key == pygame.K_2:
                    return 2  
                if evento.key == pygame.K_3:
                    return 3  

def main():
    dificultad = menu()
    if dificultad is None:
        return

    velocidad_caida = {1: 3, 2: 5, 3: 8} 
    velocidad = velocidad_caida[dificultad]

    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Juego de Tortuga y Alimentos")
    reloj = pygame.time.Clock()
    
    jugador = Jugador()
    alimentos = []
    peligros = []
    corriendo = True
    tiempo_generacion = 0
    tiempo_peligros = 0

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jugador.mover(-5)
        if teclas[pygame.K_RIGHT]:
            jugador.mover(5)

        if tiempo_generacion >= 30:  
            alimentos.append(random.choice([Hoja(velocidad), Camarones(velocidad), Algas(velocidad)]))
            tiempo_generacion = 0

        if tiempo_peligros >= 60:  
            peligros.append(random.choice([Roca(velocidad), Medusa(velocidad)]))
            tiempo_peligros = 0

        
        for alimento in alimentos + peligros:
            alimento.caer()

        
        if Colision.verificar_colisiones(jugador, alimentos, peligros):
            corriendo = False 

        
        pantalla.blit(fondo_imagen, (0, 0)) 
        jugador.dibujar(pantalla)
        for alimento in alimentos:
            alimento.dibujar(pantalla)
        for peligro in peligros:
            peligro.dibujar(pantalla)

        pygame.display.flip()
        reloj.tick(30)
        tiempo_generacion += 1
        tiempo_peligros += 1

    pygame.quit()

if __name__ == "__main__":
    main()