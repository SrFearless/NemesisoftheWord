import pygame
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.direction = "down"  # Direção para animações

    def update(self):
        # Movimento do jogador
        keys = pygame.key.get_pressed()

        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.direction = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
            self.direction = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
            self.direction = "down"

        # Atualiza a posição
        self.rect.x += dx
        self.rect.y += dy

        # Mantém o jogador dentro da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT