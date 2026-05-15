import math

import pygame
import numpy as np

from contants import *


class Circulo:
    def __init__(self, x, y, raio, angulo_graus, sx, sy, num_jogador, cor=CIANO_NEON):
        self.x = x
        self.y = y
        self.raio = raio
        self.tx = x
        self.ty = y
        self.angulo_graus = angulo_graus
        self.sx = sx
        self.sy = sy
        self.cor = cor
        self.num_jogador = num_jogador
        self.pontos = self._criar_pontos()

    def __str__(self):
        return f"Jogador {self.num_jogador}"

    def _criar_pontos(self) -> list:
        """
        Cria lista dos pontos externos da cirncuferencia (poligono com 20 lados). Para isso, faz se um for loop, de 0 a 360 com step 18 (360/18=20 pontos),
        cada valor gerado representa um angulo em graus, ele e convertido em radianos.

        O cosseno do angulo e multiplicado pelo raio, gerando o valor de X.
        O seno do angulo e multiplicado pelo raio, gerando o valor de Y.

        Os valores de X e Y são salvos juntos em uma tupla.
        """
        circulo = [(round(math.cos(math.radians(i))*self.raio,2),round(math.sin(math.radians(i))*self.raio,2)) for i in range(0, 360, 18)]
        
        # para fins esteticos, cria-se um triangulo com dois pontos pertencentes a circunferencia
        triangulo = [(0,0), circulo[14], circulo[16]]

        # Formato: (lista dos vértices, cor, espessura da linha: 0=preenchido)
        return [
            (circulo, self.cor, 0),
            (triangulo, PRETO, 0)
        ]

    def distancia_entre_centros(self, outro_x, outro_y) -> float:
        """
        Para o calculo da distancia, sao necessarias as coordenadas dos centros das duas circunferencias. O calculo e o seguinte:
        d = raiz quadrada de ((Xa-Xb)² + (Ya-Yb)²)
        """
        return math.sqrt(math.pow((self.tx - outro_x),2) + math.pow((self.ty - outro_y), 2))

    def transformar_vertices(self, forma) -> list:
        """
        A funcao gera os valores atualizados dos vertices do objeto para ser renderizado.

        Para isso, ele aplica as transformações geometricas não comutativas, seguindo a ordem:
            1. Escalonamento
            2. Rotação
            3. Translação
        """
        rad = math.radians(self.angulo_graus)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        vertices_transformados = []
        for x, y in forma:
            # 1. Escala
            nx = x * self.sx
            ny = y * self.sy
            
            # 2. Rotação
            rx = nx * cos_a - ny * sin_a
            ry = nx * sin_a + ny * cos_a
            
            # 3. Translação
            final_x = rx + self.tx
            final_y = ry + self.ty

            final_x = max(final_x, ESPESSURA_BORDA) if final_x < LARGURA - ESPESSURA_BORDA else LARGURA - ESPESSURA_BORDA # limita a borda
            final_y = max(final_y, ESPESSURA_BORDA) if final_y < ALTURA - ESPESSURA_BORDA else ALTURA - ESPESSURA_BORDA # limita a borda
            
            vertices_transformados.append((final_x, final_y))
        return vertices_transformados

    def _calcular_iluminacao_2d(self, cor, vertices) -> tuple:
        """Funcao para calcular cor de acordo com distância da fonte de luz"""
        # 1. Encontrar o centro do polígono (média dos pontos X e Y)
        # Assumindo vértices como [(x1, y1), (x2, y2), ...]
        centro_x = sum(v[0] for v in vertices) / len(vertices)
        centro_y = sum(v[1] for v in vertices) / len(vertices)
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
        intensidade = intensidade * (300 / (300 + distancia)) 

        fator_final = min(1.0, intensidade + LUZ_AMBIENTE)
        
        # 6. Retornar cor
        cor_final = (np.array(cor) * fator_final).astype(int)
        return tuple(np.clip(cor_final, 0, 255))

    def desenhar(self, tela):
        """Funcao mestra que renderiza o objeto"""
        for forma_v, cor, espessura in self.pontos:
            novos_pontos = self.transformar_vertices(forma_v)
            cor_com_luz = self._calcular_iluminacao_2d(cor, novos_pontos)
            pygame.draw.polygon(tela, cor_com_luz, novos_pontos, espessura)
