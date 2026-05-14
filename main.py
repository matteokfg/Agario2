import math
import random
import time

import pygame
import numpy as np

from contants import *
from moeda import Moeda
from circulo import Circulo


# Inicialização do Pygame
pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Agar.io v0.5")
relogio = pygame.time.Clock()

fonte = pygame.font.SysFont("Courier New", 18, bold=True)

# Load and optimize the texture
# texture = pygame.image.load('saturno.jpg').convert_alpha()

# texture = pygame.transform.scale(texture, (65, 65))


# para que serve np.array(COR_LUZ)?
def calcular_iluminacao_2d(vertices, cor_base):
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
        return cor_base
    vetor_luz_norm = vetor_luz / distancia

    # 4. Produto Escalar (Lambert)
    # Quanto mais "embaixo" da luz o polígono estiver, mais forte o brilho
    dot_product = np.dot(np.array(NORMAL_2D), vetor_luz_norm)
    
    intensidade = max(0, dot_product)
    
    # 5. Atenuação opcional: a luz perde força com a distância? 
    # Se quiser uma luz global (sol), ignore a linha abaixo.
    intensidade = intensidade * (500 / (500 + distancia)) 

    fator_final = min(1.0, intensidade + LUZ_AMBIENTE)
    
    # 6. Aplicar cor
    cor_final = (np.array(cor_base) * fator_final).astype(int)
    return tuple(np.clip(cor_final, 0, 255))

# --- EXEMPLO NO LOOP DE DESENHO ---
# vertices_exemplo = [(100, 100), (200, 100), (150, 200)]
# cor_poligono = np.array([100, 150, 255]) # Azul claro
# cor_com_luz = calcular_iluminacao_2d(vertices_exemplo, cor_poligono)
# pygame.draw.polygon(screen, cor_com_luz, vertices_exemplo)

# --- Inicialização ---
bordas = [
    [(0,0), (0,ALTURA), (ESPESSURA_BORDA,ALTURA), (ESPESSURA_BORDA,0)],
    [(0,0), (LARGURA,0), (LARGURA,ESPESSURA_BORDA), (0,ESPESSURA_BORDA)],
    [(LARGURA,0), (LARGURA,ALTURA), (LARGURA-ESPESSURA_BORDA,ALTURA), (LARGURA-ESPESSURA_BORDA,0)],
    [(0,ALTURA), (LARGURA,ALTURA), (LARGURA,ALTURA-ESPESSURA_BORDA), (0,ALTURA-ESPESSURA_BORDA)]
]


moedas = [Moeda() for _ in range(3)]

c1 = Circulo(700,300,RAIO, 0, 1.0, 1.0, 1)

c2 = Circulo(100,300,RAIO, 0, 1.0, 1.0, 2, LARANJA_NEON)


distancia_centros_circunferencia = None
soma_raios = None

rodando = True

