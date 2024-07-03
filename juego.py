import pygame
import sys
import random


ANCHO = 1000
ALTO = 600

FPS = 30

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
HC74225 = (199, 66, 37)
H61CD35 = (97, 205, 53)

puntuacion = 0
nivel = 0
stage = "inicio"

consolas = pygame.font.match_font('consolas')
times = pygame.font.match_font('times')
arial = pygame.font.match_font('arial')
courier = pygame.font.match_font('courier')
gotica = pygame.font.match_font('Showcard Gothic')


#mixer para los sonidos y la musica
pygame.mixer.init()
pygame.mixer.music.load('sonidos/music.ogg')
pygame.mixer.music.play(1)

#variables de efectos de sonidos
laser = pygame.mixer.Sound('sonidos/sfx_laser1.ogg')
explosion = pygame.mixer.Sound('sonidos/explosion.wav')
golpe = pygame.mixer.Sound('sonidos/golpe.wav')
powerup = pygame.mixer.Sound('sonidos/powerUp.wav')

#variables de imagenes de fondo
fondo = pygame.image.load("img/fondo.png")
inicio_img= pygame.image.load("img/inicio.png")
game_over_img= pygame.image.load("img/gameOver.png")

def muestra_texto(pantalla,fuente,texto,color, dimensiones, x, y):
	tipo_letra = pygame.font.Font(fuente,dimensiones)
	superficie = tipo_letra.render(texto,True, color)
	rectangulo = superficie.get_rect()
	rectangulo.center = (x, y)
	pantalla.blit(superficie,rectangulo)

def barra_hp(pantalla,x,y,hps):
    largo = 200
    ancho = 25
    calculo_barra = int((jugador.get_hp()/100)*largo)
    borde = pygame.Rect(x,y,largo,ancho)
    barra = pygame.Rect(x,y,calculo_barra,ancho)
    pygame.draw.rect(pantalla,AZUL,borde,3)
    pygame.draw.rect(pantalla,VERDE,barra)
    #dibujar icono
    pantalla.blit(pygame.image.load('img/jugador_icon.png'),(545,15))


class Enemigo(pygame.sprite.Sprite):
	# Sprite del enemigo
    def __init__(self):
	# Heredamos el init de la clase Sprite de Pygame
        super().__init__()
		# Rectángulo (enemigos)
        self.image = pygame.image.load("img/enemigo.png")
		# Obtiene el rectángulo (sprite)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(ALTO - self.rect.height) * -1
        self.velocidad_x = 5
        self.velocidad_y = 2
        self.radius = 38
        self.hp = 15

    def update(self):
        self.rect.y += self.velocidad_y
        self.rect.x += self.velocidad_x

         # rebota el margen derecho
        if self.rect.right > ANCHO:
            self.velocidad_x -=1
        # rebota el margen izquierdo
        if self.rect.left < 0:
            self.velocidad_x +=1

        if self.rect.top > ALTO + 100:
            self.kill()


    def baja_vida(self):
        self.hp -= 5

    def get_hp(self):
        return self.hp

class EnemigosAzules(Enemigo):
    def __init__(self):
	# Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        self.image = pygame.image.load("img/enemigoAzul.png")
        self.hp = 45

class EnemigosNaranjas(Enemigo):
    def __init__(self):
	# Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        self.image = pygame.image.load("img/enemigoNaranja.png")
        self.hp = 35

class EnemigosVerdes(Enemigo):
    def __init__(self):
	# Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        self.image = pygame.image.load("img/enemigoVerde.png")
        self.hp = 25

