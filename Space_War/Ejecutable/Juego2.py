import pygame
import sys
import random
import time
from pygame.locals import *

pygame.init()

#Constantes
ancho = 1500
alto = 786
score = 0
listaEnemigo1 = []
listaEnemigo2 = []
listaEnemigo3 = []
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

#Clases
class NaveEspacial(pygame.sprite.Sprite):
    #Metodos
    def __init__(self):
        #Atributos
        pygame.sprite.Sprite.__init__(self)
        self.ImagenNave = pygame.image.load('Imagenes/nave.png')
        self.ImagenNave = pygame.transform.scale(self.ImagenNave, (77, 77))
        self.ImagenExplosion = pygame.image.load('Imagenes/explosion.png')
        self.ImagenExplosion = pygame.transform.scale(self.ImagenExplosion, (92, 84))
        self.lista = [self.ImagenNave, self.ImagenExplosion]
        self.Nave = self.lista[0]
        self.rect = self.Nave.get_rect()
        self.rect.centerx = ancho//2
        self.rect.centery = alto-70
        self.listaDisparo = []
        self.vida = True
        self.velocidad = 0
        self.sonidoDisparo = pygame.mixer.Sound('Sonidos/Shoot.wav')

    def movimiento(self):
        if self.vida == True :
            if self.rect.left <= 0 :
                self.rect.right = ancho - 10
            elif self.rect.right >= ancho  :
                self.rect.left = 10 

    def movimientoLateral(self):
        self.rect.centerx += self.velocidad
        self.movimiento()

    def sonidos(self):
        self.sonidoDisparo.play()

    def disparar(self, x, y):
        miProyectil = Proyectil(x, y,'Imagenes/disparo1.png', True)
        self.listaDisparo.append(miProyectil)
        
    def dibujar(self, superficie):
        superficie.blit(self.Nave, self.rect)

    def destruccion(self):
        self.vida = False
        self.velocidad = 0
        self.Nave = self.lista[1]
        self.sonidoExplosion = pygame.mixer.Sound('Sonidos/Explosion.wav')
        self.sonidoExplosion.play()
        
class Proyectil(pygame.sprite.Sprite):
    
    def __init__(self, posx, posy, ruta, personaje):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenProyectil = pygame.image.load(ruta)
        if personaje == True:
            self.ImagenProyectil = pygame.transform.scale(self.ImagenProyectil, (21, 21))
        else:
            self.ImagenProyectil = pygame.transform.scale(self.ImagenProyectil, (20, 34))
        self.rect = self.ImagenProyectil.get_rect()
        self.rect.top = posy
        self.rect.centerx = posx
        self.disparoPersonaje = personaje
        if personaje == True:
            self.velocidadDisparo = 7
        else:
            self.velocidadDisparo = 5
        
    def trayectoria(self):
        if self.disparoPersonaje == True:
            self.rect.top = self.rect.top - self.velocidadDisparo
        else:
            self.rect.top = self.rect.top + self.velocidadDisparo
        
    def dibujar(self, superficie):
        superficie.blit(self.ImagenProyectil, self.rect)

    def colisionEnemigo(self, listdispE, listE, proyectil, score, puntos):
        for enemigo in listE:
            if self.rect.colliderect(enemigo.rect):
                enemigo.destruccionEnemigo()
                listE.remove(enemigo)
                listdispE.remove(proyectil)
                score += puntos
        return score

