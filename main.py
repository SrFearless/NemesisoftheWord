import pygame
import os
import sys
import random
import math
from player import Player
from enemy import Enemy

# Inicialização do Pygame
pygame.init()

# Configurações da janela
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NemesisoftheWord")
clock = pygame.time.Clock()
FPS = 60

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Classe para efeitos visuais
class Effect(pygame.sprite.Sprite):
    def __init__(self, x, y, effect_type):
        super().__init__()
        self.effect_type = effect_type
        self.lifetime = 10

        if effect_type == "sword":
            self.frames = []
            # Cria frames para efeito de espada
            for i in range(4):
                surf = pygame.Surface((40, 15), pygame.SRCALPHA)
                alpha = 200 - (i * 50)
                pygame.draw.rect(surf, (255, 255, 0, alpha), (0, 0, 30 + i * 3, 10))
                self.frames.append(surf)

            self.image = self.frames[0]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.current_frame = 0

    def update(self):
        self.lifetime -= 1

        # Anima o efeito
        if self.lifetime > 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
        else:
            self.kill()

# Funções de desenho
def draw_health_bar(surface, x, y, percentage, width=100, height=10):
    fill = (percentage / 100) * width
    outline_rect = pygame.Rect(x, y, width, height)
    fill_rect = pygame.Rect(x, y, fill, height)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Cria o jogador
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
effects = pygame.sprite.Group()

all_sprites.add(player)

# Variáveis do jogo
enemy_spawn_timer = 0
enemy_spawn_delay = 1000
game_over = False
score = 0
level = 1
enemies_per_level = 10
enemies_defeated = 0
combo_counter = 0
combo_timer = 0

# Game loop
running = True
while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    # Processa eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and not game_over:
                if player.attack():
                    # Cria efeito visual da espada
                    if player.direction == "right":
                        effect_x = player.rect.right + 15
                    else:
                        effect_x = player.rect.left - 15
                    effect = Effect(effect_x, player.rect.centery, "sword")
                    effects.add(effect)
                    all_sprites.add(effect)

                    # Verifica colisão com inimigos
                    sword_hitbox = player.get_sword_hitbox()
                    if sword_hitbox:
                        for enemy in enemies:
                            if sword_hitbox.colliderect(enemy.rect):
                                enemy.health -= player.attack_damage
                                combo_counter += 1
                                combo_timer = 60

                                if enemy.health <= 0:
                                    score += 10 + (combo_counter * 2)
                                    enemies_defeated += 1
                                    enemy.kill()

    if not game_over:
        # Atualiza combo timer
        if combo_timer > 0:
            combo_timer -= 1
        else:
            combo_counter = 0

        # Atualiza
        keys = pygame.key.get_pressed()
        player.update(keys)

        # Spawn de inimigos
        if current_time - enemy_spawn_timer > enemy_spawn_delay and len(enemies) < 5 + level:
            enemy = Enemy(player)
            all_sprites.add(enemy)
            enemies.add(enemy)
            enemy_spawn_timer = current_time

        # Atualiza inimigos
        for enemy in enemies:
            enemy.update()

        # Atualiza efeitos
        effects.update()

        # Colisão: Inimigo vs Jogador
        hits = pygame.sprite.spritecollide(player, enemies, False)
        for enemy in hits:
            player.health -= 0.5
            if player.health <= 0:
                game_over = True

        # Aumenta a dificuldade
        if enemies_defeated >= enemies_per_level:
            level += 1
            enemies_per_level += 10
            enemies_defeated = 0
            enemy_spawn_delay = max(500, enemy_spawn_delay - 100)

    # Desenha
    screen.fill(BLACK)

    # Desenha todos os sprites
    all_sprites.draw(screen)

    # Desenha a hitbox da espada (para debug)
    if player.attacking:
        sword_hitbox = player.get_sword_hitbox()
        if sword_hitbox:
            pygame.draw.rect(screen, ORANGE, sword_hitbox, 2)

    # Desenha barras de vida dos inimigos
    for enemy in enemies:
        health_percent = (enemy.health / enemy.max_health) * 100
        draw_health_bar(screen, enemy.rect.x, enemy.rect.y - 10, health_percent, 25, 5)

    # Desenha UI
    draw_health_bar(screen, 10, 10, player.health)
    draw_text(screen, f"Vida: {int(player.health)}/{player.max_health}", 24, 120, 12)
    draw_text(screen, f"Score: {score}", 24, SCREEN_WIDTH - 60, 10)
    draw_text(screen, f"Level: {level}", 24, SCREEN_WIDTH - 60, 40)
    draw_text(screen, f"Inimigos: {enemies_defeated}/{enemies_per_level}", 24, SCREEN_WIDTH - 100, 70)

    # Combo counter
    if combo_counter > 1:
        draw_text(screen, f"COMBO x{combo_counter}!", 32, SCREEN_WIDTH // 2, 10, YELLOW)

    # Instruções
    draw_text(screen, "WASD: Mover | Espaço: Atacar com Espada", 20, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

    # Tela de Game Over
    if game_over:
        draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text(screen, f"Score Final: {score}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text(screen, f"Level Alcançado: {level}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        draw_text(screen, "Pressione ESC para sair", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)

    # Atualiza a tela
    pygame.display.flip()

# Encerra o Pygame
pygame.quit()
sys.exit()