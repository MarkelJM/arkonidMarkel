

import os
from tkinter import BOTTOM
from turtle import left

import pygame as pg
from pygame.sprite import Sprite
from . import ANCHO, ALTO, MOVIMIENTO_JUGADOR, FPS, VIDAS


class Raqueta(Sprite):

    margen_inferior = 40
    velocidad = 10
    fps_animacion = 12
    limite_iteracion = FPS / fps_animacion
    iteracion = 0

    def __init__(self) -> None:
        super().__init__()
        self.sprites = []
        for i in range(3):
            self.sprites.append(
                pg.image.load(
                    os.path.join("resources", "images", f"electric0{i}.png")
                )
            )
        # preparar la primera foto para luego animar y crear el contador en el update
        self.siguiente_imagen = 0
        self.image = self.sprites[self.siguiente_imagen]

        self.rect = self.image.get_rect(
            midbottom=(ANCHO/2, ALTO - self.margen_inferior))

        # velocidad inicial
        self.velocidad_x = 0
        # valores decimales, ya que 'rect' solo se queda enteros

    def update(self) -> None:

        tecla = pg.key.get_pressed()
        if tecla[pg.K_RIGHT]:
            self.rect.x += self.velocidad
            if self.rect.right > ANCHO:
                self.rect.right = ANCHO
        if tecla[pg.K_LEFT]:
            self.rect.x -= self.velocidad
            if self.rect.left < 0:
                self.rect.left = 0

         # animamos el rayo

        self.iteracion += 1
        if self.iteracion == self.limite_iteracion:
            self.siguiente_imagen += 1
            if self.siguiente_imagen >= len(self.sprites):
                self.siguiente_imagen = 0
            self.image = self.sprites[self.siguiente_imagen]
            self.iteracion = 0


class Ladrillo(Sprite):
    def __init__(self, fila, columna, puntos):
        super().__init__()

        ladrillo_verde = os.path.join("resources", "images", "greenTile.png")
        self.image = pg.image.load(ladrillo_verde)
        ancho = self.image.get_width()
        alto = self.image.get_height()
        self.rect = self.image.get_rect(x=columna * ancho, y=fila * alto)
        self.valor_puntos = puntos  # al crear el ladrillo tenga un valor para la puntuacion
        puntos_acumulada = 0


class Pelota(Sprite):
    # para cuando tengamo colision con cilliderect crea,ps un margen, para que si la t la raqueta se "unen"
    # no de problemas de rebotar constantemente dentro
    margen_raqueta_pelota = 5
    velocidad_x = 5
    velocidad_y = 5
    juego_iniciado = False

    def __init__(self, **kwargs):
        super().__init__()

        pelota = os.path.join("resources", "images", "ball1.png")
        self.image = pg.image.load(pelota)
        self.rect = self.image.get_rect(**kwargs)
        # al inicializar la clase, establecemos vidas como el número total
        # de vidas que están especificadas en la configuración
        self.vidas = VIDAS

    def update(self, raqueta):
        if not self.juego_iniciado:
            self.rect = self.image.get_rect(midbottom=raqueta.rect.midtop)
        else:
            self.rect.x += self.velocidad_x
            if self.rect.right > ANCHO or self.rect.left < 0:
                self.velocidad_x = -self.velocidad_x

            self.rect.y += self.velocidad_y
            if self.rect.top <= 0:
                self.velocidad_y = -self.velocidad_y

            if self.rect.top > ALTO:
                self.pierdes()
                self.juego_iniciado = False

    def pierdes(self):
        # Es imposible quitar una vida porque VIDAS no tiene
        # ningún valor. Voy a inicializarlo en el constructor
        # Además, voy a cambiarlo a minúsculas porque no es una
        # constante
        self.vidas = self.vidas - 1
        # agrego f a la cadena para que aplique el formato
        print(f"Pierdes una vida {self.vidas}")
        if self.vidas < 1:
            self.sigo_jugando = False

        """
        VIDAS = VIDAS -1
        print("1 vida menos")
        if VIDAS == 0:
            print("GAME OVER")
            self.salir = True

        print("pierdes una vida")
        """

    def reset(self):
        print("recolocamos la pelota sobre inicial")

    def hay_colision(self, otro_objeto):
        if self.rect.colliderect(otro_objeto):
            # hay colision

            self.rect.y = self.rect.y - self.margen_raqueta_pelota
            self.velocidad_y = -self.velocidad_y
