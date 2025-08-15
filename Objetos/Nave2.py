# nave.py
import pygame

from Objetos.Projetil import Projetil


class Nave2:
    def __init__(self, largura_tela, altura_tela, **kwargs):
        self.largura = 50
        self.altura = 50

        # self.cor agora pega o valor de 'cor' nos kwargs, ou usa BRANCO como padrão
        self.cor = kwargs.get('cor', (255, 255, 255))
        self.rect = pygame.Rect(0, 0, self.largura, self.altura)
        self.rect.centerx = largura_tela // 2
        self.rect.bottom = altura_tela - 10

        # self.velocidade agora pega o valor de 'velocidade' nos kwargs, ou usa 5 como padrão
        self.velocidade = kwargs.get('velocidade', 5)
        self.largura_tela = largura_tela

    def mover(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < self.largura_tela:
            self.rect.x += self.velocidade

    def atirar(self, cor_projetil):
        return Projetil(self.rect.centerx, self.rect.top, cor_projetil)

    def desenhar(self, superficie):
        pontos_triangulo = [
            (self.rect.centerx, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom)
        ]
        pygame.draw.polygon(superficie, self.cor, pontos_triangulo)