class Invasor(pygame.sprite.Sprite):
    
    def __init__(self, posx, posy, distancia, imagenUno, ancho, alto):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenInvasor = pygame.image.load(imagenUno)
        self.ImagenInvasor = pygame.transform.scale(self.ImagenInvasor, (ancho, alto))
        self.rect = self.ImagenInvasor.get_rect()
        self.rect.top = posy
        self.rect.centerx = posx
        self.velocidad = 3
        self.listaDisparo = []
        self.rangoDisparo = 2
        self.derecha = True
        self.contador = 0
        self.aceleracion = 1
        self.maxDescenso = self.rect.top + 50
        self.limiteDerecha = posx + distancia
        self.limiteIzquierda = posx - distancia
        self.conquista = False
        
    def dibujar(self, superficie):
        superficie.blit(self.ImagenInvasor, self.rect)

    def __movimientos(self):
        if self.contador < 5:
             self.__movimientoLateral()
        else:
            self.__movimientoDescenso()

    def __movimientoLateral(self):
        if self.derecha == True :
            self.rect.left += self.velocidad
            if self.rect.left >= self.limiteDerecha:
                self.derecha = False
                self.contador += 1
        else:
            self.rect.left -= self.velocidad
            if self.rect.right <= self.limiteIzquierda:
                self.derecha = True
                self.contador += 1

    def __movimientoDescenso(self):
        if self.maxDescenso <= self.rect.top :
            self.contador = 0
            self.maxDescenso = self.rect.top + 50
            self.velocidad = self.velocidad + self.aceleracion
        else:
            self.rect.top += 2

    def __ataque(self):
        if (random.randint(0, 375) <= self.rangoDisparo) :
            self.__disparo()

    def __disparo(self):
        x, y = self.rect.center
        miProyectil = Proyectil(x, y, 'Imagenes/disparo3.png', False)
        self.listaDisparo.append(miProyectil)

    def comportamiento(self):
        if self.conquista == False :
            self.__movimientos()
            self.__ataque()

    def destruccionEnemigo(self):
        self.sonidoDestruccion = pygame.mixer.Sound('Sonidos/Destruccion.wav')
        self.sonidoDestruccion.play()

    def destruccionJugador(self, superficie, jugador, enemigo, apagar):
        enemigo.comportamiento()
        enemigo.dibujar(superficie)
        if len(enemigo.listaDisparo) > 0:
            for proyectil in enemigo.listaDisparo:
                proyectil.dibujar(superficie)
                proyectil.trayectoria()
                if proyectil.rect.colliderect(jugador.rect):
                    jugador.destruccion()
                    detenertodo()
                    apagar = 1
                if proyectil.rect.top > alto + 10 :
                    enemigo.listaDisparo.remove(proyectil)
                else:
                    for disparo in jugador.listaDisparo:
                        if proyectil.rect.colliderect(disparo):
                            jugador.listaDisparo.remove(disparo)
                            enemigo.listaDisparo.remove(proyectil)
        elif enemigo.rect.colliderect(jugador.rect):
            jugador.destruccion()
            detenertodo()
            apagar = 1
        elif enemigo.rect.top > alto:
            jugador.destruccion()
            detenertodo()
            apagar = 1
        return apagar
    
class JefeFinal(Invasor):
    
    def __init__(self, posx, posy, distancia, anch, alt):
        pygame.sprite.Sprite.__init__(self)
        self.a = anch
        self.b = alt
        self.ImagenJefe = pygame.image.load('Imagenes/jefefinal.png')
        self.ImagenJefe = pygame.transform.scale(self.ImagenJefe, (self.a, self.b))
        self.rect = self.ImagenJefe.get_rect()
        self.rect.centery = posy
        self.rect.centerx = posx
        self.velocidad = 10
        self.listaDisparo = []
        self.rangoDisparo = 5
        self.derecha = True
        self.contador = 0
        self.aceleracion = 5
        self.maxDescenso = self.rect.top + 50
        self.limiteDerecha = posx + distancia
        self.limiteIzquierda = posx - distancia
        self.conquista = False

    def posicion(self):
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.rect = self.ImagenJefe.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def __movimientos(self):
        if self.contador < 3:
             self.__movimientoLateral()
        else:
            self.__movimientoDescenso()

    def cambioimagen(self):
        self.a -= 60
        self.b -= 20
        self.ImagenJefe = pygame.transform.scale(self.ImagenJefe, (self.a, self.b))

    def imagen(self, superficie):
        superficie.blit(self.ImagenJefe, self.rect)

    def ataque(self):
        if (random.randint(0, 30) <= self.rangoDisparo):
            self.disparo()

    def disparo(self):
        x, y = self.rect.center
        miProyectil = Proyectil(x, y, 'Imagenes/disparo3.png', False)
        self.listaDisparo.append(miProyectil)
        
