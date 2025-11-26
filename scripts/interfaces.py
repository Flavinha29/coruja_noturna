import pygame
import math

class Texto:
    def __init__(self, tela, texto, x, y, cor, tamanho=30, centralizado=False):
        self.tela = tela
        self.texto = texto
        self.x = x
        self.y = y
        self.cor = cor
        self.tamanho = tamanho
        self.centralizado = centralizado
        self.fonte = pygame.font.SysFont('Arial', self.tamanho, bold=True)
        self.atualizar_texto(texto)
    
    def atualizar_texto(self, novo_texto):
        self.texto = novo_texto
        self.superficie = self.fonte.render(self.texto, True, self.cor)
    
    def desenhar(self):
        if self.centralizado:
            rect = self.superficie.get_rect(center=(self.x, self.y))
            self.tela.blit(self.superficie, rect)
        else:
            self.tela.blit(self.superficie, (self.x, self.y))

class Botao:
    def __init__(self, tela, texto, x, y, largura, altura, cor_fundo, cor_texto, centralizado=False):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        
        if centralizado:
            self.x = x - largura // 2
            self.y = y - altura // 2
        else:
            self.x = x
            self.y = y
            
        self.texto = Texto(tela, texto, self.x + largura//2, self.y + altura//2, cor_texto, 24, centralizado=True)
        self.rect = pygame.Rect(self.x, self.y, largura, altura)
        self.cor_fundo = cor_fundo
        self.cor_texto = cor_texto
        self.cor_borda = (min(255, cor_fundo[0] + 50), min(255, cor_fundo[1] + 50), min(255, cor_fundo[2] + 50))
    
    def desenhar(self):
        # Fundo do botão com borda
        pygame.draw.rect(self.tela, self.cor_fundo, self.rect, border_radius=10)
        pygame.draw.rect(self.tela, self.cor_borda, self.rect, 3, border_radius=10)
        
        # Efeito de hover (opcional)
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            pygame.draw.rect(self.tela, (255, 255, 255, 50), self.rect, border_radius=10)
        
        self.texto.desenhar()
    
    def clique(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            return True
        return False