import pygame
import sys
import random
from pygame.locals import *

pygame.init()

#Constantes
ANCHO = 1500
ALTO = 786
listaEnemigos = []
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

#Clases
class NaveEspacial(pygame.sprite.Sprite):
    #Metodos
    def __init__(self):
        #Atributos
        pygame.sprite.Sprite.__init__(self)     #Se debe inicializar el pygame
        self.ImagenNave = pygame.image.load('Imagenes/nave.png')    #Cargamos la imagen de la nave
        self.ImagenNave = pygame.transform.scale(self.ImagenNave, (77, 77))     #Reescalamos la imagen de la nave
        self.Nave = self.ImagenNave     #Al iniciar la clase Nave, esta comienza con la imagen de la nave por default
        self.rect = self.Nave.get_rect()    #Almacena la ubicacion de la nave
        self.rect.centerx = ANCHO//2    #Ubica el centro horizontal de la nave al medio de la pantalla
        self.rect.centery = ALTO-70     #Ubica el centro vertical de la nave mas arriba del borde inferior de la pantalla
        self.vida = True        #Mientras la nave siga con vida podra ejecutar todos sus metodos
        self.velocidad = 0      #La nave no se mueve al inicio
        self.score = 0      #Puntuacion obtenida por el jugador
    #Este metodo realiza el movimiento de la nave
    def movimiento(self):
        if self.vida == True :              #Mientras siga con vida la nave se podra mover
            self.rect.centerx += self.velocidad     #La nave se movera lateralmente dependiendo de su velocidad
            #Hace que la nave pase de un extremo a otro de la pantalla si es que sale de esta
            if self.rect.left <= 0 :        #Si se pasa de la derecha de la pantalla
                self.rect.right = ANCHO - 10    #Reubica la nave a la izquierda de la pantalla usando su borde derecho
            elif self.rect.right >= ANCHO  :    #Si se pasa de la izquierda de la pantalla
                self.rect.left = 10             #Reubica la nave a la izquierda de la pantalla usando su borde izquierdo
    #Este metodo dibua la nave en su posicion actual   
    def dibujar(self, superficie):
        superficie.blit(self.Nave, self.rect)   #Superpone la imagen en el fondo
    #Este metodo se encarga de que la nave deje de moverse cuando se destruya
    def destruccion(self):
        self.vida = False

class Meteoro(pygame.sprite.Sprite):
    #Metodos
    def __init__(self, posx, posy, ruta_imagen, ancho, alto, velocidad):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenMeteor = pygame.image.load(ruta_imagen)
        self.ImagenMeteor = pygame.transform.scale(self.ImagenMeteor, (ancho, alto))
        self.rect = self.ImagenMeteor.get_rect()
        self.rect.top = posy
        self.rect.centerx = posx
        self.velocidad = velocidad
        self.derecha = True
        self.maxDescenso = self.rect.top + 50

    def dibujar(self, superficie):
        superficie.blit(self.ImagenMeteor, self.rect)

    def movimiento(self, enemigo, list_naves):
        if self.rect.top <= ALTO:
            self.rect.top += self.velocidad
        else:
            listaEnemigos.remove(enemigo)
            for i, nave in enumerate(list_naves):
                nave.score += 100
     
#Funciones
def textos(superficie, texto, color, tamaño, posx, posy, centrar):
    mifuente = pygame.font.Font(None, tamaño)
    texto = mifuente.render(texto, 0, color)
    texto_rect = texto.get_rect()
    if centrar == True:
        texto_rect.center = (ANCHO//2), posy
    else:
        texto_rect.center = posx, posy
    superficie.blit(texto, texto_rect)

def crearEnemigos(enemig_rate):
    if random.random() <= enemig_rate:
        posx = random.randint(50, ANCHO-50)
        posy = -110
        velocidad = random.randint(3, 5)
        enemigo = Meteoro(posx, posy, 'Imagenes/meteoro1.png', 220, 170, velocidad)
        listaEnemigos.append(enemigo)

def reiniciarEnemigos():
    listaEnemigos.clear()

def pausa():
    pausar = True
    while pausar :
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN :
                if event.key == K_p :
                    pausar = False
        pygame.display.update()

def Run_MeteorDodge():
    #Ventana
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Meteor Dodge")
    ImagenFondo = pygame.image.load('Imagenes/fondo.png')
    ImagenFondo = pygame.transform.scale(ImagenFondo, (ANCHO, ALTO))
    pygame.mixer.music.load('Sonidos/Fondo.mp3')
    pygame.mixer.music.play(2)
    naves_espaciales = [NaveEspacial()]
    enemig_rate = 0.015
    game_over = False
    reiniciar = False
    reloj = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 100)
    
    while True :

        if game_over == False:
            ventana.blit(ImagenFondo, (0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN :
                    if event.key == K_LEFT :
                        for i, nave in enumerate(naves_espaciales):
                            nave.velocidad = -7
                    elif event.key == K_RIGHT :
                        for i, nave in enumerate(naves_espaciales):
                            nave.velocidad = +7
                    elif event.key == K_p :
                        textos(ventana, 'PAUSA', BLANCO, 90, 0, ALTO//2, True)
                        pausa()     
                elif event.type == pygame.KEYUP :
                    if (event.key == K_LEFT) or (event.key == K_RIGHT) :
                        for i, nave in enumerate(naves_espaciales):
                            nave.velocidad = 0
            for i, nave in enumerate(naves_espaciales):
                nave.movimiento()
                nave.dibujar(ventana)
            #Cada vuelta del lazo existe la posibilidad que se cree un enemigo
            crearEnemigos(enemig_rate)
            #Verificar si el jugador fue destruido por alguno de los enemigos
            for enemigo in listaEnemigos:
                enemigo.movimiento(enemigo, naves_espaciales)
                enemigo.dibujar(ventana)
                for i, nave in enumerate(naves_espaciales):
                    if enemigo.rect.colliderect(nave.rect):
                        pygame.mixer.music.stop()
                        nave.destruccion()
                        game_over = True
            
            textos(ventana, 'SCORE: ' + str(naves_espaciales[0].score), BLANCO, 45, 125, 50, False)     
            reloj.tick(60)
            pygame.display.update()         

        else:
            textos(ventana, 'GAME OVER', BLANCO, 90, 0, ALTO//2, True)
            textos(ventana, 'Presione Q si desea reiniciar el juego o pulse E si desea salir', BLANCO, 40, 0, ALTO//2 + 75, True)
            pygame.display.update()
            reiniciar = True
            while reiniciar == True :
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_q :
                            reiniciarEnemigos()
                            Run_MeteorDodge()
                        if event.key == K_e :
                            pygame.quit()
                            sys.exit()
        
if __name__ == '__main__':
    #Ejecucion del menu
    intro = True
    Logo = pygame.image.load('Imagenes/logo.png')
    Logo = pygame.transform.scale(Logo, (1700, 800))
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Space War")
    while intro == True:
        ventana.fill(NEGRO)
        Logo_rect = Logo.get_rect()
        Logo_rect.center = ANCHO//2, ALTO//2 - 75
        ventana.blit(Logo, Logo_rect)
        textos(ventana, 'Presione Q si desea jugar o pulse E si desea salir', BLANCO, 50, 0, 550, True)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_q :
                    intro = False
                if event.key == K_e :
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

    Run_MeteorDodge()
