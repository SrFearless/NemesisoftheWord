import os
import sys

# Configurações da janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Meu RPG"

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Caminhos para assets
def get_resource_path(relative_path):
    try:
        # PyInstaller cria uma pasta temporária e caminho diferente
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, "assets", relative_path)


# Imagens - usando caminhos relativos simples para evitar erros
PLAYER_IMAGE = "assets/images/player.png"
BACKGROUND_IMAGE = "assets/images/backgrounds.png"

# Áudio
BACKGROUND_MUSIC = "assets/audio/music/theme.ogg"

# Configurações do jogador
PLAYER_SPEED = 5
PLAYER_HEALTH = 100