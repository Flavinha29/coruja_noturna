import pickle
import os

class GerenciadorProgresso:
    def __init__(self):
        self.arquivo = "data/progress.dat"
        self.recorde_geral = 0
        self.fase_atual = 1  # Sempre começa na fase 1
        self.fases_completadas = 0
        self.recordes_fases = {1: 0, 2: 0, 3: 0}
        
        os.makedirs("data", exist_ok=True)
        self.carregar()
    
    def carregar(self):
        try:
            if os.path.exists(self.arquivo):
                with open(self.arquivo, 'rb') as f:
                    data = pickle.load(f)
                    self.recorde_geral = data.get('recorde_geral', 0)
                    # NÃO carrega fase_atual - sempre começa na 1
                    self.fases_completadas = data.get('fases_completadas', 0)
                    self.recordes_fases = data.get('recordes_fases', {1:0, 2:0, 3:0})
        except:
            self.salvar()
    
    def salvar(self):
        data = {
            'recorde_geral': self.recorde_geral,
            'fase_atual': 1,  # SEMPRE salva como fase 1
            'fases_completadas': self.fases_completadas,
            'recordes_fases': self.recordes_fases
        }
        with open(self.arquivo, 'wb') as f:
            pickle.dump(data, f)
    
    def atualizar_recorde(self, pontuacao):
        if pontuacao > self.recorde_geral:
            self.recorde_geral = pontuacao
            self.salvar()
            return True
        return False
    
    def completar_fase(self, fase, pontuacao):
        """Quando completa uma fase, apenas atualiza o recorde da fase"""
        if pontuacao > self.recordes_fases.get(fase, 0):
            self.recordes_fases[fase] = pontuacao
            self.salvar()
        
        # NÃO avança automaticamente - o jogo avança na mesma sessão
        return True
    
    def resetar_para_fase_1(self):
        """Reseta para fase 1 (usado quando morre)"""
        self.fase_atual = 1
        self.salvar()
        return True
    
    def resetar_tudo(self):
        """Reseta TODO o progresso (apenas para menu)"""
        self.recorde_geral = 0
        self.fase_atual = 1
        self.fases_completadas = 0
        self.recordes_fases = {1: 0, 2: 0, 3: 0}
        self.salvar()