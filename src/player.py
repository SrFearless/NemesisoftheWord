import pygame
import os
from src.animation import Animation

# Cores para fallback
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        print("Inicializando Player com animações multidirecionais...")

        # Carrega as animações
        self.animations = self.load_animations()
        self.current_state = 'idle'
        self.direction = 'down'
        self.facing = 'down'

        self.image = self.animations['idle']['down'].get_current_frame()

        # HITBOXES - Ajustadas para melhor centralização
        # A hitbox principal deve ser baseada no tamanho da imagem
        image_width, image_height = self.image.get_size()

        # Hitbox principal (um pouco menor que a imagem)
        self.rect = pygame.Rect(0, 0, image_width * 0.6, image_height * 0.6)  # 60% do tamanho da imagem
        self.rect.center = (x, y)

        # Hitbox de colisão (ainda menor para precisão)
        self.collision_rect = pygame.Rect(0, 0, image_width * 0.4, image_height * 0.4)  # 40% do tamanho da imagem
        self.collision_rect.center = self.rect.center

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

        print(f"Player criado em posição: ({x}, {y})")
        print(f"Tamanho da imagem: {image_width}x{image_height}")
        print(f"Tamanho da hitbox: {self.rect.width}x{self.rect.height}")

    def load_animations(self):
        """Carrega animações para todas as direções"""
        animations = {
            'idle': {},
            'walk': {},
            'attack': {}
        }

        directions = ['down', 'up', 'left', 'right']

        for state in ['idle', 'walk', 'attack']:
            for direction in directions:
                try:
                    frames = self.load_frames(state, direction)
                    if frames:
                        if state == 'idle':
                            animations[state][direction] = Animation(frames, 150)
                        elif state == 'walk':
                            animations[state][direction] = Animation(frames, 100)
                        elif state == 'attack':
                            animations[state][direction] = Animation(frames, 50)
                        print(f"✓ {state}_{direction}: {len(frames)} frames")
                    else:
                        print(f"✗ Criando fallback para {state}_{direction}")
                        animations[state][direction] = self.create_fallback_animation(state, direction)
                except Exception as e:
                    print(f"❌ Erro em {state}_{direction}: {e}")
                    animations[state][direction] = self.create_fallback_animation(state, direction)

        return animations

    def load_frames(self, state, direction):
        """Carrega frames para um estado e direção específicos"""
        frames = []
        frame_count = 4 if state in ['idle', 'attack'] else 6  # 4 frames para idle/attack, 6 para walk

        for i in range(frame_count):
            frame_path = f'assets/images/player/{state}/{direction}/frame_{i}.png'
            if os.path.exists(frame_path):
                frame = pygame.image.load(frame_path).convert_alpha()
                frame = pygame.transform.scale(frame, (128, 128))
                frames.append(frame)

        return frames if frames else None

    def create_fallback_animation(self, state, direction):
        """Cria animação de fallback para uma direção específica"""
        frames = []
        frame_count = 4 if state in ['idle', 'attack'] else 6

        # Cores base por direção
        direction_colors = {
            'down': BLUE,
            'up': GREEN,
            'left': ORANGE,
            'right': PURPLE
        }

        base_color = direction_colors.get(direction, BLUE)

        for i in range(frame_count):
            surf = pygame.Surface((128, 128), pygame.SRCALPHA)

            # Base do personagem (centralizada)
            pygame.draw.circle(surf, base_color, (64, 64), 40)

            # Indicador de direção (seta)
            if direction == 'down':
                pygame.draw.polygon(surf, WHITE, [(56, 80), (64, 96), (72, 80)])
            elif direction == 'up':
                pygame.draw.polygon(surf, WHITE, [(56, 48), (64, 32), (72, 48)])
            elif direction == 'left':
                pygame.draw.polygon(surf, WHITE, [(48, 56), (32, 64), (48, 72)])
            elif direction == 'right':
                pygame.draw.polygon(surf, WHITE, [(80, 56), (96, 64), (80, 72)])

            # Animação adicional baseada no estado
            if state == 'walk':
                offset = i * 6 - (frame_count * 6 // 2) + 3
                if direction in ['down', 'up']:
                    pygame.draw.circle(surf, BLACK, (64, 64 + offset), 10)
                else:
                    pygame.draw.circle(surf, BLACK, (64 + offset, 64), 10)

            elif state == 'attack':
                if i < 2:  # Primeiros frames mostram arma
                    weapon_color = YELLOW
                    if direction == 'down':
                        pygame.draw.rect(surf, weapon_color, (56, 90, 16, 30))
                    elif direction == 'up':
                        pygame.draw.rect(surf, weapon_color, (56, 8, 16, 30))
                    elif direction == 'left':
                        pygame.draw.rect(surf, weapon_color, (8, 56, 30, 16))
                    elif direction == 'right':
                        pygame.draw.rect(surf, weapon_color, (90, 56, 30, 16))

            frames.append(surf)

        duration = 150 if state == 'idle' else 100 if state == 'walk' else 50
        return Animation(frames, duration)

    def update(self, keys):
        dx, dy = 0, 0
        self.is_moving = False
        old_direction = self.direction

        # Movimento e detecção de direção
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.direction = 'left'
            self.facing = 'left'
            self.is_moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.direction = 'right'
            self.facing = 'right'
            self.is_moving = True

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
            self.direction = 'up'
            self.facing = 'up'
            self.is_moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
            self.direction = 'down'
            self.facing = 'down'
            self.is_moving = True

        # Se não está se movendo, mantém a última direção virada
        if not self.is_moving:
            self.direction = self.facing

        # Move o retângulo principal
        self.rect.x += dx
        self.rect.y += dy

        # Atualiza a hitbox de colisão para seguir o retângulo principal
        self.collision_rect.center = self.rect.center

        # Atualiza estado da animação
        new_state = 'attack' if self.attacking else 'walk' if self.is_moving else 'idle'

        # Reseta animação se mudou de estado ou direção
        if new_state != self.current_state or old_direction != self.direction:
            self.current_state = new_state
            self.animations[self.current_state][self.direction].reset()

        # Atualiza animação
        self.animations[self.current_state][self.direction].update()
        self.image = self.animations[self.current_state][self.direction].get_current_frame()

        # Cooldown do ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            if self.attack_cooldown == 0:
                self.attacking = False

        # Mantém o jogador dentro da tela
        self.keep_in_bounds()

    def keep_in_bounds(self):
        """Mantém o jogador dentro dos limites da tela"""
        # Limites para a hitbox principal
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(1600, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(1200, self.rect.bottom)

        # Atualiza a hitbox de colisão para seguir a principal
        self.collision_rect.center = self.rect.center

    def attack(self):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_cooldown = 30
            self.animations['attack'][self.facing].reset()
            return True
        return False

    def get_sword_hitbox(self):
        if not self.attacking:
            return None

        # Hitbox baseada na direção do ataque
        if self.facing == 'down':
            return pygame.Rect(self.collision_rect.centerx - 15, self.collision_rect.bottom, 30, self.attack_range)
        elif self.facing == 'up':
            return pygame.Rect(self.collision_rect.centerx - 15, self.collision_rect.top - self.attack_range, 30,
                               self.attack_range)
        elif self.facing == 'left':
            return pygame.Rect(self.collision_rect.left - self.attack_range, self.collision_rect.centery - 15,
                               self.attack_range, 30)
        elif self.facing == 'right':
            return pygame.Rect(self.collision_rect.right, self.collision_rect.centery - 15, self.attack_range, 30)

    def draw_debug(self, surface):
        """Desenha informações de debug para o player"""
        # Hitbox principal (verde)
        pygame.draw.rect(surface, (0, 255, 0), self.rect, 2)

        # Hitbox de colisão (vermelho)
        pygame.draw.rect(surface, (255, 0, 0), self.collision_rect, 2)

        # Centro do player (ponto azul)
        pygame.draw.circle(surface, (0, 0, 255), self.rect.center, 3)

        # Texto com posição
        font = pygame.font.SysFont(None, 20)
        pos_text = f"Pos: ({self.rect.centerx}, {self.rect.centery})"
        text_surface = font.render(pos_text, True, WHITE)
        surface.blit(text_surface, (self.rect.x, self.rect.y - 20))