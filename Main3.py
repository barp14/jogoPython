import pygame
import random

from Objetos.Asteroide import Asteroide
# from Objetos.Nave import Nave
from Objetos.Nave2 import Nave2

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
    # nave = Nave(LARGURA_TELA, ALTURA_TELA, BRANCO)

    # Criando uma nave personalizada usando **kwargs
    nave2 = Nave2(LARGURA_TELA, ALTURA_TELA, cor=(0, 0, 255), velocidade=10)  # Uma nave azul e rápida!

    asteroides = []
    projeteis = []

    pontuacao = 0
    rodando = True

    while rodando:
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    projeteis.append(nave2.atirar(VERMELHO))

        nave2.mover()

        if random.random() < 0.02:
            # Passa as dimensões da tela para a classe Asteroide
            asteroides.append(Asteroide(LARGURA_TELA, ALTURA_TELA, BRANCO))

        for asteroide in asteroides:
            asteroide.mover()

        for projetil in projeteis:
            projetil.mover()

        for asteroide in asteroides[:]:
            if asteroide.rect.top > ALTURA_TELA:
                asteroides.remove(asteroide)

        for projetil in projeteis[:]:
            if projetil.rect.bottom < 0:
                projeteis.remove(projetil)

        for asteroide in asteroides:
            if nave2.rect.colliderect(asteroide.rect):
                print(f"Colisão! Sua pontuação final é: {pontuacao}")
                rodando = False

        for projetil in projeteis[:]:
            for asteroide in asteroides[:]:
                if projetil.rect.colliderect(asteroide.rect):
                    projeteis.remove(projetil)
                    asteroides.remove(asteroide)
                    pontuacao += 1
                    break

        # 3. Desenho na Tela - Passando 'tela' para cada objeto
        # --------------------------------------------------------------------------------------------------------------
        tela.fill(PRETO)

        nave2.desenhar(tela)

        for asteroide in asteroides:
            asteroide.desenhar(tela)

        for projetil in projeteis:
            projetil.desenhar(tela)

        fonte = pygame.font.Font(None, 36)
        texto_pontuacao = fonte.render(f"Pontos: {pontuacao}", True, BRANCO)
        tela.blit(texto_pontuacao, (10, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    loop_jogo()