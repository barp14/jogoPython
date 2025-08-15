import pygame
import random

class Asteroide:
    # Recebe as dimensões e a cor como parâmetros
    def __init__(self, largura_tela, altura_tela, cor):
        self.raio = 20
        self.cor = cor
        self.rect = pygame.Rect(0, 0, self.raio * 2, self.raio * 2)
        self.rect.x = random.randrange(largura_tela - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidade = random.randrange(1, 8)

    def mover(self):
        self.rect.y += self.velocidade

    def desenhar(self, superficie):
        # A superfície (tela) é passada como parâmetro
        pygame.draw.circle(superficie, self.cor, self.rect.center, self.raio)