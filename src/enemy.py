import pygame
import random
import math
import os
from src.animation import Animation

# Cores para fallback
RED = (255, 0, 0)
DARK_RED = (200, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        print("Inicializando Inimigo com animações multidirecionais...")

        # Carrega as animações
        self.animations = self.load_animations()
        self.current_state = 'idle'
        self.direction = 'down'
        self.facing = 'down'

        self.image = self.animations['idle']['down'].get_current_frame()

        # HITBOXES REDUZIDAS - tamanho original do sprite é 128x128
        # Hitbox principal reduzida para 60x60 (47% do tamanho original)
        self.rect = pygame.Rect(0, 0, 60, 60)

        # Hitbox de colisão ainda menor para mais precisão (40x40)
        self.collision_rect = pygame.Rect(0, 0, 40, 40)

        self.player = player
        self.speed = random.uniform(1.0, 3.0)
        self.health = 30
        self.max_health = 30
        self.is_moving = False

        self.spawn()
        print(f"Inimigo criado. Hitbox: {self.rect.size}, Collision: {self.collision_rect.size}")

    def load_animations(self):
        """Carrega animações para todas as direções"""
        animations = {
            'idle': {},
            'walk': {},
            'attack': {}
        }

        directions = ['down', 'up', 'left', 'right']

        for state in ['idle', 'walk']:
            for direction in directions:
                try:
                    frames = self.load_frames(state, direction)
                    if frames:
                        if state == 'idle':
                            animations[state][direction] = Animation(frames, 200)
                        elif state == 'walk':
                            animations[state][direction] = Animation(frames, 150)
                        print(f"✓ Inimigo {state}_{direction}: {len(frames)} frames")
                    else:
                        print(f"✗ Criando fallback para inimigo {state}_{direction}")
                        animations[state][direction] = self.create_fallback_animation(state, direction)
                except Exception as e:
                    print(f"❌ Erro em inimigo {state}_{direction}: {e}")
                    animations[state][direction] = self.create_fallback_animation(state, direction)

        return animations

    def load_frames(self, state, direction):
        """Carrega frames para um estado e direção específicos"""
        frames = []
        frame_count = 4

        for i in range(frame_count):
            frame_path = f'assets/images/enemy/{state}/{direction}/frame_{i}.png'
            if os.path.exists(frame_path):
                frame = pygame.image.load(frame_path).convert_alpha()
                frame = pygame.transform.scale(frame, (128, 128))
                frames.append(frame)

        return frames if frames else None

    def create_fallback_animation(self, state, direction):
        """Cria animação de fallback para uma direção específica"""
        frames = []
        frame_count = 4

        # Cores base por direção para inimigos
        direction_colors = {
            'down': RED,
            'up': DARK_RED,
            'left': (150, 0, 0),
            'right': (180, 0, 0)
        }

        base_color = direction_colors.get(direction, RED)

        for i in range(frame_count):
            # Aumentando o fallback para 128x128 para coincidir com sprites reais
            surf = pygame.Surface((128, 128), pygame.SRCALPHA)

            # Base do inimigo (círculo vermelho centralizado)
            pygame.draw.circle(surf, base_color, (64, 64), 40)

            # Olhos do inimigo
            if direction == 'down':
                pygame.draw.circle(surf, BLACK, (54, 54), 8)  # Olho esquerdo
                pygame.draw.circle(surf, BLACK, (74, 54), 8)  # Olho direito
                pygame.draw.rect(surf, BLACK, (57, 80, 14, 6))  # Boca
            elif direction == 'up':
                pygame.draw.circle(surf, BLACK, (54, 44), 8)
                pygame.draw.circle(surf, BLACK, (74, 44), 8)
                pygame.draw.rect(surf, BLACK, (57, 30, 14, 6))
            elif direction == 'left':
                pygame.draw.circle(surf, BLACK, (44, 54), 8)
                pygame.draw.circle(surf, BLACK, (44, 74), 8)
                pygame.draw.rect(surf, BLACK, (30, 57, 6, 14))
            elif direction == 'right':
                pygame.draw.circle(surf, BLACK, (84, 54), 8)
                pygame.draw.circle(surf, BLACK, (84, 74), 8)
                pygame.draw.rect(surf, BLACK, (92, 57, 6, 14))

            # Animação de movimento
            if state == 'walk':
                offset = i * 8 - 12  # Movimento mais pronunciado
                if direction in ['down', 'up']:
                    pygame.draw.ellipse(surf, (0, 0, 0, 100), (44, 100 + offset, 40, 12))
                else:
                    pygame.draw.ellipse(surf, (0, 0, 0, 100), (44 + offset, 100, 40, 12))

            frames.append(surf)

        duration = 200 if state == 'idle' else 150
        return Animation(frames, duration)

    def determine_direction(self, dx, dy):
        """Determina a direção baseada no movimento"""
        if abs(dx) > abs(dy):
            return 'left' if dx < 0 else 'right'
        else:
            return 'up' if dy < 0 else 'down'

    def spawn(self):
        side = random.choice(['top', 'right', 'bottom', 'left'])

        if side == 'top':
            self.rect.x = random.randint(0, 1600)
            self.rect.y = -60
            self.direction = 'down'
            self.facing = 'down'
        elif side == 'right':
            self.rect.x = 1600 + 60
            self.rect.y = random.randint(0, 1200)
            self.direction = 'left'
            self.facing = 'left'
        elif side == 'bottom':
            self.rect.x = random.randint(0, 1600)
            self.rect.y = 1200 + 60
            self.direction = 'up'
            self.facing = 'up'
        elif side == 'left':
            self.rect.x = -60
            self.rect.y = random.randint(0, 1200)
            self.direction = 'right'
            self.facing = 'right'

        # Centraliza a hitbox de colisão
        self.collision_rect.center = self.rect.center

    def update(self):
        # Calcula direção para o jogador
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery

        dist = math.sqrt(dx * dx + dy * dy)
        self.is_moving = dist > 20

        # Determina nova direção
        old_direction = self.direction
        self.direction = self.determine_direction(dx, dy)
        self.facing = self.direction

        # Atualiza estado da animação
        new_state = 'walk' if self.is_moving else 'idle'

        # Reseta animação se mudou de estado ou direção
        if new_state != self.current_state or old_direction != self.direction:
            self.current_state = new_state
            self.animations[self.current_state][self.direction].reset()

        # Atualiza animação
        self.animations[self.current_state][self.direction].update()
        self.image = self.animations[self.current_state][self.direction].get_current_frame()

        # Movimento em direção ao jogador
        if dist > 0:
            dx = dx / dist * self.speed
            dy = dy / dist * self.speed
            self.rect.x += dx
            self.rect.y += dy

            # Atualiza a hitbox de colisão
            self.collision_rect.center = self.rect.center

        # Mantém dentro dos limites da tela
        self.keep_in_bounds()

    def keep_in_bounds(self):
        """Mantém o inimigo dentro dos limites da tela"""
        self.rect.left = max(-100, self.rect.left)  # Permite um pouco fora para spawn
        self.rect.right = min(1700, self.rect.right)
        self.rect.top = max(-100, self.rect.top)
        self.rect.bottom = min(1300, self.rect.bottom)

        # Atualiza hitbox de colisão
        self.collision_rect.center = self.rect.center

    def draw_debug(self, surface):
        """Desenha informações de debug para o inimigo"""
        # Hitbox principal (verde)
        pygame.draw.rect(surface, (0, 255, 0), self.rect, 2)

        # Hitbox de colisão (vermelho)
        pygame.draw.rect(surface, (255, 0, 0), self.collision_rect, 2)

        # Centro (ponto azul)
        pygame.draw.circle(surface, (0, 0, 255), self.rect.center, 3)

        # Texto com vida
        font = pygame.font.SysFont(None, 16)
        health_text = f"HP: {self.health}"
        text_surface = font.render(health_text, True, WHITE)
        surface.blit(text_surface, (self.rect.x, self.rect.y - 15))