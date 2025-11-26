import pygame
import sys
from scripts.cenas import PartidaCoruja, MenuPrincipal, TelaGameOver

class JogoCoruja:
    def __init__(self):
        pygame.init()
        
        # Configurações da tela
        self.LARGURA, self.ALTURA = 600, 500
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption("Coruja Noturna Coletora")
        
        self.relogio = pygame.time.Clock()
        self.cena_atual = "menu"
        
        # Inicializa cenas
        self.menu = MenuPrincipal(self.tela)
        self.partida = PartidaCoruja(self.tela)
        self.game_over = None
        
        # Cores do cenário
        self.cor_ceu = (25, 25, 50)
        self.cor_estrelas_fundo = []
        self.inicializar_estrelas_fundo()
    
    def inicializar_estrelas_fundo(self):
        for _ in range(50):
            x = pygame.time.get_ticks() % self.LARGURA
            y = pygame.time.get_ticks() % self.ALTURA
            brilho = pygame.time.get_ticks() % 155 + 100
            self.cor_estrelas_fundo.append((x, y, brilho))
    
    def desenhar_fundo(self):
        self.tela.fill(self.cor_ceu)
        tempo = pygame.time.get_ticks() // 500
        for i, (x, y, brilho_base) in enumerate(self.cor_estrelas_fundo):
            brilho = brilho_base + (tempo + i) % 56
            brilho = max(100, min(255, brilho))
            cor_estrela = (brilho, brilho, brilho)
            pygame.draw.circle(self.tela, cor_estrela, (x, y), 1)
    
    def executar(self):
        executando = True
        
        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.cena_atual == "jogando":
                        self.partida.pular()
                elif evento.type == pygame.KEYDOWN:
                    if self.cena_atual == "jogando":
                        if evento.key == pygame.K_SPACE:
                            self.partida.pular()
                        elif evento.key == pygame.K_LEFT:
                            self.partida.mover_esquerda()
                        elif evento.key == pygame.K_RIGHT:
                            self.partida.mover_direita()
                elif evento.type == pygame.KEYUP:
                    if self.cena_atual == "jogando":
                        if evento.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                            self.partida.parar_movimento()
                    elif evento.key == pygame.K_ESCAPE:
                        if self.cena_atual == "jogando":
                            self.cena_atual = "menu"
            
            # Desenha o fundo
            self.desenhar_fundo()
            
            # Gerencia as cenas
            if self.cena_atual == "menu":
                self.cena_atual = self.menu.atualizar()
            
            elif self.cena_atual == "jogando":
                self.cena_atual = self.partida.atualizar()
                
                if self.cena_atual == "game_over":
                    self.game_over = TelaGameOver(self.tela, self.partida.pontuacao, self.partida.record)
            
            elif self.cena_atual == "game_over":
                self.cena_atual = self.game_over.atualizar()
                
                if self.cena_atual == "jogando":
                    self.partida.reset()
            
            pygame.display.flip()
            self.relogio.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jogo = JogoCoruja()
    jogo.executar()