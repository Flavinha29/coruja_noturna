import pygame
import random

class SistemaFases:
    def __init__(self):
        # Configurações das 3 fases progressivas - PROBABILIDADES AJUSTADAS
        self.fases = {
            1: {
                "nome": "Floresta Calma",
                "objetivo": 100,
                "velocidade": 3,
                "intervalo_estrelas": 60,
                "intervalo_obstaculos": 100,  # Aumentado de 90 para 100
                "obstaculos": ["galho"],
                "prob_galho": 1.0,
                "prob_nuvem": 0.0,
                "prob_lua": 0.0,
                "prob_estrela_dourada": 0.0,
                "cor_ceu": (10, 15, 40),
                "descricao": "Apenas galhos para começar!"
            },
            2: {
                "nome": "Céu Estrelado",
                "objetivo": 250,
                "velocidade": 4,
                "intervalo_estrelas": 50,
                "intervalo_obstaculos": 80,  # Aumentado de 70 para 80
                "obstaculos": ["galho", "nuvem"],
                "prob_galho": 0.5,  # Reduzido de 0.6 para 0.5
                "prob_nuvem": 0.5,  # Aumentado de 0.4 para 0.5
                "prob_lua": 0.0,
                "prob_estrela_dourada": 0.2,
                "cor_ceu": (5, 10, 30),
                "descricao": "Cuidado com as nuvens!"
            },
            3: {
                "nome": "Neblina Misteriosa",
                "objetivo": 500,
                "velocidade": 5,
                "intervalo_estrelas": 40,
                "intervalo_obstaculos": 60,  # Aumentado de 50 para 60
                "obstaculos": ["galho", "nuvem", "lua"],
                "prob_galho": 0.4,  # Reduzido de 0.5 para 0.4
                "prob_nuvem": 0.4,  # Aumentado de 0.3 para 0.4
                "prob_lua": 0.2,   # Mantido 0.2
                "prob_estrela_dourada": 0.3,
                "cor_ceu": (15, 15, 35),
                "descricao": "Agora tem luas!"
            }
        }
        
        self.fase_atual = 1
        self.config = self.fases[1]
        
    def get_config(self):
        return self.config
    
    def verificar_conclusao(self, pontuacao):
        return pontuacao >= self.config["objetivo"]
    
    def avancar_fase(self):
        if self.fase_atual < 3:
            self.fase_atual += 1
            self.config = self.fases[self.fase_atual]
            return True
        return False