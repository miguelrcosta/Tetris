
import pygame
import random

# Inicializar pygame
pygame.init()

# Configurações do ecrã
largura_bloco = 30
largura_jogo = 10
altura_jogo = 20
largura_tela = largura_bloco * largura_jogo
altura_tela = largura_bloco * altura_jogo
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Tetris")

# Cores
cores = [
    (0, 0, 0),       # preto
    (255, 0, 0),     # vermelho
    (0, 255, 0),     # verde
    (0, 0, 255),     # azul
    (255, 255, 0),   # amarelo
    (255, 165, 0),   # laranja
    (0, 255, 255),   # ciano
    (128, 0, 128)    # roxo
]

# Peças do Tetris
formas = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 4],
     [4, 4]],

    [[0, 5, 0],
     [5, 5, 5]],

    [[6, 0, 0],
     [6, 6, 6]],

    [[0, 0, 7],
     [7, 7, 7]]
]

# Classe da peça
class Peca:
    def __init__(self, x, y, forma):
        self.x = x
        self.y = y
        self.forma = forma
        self.altura = len(forma)
        self.largura = len(forma[0])
        self.id = max([max(row) for row in forma])

    def rotacionar(self):
        self.forma = [list(row) for row in zip(*self.forma[::-1])]
        self.altura = len(self.forma)
        self.largura = len(self.forma[0])

# Funções do jogo
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

# Loop principal
def main():
    grid = criar_grid()
    relogio = pygame.time.Clock()
    tempo_queda = 500
    contador = 0
    peca = Peca(3, 0, random.choice(formas))
    proxima = Peca(3, 0, random.choice(formas))
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
            peca.y += 1
            if colisao(grid, peca):
                peca.y -= 1
                fundir(grid, peca)
                grid, _ = limpar_linhas(grid)
                peca = proxima
                proxima = Peca(3, 0, random.choice(formas))
                if colisao(grid, peca):
                    jogo_ativo = False
            contador = 0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_ativo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    peca.x -= 1
                    if colisao(grid, peca): peca.x += 1
                elif evento.key == pygame.K_RIGHT:
                    peca.x += 1
                    if colisao(grid, peca): peca.x -= 1
                elif evento.key == pygame.K_DOWN:
                    peca.y += 1
                    if colisao(grid, peca): peca.y -= 1
                elif evento.key == pygame.K_UP:
                    peca.rotacionar()
                    if colisao(grid, peca):
                        for _ in range(3): peca.rotacionar()

    pygame.quit()

if __name__ == '__main__':
    main()
