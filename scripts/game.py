import pygame
import random
import sys
from fase_system import SistemaFasesSystem
from game_manager import GameManager

class Game:
    def __init__(self, screen, game_manager):
        self.screen = screen
        self.game_manager = game_manager
        self.phase_system = SistemaFasesSystem()
        
        # Configura fase inicial
        self.phase_system.current_phase = game_manager.current_phase
        self.phase_system.current_config = self.phase_system.phases[game_manager.current_phase]
        
        # Variáveis do jogo
        self.score = 0
        self.game_over = False
        self.paused = False
        
        # Tempos para spawn
        self.last_star_time = 0
        self.last_branch_time = 0
        self.last_cloud_time = 0
        self.last_moon_time = 0
        
        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        
        # Carrega sprites
        self.load_sprites()
        
        # Configurações iniciais da fase
        self.update_phase_config()
        
        # Neblina (se houver)
        self.fog_surface = None
        if self.phase_system.has_fog():
            self.create_fog()
    
    def update_phase_config(self):
        """Atualiza configurações baseadas na fase atual"""
        config = self.phase_system.get_current_config()
        
        # Velocidades de spawn
        self.star_spawn_time = self.phase_system.get_spawn_time("star")
        self.branch_spawn_time = self.phase_system.get_spawn_time("branch")
        self.cloud_spawn_time = self.phase_system.get_spawn_time("cloud")
        self.moon_spawn_time = self.phase_system.get_spawn_time("moon")
        
        # Atualiza background
        self.background_color = self.phase_system.get_background_color()
        
        print(f"Fase {self.phase_system.current_phase} carregada: {config['name']}")
        print(f"Objetivo: {config['target_score']} pontos")
    
    def create_fog(self):
        """Cria superfície de neblina"""
        fog_alpha = self.phase_system.get_fog_alpha()
        self.fog_surface = pygame.Surface((600, 500))
        self.fog_surface.fill((200, 200, 220))  # Cor da neblina
        self.fog_surface.set_alpha(fog_alpha)
    
    def load_sprites(self):
        """Carrega sprites do jogo"""
        # (Mantenha seu código atual de carregamento de sprites)
        # Adicione apenas o necessário para as fases
        
        # Exemplo simplificado:
        self.owl_sprite = pygame.image.load("assets/owl.png").convert_alpha()
        self.star_sprite = pygame.image.load("assets/star.png").convert_alpha()
        self.gold_star_sprite = pygame.image.load("assets/gold_star.png").convert_alpha()
        self.branch_sprite = pygame.image.load("assets/branch.png").convert_alpha()
        self.cloud_sprite = pygame.image.load("assets/cloud.png").convert_alpha()
        self.moon_sprite = pygame.image.load("assets/moon.png").convert_alpha()
    
    def spawn_items(self, current_time):
        """Spawna itens baseado na fase atual"""
        config = self.phase_system.get_current_config()
        
        # Spawn de estrelas
        if current_time - self.last_star_time > self.star_spawn_time:
            # Decide se é estrela dourada
            if self.phase_system.should_spawn_gold_star() and "gold_star" in config["items"]:
                self.spawn_star(is_gold=True)
            else:
                self.spawn_star(is_gold=False)
            self.last_star_time = current_time
        
        # Spawn de obstáculos baseado na fase
        obstacles = config["obstacles"]
        
        if "branches" in obstacles:
            if current_time - self.last_branch_time > self.branch_spawn_time:
                self.spawn_branch()
                self.last_branch_time = current_time
        
        if "clouds" in obstacles:
            if current_time - self.last_cloud_time > self.cloud_spawn_time:
                self.spawn_cloud()
                self.last_cloud_time = current_time
        
        if "moon" in obstacles:
            if current_time - self.last_moon_time > self.moon_spawn_time:
                self.spawn_moon()
                self.last_moon_time = current_time
    
    def check_phase_completion(self):
        """Verifica se completou a fase atual"""
        config = self.phase_system.get_current_config()
        target = config["target_score"]
        
        if self.score >= target:
            # Atualiza recorde da fase
            self.game_manager.update_phase_score(self.phase_system.current_phase, self.score)
            
            # Verifica se tem próxima fase
            if self.phase_system.current_phase < 3:
                return True  # Pode avançar de fase
            else:
                # Última fase completada
                return "game_complete"
        
        return False
    
    def advance_to_next_phase(self):
        """Avança para a próxima fase"""
        if self.phase_system.advance_phase():
            # Desbloqueia no game manager
            next_phase = self.phase_system.current_phase
            self.game_manager.unlock_next_phase()
            self.game_manager.set_current_phase(next_phase)
            
            # Reseta alguns valores mas mantém pontuação
            self.clear_obstacles()
            self.update_phase_config()
            
            # Atualiza neblina se necessário
            if self.phase_system.has_fog():
                self.create_fog()
            else:
                self.fog_surface = None
            
            print(f"Avançou para Fase {next_phase}: {self.phase_system.current_config['name']}")
            return True
        
        return False
    
    def clear_obstacles(self):
        """Limpa todos os obstáculos da tela"""
        for obstacle in self.obstacles:
            obstacle.kill()
    
    def draw(self):
        """Desenha todos os elementos na tela"""
        # Fundo da fase
        self.screen.fill(self.background_color)
        
        # Desenha sprites
        self.all_sprites.draw(self.screen)
        
        # Desenha neblina se houver
        if self.fog_surface:
            self.screen.blit(self.fog_surface, (0, 0))
        
        # Desenha HUD
        self.draw_hud()
        
        # Se fase completada, mostra mensagem
        phase_complete = self.check_phase_completion()
        if phase_complete == True:
            self.draw_phase_complete_message()
        elif phase_complete == "game_complete":
            self.draw_game_complete_message()
    
    def draw_hud(self):
        """Desenha informações da fase atual"""
        font = pygame.font.SysFont(None, 28)
        
        # Pontuação
        score_text = font.render(f"Pontos: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Fase atual
        phase_text = font.render(f"Fase: {self.phase_system.current_phase} - {self.phase_system.current_config['name']}", 
                                True, (255, 255, 200))
        self.screen.blit(phase_text, (10, 40))
        
        # Objetivo da fase
        target = self.phase_system.current_config["target_score"]
        objective_text = font.render(f"Objetivo: {target} pontos", True, (200, 255, 200))
        self.screen.blit(objective_text, (10, 70))
        
        # Barra de progresso
        progress = min(self.score / target, 1.0)
        bar_width = 200
        bar_height = 15
        pygame.draw.rect(self.screen, (50, 50, 50), (400, 15, bar_width, bar_height))
        pygame.draw.rect(self.screen, (100, 255, 100), (400, 15, bar_width * progress, bar_height))
    
    def draw_phase_complete_message(self):
        """Desenha mensagem de fase concluída"""
        font_large = pygame.font.SysFont(None, 48)
        font_small = pygame.font.SysFont(None, 32)
        
        # Fundo semi-transparente
        overlay = pygame.Surface((600, 500))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Mensagens
        complete_text = font_large.render("FASE CONCLUÍDA!", True, (255, 255, 100))
        next_phase_text = font_small.render("Avançando para próxima fase...", True, (200, 200, 255))
        continue_text = font_small.render("Pressione ESPAÇO para continuar", True, (200, 255, 200))
        
        self.screen.blit(complete_text, (600//2 - complete_text.get_width()//2, 150))
        self.screen.blit(next_phase_text, (600//2 - next_phase_text.get_width()//2, 220))
        self.screen.blit(continue_text, (600//2 - continue_text.get_width()//2, 280))
    
    def draw_game_complete_message(self):
        """Desenha mensagem de jogo completo"""
        font_large = pygame.font.SysFont(None, 48)
        font_small = pygame.font.SysFont(None, 32)
        
        overlay = pygame.Surface((600, 500))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        complete_text = font_large.render("JOGO COMPLETO!", True, (255, 200, 50))
        congrats_text = font_small.render("Você completou todas as fases!", True, (200, 255, 200))
        final_score_text = font_small.render(f"Pontuação Final: {self.score}", True, (255, 255, 255))
        restart_text = font_small.render("Pressione R para reiniciar", True, (200, 200, 255))