import pygame
import math
import random
import os

from scripts.coruja import Coruja
from scripts.estrelas import GerenciadorEstrelas
from scripts.obstaculos import GerenciadorObstaculos
from scripts.interfaces import Texto, Botao

class PartidaCoruja:
    def __init__(self, tela):
        self.tela = tela
        self.coruja = Coruja(tela)
        self.estrelas = GerenciadorEstrelas(tela)
        self.obstaculos = GerenciadorObstaculos(tela)
        self.estado = "jogando"
        
        self.pontuacao = 0
        self.tempo_jogo = 0
        self.velocidade_extra = 0
        self.record = 0
        
        # Interface
        self.texto_pontos = Texto(tela, f"Pontos: {self.pontuacao}", 20, 20, (255, 255, 255), 32)
        self.texto_record = Texto(tela, f"Recorde: {self.record}", 20, 60, (200, 200, 200), 24)
        self.texto_controles = Texto(tela, "← → mover   ESPAÇO voar", 20, 450, (150, 150, 150), 18)
    
    def pular(self):
        self.coruja.pular()
    
    def mover_esquerda(self):
        self.coruja.mover_esquerda()
    
    def mover_direita(self):
        self.coruja.mover_direita()
    
    def parar_movimento(self):
        self.coruja.parar_movimento()
    
    def atualizar(self):
        self.tempo_jogo += 1
        self.velocidade_extra = min(5, self.tempo_jogo // 180)
        
        self.coruja.atualizar()
        self.estrelas.atualizar(self.tempo_jogo)
        self.obstaculos.atualizar(self.tempo_jogo, self.velocidade_extra)
        
        pontos_coletados = self.estrelas.coletar_estrelas(self.coruja.get_rect())
        self.pontuacao += pontos_coletados
        
        if self.pontuacao > self.record:
            self.record = self.pontuacao
        
        self.texto_pontos.atualizar_texto(f"Pontos: {self.pontuacao}")
        self.texto_record.atualizar_texto(f"Recorde: {self.record}")
        
        if self.obstaculos.verificar_colisoes(self.coruja.get_rect()):
            self.estado = "game_over"
        
        self.estrelas.desenhar()
        self.obstaculos.desenhar()
        self.coruja.desenhar()
        self.texto_pontos.desenhar()
        self.texto_record.desenhar()
        self.texto_controles.desenhar()
        
        return self.estado
    
    def reset(self):
        self.coruja = Coruja(self.tela)
        self.estrelas.reset()
        self.obstaculos.reset()
        self.pontuacao = 0
        self.tempo_jogo = 0
        self.velocidade_extra = 0
        self.estado = "jogando"
        self.texto_pontos.atualizar_texto(f"Pontos: {self.pontuacao}")

class MenuPrincipal:
    def __init__(self, tela):
        self.tela = tela
        self.estado = "menu"
        self.LARGURA, self.ALTURA = tela.get_size()
        
        # Interface melhorada
        self.titulo = Texto(tela, "CORUJA NOTURNA", self.LARGURA//2, 80, (255, 255, 255), 64, centralizado=True)
        self.subtitulo = Texto(tela, "Coletora de Estrelas", self.LARGURA//2, 150, (200, 200, 255), 32, centralizado=True)
        
        # Botões centralizados e mais bonitos
        self.botao_jogar = Botao(tela, "VOAR", self.LARGURA//2, 250, 200, 60, (100, 150, 255), (255, 255, 255), centralizado=True)
        self.botao_sair = Botao(tela, "SAIR", self.LARGURA//2, 330, 200, 60, (255, 100, 100), (255, 255, 255), centralizado=True)
        
        # Instruções mais claras
        self.instrucoes1 = Texto(tela, "CLIQUE ou ESPAÇO para voar", self.LARGURA//2, 420, (200, 200, 200), 20, centralizado=True)
        self.instrucoes2 = Texto(tela, "← → para se mover", self.LARGURA//2, 450, (200, 200, 200), 20, centralizado=True)
        
        # Elementos decorativos - AGORA COM IMAGEM ESTÁTICA
        self.coruja_decorativa = CorujaDecorativa(tela)
    
    def atualizar(self):
        # Desenha tudo
        self.titulo.desenhar()
        self.subtitulo.desenhar()
        self.botao_jogar.desenhar()
        self.botao_sair.desenhar()
        self.instrucoes1.desenhar()
        self.instrucoes2.desenhar()
        self.coruja_decorativa.desenhar()
        
        # Verifica cliques nos botões
        if self.botao_jogar.clique():
            self.estado = "jogando"
        
        if self.botao_sair.clique():
            pygame.quit()
            exit()  # Sai do programa completamente
        
        return self.estado

class TelaGameOver:
    def __init__(self, tela, pontuacao, recorde):
        self.tela = tela
        self.estado = "game_over"
        self.pontuacao = pontuacao
        self.recorde = recorde
        self.LARGURA = tela.get_width()
        
        # Interface melhorada
        self.titulo = Texto(tela, "FIM DO VOO!", self.LARGURA//2, 100, (255, 150, 150), 48, centralizado=True)
        self.texto_pontos = Texto(tela, f"Pontuação: {self.pontuacao}", self.LARGURA//2, 180, (255, 255, 255), 32, centralizado=True)
        self.texto_recorde = Texto(tela, f"Recorde: {self.recorde}", self.LARGURA//2, 220, (255, 255, 100), 28, centralizado=True)
        
        # Botões com "SAIR" em vez de "MENU"
        self.botao_reiniciar = Botao(tela, "VOAR NOVAMENTE", self.LARGURA//2, 300, 240, 50, (100, 200, 100), (255, 255, 255), centralizado=True)
        self.botao_sair = Botao(tela, "SAIR", self.LARGURA//2, 370, 100, 50, (255, 100, 100), (255, 255, 255), centralizado=True)
    
    def atualizar(self):
        self.titulo.desenhar()
        self.texto_pontos.desenhar()
        self.texto_recorde.desenhar()
        self.botao_reiniciar.desenhar()
        self.botao_sair.desenhar()
        
        if self.botao_reiniciar.clique():
            self.estado = "jogando"
        
        if self.botao_sair.clique():
            pygame.quit()
            exit()  # Sai do programa completamente
        
        return self.estado

# Classe para a coruja decorativa no menu - AGORA COM IMAGEM ESTÁTICA
class CorujaDecorativa:
    def __init__(self, tela):
        self.tela = tela
        self.largura, self.altura = 80, 60  # Um pouco maior que a do jogo
        self.x = tela.get_width() // 2 - self.largura // 2
        self.y = 350  # Posição fixa
        
        # Tenta carregar a imagem da coruja
        self.tem_imagem = False
        try:
            caminhos = [
                'assets/sprites/coruja.png',
                'assets/sprites/coruja.PNG',
                'assets/sprites/coruja.jpg',
                './assets/sprites/coruja.png'
            ]
            
            for caminho in caminhos:
                if os.path.exists(caminho):
                    self.imagem = pygame.image.load(caminho)
                    self.imagem = pygame.transform.scale(self.imagem, (self.largura, self.altura))
                    self.tem_imagem = True
                    print("✅ Imagem da coruja decorativa carregada!")
                    break
        except Exception as e:
            print(f"⚠️  Erro ao carregar coruja decorativa: {e}")
            self.tem_imagem = False
        
        # Fallback caso a imagem não carregue
        self.cor_corpo = (200, 160, 60)
        self.cor_olhos = (0, 0, 0)
        self.cor_bico = (255, 200, 0)
    
    def atualizar(self):
        # Agora é estática - não faz nada
        pass
    
    def desenhar(self):
        if self.tem_imagem:
            # Usa a imagem PNG da coruja
            self.tela.blit(self.imagem, (self.x, self.y))
        else:
            # Fallback: desenha coruja com formas (estática)
            corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)
            pygame.draw.ellipse(self.tela, self.cor_corpo, corpo)
            
            # Olhos
            olho_esq = pygame.Rect(self.x + 15, self.y + 15, 20, 20)
            olho_dir = pygame.Rect(self.x + 45, self.y + 15, 20, 20)
            pygame.draw.ellipse(self.tela, self.cor_olhos, olho_esq)
            pygame.draw.ellipse(self.tela, self.cor_olhos, olho_dir)
            
            # Bico
            bico = [
                (self.x + 40, self.y + 45), 
                (self.x + 35, self.y + 55),
                (self.x + 45, self.y + 55)
            ]
            pygame.draw.polygon(self.tela, self.cor_bico, bico)