import pygame
import math
import random


# Inicialização do Pygame
pygame.init()
LARGURA, ALTURA = 1000, 700
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Transformações Geométricas - A Nave e o Espaço")
relogio = pygame.time.Clock()

# Cores Cyberpunk / Neon
PRETO = (10, 10, 15)
BRANCO = (255, 255, 255)
CIANO_NEON = (0, 255, 255)
MAGENTA_NEON = (255, 0, 255)
LARANJA_NEON = (255, 100, 0)
AZUL_CLARO = (100, 200, 255)

# --- Definição da Nave  ---
def criar_pontos_circulo(raio=1):
    circulo = [(round(math.cos(math.radians(i))*raio,2),round(math.sin(math.radians(i))*raio,2)) for i in range(0, 360, 18)]

    triangulo = [(0,0), (35, 25), (-35, 25)]
    # Formato: (vértices, cor, espessura da linha: 0=preenchido)
    return [
        (circulo, LARANJA_NEON, 0),
        (triangulo, PRETO, 0)
    ]

# Estrela de fundo
estrela_original = [(-1, -1), (1, -1), (1, 1), (-1, 1)]

# --- Função Mestra de Transformação ---
def transformar_vertices(vertices, tx, ty, angulo_graus, sx, sy, mirror_y=False):
    rad = math.radians(angulo_graus)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    # ESPELHAMENTO NO EIXO Y (Inverte o sinal da escala em Y)
    escala_x_final = sx
    escala_y_final = sy * (-1 if mirror_y else 1)

    vertices_transformados = []
    for x, y in vertices:
        # 1. Escala e Espelhamento Y
        nx = x * escala_x_final
        ny = y * escala_y_final
        
        # 2. Rotação
        rx = nx * cos_a - ny * sin_a
        ry = nx * sin_a + ny * cos_a
        
        # 3. Translação com Screen Wrapping (Bordas infinitas)
        final_x = (rx + tx) % LARGURA
        final_y = (ry + ty) % ALTURA
        
        vertices_transformados.append((final_x, final_y))
    return vertices_transformados

# ------- calculo de distancia entre circunferencias --------
def distancia_entre_centros(x1, y1, x2, y2):
    return math.sqrt(math.pow((x1 - x2),2) + math.pow((y1 - y2), 2))


# --- Classes ---
class Estrela:
    def __init__(self):
        self.raio = 15
        self.x = random.randrange(LARGURA - self.raio)
        self.y = random.randrange(ALTURA - self.raio)
        self.escala = 1
        self.pontos = criar_pontos_circulo(self.raio)[0][0]

    def atualizar_e_desenhar(self, surface):
        v = transformar_vertices(self.pontos, self.x, self.y, 0, self.escala, self.escala)
        pygame.draw.polygon(surface, BRANCO, v, 0)

# --- Inicialização ---
RAIO = 45
raio_1 = RAIO
raio_2 = RAIO
formas_circulo_1 = criar_pontos_circulo(raio_1)
formas_circulo_2 = criar_pontos_circulo(raio_2)
nave_x_2, nave_y_2 = 100, 300
nave_x_1, nave_y_1 = 700, 300
nave_angulo_1 = 0
nave_angulo_2 = 0
nave_escala_1 = 1.0
nave_escala_2 = 1.0
nave_mirror_y = False
distancia_centros_circunferencia = 100

