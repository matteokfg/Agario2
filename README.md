# Agario2

Este projeto é um jogo interativo desenvolvido em Python utilizando a biblioteca **Pygame**, inspirado em mecânicas de *Agar.io*, *Pacman* e *Pega-Pega*. O software foi construído como parte prática da disciplina de **Computação Gráfica**, servindo como laboratório para a aplicação de conceitos matemáticos e geométricos essenciais no pipeline de renderização 2D.

## O Jogo e Mecânicas

O jogo coloca dois jogadores em uma arena onde o objetivo é crescer consumindo moedas ou eliminar o adversário consumindo-o (caso você seja maior que ele).

* **Jogador 1 (Ciano)**: Controlado pelas setas do teclado (Movimentação e Rotação).
* **Jogador 2 (Laranja)**: Controlado pelas teclas `W`, `A`, `S`, `D` (Movimentação e Rotação).
* **Moedas**: Surgem aleatoriamente pelo mapa. Coletá-las aumenta o tamanho (escala e raio) do jogador.
* **Mundança de Cenário**: Pressione a tecla `T` para alternar as texturas de fundo em tempo real.

## Como Executar o Projeto

1. Certifique-se de ter o Python instalado.
2. Instale as dependências listadas no arquivo `requirements.txt`:
```
pip install -r requirements.txt
```

3. Execute o arquivo principal para iniciar o jogo:
```
python main.py
```

> Recomendação: usar um ambeinte virtual do python.
>
> Criar ambiente: `python -m venv .venv`
>
> Iniciar ambiente: `.venv\Scripts\activate`

## Conceitos de Computação Gráfica Aplicados

Abaixo estão detalhados os fundamentos teóricos implementados manualmente no código (sem depender de funções prontas de matrizes do Pygame).

### 1. Modelagem Procedural de Polígonos

Em computação gráfica, formas curvas são frequentemente aproximadas por polígonos de múltiplos lados. No arquivo `circulo.py` e `moeda.py`, a circunferência não é desenhada como uma primitiva nativa de círculo, mas sim gerada via código como um **polígono regular de 20 lados**.

A amostragem angular é feita a cada 18° (pois $360^\circ / 20 = 18^\circ$), e as coordenadas locais dos vértices são determinadas usando funções trigonométricas ($r = raio$):

$$x = r \cdot \cos(\theta)$$

$$y = r \cdot \sin(\theta)$$

### 2. Pipeline de Transformações Geométricas 2D

As transformações lineares e afins são aplicadas manualmente a cada vértice do modelo antes da renderização na função `transformar_vertices`. Como as transformações matriciais **não são comutativas**, a ordem de aplicação altera drasticamente o resultado final. O pipeline segue a ordem padrão da Computação Gráfica:

1. **Escalonamento**: Altera o tamanho do objeto a partir da origem local, multiplicando os vértices por fatores de escala ($s_x, s_y$).
2. **Rotação**: Rotaciona os pontos em torno da origem com base no ângulo atual ($\theta$) convertido para radianos:

$$X_f = X_i \cdot \cos(\theta) - Y_i \cdot \sin(\theta)$$


$$Y_f = X_i \cdot \sin(\theta) + Y_i \cdot \cos(\theta)$$


3. **Translação**: Move o objeto para a sua posição global no mundo do jogo, somando as coordenadas de translação ($t_x, t_y$).

### 3. Modelo de Iluminação Plana (Flat Shading) e Atenuação

Para dar uma sensação de profundidade ao ambiente bidimensional, foi implementado um modelo customizado de iluminação baseado na **Refletância Lambertiana**:

* **Vetor de Luz e Normal**: Cada polígono calcula seu centro de massa (baricentro). A partir dele, gera-se um vetor em direção à fonte de luz fixa (`POSICAO_LUZ_FIXA`). A superfície do jogo possui uma normal constante $\vec{N} = [0, 0, 1]$, indicando que ela "olha" diretamente para a tela.
* **Produto Escalar**: A intensidade da luz direta é calculada através do produto escalar entre a normal e o vetor de luz normalizado:

$$I_{direta} = \max(0, \vec{N} \cdot \vec{L}_{norm})$$


* **Atenuação por Distância**: A intensidade da luz decai conforme o objeto se afasta da fonte, utilizando uma curva de atenuação matemática:

$$F_{atenuacao} = \frac{300}{300 + d}$$


* **Luz Ambiente**: Garante que o objeto nunca fique completamente invisível na ausência de luz direta. A cor final é o resultado da multiplicação da cor base pelo fator de iluminação limitado ao teto de 100% (clipping).

### 4. Mapeamento de Texturas

Para o preenchimento do plano de fundo, o projeto faz uso de **mapeamento de textura** em polígonos convexos através da função `pygame.gfxdraw.textured_polygon`. Os vértices do retângulo de fundo são mapeados diretamente para as coordenadas UV da imagem carregada de forma estática, permitindo que o motor renderize superfícies estilizadas (como padrões xadrez ou pedras).

### 5. Detecção de Colisão por Distância Euclidiana

A detecção de colisão entre os jogadores e as moedas utiliza o conceito geométrico clássico de intersecção de círculos. Em vez de testar caixas de colisão delimitadoras (*Bounding Boxes*), o código calcula a **Distância Euclidiana** entre os centros das circunferências:

$$d = \sqrt{(x_a - x_b)^2 + (y_a - y_b)^2}$$

Se a distância $d$ for menor ou igual à soma dos raios dos dois objetos ($r_a + r_b$), uma colisão é registrada pelo sistema do jogo.


## Estrutura do Repositório

* `main.py`: Gerencia a inicialização, captura de eventos do teclado, loop principal do jogo, lógica de colisões e atualizações do HUD.
* `circulo.py`: Contém a classe `Circulo`, responsável pela modelagem do jogador, cálculo do pipeline de transformações e rasterização do polígono de iluminação do jogador.
* `moeda.py`: Contém a classe `Moeda`, modelada com uma estética interna de losango, aplicando transformações e iluminação própria.
* `contants.py`: Centraliza as variáveis de ambiente, configurações da tela, paleta de cores RGB neon e vetores de iluminação global.
* `requirements.txt`: Lista de bibliotecas externas necessárias para execução do ecossistema do projeto.

> Observação: README.md gerado com a ajuda do _Google Gemini_, versão _Raciocínio_, no dia 2026-05-16.
>
> **Prompt**: 
> "Use os arquivos em anexo para gerar um arquivo readme.md. O projeto/repositório é de um jogo inspirado no agar.io, pacman e pega-pega, feito em pygame, com o objetivo de ser um projeto para aplicar os conceitos aprendidos na matéria 'Computação gráfica'. Logo faça uma explicação/resumo do código que também dê um pouco de foco na parte teórica como as transformações geométricas, cálculo da luz, texturas e cálculo da distância entre circunferências."