#Funciones

def textos(superficie, texto, color, tamaño, posx, posy, centrar):
    mifuente = pygame.font.Font(None, tamaño)
    texto = mifuente.render(texto, 0, color)
    texto_rect = texto.get_rect()
    if centrar == True:
        texto_rect.center = (ancho//2), posy
    else:
        texto_rect.center = posx, posy
        
    superficie.blit(texto, texto_rect)

def detenertodo():
    pygame.mixer.music.stop()
    for enemigo in listaEnemigo1:
        for disparo in enemigo.listaDisparo:
            enemigo.listaDisparo.remove(disparo)
        enemigo.conquista = True
    for enemigo in listaEnemigo2:
        for disparo in enemigo.listaDisparo:
            enemigo.listaDisparo.remove(disparo)
        enemigo.conquista = True
    for enemigo in listaEnemigo3:
        for disparo in enemigo.listaDisparo:
            enemigo.listaDisparo.remove(disparo)
        enemigo.conquista = True

def cargarEnemigos():
    posx = 180
    for x in range(1, 8):
        enemigo = Invasor(posx, 40, 55, 'Imagenes/invasor1.png', 39, 34)
        listaEnemigo1.append(enemigo)
        posx += 190
    posx = 180
    for x in range(1, 8):
        enemigo = Invasor(posx, -35, 55, 'Imagenes/invasor2.png', 39, 34)
        listaEnemigo2.append(enemigo)
        posx += 190
    posx = 180
    for x in range(1, 8):
        enemigo = Invasor(posx, -110, 55, 'Imagenes/invasor3A.png', 39, 34)
        listaEnemigo3.append(enemigo)
        posx += 190

def reiniciarEnemigos():
    while len(listaEnemigo1) != 0 :
        for enemigo in listaEnemigo1:
            listaEnemigo1.remove(enemigo)
    while len(listaEnemigo2) != 0 :
        for enemigo in listaEnemigo2:
            listaEnemigo2.remove(enemigo)
    while len(listaEnemigo3) != 0 :
        for enemigo in listaEnemigo3:
            listaEnemigo3.remove(enemigo)

def pausa ():
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

def menu():
    intro = True
    Logo = pygame.image.load('Imagenes/logo.png')
    Logo = pygame.transform.scale(Logo, (700, 300))
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Space War")
    while intro == True:
        ventana.fill(BLANCO)
        Logo_rect = Logo.get_rect()
        Logo_rect.center = ancho//2, alto//2 - 75
        ventana.blit(Logo, Logo_rect)
        textos(ventana, 'Presione Q si desea jugar o pulse E si desea salir', NEGRO, 50, 0, 500, True)
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
    SpaceInvader()

def SpaceInvader():
    #Ventana
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Space War")
    ImagenFondo = pygame.image.load('Imagenes/fondo.png')
    ImagenFondo = pygame.transform.scale(ImagenFondo, (ancho, alto))
    pygame.mixer.music.load('Sonidos/Fondo.mp3')
    pygame.mixer.music.play(2)
    jugador = NaveEspacial()
    cargarEnemigos()
    enJuego = True
    reiniciar = False
    apagar = 0
    score = 0
    reloj = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 100)
    jefefinal = JefeFinal(ancho//2, 150, 120, 600, 200)
    contador = 0
    while True :
        reloj.tick(60)
        jugador.movimiento()
        jugador.movimientoLateral()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if enJuego == True:
                if event.type == pygame.KEYDOWN :
                    if event.key == K_LEFT :
                        jugador.velocidad = -7
                    if event.key == K_RIGHT :
                        jugador.velocidad = +7
                    if event.key == K_p :
                        textos(ventana, 'PAUSA', BLANCO, 90, 0, alto//2, True)
                        pausa()
                         
                if event.type == pygame.KEYUP :
                    if (event.key == K_LEFT) or (event.key == K_RIGHT) :
                        jugador.velocidad = 0
        
                if pygame.mouse.get_pressed() == (1,0,0) :
                    if event.type == pygame.USEREVENT:
                        if (len(jugador.listaDisparo) >= 0) and (len(jugador.listaDisparo) <= 3) :
                            jugador.sonidos()
                            x = jugador.rect.centerx
                            y = jugador.rect.centery - 45
                            jugador.disparar(x, y)
        
        ventana.blit(ImagenFondo, (0, 0))
        
        #Destruccion de enemigos
        if len(jugador.listaDisparo) > 0:
            for proyectil in jugador.listaDisparo:
                proyectil.dibujar(ventana)
                proyectil.trayectoria()
                if proyectil.rect.top >= -10:
                    score = proyectil.colisionEnemigo(jugador.listaDisparo, listaEnemigo1, proyectil, score, 100)
                    score = proyectil.colisionEnemigo(jugador.listaDisparo, listaEnemigo2, proyectil, score, 200)
                    score = proyectil.colisionEnemigo(jugador.listaDisparo, listaEnemigo3, proyectil, score, 300)
                else:
                    jugador.listaDisparo.remove(proyectil)

        #Destruccion de jugador           
        if len(listaEnemigo1) + len(listaEnemigo2) + len(listaEnemigo3) != 0:
            for enemigo in listaEnemigo1:
                apagar = enemigo.destruccionJugador(ventana, jugador, enemigo, apagar)
            for enemigo in listaEnemigo2:
                apagar = enemigo.destruccionJugador(ventana, jugador, enemigo, apagar)
            for enemigo in listaEnemigo3:
                apagar = enemigo.destruccionJugador(ventana, jugador, enemigo, apagar)     
        else:
            jefefinal.comportamiento()
            jefefinal.imagen(ventana)
            jefefinal.ataque()
            for proyectil in jefefinal.listaDisparo:
                    proyectil.dibujar(ventana)
                    proyectil.trayectoria()
                    if proyectil.rect.colliderect(jugador.rect):
                        jugador.destruccion()
                        detenertodo()
                        apagar = 1
                    if proyectil.rect.top > alto + 10 :
                        jefefinal.listaDisparo.remove(proyectil)
                    else:
                        for disparo in jugador.listaDisparo:
                            if proyectil.rect.colliderect(disparo):
                                jugador.listaDisparo.remove(disparo)
                                jefefinal.listaDisparo.remove(proyectil)
                        
            for proyectil in jugador.listaDisparo:
                if proyectil.rect.colliderect(jefefinal.rect):
                    jefefinal.destruccionEnemigo()
                    jefefinal.cambioimagen()
                    jefefinal.posicion()
                    jugador.listaDisparo.remove(proyectil)
                    contador += 1
                    score += 500
                    if contador == 9:
                        detenertodo()
                        reiniciar = True
                        textos(ventana, 'YOU WIN', BLANCO, 90, 0, alto//2, True)
                        
        textos(ventana, 'SCORE: ' + str(score), BLANCO, 45, 125, 50, False)
                    
        if apagar == 1:
            enJuego = False
            reiniciar = True          
           
        if enJuego == False :
            textos(ventana, 'GAME OVER', BLANCO, 90, 0, alto//2, True)
            textos(ventana, 'Presione Q si desea reiniciar el juego o pulse E si desea salir', BLANCO, 40, 0, alto//2 + 75, True)
            
        jugador.dibujar(ventana)
        pygame.display.update()

        while reiniciar == True :
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_q :
                        reiniciarEnemigos()
                        SpaceInvader()
                    if event.key == K_e :
                        pygame.quit()
                        sys.exit()
       
menu()
