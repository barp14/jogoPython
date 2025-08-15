import pygame

class Projetil:
    def __init__(self, x, y, cor):
        self.largura = 5
        self.altura = 10
        self.cor = cor
        self.rect = pygame.Rect(x - self.largura // 2, y, self.largura, self.altura)
        self.velocidade = -10

    def mover(self):
        self.rect.y += self.velocidade

    def desenhar(self, superficie):
        # A superfície (tela) é passada como parâmetro
        pygame.draw.rect(superficie, self.cor, self.rect)