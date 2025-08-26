import pygame
import random
import math
from animation import Animation

# Cores para fallback
RED = (255, 0, 0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

        self.animations = self.load_animations()
        self.current_state = 'idle'
        self.direction = 'right'

        self.image = self.animations['idle'].get_current_frame()
        self.rect = self.image.get_rect()
        self.player = player

        self.speed = random.uniform(1.0, 3.0)
        self.health = 30
        self.max_health = 30
        self.is_moving = False

        self.spawn()

    def load_animations(self):
        """Carrega animações reais do inimigo"""
        try:
            idle_frames = []
            walk_frames = []

            for i in range(4):
                frame_path = f'assets/images/enemy/idle/idle_{i}.png'
                frame = pygame.image.load(frame_path).convert_alpha()
                frame = pygame.transform.scale(frame, (50, 50))
                idle_frames.append(frame)

                frame_path = f'assets/images/enemy/walk/walk_{i}.png'
                frame = pygame.image.load(frame_path).convert_alpha()
                frame = pygame.transform.scale(frame, (50, 50))
                walk_frames.append(frame)

            print("Sprites do inimigo carregados com sucesso!")

            return {
                'idle': Animation(idle_frames, 200),
                'walk': Animation(walk_frames, 150)
            }

        except Exception as e:
            print(f"Erro ao carregar sprites do inimigo: {e}")
            print("Usando sprites de fallback...")
            return self.create_fallback_animations()

    def create_fallback_animations(self):
        """Cria animações de fallback para inimigo"""
        idle_frames = []
        walk_frames = []

        for i in range(4):
            # Idle (vermelho)
            surf = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(surf, RED, (25, 25), 20)
            idle_frames.append(surf)

            # Walk (vermelho escuro)
            surf = pygame.Surface((50, 50), pygame.SRCALPHA)
            offset = i * 3 - 4
            pygame.draw.circle(surf, (200, 0, 0), (25, 25 + offset), 20)
            walk_frames.append(surf)

        return {
            'idle': Animation(idle_frames, 200),
            'walk': Animation(walk_frames, 150)
        }

    def spawn(self):
        side = random.choice(['top', 'right', 'bottom', 'left'])

        if side == 'top':
            self.rect.x = random.randint(0, 1600)
            self.rect.y = -50
        elif side == 'right':
            self.rect.x = 1600 + 50
            self.rect.y = random.randint(0, 1200)
        elif side == 'bottom':
            self.rect.x = random.randint(0, 1600)
            self.rect.y = 1200 + 50
        elif side == 'left':
            self.rect.x = -50
            self.rect.y = random.randint(0, 1200)

    def update(self):
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery

        dist = math.sqrt(dx * dx + dy * dy)
        self.is_moving = dist > 20

        self.current_state = 'walk' if self.is_moving else 'idle'
        self.animations[self.current_state].update()
        self.image = self.animations[self.current_state].get_current_frame()

        if dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'

        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

        if dist > 0:
            dx = dx / dist * self.speed
            dy = dy / dist * self.speed
            self.rect.x += dx
            self.rect.y += dy