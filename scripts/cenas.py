import pygame
import math
import random
import os

from scripts.coruja import Coruja
from scripts.estrelas import GerenciadorEstrelas
from scripts.obstaculos import GerenciadorObstaculos
from scripts.interfaces import Texto, Botao
from scripts.fase_system import SistemaFases
from scripts.game_manager import GerenciadorProgresso

class PartidaCoruja:
    def __init__(self, tela, gerenciador):
        self.tela = tela
        self.gerenciador = gerenciador
        
        # Sistema de fases - SEMPRE começa na fase 1
        self.fase_sistema = SistemaFases()
        self.fase_sistema.fase_atual = 1
        self.fase_sistema.config = self.fase_sistema.fases[1]
        
        self.coruja = Coruja(tela)
        self.estrelas = GerenciadorEstrelas(tela)
        self.obstaculos = GerenciadorObstaculos(tela)
        
        # Configurar fase inicial (sempre fase 1)
        self.configurar_fase()
        
        self.estado = "jogando"
        self.pontuacao = 0
        self.tempo_jogo = 0
        self.record = gerenciador.recorde_geral
        
        # Interface - mostra fase atual durante o jogo
        self.texto_pontos = Texto(tela, f"Pontos: {self.pontuacao}", 20, 20, (255, 255, 255), 32)
        self.texto_record = Texto(tela, f"Recorde: {self.record}", 20, 60, (200, 200, 200), 24)
        self.texto_fase = Texto(tela, f"Fase: {self.fase_sistema.fase_atual} - {self.fase_sistema.config['nome']}", 
                               20, 100, (200, 255, 200), 24)
        self.texto_objetivo = Texto(tela, f"Objetivo: {self.fase_sistema.config['objetivo']} pontos", 
                                   20, 130, (255, 255, 200), 20)
        self.texto_controles = Texto(tela, "← → para mover", 20, 450, (150, 150, 150), 18)  # MODIFICADO
    
    # ADICIONE ESTES MÉTODOS DE MOVIMENTO (SEM PULAR):
    def mover_esquerda(self):
        """Move a coruja para esquerda (seta ←)"""
        self.coruja.mover_esquerda()
    
    def mover_direita(self):
        """Move a coruja para direita (seta →)"""
        self.coruja.mover_direita()
    
    def parar_movimento(self):
        """Para o movimento lateral da coruja"""
        self.coruja.parar_movimento()
    
    def configurar_fase(self):
        """Aplica configurações da fase atual"""
        config = self.fase_sistema.config
        
        # Configura estrelas
        self.estrelas.intervalo_estrelas = config["intervalo_estrelas"]
        self.estrelas.prob_estrela_dourada = config["prob_estrela_dourada"]
        
        # Configura obstáculos
        self.obstaculos.velocidade_base = config["velocidade"]
        self.obstaculos.intervalo_obstaculos = config["intervalo_obstaculos"]
        self.obstaculos.tipos_obstaculos = config["obstaculos"]
        
        # Atualiza probabilidades
        prob_map = {
            'galho': config["prob_galho"],
            'nuvem': config["prob_nuvem"],
            'lua': config["prob_lua"]
        }
        
        # Filtra apenas os obstáculos ativos
        tipos_ativos = []
        probabilidades_ativas = []
        
        for tipo, prob in prob_map.items():
            if prob > 0 and tipo in self.obstaculos.tipos_obstaculos:
                tipos_ativos.append(tipo)
                probabilidades_ativas.append(prob)
        
        self.obstaculos.tipos_obstaculos = tipos_ativos
        self.obstaculos.probabilidades = probabilidades_ativas
        
        print(f"🎮 Iniciando Fase {self.fase_sistema.fase_atual}: {config['nome']}")
        print(f"🎯 Objetivo: {config['objetivo']} pontos")
    
    def atualizar(self):
        self.tempo_jogo += 1
        
        self.coruja.atualizar()
        self.estrelas.atualizar(self.tempo_jogo)
        self.obstaculos.atualizar(self.tempo_jogo)
        
        pontos_coletados = self.estrelas.coletar_estrelas(self.coruja.get_rect())
        self.pontuacao += pontos_coletados
        
        # Atualiza recorde geral
        if self.pontuacao > self.record:
            self.record = self.pontuacao
            self.gerenciador.atualizar_recorde(self.pontuacao)
        
        self.texto_pontos.atualizar_texto(f"Pontos: {self.pontuacao}")
        self.texto_record.atualizar_texto(f"Recorde: {self.record}")
        
        # Verifica colisões - SE MORRER
        if self.obstaculos.verificar_colisoes(self.coruja.get_rect()):
            self.estado = "game_over"
            print(f"💥 Game Over na Fase {self.fase_sistema.fase_atual}")
        
        # Verifica se completou a fase - AVANÇA NA MESMA SESSÃO
        if self.fase_sistema.verificar_conclusao(self.pontuacao):
            print(f"✅ Fase {self.fase_sistema.fase_atual} concluída!")
            
            # Atualiza recorde da fase no gerenciador
            self.gerenciador.completar_fase(self.fase_sistema.fase_atual, self.pontuacao)
            
            # Avança para próxima fase automaticamente (apenas nesta sessão)
            if self.fase_sistema.avancar_fase():
                self.configurar_fase()
                print(f"🚀 Avançando para Fase {self.fase_sistema.fase_atual}")
                # Atualiza texto da fase
                config = self.fase_sistema.config
                self.texto_fase.atualizar_texto(f"Fase: {self.fase_sistema.fase_atual} - {config['nome']}")
                self.texto_objetivo.atualizar_texto(f"Objetivo: {config['objetivo']} pontos")
            else:
                print("🏆 Todas as fases completadas nesta sessão!")
        
        # Desenha tudo
        self.estrelas.desenhar()
        self.obstaculos.desenhar()
        self.coruja.desenhar()
        self.texto_pontos.desenhar()
        self.texto_record.desenhar()
        self.texto_fase.desenhar()
        self.texto_objetivo.desenhar()
        self.texto_controles.desenhar()
        
        return self.estado
    
    def reset(self):
        """Reinicia o jogo - SEMPRE volta para a FASE 1"""
        self.gerenciador.resetar_para_fase_1()
        
        # Reseta sistema de fases para fase 1
        self.fase_sistema = SistemaFases()
        self.fase_sistema.fase_atual = 1
        self.fase_sistema.config = self.fase_sistema.fases[1]
        
        # Reseta todos os elementos do jogo
        self.coruja = Coruja(self.tela)
        self.estrelas.reset()
        self.obstaculos.reset()
        self.pontuacao = 0
        self.tempo_jogo = 0
        self.estado = "jogando"
        
        # Reconfigura para fase 1
        self.configurar_fase()
        
        # Atualiza textos
        self.texto_pontos.atualizar_texto(f"Pontos: {self.pontuacao}")
        config = self.fase_sistema.config
        self.texto_fase.atualizar_texto(f"Fase: {self.fase_sistema.fase_atual} - {config['nome']}")
        self.texto_objetivo.atualizar_texto(f"Objetivo: {config['objetivo']} pontos")
        
        print("🔄 Reiniciando jogo na Fase 1")

