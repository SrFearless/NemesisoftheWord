import pygame
from config import *
from player import Player
from enemy import Enemy
from animation import Animation  # Adicione esta linha


class Game:
    def __init__(self):
        # Inicializa a janela do jogo
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Carrega assets com verificação de arquivo
        try:
            self.background = pygame.image.load(BACKGROUND_IMAGE).convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            print(f"Erro ao carregar background: {BACKGROUND_IMAGE}")
            # Cria um background simples como fallback
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((50, 120, 80))  # Verde escuro

        # Tenta carregar música de fundo
        try:
            pygame.mixer.music.load(BACKGROUND_MUSIC)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # -1 para loop infinito
        except:
            print(f"Erro ao carregar música: {BACKGROUND_MUSIC}")

        # Cria o jogador
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Cria grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def run(self):
        # Game loop
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Processa eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        # Atualiza todos os sprites
        self.all_sprites.update()

    def draw(self):
        # Desenha o background
        self.screen.blit(self.background, (0, 0))

        # Desenha todos os sprites
        self.all_sprites.draw(self.screen)

        # Atualiza a tela
        pygame.display.flip()