vencedor = None

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    
    # Rotação
    if teclas[pygame.K_a]: c2.angulo_graus -= 2
    if teclas[pygame.K_d]: c2.angulo_graus += 2

    if teclas[pygame.K_LEFT]: c1.angulo_graus -= 2
    if teclas[pygame.K_RIGHT]: c1.angulo_graus += 2
    
    
    # Translação
    mudar_x_1, mudar_y_1 = 0, 0
    mudar_x_2, mudar_y_2 = 0, 0

    vel_circunferencia = 3

    if teclas[pygame.K_w]: 
        """
        Inicialmente, o visual da circunferencia está com o bico para 90º, mas seu real ângulo é de 0º. Se queremos que nesse caso apenas o eixo Y seja alterado,
        devemos utilizar o valor do cosseno do ângulo.
        Agora, se configuramos o ângulo para 45º (visualmente), na verdade, queremos que ele atue como um ângulo de -45º. Mas como o círculo trigonométrico
        de 1 volta só vai até 360º, devemos fazer 360 - 45 = 315º. Logo, queremos que o eixo Y seja mofificado pelo cosseno de 315º. Mas com o visual está
        inclinado, o eixo X também deve ser alterado. Para isso, vamos utilizar o "oposto" do cosseno, o seno de 315º.
        """
        mudar_y_2 -= vel_circunferencia * math.cos(math.radians(360-c2.angulo_graus))
        mudar_x_2 -= vel_circunferencia * math.sin(math.radians(360-c2.angulo_graus))
    if teclas[pygame.K_s]: 
        mudar_y_2 += vel_circunferencia * math.cos(math.radians(360-c2.angulo_graus))
        mudar_x_2 += vel_circunferencia * math.sin(math.radians(360-c2.angulo_graus))
    # if teclas[pygame.K_a]: mudar_x_2 -= vel_circunferencia
    # if teclas[pygame.K_d]: mudar_x_2 += vel_circunferencia


    if teclas[pygame.K_UP]: 
        """
        Inicialmente, o visual da circunferencia está com o bico para 90º, mas seu real ângulo é de 0º. Se queremos que nesse caso apenas o eixo Y seja alterado,
        devemos utilizar o valor do cosseno do ângulo.
        Agora, se configuramos o ângulo para 45º (visualmente), na verdade, queremos que ele atue como um ângulo de -45º. Mas como o círculo trigonométrico
        de 1 volta só vai até 360º, devemos fazer 360 - 45 = 315º. Logo, queremos que o eixo Y seja mofificado pelo cosseno de 315º. Mas com o visual está
        inclinado, o eixo X também deve ser alterado. Para isso, vamos utilizar o "oposto" do cosseno, o seno de 315º.
        """
        mudar_y_1 -= vel_circunferencia * math.cos(math.radians(360-c1.angulo_graus))
        mudar_x_1 -= vel_circunferencia * math.sin(math.radians(360-c1.angulo_graus))
    if teclas[pygame.K_DOWN]: 
        mudar_y_1 += vel_circunferencia * math.cos(math.radians(360-c1.angulo_graus))
        mudar_x_1 += vel_circunferencia * math.sin(math.radians(360-c1.angulo_graus))
    # if teclas[pygame.K_LEFT]: mudar_x_1 -= vel_circunferencia
    # if teclas[pygame.K_RIGHT]: mudar_x_1 += vel_circunferencia

    c1.tx += mudar_x_1
    c1.ty += mudar_y_1

    c2.tx += mudar_x_2
    c2.ty += mudar_y_2

    c1.tx = max(c1.tx, 45 + ESPESSURA_BORDA) if c1.tx < LARGURA - c1.raio - ESPESSURA_BORDA else LARGURA - c1.raio - ESPESSURA_BORDA
    c1.ty = max(c1.ty, 45 + ESPESSURA_BORDA) if c1.ty < ALTURA - c1.raio - ESPESSURA_BORDA else ALTURA - c1.raio - ESPESSURA_BORDA

    c2.tx = max(c2.tx, 45 + ESPESSURA_BORDA) if c2.tx < LARGURA - c2.raio - ESPESSURA_BORDA else LARGURA - c2.raio - ESPESSURA_BORDA
    c2.ty = max(c2.ty, 45 + ESPESSURA_BORDA) if c2.ty < ALTURA - c2.raio - ESPESSURA_BORDA else ALTURA - c2.raio - ESPESSURA_BORDA

    # --- Renderização ---
    tela.fill(PRETO)
    
    # 1. Desenhar Estrelas
    for e in moedas:
        e.atualizar_e_desenhar(tela)

    # 2. Desenhar a circunferencia Bonita
    c1.desenhar(tela)

    c2.desenhar(tela)

    # ------- verifica se foi comido -----------------
    distancia_centros_circunferencia = c1.distancia_entre_centros(c2.tx, c2.ty)
    soma_raios = c1.raio + c2.raio
    if distancia_centros_circunferencia <= soma_raios and c1.raio != c2.raio:
        rodando = False
        if c1.raio > c2.raio:
            vencedor = c1
        else:
            vencedor = c2

    # -------------- verifica se comeu a amora --------
    for moeda in moedas:
        distancia_1 = c1.distancia_entre_centros(moeda.x, moeda.y)
        distancia_2 = c2.distancia_entre_centros(moeda.x, moeda.y)
        soma_raios_1 = moeda.raio + c1.raio
        soma_raios_2 = moeda.raio + c2.raio

        if distancia_1 <= soma_raios_1 and distancia_2 <= soma_raios_2:
            if distancia_1 > distancia_2:
                c2.sx += 0.5
                c2.sy += 0.5
                c2.raio = RAIO * c2.sx
                moedas.remove(moeda)
            elif distancia_2 > distancia_1:
                c1.sx += 0.5
                c1.sy += 0.5
                c1.raio = RAIO * c1.sx
                moedas.remove(moeda)
            else:
                pass
        elif distancia_1 <= soma_raios_1:
            c1.sx += 0.5
            c1.sy += 0.5
            c1.raio = RAIO * c1.sx
            moedas.remove(moeda)
        elif distancia_2 <= soma_raios_2:
            c2.sx += 0.5
            c2.sy += 0.5
            c2.raio = RAIO * c2.sx
            moedas.remove(moeda)
        else:
            pass

    # --- HUD ---
    textos = [
        "CONTROLES DO MOTOR GRÁFICO:",
        f"Translação (Setas): X={c1.tx%LARGURA:.0f}, Y={c1.ty%ALTURA:.0f}",
        f"Translação (Setas): X={c2.tx%LARGURA:.0f}, Y={c2.ty%ALTURA:.0f}",
        f"Rotação (LEFT, RIGHT)  : {c1.angulo_graus%360}°",
        f"Rotação (A, D)  : {c2.angulo_graus%360}°",
        f"Distancia {distancia_centros_circunferencia}"
    ]
    for i, t in enumerate(textos):
        cor_txt = CIANO_NEON if i % 2 == 1 else BRANCO if i == 0 else LARANJA_NEON
        x_HUD = 500 if i % 2 == 1 else 15
        superficie = fonte.render(t, True, cor_txt)
        tela.blit(superficie, (x_HUD, 15 + i * 22 if i < 2 else 15 + (math.ceil(i/2)) * 22))

    # tela.blit(texture, (c1.tx, c1.ty))
    for borda in bordas:
        cor_com_luz = calcular_iluminacao_2d(borda, VERDE_BORDA)
        pygame.draw.polygon(tela, cor_com_luz, borda, 0)


    pygame.display.flip()
    relogio.tick(60)

if vencedor is not None:
    textos = [
        "Resultado da partida:",
        f"Parabens!! {vencedor} venceu!"
    ]
    for i, t in enumerate(textos):
        cor_txt = BRANCO if i == 0 else AZUL_CLARO
        superficie = fonte.render(t, True, cor_txt)
        tela.blit(superficie, (LARGURA // 2, (ALTURA//2) + i * 22))
    pygame.display.flip()
    relogio.tick(60)
    time.sleep(5)

pygame.quit()