class MenuPrincipal:
    def __init__(self, tela, gerenciador):
        self.tela = tela
        self.gerenciador = gerenciador
        self.estado = "menu"
        self.LARGURA, self.ALTURA = tela.get_size()
        
        self.titulo = Texto(tela, "CORUJA NOTURNA", self.LARGURA//2, 80, (255, 255, 255), 64, centralizado=True)
        self.subtitulo = Texto(tela, "Coletora de Estrelas", self.LARGURA//2, 150, (200, 200, 255), 32, centralizado=True)
        
        self.texto_recorde = Texto(tela, f"Recorde: {gerenciador.recorde_geral}", 
                                 self.LARGURA//2, 200, (255, 200, 100), 28, centralizado=True)
        
        # Botões
        self.botao_jogar = Botao(tela, "VOAR", self.LARGURA//2, 280, 200, 60, (100, 150, 255), (255, 255, 255), centralizado=True)
        self.botao_resetar = Botao(tela, "RESETAR FASES", self.LARGURA//2, 360, 200, 50, (255, 100, 100), (255, 255, 255), centralizado=True)
        self.botao_sair = Botao(tela, "SAIR", self.LARGURA//2, 420, 200, 50, (150, 150, 150), (255, 255, 255), centralizado=True)
        
        # Instruções atualizadas
        self.instrucoes = Texto(tela, "Use ← → para mover a coruja", 
                               self.LARGURA//2, 470, (150, 150, 150), 18, centralizado=True)
        
        self.coruja_decorativa = CorujaDecorativa(tela)
    
    def atualizar(self):
        self.titulo.desenhar()
        self.subtitulo.desenhar()
        self.texto_recorde.desenhar()
        self.botao_jogar.desenhar()
        self.botao_resetar.desenhar()
        self.botao_sair.desenhar()
        self.instrucoes.desenhar()
        self.coruja_decorativa.desenhar()
        
        if self.botao_jogar.clique():
            self.estado = "jogando"
        
        if self.botao_resetar.clique():
            self.gerenciador.resetar()
            self.texto_recorde.atualizar_texto(f"Recorde: {self.gerenciador.recorde_geral}")
            print("🔄 Progresso resetado!")
        
        if self.botao_sair.clique():
            pygame.quit()
            exit()
        
        return self.estado

class TelaGameOver:
    def __init__(self, tela, pontuacao, recorde, fase_atual):
        self.tela = tela
        self.estado = "game_over"
        self.pontuacao = pontuacao
        self.recorde = recorde
        self.fase_atual = fase_atual
        self.LARGURA = tela.get_width()
        
        self.titulo = Texto(tela, "FIM DO VOO!", self.LARGURA//2, 80, (255, 150, 150), 48, centralizado=True)
        self.texto_pontos = Texto(tela, f"Pontuação: {self.pontuacao}", self.LARGURA//2, 150, (255, 255, 255), 32, centralizado=True)
        self.texto_recorde = Texto(tela, f"Recorde Geral: {self.recorde}", self.LARGURA//2, 190, (255, 255, 100), 28, centralizado=True)
        self.texto_info = Texto(tela, "Próximo voo: Fase 1", self.LARGURA//2, 240, (200, 255, 200), 24, centralizado=True)
        
        self.botao_reiniciar = Botao(tela, "VOAR NOVAMENTE", self.LARGURA//2, 300, 240, 50, (100, 200, 100), (255, 255, 255), centralizado=True)
        self.botao_menu = Botao(tela, "MENU", self.LARGURA//2, 370, 100, 50, (100, 100, 200), (255, 255, 255), centralizado=True)
        self.botao_sair = Botao(tela, "SAIR", self.LARGURA//2, 430, 100, 50, (255, 100, 100), (255, 255, 255), centralizado=True)
    
    def atualizar(self):
        self.titulo.desenhar()
        self.texto_pontos.desenhar()
        self.texto_recorde.desenhar()
        self.texto_info.desenhar()
        self.botao_reiniciar.desenhar()
        self.botao_menu.desenhar()
        self.botao_sair.desenhar()
        
        if self.botao_reiniciar.clique():
            self.estado = "jogando"
        
        if self.botao_menu.clique():
            self.estado = "menu"
        
        if self.botao_sair.clique():
            pygame.quit()
            exit()
        
        return self.estado

class CorujaDecorativa:
    def __init__(self, tela):
        self.tela = tela
        self.largura, self.altura = 80, 60
        self.x = tela.get_width() // 2 - self.largura // 2
        self.y = 500
        
        self.tem_imagem = False
        try:
            caminhos = [
                'assets/sprites/coruja.png',
                'assets/sprites/coruja.PNG',
                './assets/sprites/coruja.png'
            ]
            
            for caminho in caminhos:
                if os.path.exists(caminho):
                    self.imagem = pygame.image.load(caminho)
                    self.imagem = pygame.transform.scale(self.imagem, (self.largura, self.altura))
                    self.tem_imagem = True
                    break
        except:
            self.tem_imagem = False
        
        self.cor_corpo = (200, 160, 60)
        self.cor_olhos = (0, 0, 0)
        self.cor_bico = (255, 200, 0)
    
    def desenhar(self):
        if self.tem_imagem:
            self.tela.blit(self.imagem, (self.x, self.y))
        else:
            corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)
            pygame.draw.ellipse(self.tela, self.cor_corpo, corpo)
            
            olho_esq = pygame.Rect(self.x + 15, self.y + 15, 20, 20)
            olho_dir = pygame.Rect(self.x + 45, self.y + 15, 20, 20)
            pygame.draw.ellipse(self.tela, self.cor_olhos, olho_esq)
            pygame.draw.ellipse(self.tela, self.cor_olhos, olho_dir)
            
            bico = [
                (self.x + 40, self.y + 45), 
                (self.x + 35, self.y + 55),
                (self.x + 45, self.y + 55)
            ]
            pygame.draw.polygon(self.tela, self.cor_bico, bico)