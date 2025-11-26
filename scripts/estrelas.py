import pygame
import random
import os

class GerenciadorEstrelas:
    def __init__(self, tela):
        self.tela = tela
        self.estrelas = []
        self.tempo_ultima_estrela = 0
        self.intervalo_estrelas = 60
        
        # Tenta carregar imagens
        self.imagem_estrela = None
        self.imagem_estrela_dourada = None
        
        try:
            # Estrela normal
            caminhos = ['assets/sprites/estrela.png', './assets/sprites/estrela.png']
            for caminho in caminhos:
                try:
                    self.imagem_estrela = pygame.image.load(caminho)
                    self.imagem_estrela = pygame.transform.scale(self.imagem_estrela, (30, 30))
                    print("✅ Estrela normal carregada!")
                    break
                except:
                    continue
            
            # Estrela dourada
            caminhos = ['assets/sprites/estrela_dourada.png', './assets/sprites/estrela_dourada.png']
            for caminho in caminhos:
                try:
                    self.imagem_estrela_dourada = pygame.image.load(caminho)
                    self.imagem_estrela_dourada = pygame.transform.scale(self.imagem_estrela_dourada, (30, 30))
                    print("✅ Estrela dourada carregada!")
                    break
                except:
                    continue
                    
        except Exception as e:
            print(f"❌ Erro ao carregar estrelas: {e}")
    
    def atualizar(self, tempo_jogo):
        if tempo_jogo - self.tempo_ultima_estrela > self.intervalo_estrelas:
            self.adicionar_estrela()
            self.tempo_ultima_estrela = tempo_jogo
        
        for estrela in self.estrelas[:]:
            estrela['y'] += 3
            if estrela['y'] > self.tela.get_height():
                self.estrelas.remove(estrela)
    
    def adicionar_estrela(self):
        x = random.randint(50, self.tela.get_width() - 50)
        y = -20
        tipo = random.choices(['normal', 'dourada'], weights=[0.8, 0.2])[0]
        
        self.estrelas.append({
            'x': x, 'y': y, 'tipo': tipo,
            'rect': pygame.Rect(x, y, 30, 30)
        })
    
    def desenhar(self):
        for estrela in self.estrelas:
            estrela['rect'] = pygame.Rect(estrela['x'], estrela['y'], 30, 30)
            
            if estrela['tipo'] == 'normal' and self.imagem_estrela:
                self.tela.blit(self.imagem_estrela, (estrela['x'], estrela['y']))
            elif estrela['tipo'] == 'dourada' and self.imagem_estrela_dourada:
                self.tela.blit(self.imagem_estrela_dourada, (estrela['x'], estrela['y']))
            else:
                # Fallback
                cor = (255, 255, 255) if estrela['tipo'] == 'normal' else (255, 215, 0)
                pygame.draw.circle(self.tela, cor, (estrela['x'] + 15, estrela['y'] + 15), 15)
    
    def coletar_estrelas(self, rect_coruja):
        pontos = 0
        for estrela in self.estrelas[:]:
            if rect_coruja.colliderect(estrela['rect']):
                self.estrelas.remove(estrela)
                pontos += 10 if estrela['tipo'] == 'normal' else 50
        return pontos
    
    def reset(self):
        self.estrelas = []
        self.tempo_ultima_estrela = 0