import os
import pygame as pg
from .entidades import Ladrillo, Pelota, Raqueta
from . import ANCHO, ALTO, COLOR_MENSAJE_ESPACIO, COLOR_PORTADA, FPS, VIDAS

class Escena:
    def __init__(self,pantalla: pg.Surface):
        self.pantalla = pantalla
        self.relog = pg.time.Clock()

    def bucle_principal(self):
        
        pass
    

class Portada(Escena):
    def __init__(self,pantalla: pg.Surface):
        super().__init__(pantalla)
        self.logo = pg.image.load(os.path.join("resources","images", "arkanoid_name.png")) #os.path.join() adapta las barras a linux, mac o windows
        #self.letra_inicio = pg.font.SysFont('roboto', 40)  
        font_file = os.path.join("resources", "fonts","CabinSketch-Bold.ttf")
        self.tipografia = pg.font.Font(font_file, 30)     
    

    def bucle_principal(self):
        salir = False        
        while not salir:
            

            for event in pg.event.get():
                if event.type == pg.QUIT :
                    pg.quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                                    
                        salir = True
            self.pantalla.fill(COLOR_PORTADA)
            self.pintar_texto()
            self.pintar_logo()
            pg.display.flip()

    def pintar_logo(self):
        ancho_logo = self.logo.get_width()
        
        pos_x = (ANCHO -ancho_logo )/2
        pos_y = ALTO /3
        self.pantalla.blit(self.logo, (pos_x, pos_y))

    def pintar_texto(self):
        
        
        #self.letra_inicio = pg.font.Font("CabinSketch-Bold.ttf", 40)
        mensaje_inicio = "presiona 'ESPACIO' para iniciar la partida"
        texto = pg.font.Font.render(self.tipografia , mensaje_inicio, False, COLOR_MENSAJE_ESPACIO)
        pos_x =  (ANCHO- texto.get_width()) / 2
        pos_y =  (ALTO) *0.9
        pg.Surface.blit(self.pantalla, texto, (pos_x, pos_y))
        



class Partida(Escena):
    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)
        bg_file = os.path.join("resources", "images", "background.jpg")
        self.fondo = pg.image.load(bg_file)
        self.jugador = Raqueta()
        self.crear_muro()
        self.pelotita = Pelota(midbottom= self.jugador.rect.midtop)
        self.vida_pelota = Pelota()
        self.contador_vidas = 0
        self.imagen_vidas()

    def bucle_principal(self):
        salir = False 
        partida_iniciada = False       
        while not salir:
            self.relog.tick(FPS)
            self.jugador.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True
                if event.type == pg.KEYDOWN and  event.key == pg.K_SPACE:
                    partida_iniciada = True
            self.pantalla.fill((0, 99, 0))
            self.pintar_fondo()

            self.jugador.update()
            self.pelotita.update(self.jugador, partida_iniciada) 
            self.pelotita.hay_colision(self.jugador)
            golpeados = pg.sprite.spritecollide(self.pelotita, self.ladrillos, True)

            #imagen vidas
            

            puntos_totales = 0
                  
            if len(golpeados) > 0:
                self.pelotita.velocidad_y *= -1
                
                for self.ladrillo in golpeados:
                    puntos_totales += self.ladrillo.valor_puntos  + 1 #ya que las filas empiezan desde 0
                    print(puntos_totales)
            
                     
                    #para los ladrillos golpeados, sumar puntuacion        

            self.pantalla.blit(self.jugador.image, self.jugador.rect)

            #pintar la pelota
            self.pantalla.blit(self.pelotita.image, self.pelotita.rect)

            #pintar el muro
            self.ladrillos.draw(self.pantalla)

            pg.display.flip()
    
    def pintar_fondo(self):
        self.pantalla.blit(self.fondo, (0,0))

    def crear_muro(self):
        num_filas = 5
        num_columnas = 4
        self.ladrillos = pg.sprite.Group()
        self.ladrillos.empty() # no es necesario, pero sirve para asegurar que esta vacio
        es_el_primero = True
        margen_x = 40
        margen_y = 40
        
        #posicion_inicial = 0
        

        for fila in range(num_filas):
            for columna in range(num_columnas):
                ladrillo = Ladrillo (fila , columna) #el ultimo 'fila' es la para la puntuacion
                
                margen_x = (ANCHO - ladrillo.image.get_width()* num_columnas)//2 
                ladrillo.rect.x += margen_x 
                ladrillo.rect.y += margen_y             
                self.ladrillos.add(ladrillo)

    def imagen_vidas(self):
        #creamos como vidas imagenes
        #me da error en escenas por: 'list' object is not callable--> modifico sin crear lista
        self.vida_pelota = pg.sprite.Group()

        for pel in range(VIDAS):
                pelota = Pelota () #el ultimo 'fila' es la para la puntuacion
                
                pelota.rect.x +=   pelota.image.get_width()+ 10
                pelota.rect.y = 5             
                self.vida_pelota.add(pelota)
        

        """
        for i in range (VIDAS):
            self.imagen_vidas.append(
                pg.image.load(
                    os.path.join("resources", "images", "ball1.png")
                )
            )
            self.pelotita.rect.x += self.imagen.get_width() 
            self.pelotita.rect.y = ALTO -5
            """
    

class HallOfFame(Escena):
    def bucle_principal(self):
        salir = False        
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True
            self.pantalla.fill((0, 0, 99))
            pg.display.flip()
