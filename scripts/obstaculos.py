import pygame
import random
import os

class GerenciadorObstaculos:
    def __init__(self, tela):
        self.tela = tela
        self.obstaculos = []
        self.tipos_obstaculos = ['galho', 'nuvem', 'lua']
        self.probabilidades = [0.6, 0.3, 0.1]
        self.tempo_ultimo_obstaculo = 0
        self.intervalo_obstaculos = 90
        
        # Tenta carregar imagens
        self.imagens = {}
        try:
            sprites = {
                'galho': 'assets/sprites/galho.png',
                'nuvem': 'assets/sprites/nuvem.png', 
                'lua': 'assets/sprites/lua.png'
            }
            
            for nome, caminho in sprites.items():
                try:
                    self.imagens[nome] = pygame.image.load(caminho)
                    print(f"✅ {nome} carregado!")
                except Exception as e:
                    print(f"❌ Erro ao carregar {nome}: {e}")
                    self.imagens[nome] = None
                    
        except Exception as e:
            print(f"Erro geral: {e}")
    
    def atualizar(self, tempo_jogo, velocidade_extra=0):
        intervalo = max(30, self.intervalo_obstaculos - (tempo_jogo // 180))
        
        if tempo_jogo - self.tempo_ultimo_obstaculo > intervalo:
            self.adicionar_obstaculo()
            self.tempo_ultimo_obstaculo = tempo_jogo
        
        velocidade = 3 + velocidade_extra
        for obstaculo in self.obstaculos[:]:
            obstaculo['y'] += velocidade
            if obstaculo['y'] > self.tela.get_height():
                self.obstaculos.remove(obstaculo)
    
    def adicionar_obstaculo(self):
        tipo = random.choices(self.tipos_obstaculos, self.probabilidades)[0]
        x = random.randint(50, self.tela.get_width() - 100)
        y = -100
        
        tamanhos = {
            'galho': (80, 20),
            'nuvem': (120, 40), 
            'lua': (60, 60)
        }
        
        largura, altura = tamanhos[tipo]
        
        self.obstaculos.append({
            'x': x, 'y': y, 'tipo': tipo,
            'largura': largura, 'altura': altura,
            'rect': pygame.Rect(x, y, largura, altura)
        })
    
    def desenhar(self):
        for obstaculo in self.obstaculos:
            obstaculo['rect'] = pygame.Rect(obstaculo['x'], obstaculo['y'], 
                                          obstaculo['largura'], obstaculo['altura'])
            
            if obstaculo['tipo'] in self.imagens and self.imagens[obstaculo['tipo']]:
                # Usa imagem PNG
                imagem = pygame.transform.scale(
                    self.imagens[obstaculo['tipo']], 
                    (obstaculo['largura'], obstaculo['altura'])
                )
                self.tela.blit(imagem, (obstaculo['x'], obstaculo['y']))
            else:
                # Fallback com cores
                cores = {
                    'galho': (139, 69, 19),
                    'nuvem': (200, 200, 200),
                    'lua': (220, 220, 220)
                }
                cor = cores[obstaculo['tipo']]
                
                if obstaculo['tipo'] == 'galho':
                    pygame.draw.rect(self.tela, cor, obstaculo['rect'])
                elif obstaculo['tipo'] == 'nuvem':
                    pygame.draw.ellipse(self.tela, cor, obstaculo['rect'])
                else:  # lua
                    pygame.draw.circle(self.tela, cor, 
                                     (obstaculo['x'] + 30, obstaculo['y'] + 30), 30)
    
    def verificar_colisoes(self, rect_coruja):
        for obstaculo in self.obstaculos:
            if rect_coruja.colliderect(obstaculo['rect']):
                return True
        return False
    
    def reset(self):
        self.obstaculos = []
        self.tempo_ultimo_obstaculo = 0