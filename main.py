import pygame
import math
import random
import time

# Inicialização do Pygame
pygame.init()
LARGURA, ALTURA = 1000, 700
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Agar.io v0.5")
relogio = pygame.time.Clock()

# Cores Cyberpunk / Neon
PRETO = (10, 10, 15)
BRANCO = (255, 255, 255)
CIANO_NEON = (0, 255, 255)
MAGENTA_NEON = (255, 0, 255)
LARANJA_NEON = (255, 100, 0)
AZUL_CLARO = (100, 200, 255)

RAIO = 45


# --- Classes ---
class Circulo:
    def __init__(self, x, y, raio, angulo_graus, sx, sy, cor=CIANO_NEON):
        self.x = x
        self.y = y
        self.raio = raio
        self.tx = x
        self.ty = y
        self.angulo_graus = angulo_graus
        self.sx = sx
        self.sy = sy
        self.cor = cor
        self.pontos = self._criar_pontos()

    # --- Definição da circunferencia  ---
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

    # --- Calculo de distancia entre circunferencias --------
    def distancia_entre_centros(self, outro_x, outro_y) -> float:
        """
        Para o calculo da distancia, sao necessarias as coordenadas dos centros das duas circunferencias. O calculo e o seguinte:
        d = raiz quadrada de ((Xa-Xb)² + (Ya-Yb)²)
        """
        return math.sqrt(math.pow((self.tx - outro_x),2) + math.pow((self.ty - outro_y), 2))

    # --- Função Mestra de Transformação ---
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

            final_x = max(final_x, 0) if final_x < LARGURA else LARGURA # limita a borda
            final_y = max(final_y, 0) if final_y < ALTURA else ALTURA # limita a borda
            
            vertices_transformados.append((final_x, final_y))
        return vertices_transformados

    # --- Funcao Mestra para renderizar objeto
    def desenhar(self, tela):
        """Funcao que renderiza o objeto"""
        for forma_v, cor, espessura in self.pontos:
            novos_pontos = self.transformar_vertices(forma_v)
            pygame.draw.polygon(tela, cor, novos_pontos, espessura)


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

# --- Inicialização ---
moedas = [Moeda() for _ in range(3)]

c1 = Circulo(700,300,RAIO, 0, 1.0, 1.0)

c2 = Circulo(100,300,RAIO, 0, 1.0, 1.0, LARANJA_NEON)


distancia_centros_circunferencia = None
soma_raios = None

rodando = True

fonte = pygame.font.SysFont("Courier New", 18, bold=True)

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
    if teclas[pygame.K_a]: mudar_x_2 -= vel_circunferencia
    if teclas[pygame.K_d]: mudar_x_2 += vel_circunferencia


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
    if teclas[pygame.K_LEFT]: mudar_x_1 -= vel_circunferencia
    if teclas[pygame.K_RIGHT]: mudar_x_1 += vel_circunferencia

    c1.tx += mudar_x_1
    c1.ty += mudar_y_1

    c2.tx += mudar_x_2
    c2.ty += mudar_y_2

    c1.tx = max(c1.tx, 0) if c1.tx < LARGURA - c1.raio else LARGURA - c1.raio
    c1.ty = max(c1.ty, 0) if c1.ty < ALTURA - c1.raio else ALTURA - c1.raio

    c2.tx = max(c2.tx, 0) if c2.tx < LARGURA - c2.raio else LARGURA - c2.raio
    c2.ty = max(c2.ty, 0) if c2.ty < ALTURA - c2.raio else ALTURA - c2.raio

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
        f"Rotação (A, D)  : {c1.angulo_graus%360}°",
        f"Distancia {distancia_centros_circunferencia}"
    ]
    for i, t in enumerate(textos):
        cor_txt = BRANCO if i == 0 else LARANJA_NEON
        superficie = fonte.render(t, True, cor_txt)
        tela.blit(superficie, (15, 15 + i * 22))

    pygame.display.flip()
    relogio.tick(60)


textos = [
    "Resultado da partida:",
    f"Parabens!! Voce venceu!"
]
for i, t in enumerate(textos):
    cor_txt = BRANCO if i == 0 else AZUL_CLARO
    superficie = fonte.render(t, True, cor_txt)
    tela.blit(superficie, (LARGURA // 2, (ALTURA//2) + i * 22))
pygame.display.flip()
relogio.tick(60)
time.sleep(5)

pygame.quit()