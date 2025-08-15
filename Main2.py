import pygame
import random

from Objetos.Asteroide import Asteroide
from Objetos.Nave import Nave

# 1. Configurações Iniciais
# ======================================================================================================================

pygame.init()

# Define as dimensões e constantes globais aqui, onde serão usadas
LARGURA_TELA, ALTURA_TELA = 800, 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Nave")

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

clock = pygame.time.Clock()

# 2. Lógica do Jogo Principal
# ======================================================================================================================

def loop_jogo():
    """Função principal do jogo."""

    # Passa as dimensões da tela para a classe Nave ao instanciá-la
    nave = Nave(LARGURA_TELA, ALTURA_TELA, BRANCO)

    rodando = True

    while rodando:
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        nave.mover()

        # 3. Desenho na Tela - Passando 'tela' para cada objeto
        # --------------------------------------------------------------------------------------------------------------
        tela.fill(PRETO)

        nave.desenhar(tela)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    loop_jogo()