class Jugador(pygame.sprite.Sprite):
    # Sprite del jugador
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # Rectángulo (jugador)
        self.image = pygame.image.load("img/jugador.png")
        #self.image.fill(HC74225)
        # Obtiene el rectángulo (sprite)
        self.rect = self.image.get_rect()
        # Centra el rectángulo (sprite)
        self.rect.center = (ANCHO // 2, ALTO-self.rect.width)
        # Velocidad inicial del personaje
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.radius = 40
        #tiempo entre disparos
        self.cadencia = 200
        self.ultimo_disparo = pygame.time.get_ticks()
        self.hp = 100
        self.dos_disparos = False
        self.ultimo_dos_disparos = pygame.time.get_ticks()


		
    def update(self):
		# Actualiza esto cada vuelta de bucle.
        # Mantiene las teclas pulsadas
        self.velocidad_x = 0
        self.velocidad_y = 0
        teclas = pygame.key.get_pressed()
        # Mueve al personaje hacia la izquierda
        if teclas[pygame.K_a]:
            self.velocidad_x = -20
        if teclas[pygame.K_d]:
            self.velocidad_x = 20
        if teclas[pygame.K_w]:
            self.velocidad_y = -10
        if teclas[pygame.K_s]:
            self.velocidad_y = 10

            #disparo de laser(es)
        if teclas[pygame.K_SPACE]:
            ahora = pygame.time.get_ticks()
            #cuando tienes 1 bala
            if ahora - self.ultimo_disparo > self.cadencia and not self.dos_disparos:
                jugador.disparo()
                self.ultimo_disparo = ahora
                #cuando tienes 2 balas
            elif ahora - self.ultimo_disparo > self.cadencia and self.dos_disparos and ahora - self.ultimo_dos_disparos < 4000:
                jugador.disparo2()
                self.ultimo_disparo = ahora
                #desactivar poder
            elif self.dos_disparos and ahora - self.ultimo_dos_disparos > 4000:
                self.dos_disparos = False
                self.ultimo_dos_disparos = pygame.time.get_ticks()
                
            #actualizar posicion
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        # Limita el margen derecho
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
            # Limita el margen izquierdo
        if self.rect.left < 0:
            self.rect.left = 0
        # Limita el margen inferior
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO

        # Limita el margen superior
        if self.rect.top < 0:
            self.rect.top = 0
    def disparo(self):
        bala = Disparos(self.rect.centerx, self.rect.top + 50)
        balas.add(bala)
        laser.play()
    
    def disparo2(self):
        bala = Disparos(self.rect.centerx-20, self.rect.top + 50)
        bala2 = Disparos(self.rect.centerx+20, self.rect.top + 50)
        balas.add(bala)
        balas.add(bala2)
        laser.play()

    def baja_vida(self):
        self.hp -= 15
    
    def get_hp(self):
        return self.hp
    
    def sube_vida(self):
        self.hp += 15
        if self.hp > 100:
            self.hp = 100

    def set_dos_disparos(self,estado):
        self.dos_disparos = estado
        self.ultimo_dos_disparos = pygame.time.get_ticks()

    def reset_hp(self):
        self.hp = 100

class Disparos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("img/disparo.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.radius = 10
    def update(self):
        self.rect.y -= 25
        if self.rect.bottom < 0:
            self.kill()

class Objeto(pygame.sprite.Sprite):
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # Rectángulo (enemigos)
        self.image = pygame.image.load("img/meteorito.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = -600 - random.randrange(-ALTO,0)
        self.velocidad = random.randrange(1, 7)


    def update(self):
        self.rect.y += self.velocidad
        if self.rect.y > ALTO:
            self.kill()

class Meteoritos(Objeto):
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # Rectángulo (enemigos)
        self.image = pygame.image.load("img/meteorito.png")

class Disparo_plus(Objeto):
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # Rectángulo (enemigos)
        self.image = pygame.image.load("img/Star2.png")

class HP_plus(Objeto):
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # Rectángulo (enemigos)
        self.image = pygame.image.load("img/Star1.png")

sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
enemigos_azules = pygame.sprite.Group()
enemigos_verdes = pygame.sprite.Group()
enemigos_naranjas = pygame.sprite.Group()
balas = pygame.sprite.Group()
meteoritos = pygame.sprite.Group()
disparo_pluses = pygame.sprite.Group()
hp_pluses = pygame.sprite.Group()

jugador = Jugador()


# enemigo = Enemigo()
# enemigos.add(enemigo)
sprites.add(jugador)

#configuracion de pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Invasores espaciales Elena')
icono=pygame.image.load('img/jugador_icon.png')
pygame.display.set_icon(icono)
clock = pygame.time.Clock()
# Especificación de la paleta de colores

def reiniciar_grupos(cantidad):
    for x in enemigos:
        x.kill()
    for x in enemigos_azules:
        x.kill()
    for x in enemigos_naranjas:
        x.kill()
    for x in enemigos_verdes:
        x.kill()
    for x in meteoritos:
        x.kill()
    for x in disparo_pluses:
        x.kill()
    for x in hp_pluses:
        x.kill()
    for x in sprites:
        x.kill()

    for x in range(cantidad):
        enemigo = Enemigo()
        enemigos.add(enemigo)
    for x in range(cantidad):
        enemigo = EnemigosAzules()
        enemigos_azules.add(enemigo)
    for x in range(cantidad):
        enemigo = EnemigosNaranjas()
        enemigos_naranjas.add(enemigo)
    for x in range(cantidad):
        enemigo = EnemigosVerdes()
        enemigos_verdes.add(enemigo)
    for x in range(1):
        meteorito = Meteoritos()
        meteoritos.add(meteorito)
    for x in range(cantidad):
        disparo2 = Disparo_plus()
        disparo_pluses.add(disparo2)
    for x in range(cantidad*3):
        hp_plus = HP_plus()
        hp_pluses.add(hp_plus)

    sprites.add(jugador)


Jugando = True
arranque = True
inicio = False




while Jugando:
    match stage:
        case "inicio":
            pantalla.blit(inicio_img,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Jugando = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Botón izquierdo del ratón
                        pos = event.pos  # Obtener la posición del clic
                        print(f"Clic en la posición: {pos}")
                        inicio = False
                        nivel += 1
                        stage = "Juego"
            pygame.display.flip()
        case "Juego":
            if arranque:
                reiniciar_grupos(nivel)  
                arranque = False    
            #velocidad 
            clock.tick(FPS)
            #evento de los juegos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pantalla.blit(fondo,(0,0))
            sprites.update()
            enemigos.update()
            enemigos_naranjas.update()
            enemigos_verdes.update()
            enemigos_azules.update()
            balas.update()
            meteoritos.update()
            disparo_pluses.update()
            hp_pluses.update()

            colision_disparos= pygame.sprite.groupcollide(enemigos, balas, False, True, pygame.sprite.collide_circle)

            colision_disparos_verdes = pygame.sprite.groupcollide(enemigos_verdes, balas, False, True, pygame.sprite.collide_circle)

            colision_disparos_azules = pygame.sprite.groupcollide(enemigos_azules, balas, False, True, pygame.sprite.collide_circle)

            colision_disparos_naranjas = pygame.sprite.groupcollide(enemigos_naranjas, balas, False, True, pygame.sprite.collide_circle)

            colision_nave_enemigos = pygame.sprite.spritecollide(jugador,enemigos,True,pygame.sprite.collide_circle)

            colision_nave_enemigos_verdes = pygame.sprite.spritecollide(jugador,enemigos_verdes,True,pygame.sprite.collide_circle)

            colision_nave_enemigos_azules = pygame.sprite.spritecollide(jugador,enemigos_azules,True,pygame.sprite.collide_circle)

            colision_nave_enemigos_naranjas = pygame.sprite.spritecollide(jugador,enemigos_naranjas,True,pygame.sprite.collide_circle)

            colision_nave_meteoritos = pygame.sprite.spritecollide(jugador,meteoritos,True,pygame.sprite.collide_circle)

            colision_nave_2disparos = pygame.sprite.spritecollide(jugador,disparo_pluses,True,pygame.sprite.collide_circle)

            colision_nave_hp_plus = pygame.sprite.spritecollide(jugador,hp_pluses,True,pygame.sprite.collide_circle)

            if colision_nave_hp_plus:
                powerup.play()
                jugador.sube_vida()

            if colision_nave_2disparos:
                powerup.play()
                jugador.set_dos_disparos(True)  

            if colision_nave_meteoritos:
                golpe.play()
                jugador.baja_vida()
                jugador.baja_vida()
                if jugador.get_hp() <= 0:
                    stage = "game over"

            if colision_nave_enemigos:
                golpe.play()
                jugador.baja_vida()
                if jugador.get_hp() <= 0:
                    stage = "game over"

            if colision_nave_enemigos_verdes:
                golpe.play()
                jugador.baja_vida()
                if jugador.get_hp() <= 0:
                    stage = "game over"

            if colision_nave_enemigos_azules:
                golpe.play()
                jugador.baja_vida()
                if jugador.get_hp() <= 0:
                    stage = "game over"

            if colision_nave_enemigos_naranjas:
                golpe.play()
                jugador.baja_vida()
                if jugador.get_hp() <= 0:
                    stage = "game over"

            if colision_disparos:
                puntuacion += 10
                explosion.play()
                for enemy in colision_disparos:
                    enemy.baja_vida()
                    if(enemy.get_hp() <= 0):
                        enemy.kill()

            if colision_disparos_verdes:
                puntuacion += 25
                explosion.play()
                for enemy in colision_disparos_verdes:
                    enemy.baja_vida()
                    if(enemy.get_hp() <= 0):
                        enemy.kill()


            if colision_disparos_azules:
                puntuacion += 50
                explosion.play()
                for enemy in colision_disparos_azules:
                    enemy.baja_vida()
                    if(enemy.get_hp() <= 0):
                        enemy.kill()


            if colision_disparos_naranjas:
                puntuacion += 100
                explosion.play()
                for enemy in colision_disparos_naranjas:
                    enemy.baja_vida()
                    if(enemy.get_hp() <= 0):
                        enemy.kill() 



            meteoritos.draw(pantalla)
            hp_pluses.draw(pantalla)
            disparo_pluses.draw(pantalla)
            balas.draw(pantalla)  
            sprites.draw(pantalla)
            enemigos.draw(pantalla)
            enemigos_verdes.draw(pantalla)
            enemigos_azules.draw(pantalla)
            enemigos_naranjas.draw(pantalla)
            
            
            muestra_texto(pantalla,consolas,str(puntuacion).zfill(4), ROJO, 40, 700, 70)
            barra_hp(pantalla,580,15,jugador.get_hp())
            muestra_texto(pantalla,consolas,"Nivel: "+ str(nivel), ROJO, 40, 700, 110)
            if len(enemigos) <= 0 and len(enemigos_azules) <= 0 and len(enemigos_naranjas) <= 0 and len(enemigos_verdes) <= 0:
                nivel += 1
                arranque = True 
            pygame.display.flip()
        case "game over":
            pantalla.blit(game_over_img,(0,0))
            muestra_texto(pantalla,gotica,"Nivel: "+ str(nivel), ROJO, 40, 450, 320)
            muestra_texto(pantalla,gotica,"Puntaje: "+ str(puntuacion), ROJO, 40, 450, 360)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Jugando = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Botón izquierdo del ratón
                        pos = event.pos  # Obtener la posición del clic
                        print(f"Clic en la posición: {pos}")
                        nivel = 1
                        arranque = True
                        jugador.reset_hp()
                        puntuacion = 0
                        stage = "Juego"
            pygame.display.flip()


pygame.quit()

