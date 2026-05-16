import math
import random

import pygame
import numpy as np

from contants import *


class Moeda():
    def __init__(self, cor):
        self.raio = 15
        self.x = random.randrange(LARGURA - (self.raio)*2)
        self.y = random.randrange(ALTURA - (self.raio)*2)
        self.escala = 1
        self.angulo_graus = 0
        self.pontos = self._criar_pontos_circulo()
        self.cor = cor

    def atualizar_e_desenhar(self, surface):
        """Segue a mesma ideia de Circulo.desenhar()"""
        v = self.transformar_vertices()
        cor_com_luz = self._calcular_iluminacao_2d(self.cor)
        pygame.draw.polygon(surface, cor_com_luz, v, 0)

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

    def _criar_pontos_circulo(self) -> list:
        """Segue a mesma ideia de Circulo._criar_pontos()"""
        circulo = [(round(math.cos(math.radians(i))*self.raio,2),round(math.sin(math.radians(i))*self.raio,2)) for i in range(0, 360, 18)]
        # Formato: list[vértice]
        return circulo
    
    def _calcular_iluminacao_2d(self, cor=BRANCO) -> tuple:
        # 1. Encontrar o centro do polígono (média dos pontos X e Y)
        # Assumindo vértices como [(x1, y1), (x2, y2), ...]
        centro_x = sum(v[0] for v in self.pontos) / len(self.pontos)
        centro_y = sum(v[1] for v in self.pontos) / len(self.pontos)
        centro_poligono = np.array([centro_x, centro_y, 0])

        # 2. Vetor da luz (da face para a fonte de luz)
        vetor_luz = np.array(POSICAO_LUZ_FIXA) - centro_poligono
        
        # 3. Normalização do vetor de luz
        distancia = np.linalg.norm(vetor_luz)
        if distancia == 0:
            return cor
        vetor_luz_norm = vetor_luz / distancia

        # 4. Produto Escalar (Lambert)
        # Quanto mais "embaixo" da luz o polígono estiver, mais forte o brilho
        dot_product = np.dot(np.array(NORMAL_2D), vetor_luz_norm)
        
        intensidade = max(0, dot_product)
        
        # 5. A luz perde força com a distância
        intensidade = intensidade * (500 / (500 + distancia)) 

        fator_final = min(1.0, intensidade + LUZ_AMBIENTE)
        
        # 6. Retorna cor
        cor_final = (np.array(cor) * fator_final).astype(int)
        return tuple(np.clip(cor_final, 0, 255))