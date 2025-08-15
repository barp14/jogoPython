import pygame
import random
import os

from Objetos.Asteroide import Asteroide
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
VERDE = (0, 255, 0)

clock = pygame.time.Clock()

# Exceção personalizada para quando o placar estiver vazio
class PlacarVazioError(Exception):
    """Exceção levantada quando não há registros de pontuação."""
    pass

# Funções para tratamento de arquivo de pontuações
def salvar_pontuacao(nome, pontuacao):
    try:
        with open("placar.txt", "a") as arquivo:
            arquivo.write(f"{nome}: {pontuacao}\n")
    except IOError as e:
        print(f"Erro ao salvar a pontuação: {e}")

def carregar_placar():
    try:
        if not os.path.exists("placar.txt"):
            raise PlacarVazioError("O arquivo de placar ainda não existe.")
            
        with open("placar.txt", "r") as arquivo:
            linhas = arquivo.readlines()
            
        if not linhas:
            raise PlacarVazioError("O placar está vazio.")
            
        placar = []
        for linha in linhas:
            try:
                nome, pontos = linha.strip().split(": ")
                placar.append((nome, int(pontos)))
            except ValueError:
                print(f"Formato inválido na linha: {linha}")
                
        return placar
    except PlacarVazioError as e:
        print(f"Aviso: {e}")
        return []
    except IOError as e:
        print(f"Erro ao ler o arquivo de placar: {e}")
        return []

# Função para tela de entrada de nome
def tela_entrada_nome(pontuacao):
    nome = ""
    entrada_ativa = True
    
    while entrada_ativa:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome.strip():
                    entrada_ativa = False
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                elif len(nome) < 15 and evento.unicode.isprintable():  # Limita o nome a 15 caracteres
                    nome += evento.unicode
        
        tela.fill(PRETO)
        
        # Texto de Game Over
        fonte_grande = pygame.font.Font(None, 72)
        texto_game_over = fonte_grande.render("Game Over", True, VERMELHO)
        tela.blit(texto_game_over, (LARGURA_TELA//2 - texto_game_over.get_width()//2, 100))
        
        # Exibe pontuação
        fonte = pygame.font.Font(None, 36)
        texto_pontuacao = fonte.render(f"Sua pontuação: {pontuacao}", True, BRANCO)
        tela.blit(texto_pontuacao, (LARGURA_TELA//2 - texto_pontuacao.get_width()//2, 200))
        
        # Entrada do nome
        texto_instrucao = fonte.render("Digite seu nome:", True, BRANCO)
        tela.blit(texto_instrucao, (LARGURA_TELA//2 - texto_instrucao.get_width()//2, 250))
        
        # Caixa de texto
        retangulo_entrada = pygame.Rect(LARGURA_TELA//2 - 150, 300, 300, 40)
        pygame.draw.rect(tela, BRANCO, retangulo_entrada, 2)
        
        # Texto digitado
        texto_entrada = fonte.render(nome, True, BRANCO)
        tela.blit(texto_entrada, (retangulo_entrada.x + 10, retangulo_entrada.y + 10))
        
        # Botão para confirmar
        cor_botao = VERDE if nome.strip() else (100, 100, 100)
        botao_confirmar = pygame.Rect(LARGURA_TELA//2 - 100, 370, 200, 40)
        pygame.draw.rect(tela, cor_botao, botao_confirmar)
        texto_confirmar = fonte.render("Confirmar", True, PRETO)
        tela.blit(texto_confirmar, (botao_confirmar.x + botao_confirmar.width//2 - texto_confirmar.get_width()//2, 
                                   botao_confirmar.y + botao_confirmar.height//2 - texto_confirmar.get_height()//2))
        
        # Verificar clique no botão
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and botao_confirmar.collidepoint(mouse_pos) and nome.strip():
            entrada_ativa = False
            
        pygame.display.flip()
        clock.tick(30)
    
    return nome

# Função para exibir placar
def exibir_placar():
    try:
        placar = carregar_placar()
        placar_ativo = True
        
        while placar_ativo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        placar_ativo = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    placar_ativo = False
            
            tela.fill(PRETO)
            
            # Título do placar
            fonte_grande = pygame.font.Font(None, 48)
            texto_placar = fonte_grande.render("Placar de Pontuações", True, BRANCO)
            tela.blit(texto_placar, (LARGURA_TELA//2 - texto_placar.get_width()//2, 50))
            
            # Lista de pontuações
            fonte = pygame.font.Font(None, 36)
            y_pos = 150
            
            if not placar:
                texto_vazio = fonte.render("Nenhuma pontuação registrada ainda.", True, BRANCO)
                tela.blit(texto_vazio, (LARGURA_TELA//2 - texto_vazio.get_width()//2, y_pos))
            else:
                # Ordenar placar por pontuação (decrescente)
                placar_ordenado = sorted(placar, key=lambda x: x[1], reverse=True)
                
                for i, (nome, pontos) in enumerate(placar_ordenado[:10]):  # Exibe apenas os top 10
                    texto_entrada = fonte.render(f"{i+1}. {nome}: {pontos}", True, BRANCO)
                    tela.blit(texto_entrada, (LARGURA_TELA//2 - texto_entrada.get_width()//2, y_pos))
                    y_pos += 40
            
            # Instruções para voltar
            texto_voltar = fonte.render("Clique ou pressione ESC para voltar", True, (150, 150, 150))
            tela.blit(texto_voltar, (LARGURA_TELA//2 - texto_voltar.get_width()//2, ALTURA_TELA - 50))
            
            pygame.display.flip()
            clock.tick(30)
    
    except Exception as e:
        print(f"Erro ao exibir placar: {e}")

# 2. Lógica do Jogo Principal
# ======================================================================================================================

def loop_jogo():
    """Função principal do jogo."""

    # Criando uma nave personalizada usando **kwargs
    nave2 = Nave2(LARGURA_TELA, ALTURA_TELA, cor=(0, 0, 255), velocidade=10)  # Uma nave azul e rápida!

    asteroides = []
    projeteis = []

    pontuacao = 0
    rodando = True
    game_over = False

    # Mostrar placar no início
    try:
        exibir_placar()
    except PlacarVazioError:
        pass  # Ignora se o placar estiver vazio

    while rodando:
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not game_over:
                    projeteis.append(nave2.atirar(VERMELHO))

        if not game_over:
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
                    game_over = True
                    break

            for projetil in projeteis[:]:
                for asteroide in asteroides[:]:
                    if projetil.rect.colliderect(asteroide.rect):
                        if projetil in projeteis:
                            projeteis.remove(projetil)
                        if asteroide in asteroides:
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

        if game_over:
            # Tela de Game Over
            nome = tela_entrada_nome(pontuacao)
            if nome:
                salvar_pontuacao(nome, pontuacao)
                exibir_placar()
            rodando = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    loop_jogo()