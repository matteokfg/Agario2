import pygame
import math
import random
from contants import *


class Moeda():
    def __init__(self):
        self.raio = 15
        self.x = random.randrange(LARGURA - (self.raio)*2)
        self.y = random.randrange(ALTURA - (self.raio)*2)
        self.escala = 1
        self.angulo_graus = 0
        self.pontos = self.criar_pontos_circulo()

    def atualizar_e_desenhar(self, surface):
        """Segue a mesma ideia de Circulo.desenhar()"""
        v = self.transformar_vertices()
        pygame.draw.polygon(surface, BRANCO, v, 0)

    def transformar_vertices(self) -> list:
        """Segue a mesma ideia do Circulo.transformar_vertices()"""
        rad = math.radians(self.angulo_graus)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        vertices_transformados = []
        for x, y in self.pontos:
            # 1. Escala
            nx = x * self.escala
            ny = y * self.escala
            
            # 2. Rotação
            rx = nx * cos_a - ny * sin_a
            ry = nx * sin_a + ny * cos_a
            
            # 3. Translação
            final_x = rx + self.x
            final_y = ry + self.y

            final_x = max(final_x, 0) if final_x < LARGURA else LARGURA
            final_y = max(final_y, 0) if final_y < ALTURA else ALTURA
            
            vertices_transformados.append((final_x, final_y))
        return vertices_transformados

    def criar_pontos_circulo(self) -> list:
        """Segue a mesma ideia de Circulo._criar_pontos()"""
        circulo = [(round(math.cos(math.radians(i))*self.raio,2),round(math.sin(math.radians(i))*self.raio,2)) for i in range(0, 360, 18)]
        # Formato: list[vértice]
        return circulo