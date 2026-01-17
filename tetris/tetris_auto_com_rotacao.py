
import pygame
import random
import numpy as np
from ultralytics import YOLO

modelo = YOLO("best.pt")  # Substitui pelo caminho correto

pygame.init()

largura_bloco = 30
largura_jogo = 10
altura_jogo = 20
largura_tela = largura_bloco * largura_jogo
altura_tela = largura_bloco * altura_jogo
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Tetris Auto")

cores = [
    (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 255, 255),
    (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)
]

formas = {
    'Tetrimino_Z': [[1, 1, 0], [0, 1, 1]],
    'Tetrimino_S': [[0, 2, 2], [2, 2, 0]],
    'Tetrimino_I': [[3, 3, 3, 3]],
    'Tetrimino_O': [[4, 4], [4, 4]],
    'Tetrimino_L': [[0, 0, 5], [5, 5, 5]],
    'Tetrimino_J': [[6, 0, 0], [6, 6, 6]],
    'Tetrimino_T': [[0, 7, 0], [7, 7, 7]]
}

class Peca:
    def __init__(self, x, y, forma, cor_id):
        self.x = x
        self.y = y
        self.forma = forma
        self.altura = len(forma)
        self.largura = len(forma[0])
        self.id = cor_id

    def rotacionar(self):
        self.forma = [list(row) for row in zip(*self.forma[::-1])]
        self.altura = len(self.forma)
        self.largura = len(self.forma[0])

def criar_grid():
    return [[0 for _ in range(largura_jogo)] for _ in range(altura_jogo)]

def desenhar_grid(grid):
    for y in range(altura_jogo):
        for x in range(largura_jogo):
            pygame.draw.rect(tela, cores[grid[y][x]],
                             (x * largura_bloco, y * largura_bloco, largura_bloco, largura_bloco), 0)
            pygame.draw.rect(tela, (50, 50, 50),
                             (x * largura_bloco, y * largura_bloco, largura_bloco, largura_bloco), 1)

def colisao(grid, peca):
    for y in range(peca.altura):
        for x in range(peca.largura):
            if peca.forma[y][x]:
                if (peca.y + y >= altura_jogo or
                    peca.x + x < 0 or
                    peca.x + x >= largura_jogo or
                    grid[peca.y + y][peca.x + x]):
                    return True
    return False

def fundir(grid, peca):
    for y in range(peca.altura):
        for x in range(peca.largura):
            if peca.forma[y][x]:
                grid[peca.y + y][peca.x + x] = peca.id

def limpar_linhas(grid):
    nova_grid = [linha for linha in grid if any(c == 0 for c in linha)]
    linhas_removidas = altura_jogo - len(nova_grid)
    while len(nova_grid) < altura_jogo:
        nova_grid.insert(0, [0] * largura_jogo)
    return nova_grid, linhas_removidas

def captura_tela():
    pixels = pygame.surfarray.array3d(tela)
    img = np.transpose(pixels, (1, 0, 2))
    return img

def decide_acao(modelo, imagem):
    resultados = modelo.predict(imagem, conf=0.4, verbose=False)
    if not resultados or not resultados[0].boxes:
        return None, None

    box = resultados[0].boxes[0].xywh[0]
    classe_id = int(resultados[0].boxes[0].cls[0])
    nome_classe = modelo.names[classe_id]
    x_centro = box[0].item()

    if x_centro < largura_tela // 3:
        movimento = 'left'
    elif x_centro > 2 * largura_tela // 3:
        movimento = 'right'
    else:
        movimento = 'drop'

    return movimento, nome_classe

def main():
    grid = criar_grid()
    relogio = pygame.time.Clock()
    tempo_queda = 500
    contador = 0
    forma_aleatoria = random.choice(list(formas.items()))
    peca = Peca(3, 0, forma_aleatoria[1], list(formas.keys()).index(forma_aleatoria[0]) + 1)
    proxima = Peca(3, 0, random.choice(list(formas.values())), random.randint(1, 7))
    jogo_ativo = True

    while jogo_ativo:
        tela.fill((0, 0, 0))
        desenhar_grid(grid)
        for y in range(peca.altura):
            for x in range(peca.largura):
                if peca.forma[y][x]:
                    pygame.draw.rect(tela, cores[peca.id],
                                     ((peca.x + x) * largura_bloco, (peca.y + y) * largura_bloco,
                                      largura_bloco, largura_bloco), 0)

        pygame.display.update()

        contador += relogio.get_rawtime()
        relogio.tick()

        if contador > tempo_queda:
            img = captura_tela()
            acao, classe = decide_acao(modelo, img)

            if acao == 'left':
                peca.x -= 1
                if colisao(grid, peca): peca.x += 1
            elif acao == 'right':
                peca.x += 1
                if colisao(grid, peca): peca.x -= 1
            elif acao == 'drop':
                peca.y += 1

            if classe:
                esperada = list(formas.keys()).index(classe) + 1
                while peca.id != esperada:
                    peca.rotacionar()
                    break  # Evita loop infinito

            if colisao(grid, peca):
                peca.y -= 1
                fundir(grid, peca)
                grid, _ = limpar_linhas(grid)
                forma_aleatoria = random.choice(list(formas.items()))
                peca = Peca(3, 0, forma_aleatoria[1], list(formas.keys()).index(forma_aleatoria[0]) + 1)
                if colisao(grid, peca):
                    jogo_ativo = False
            contador = 0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_ativo = False

    pygame.quit()

if __name__ == '__main__':
    main()
