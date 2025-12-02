import pygame
import os

class Coruja:
    def __init__(self, tela):
        self.tela = tela
        self.largura, self.altura = 60, 40
        self.x = tela.get_width() // 2 - self.largura // 2  # Centralizada horizontalmente
        self.y = tela.get_height() -self.altura - 10 # POSIÇÃO INFERIOR (100 pixels do fundo)
        self.velocidade_x = 0
        self.velocidade_lateral = 5
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        
        # Tenta carregar a imagem da coruja
        try:
            caminhos_tentados = [
                os.path.join('assets', 'sprites', 'coruja.png'),
                'assets/sprites/coruja.png',
                './assets/sprites/coruja.png'
            ]
            
            for caminho in caminhos_tentados:
                try:
                    print(f"Tentando carregar: {caminho}")
                    self.imagem = pygame.image.load(caminho)
                    self.imagem = pygame.transform.scale(self.imagem, (self.largura, self.altura))
                    self.tem_imagem = True
                    print("✅ Imagem da coruja carregada!")
                    break
                except:
                    continue
            else:
                raise FileNotFoundError("Imagem não encontrada")
                
        except Exception as e:
            print(f"❌ Erro ao carregar imagem: {e}")
            self.tem_imagem = False
            self.cor_corpo = (200, 160, 60)
    
    def mover_esquerda(self):
        self.velocidade_x = -self.velocidade_lateral
    
    def mover_direita(self):
        self.velocidade_x = self.velocidade_lateral
    
    def parar_movimento(self):
        self.velocidade_x = 0
    
    def atualizar(self):
        # Apenas movimento lateral
        self.x += self.velocidade_x
        
        # Limites horizontais
        if self.x < 0: 
            self.x = 0
        if self.x > self.tela.get_width() - self.largura: 
            self.x = self.tela.get_width() - self.largura
        
        # Posição Y permanece fixa na parte inferior
        # Não precisa de limites verticais
        
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
    
    def desenhar(self):
        if self.tem_imagem:
            self.tela.blit(self.imagem, (self.x, self.y))
        else:
            pygame.draw.ellipse(self.tela, self.cor_corpo, self.rect)
    
    def get_rect(self):
        return self.rect