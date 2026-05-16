import math
import random

import pygame
import numpy as np

from contants import *

# --- Inspirado no Yen
class Moeda():
    def __init__(self, cor):
        self.raio = 15
        self.x = random.randrange(LARGURA - (self.raio)*2)
        self.y = random.randrange(ALTURA - (self.raio)*2)
        self.escala = 1
        self.angulo_graus = 0
        self.cor = cor
        self.pontos = self._criar_pontos()

    def atualizar_e_desenhar(self, surface):
        """Segue a mesma ideia de Circulo.desenhar()"""
        for forma_v, cor, espessura in self.pontos:
            v = self.transformar_vertices(forma_v)
            cor_com_luz = self._calcular_iluminacao_2d(v, cor)
            pygame.draw.polygon(surface, cor_com_luz, v, espessura)

    def transformar_vertices(self, forma) -> list:
        """Segue a mesma ideia do Circulo.transformar_vertices()"""
        rad = math.radians(self.angulo_graus)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        vertices_transformados = []
        for x, y in forma:
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

    def _criar_pontos(self) -> list:
        """
        Cria lista dos pontos externos da cirncuferencia (poligono com 20 lados). Para isso, faz se um for loop, de 0 a 360 com step 18 (360/18=20 pontos),
        cada valor gerado representa um angulo em graus, ele e convertido em radianos.

        O cosseno do angulo e multiplicado pelo raio, gerando o valor de X.
        O seno do angulo e multiplicado pelo raio, gerando o valor de Y.

        Os valores de X e Y são salvos juntos em uma tupla.
        """
        circulo = [(round(math.cos(math.radians(i))*self.raio,2),round(math.sin(math.radians(i))*self.raio,2)) for i in range(0, 360, 18)]
        
        raio_losango = self.raio / 2
        # para fins esteticos, cria-se um losango no centro
        losango = [(raio_losango,0), (0, raio_losango), (-1 * raio_losango,0), (0,-1 * raio_losango)]

        # Formato: (lista dos vértices, cor, espessura da linha: 0=preenchido)
        return [
            (circulo, self.cor, 0),
            (losango, PRETO, 0)
        ]
    
    def _calcular_iluminacao_2d(self, forma, cor=BRANCO) -> tuple:
        # 1. Encontrar o centro do polígono (média dos pontos X e Y)
        # Assumindo vértices como [(x1, y1), (x2, y2), ...]
        centro_x = sum(v[0] for v in forma) / len(forma)
        centro_y = sum(v[1] for v in forma) / len(forma)
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
    
    def _set_cor(self, cor):
        self.cor = cor
        self.pontos = self._criar_pontos()