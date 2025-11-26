import pygame
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

# ... (MenuPrincipal e TelaGameOver permanecem iguais)

class MenuPrincipal:
    def __init__(self, tela):
        self.tela = tela
        self.estado = "menu"
        
        # Interface
        self.titulo = Texto(tela, "CORUJA NOTURNA", 150, 100, (255, 255, 255), 48)
        self.subtitulo = Texto(tela, "Coletora de Estrelas", 200, 160, (200, 200, 255), 24)
        self.botao_jogar = Botao(tela, "VOAR", 250, 250, 100, 50, (100, 100, 200), (255, 255, 255))
        self.instrucoes = Texto(tela, "CLIQUE para a coruja voar!", 180, 350, (200, 200, 200), 20)
    
    def atualizar(self):
        self.titulo.desenhar()
        self.subtitulo.desenhar()
        self.botao_jogar.desenhar()
        self.instrucoes.desenhar()
        
        if self.botao_jogar.clique():
            self.estado = "jogando"
        
        return self.estado

class TelaGameOver:
    def __init__(self, tela, pontuacao, recorde):
        self.tela = tela
        self.estado = "game_over"
        self.pontuacao = pontuacao
        self.recorde = recorde
        
        # Interface
        self.titulo = Texto(tela, "FIM DO VOO!", 220, 100, (255, 100, 100), 48)
        self.texto_pontos = Texto(tela, f"Pontuação: {self.pontuacao}", 230, 180, (255, 255, 255), 32)
        self.texto_recorde = Texto(tela, f"Recorde: {self.recorde}", 250, 220, (255, 255, 100), 28)
        self.botao_reiniciar = Botao(tela, "VOAR NOVAMENTE", 200, 300, 200, 50, (100, 200, 100), (255, 255, 255))
        self.botao_menu = Botao(tela, "MENU", 250, 370, 100, 50, (200, 100, 100), (255, 255, 255))
    
    def atualizar(self):
        self.titulo.desenhar()
        self.texto_pontos.desenhar()
        self.texto_recorde.desenhar()
        self.botao_reiniciar.desenhar()
        self.botao_menu.desenhar()
        
        if self.botao_reiniciar.clique():
            self.estado = "jogando"
        elif self.botao_menu.clique():
            self.estado = "menu"
        
        return self.estado