estrelas = [Estrela() for _ in range(3)]
fonte = pygame.font.SysFont("Courier New", 18, bold=True)
continuar = True
rodando = True
while rodando:
    if continuar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_m: 
                    # Ativa/Desativa o espelhamento no Eixo Y
                    nave_mirror_y = not nave_mirror_y

        teclas = pygame.key.get_pressed()
        
        # Rotação
        # if teclas[pygame.K_a]: nave_angulo_2 -= 2
        # if teclas[pygame.K_d]: nave_angulo_2 += 2
        
        
        # Translação
        mudar_x_1, mudar_y_1 = 0, 0
        mudar_x_2, mudar_y_2 = 0, 0
        vel_nave = 3
        if teclas[pygame.K_w]: 
            """
            Inicialmente, o visual da nave está com o bico para 90º, mas seu real ângulo é de 0º. Se queremos que nesse caso apenas o eixo Y seja alterado,
            devemos utilizar o valor do cosseno do ângulo.
            Agora, se configuramos o ângulo para 45º (visualmente), na verdade, queremos que ele atue como um ângulo de -45º. Mas como o círculo trigonométrico
            de 1 volta só vai até 360º, devemos fazer 360 - 45 = 315º. Logo, queremos que o eixo Y seja mofificado pelo cosseno de 315º. Mas com o visual está
            inclinado, o eixo X também deve ser alterado. Para isso, vamos utilizar o "oposto" do cosseno, o seno de 315º.
            """
            mudar_y_2 -= vel_nave * math.cos(math.radians(360-nave_angulo_2))
            mudar_x_2 -= vel_nave * math.sin(math.radians(360-nave_angulo_2))
        if teclas[pygame.K_s]: 
            mudar_y_2 += vel_nave * math.cos(math.radians(360-nave_angulo_2))
            mudar_x_2 += vel_nave * math.sin(math.radians(360-nave_angulo_2))
        if teclas[pygame.K_a]: mudar_x_2 -= vel_nave
        if teclas[pygame.K_d]: mudar_x_2 += vel_nave

        nave_x_2 += mudar_x_2
        nave_y_2 += mudar_y_2


        # Rotação
        if teclas[pygame.K_LEFT]: nave_angulo_1 -= 2
        if teclas[pygame.K_RIGHT]: nave_angulo_1 += 2


        if teclas[pygame.K_UP]: 
            """
            Inicialmente, o visual da nave está com o bico para 90º, mas seu real ângulo é de 0º. Se queremos que nesse caso apenas o eixo Y seja alterado,
            devemos utilizar o valor do cosseno do ângulo.
            Agora, se configuramos o ângulo para 45º (visualmente), na verdade, queremos que ele atue como um ângulo de -45º. Mas como o círculo trigonométrico
            de 1 volta só vai até 360º, devemos fazer 360 - 45 = 315º. Logo, queremos que o eixo Y seja mofificado pelo cosseno de 315º. Mas com o visual está
            inclinado, o eixo X também deve ser alterado. Para isso, vamos utilizar o "oposto" do cosseno, o seno de 315º.
            """
            mudar_y_1 -= vel_nave * math.cos(math.radians(360-nave_angulo_1))
            mudar_x_1 -= vel_nave * math.sin(math.radians(360-nave_angulo_1))
        if teclas[pygame.K_DOWN]: 
            mudar_y_1 += vel_nave * math.cos(math.radians(360-nave_angulo_1))
            mudar_x_1 += vel_nave * math.sin(math.radians(360-nave_angulo_1))
        if teclas[pygame.K_LEFT]: mudar_x_1 -= vel_nave
        if teclas[pygame.K_RIGHT]: mudar_x_1 += vel_nave

        nave_x_1 += mudar_x_1
        nave_y_1 += mudar_y_1

        # --- Renderização ---
        tela.fill(PRETO)
        
        # 1. Desenhar Estrelas
        for e in estrelas:
            e.atualizar_e_desenhar(tela)

        # 2. Desenhar a Nave Bonita
        for forma_v, cor, espessura in formas_circulo_1:
            v_final = transformar_vertices(forma_v, nave_x_1, nave_y_1, nave_angulo_1, nave_escala_1, nave_escala_1, nave_mirror_y)
            pygame.draw.polygon(tela, cor, v_final, espessura)

        for forma_v, cor, espessura in formas_circulo_2:
            v_final = transformar_vertices(forma_v, nave_x_2, nave_y_2, nave_angulo_2, nave_escala_2, nave_escala_2, nave_mirror_y)
            pygame.draw.polygon(tela, cor, v_final, espessura)

        # --- HUD ---
        textos = [
            "CONTROLES DO MOTOR GRÁFICO:",
            f"Translação (Setas): X={nave_x_1%LARGURA:.0f}, Y={nave_y_1%ALTURA:.0f}",
            f"Rotação (A, D)  : {nave_angulo_1%360}°",
            f"Distancia {distancia_centros_circunferencia}"
        ]
        for i, t in enumerate(textos):
            cor_txt = BRANCO if i == 0 else LARANJA_NEON
            superficie = fonte.render(t, True, cor_txt)
            tela.blit(superficie, (15, 15 + i * 22))

        distancia_centros_circunferencia = distancia_entre_centros(nave_x_1, nave_y_1, nave_x_2, nave_y_2)
        soma_raios = raio_1 + raio_2
        if distancia_centros_circunferencia <= soma_raios and raio_1 != raio_2:
            continuar = False

        for i in estrelas:
            distancia_1 = distancia_entre_centros(nave_x_1, nave_y_1, i.x, i.y)
            distancia_2 = distancia_entre_centros(nave_x_2, nave_y_2, i.x, i.y)
            soma_raios_1 = i.raio + raio_1
            soma_raios_2 = i.raio + raio_2

            if distancia_1 <= soma_raios_1 and distancia_2 <= soma_raios_2:
                if distancia_1 > distancia_2:
                    nave_escala_2 += 0.5
                    raio_2 = RAIO * nave_escala_2
                    estrelas.remove(i)
                elif distancia_2 > distancia_1:
                    nave_escala_1 += 0.5
                    raio_1 = RAIO * nave_escala_1
                    estrelas.remove(i)
                else:
                    pass
            elif distancia_1 <= soma_raios_1:
                nave_escala_1 += 0.5
                raio_1 = RAIO * nave_escala_1
                estrelas.remove(i)
            elif distancia_2 <= soma_raios_2:
                nave_escala_2 += 0.5
                raio_2 = RAIO * nave_escala_2
                estrelas.remove(i)
            else:
                pass

        pygame.display.flip()
        relogio.tick(60)
    else:
        relogio.tick(6000)
        rodando = False

pygame.quit()