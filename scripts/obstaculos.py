import pygame
import random
import os
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
        self.velocidade_base = 3  # NOVO: velocidade base ajustável
        
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
        if tempo_jogo - self.tempo_ultimo_obstaculo > self.intervalo_obstaculos:
            self.adicionar_obstaculo()
            self.tempo_ultimo_obstaculo = tempo_jogo
        
        # Usa velocidade base + extra
        velocidade = self.velocidade_base + velocidade_extra
        
        for obstaculo in self.obstaculos[:]:
            obstaculo['y'] += velocidade
            if obstaculo['y'] > self.tela.get_height():
                self.obstaculos.remove(obstaculo)
    
    # O resto do código permanece igual...
    # [manter o resto do código original]
    
    def adicionar_obstaculo(self):
        """Adiciona um novo obstáculo baseado nas probabilidades"""
        if not self.tipos_obstaculos or not self.probabilidades:
            return
        
        # Escolhe o tipo de obstáculo baseado nas probabilidades
        tipo = random.choices(self.tipos_obstaculos, self.probabilidades)[0]
        
        # Posição horizontal aleatória
        x = random.randint(50, self.tela.get_width() - 100)
        y = -100  # Começa fora da tela (em cima)
        
        # Tamanhos dos obstáculos
        tamanhos = {
            'galho': (90, 25),    # Galho: comprido e fino
            'nuvem': (140, 50),   # Nuvem: larga e baixa
            'lua': (70, 70)       # Lua: grande e redonda
        }
        
        largura, altura = tamanhos[tipo]
        
        # Cria o obstáculo
        novo_obstaculo = {
            'x': x, 
            'y': y, 
            'tipo': tipo,
            'largura': largura, 
            'altura': altura,
            'rect': pygame.Rect(x, y, largura, altura)
        }
        
        self.obstaculos.append(novo_obstaculo)
        
        # Debug: mostrar que obstáculo foi criado
        # print(f"➕ Obstáculo criado: {tipo} em ({x}, {y})")
    
    def desenhar(self):
        """Desenha todos os obstáculos na tela"""
        for obstaculo in self.obstaculos:
            # Atualiza o retângulo de colisão
            obstaculo['rect'] = pygame.Rect(
                obstaculo['x'], 
                obstaculo['y'], 
                obstaculo['largura'], 
                obstaculo['altura']
            )
            
            # Tenta usar imagem PNG
            if obstaculo['tipo'] in self.imagens and self.imagens[obstaculo['tipo']]:
                imagem = pygame.transform.scale(
                    self.imagens[obstaculo['tipo']], 
                    (obstaculo['largura'], obstaculo['altura'])
                )
                self.tela.blit(imagem, (obstaculo['x'], obstaculo['y']))
            else:
                # Fallback com cores
                cores = {
                    'galho': (139, 69, 19),    # Marrom
                    'nuvem': (200, 200, 200),  # Cinza claro
                    'lua': (220, 220, 220)     # Cinza mais claro
                }
                cor = cores[obstaculo['tipo']]
                
                if obstaculo['tipo'] == 'galho':
                    # Desenha galho como retângulo
                    pygame.draw.rect(self.tela, cor, obstaculo['rect'])
                    # Adiciona detalhes ao galho
                    pygame.draw.rect(self.tela, (101, 67, 33), 
                                   (obstaculo['x'] + 5, obstaculo['y'] + 5, 
                                    obstaculo['largura'] - 10, obstaculo['altura'] - 10))
                elif obstaculo['tipo'] == 'nuvem':
                    # Desenha nuvem como elipse
                    pygame.draw.ellipse(self.tela, cor, obstaculo['rect'])
                else:  # lua
                    # Desenha lua como círculo
                    pygame.draw.circle(self.tela, cor, 
                                     (obstaculo['x'] + 35, obstaculo['y'] + 35), 35)
    
    def verificar_colisoes(self, rect_coruja):
        """Verifica colisões entre a coruja e qualquer obstáculo"""
        for obstaculo in self.obstaculos:
            if rect_coruja.colliderect(obstaculo['rect']):
                return True
        return False
    
    def reset(self):
        """Reseta todos os obstáculos"""
        self.obstaculos = []
        self.tempo_ultimo_obstaculo = 0