import pygame
import random
from animation import Animation

# Cores para fallback
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Carrega as animações
        self.animations = self.load_animations()
        self.current_state = 'idle'
        self.direction = 'right'

        self.image = self.animations['idle'].get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.score = 0
        self.attacking = False
        self.attack_cooldown = 0
        self.attack_duration = 15
        self.attack_range = 50
        self.attack_damage = 25
        self.is_moving = False

    def load_animations(self):
        """Carrega animações reais do jogador"""
        animations = {}

        try:
            # IDLE Animation
            idle_frames = []
            for i in range(4):  # 4 frames de idle
                frame_path = f'assets/images/player/idle/idle_{i}.png'
                frame = pygame.image.load(frame_path).convert_alpha()
                frame = pygame.transform.scale(frame, (64, 64))
                idle_frames.append(frame)
            animations['idle'] = Animation(idle_frames, 150)

            # WALK Animation
            walk_frames = []
            for i in range(6):  # 6 frames de walk
                frame_path = f'assets/images/player/walk/walk_{i}.png'
                frame = pygame.image.load(frame_path).convert_alpha()
                frame = pygame.transform.scale(frame, (64, 64))
                walk_frames.append(frame)
            animations['walk'] = Animation(walk_frames, 100)

            # ATTACK Animation
            attack_frames = []
            for i in range(4):  # 4 frames de attack
                frame_path = f'assets/images/player/attack/attack_{i}.png'
                frame = pygame.image.load(frame_path).convert_alpha()
                frame = pygame.transform.scale(frame, (64, 64))
                attack_frames.append(frame)
            animations['attack'] = Animation(attack_frames, 50)

            print("Sprites do jogador carregados com sucesso!")

        except Exception as e:
            print(f"Erro ao carregar sprites do jogador: {e}")
            print("Usando sprites de fallback...")
            animations = self.create_fallback_animations()

        return animations

    def create_fallback_animations(self):
        """Cria animações de fallback"""
        idle_frames = []
        walk_frames = []
        attack_frames = []

        for i in range(4):
            # Idle (azul)
            surf = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.circle(surf, BLUE, (32, 32), 20)
            idle_frames.append(surf)

            # Walk (verde)
            surf = pygame.Surface((64, 64), pygame.SRCALPHA)
            offset = i * 3 - 4
            pygame.draw.circle(surf, GREEN, (32, 32 + offset), 20)
            walk_frames.append(surf)

            # Attack (laranja)
            surf = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.circle(surf, ORANGE, (32, 32), 25)
            if i < 2:
                pygame.draw.rect(surf, YELLOW, (32, 16, 35, 8))
            attack_frames.append(surf)

        return {
            'idle': Animation(idle_frames, 150),
            'walk': Animation(walk_frames, 100),
            'attack': Animation(attack_frames, 50)
        }

    def update(self, keys):
        dx, dy = 0, 0
        self.is_moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.direction = 'left'
            self.is_moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.direction = 'right'
            self.is_moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
            self.is_moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
            self.is_moving = True

        self.rect.x += dx
        self.rect.y += dy

        # Atualiza estado da animação
        if self.attacking:
            self.current_state = 'attack'
        elif self.is_moving:
            self.current_state = 'walk'
        else:
            self.current_state = 'idle'

        # Atualiza animação
        self.animations[self.current_state].update()
        self.image = self.animations[self.current_state].get_current_frame()

        # Flip da imagem baseado na direção
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

        # Cooldown do ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            if self.attack_cooldown == 0:
                self.attacking = False
                self.animations['attack'].reset()

        # Mantém o jogador dentro da tela
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(1600, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(1200, self.rect.bottom)

    def attack(self):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_cooldown = 30
            self.animations['attack'].reset()
            return True
        return False

    def get_sword_hitbox(self):
        if not self.attacking:
            return None

        if self.direction == "right":
            return pygame.Rect(self.rect.right, self.rect.centery - 15, self.attack_range, 30)
        else:
            return pygame.Rect(self.rect.left - self.attack_range, self.rect.centery - 15, self.attack_range, 30)