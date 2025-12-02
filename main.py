import pygame
import sys
import math
import random
from scripts.cenas import PartidaCoruja, MenuPrincipal, TelaGameOver
from scripts.game_manager import GerenciadorProgresso

class JogoCoruja:
    def __init__(self):
        pygame.init()
        
        # Configurações da tela
        self.LARGURA, self.ALTURA = 600, 500
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption("Coruja Noturna Coletora - Com Fases!")
        
        self.relogio = pygame.time.Clock()
        self.cena_atual = "menu"
        
        # Inicializa gerenciador de progresso
        self.gerenciador = GerenciadorProgresso()
        
        # Inicializa cenas - passa o gerenciador
        self.menu = MenuPrincipal(self.tela, self.gerenciador)
        self.partida = PartidaCoruja(self.tela, self.gerenciador)
        self.game_over = None
        
        # Cores do cenário - mais bonitas
        self.cor_ceu = (10, 15, 40)
        self.cor_estrelas_fundo = []
        self.inicializar_estrelas_fundo()
    
    def inicializar_estrelas_fundo(self):
        for _ in range(100):
            x = random.randint(0, self.LARGURA)
            y = random.randint(0, self.ALTURA)
            tamanho = random.choice([1, 1, 1, 2])
            brilho = random.randint(100, 255)
            velocidade = random.uniform(0.1, 0.5)
            self.cor_estrelas_fundo.append({
                'x': x, 'y': y, 'tamanho': tamanho, 
                'brilho': brilho, 'velocidade': velocidade
            })
    
    def desenhar_fundo(self):
        for y in range(self.ALTURA):
            cor = (
                self.cor_ceu[0] + int(y * 0.05),
                self.cor_ceu[1] + int(y * 0.05), 
                self.cor_ceu[2] + int(y * 0.1)
            )
            pygame.draw.line(self.tela, cor, (0, y), (self.LARGURA, y))
        
        tempo = pygame.time.get_ticks() / 1000
        for estrela in self.cor_estrelas_fundo:
            brilho = estrela['brilho'] + math.sin(tempo * estrela['velocidade']) * 50
            brilho = max(50, min(255, brilho))
            cor_estrela = (brilho, brilho, brilho)
            
            pygame.draw.circle(self.tela, cor_estrela, 
                             (estrela['x'], estrela['y']), estrela['tamanho'])
    
    def executar(self):
        executando = True
        
        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False
                
                elif evento.type == pygame.KEYDOWN:
                    if self.cena_atual == "jogando":
                        if evento.key == pygame.K_LEFT:
                            self.partida.mover_esquerda()
                        elif evento.key == pygame.K_RIGHT:
                            self.partida.mover_direita()
                    elif evento.key == pygame.K_ESCAPE:
                        if self.cena_atual == "jogando":
                            self.cena_atual = "menu"
                
                # ADICIONADO DE VOLTA: evento KEYUP para parar movimento
                elif evento.type == pygame.KEYUP:
                    if self.cena_atual == "jogando":
                        if evento.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                            self.partida.parar_movimento()
            
            # Desenha o fundo
            self.desenhar_fundo()
            
            # Gerencia as cenas
            if self.cena_atual == "menu":
                self.cena_atual = self.menu.atualizar()
            
            elif self.cena_atual == "jogando":
                self.cena_atual = self.partida.atualizar()
                
                if self.cena_atual == "game_over":
                    self.game_over = TelaGameOver(
                        self.tela, 
                        self.partida.pontuacao, 
                        self.gerenciador.recorde_geral,
                        self.partida.fase_sistema.fase_atual
                    )
            
            elif self.cena_atual == "game_over":
                self.cena_atual = self.game_over.atualizar()
                
                if self.cena_atual == "jogando":
                    # O próprio reset() da PartidaCoruja já volta para fase 1
                    self.partida.reset()
            
            pygame.display.flip()
            self.relogio.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jogo = JogoCoruja()
    jogo.executar()