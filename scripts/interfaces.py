import pygame

class Texto:
    def __init__(self, tela, texto, x, y, cor, tamanho=30):
        self.tela = tela
        self.texto = texto
        self.x = x
        self.y = y
        self.cor = cor
        self.tamanho = tamanho
        self.fonte = pygame.font.SysFont('Arial', self.tamanho, bold=True)
        self.atualizar_texto(texto)
    
    def atualizar_texto(self, novo_texto):
        self.texto = novo_texto
        self.superficie = self.fonte.render(self.texto, True, self.cor)
    
    def desenhar(self):
        self.tela.blit(self.superficie, (self.x, self.y))

class Botao:
    def __init__(self, tela, texto, x, y, largura, altura, cor_fundo, cor_texto):
        self.tela = tela
        self.texto = Texto(tela, texto, x + 10, y + 10, cor_texto, 24)
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_fundo = cor_fundo
        self.cor_texto = cor_texto
    
    def desenhar(self):
        pygame.draw.rect(self.tela, self.cor_fundo, self.rect)
        pygame.draw.rect(self.tela, self.cor_texto, self.rect, 2)
        self.texto.desenhar()
    
    def clique(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            return True
        return False