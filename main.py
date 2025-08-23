import pygame
import sys
import os

# Adiciona a pasta src ao path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game import Game


def main():
    # Inicializa o pygame
    pygame.init()

    # Cria uma instância do jogo
    game = Game()

    # Loop principal do jogo
    game.run()

    # Encerra o pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()