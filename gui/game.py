import sys

sys.path.append("..")

from conecta4.constants import *
from conecta4.game.sprite import Sprite

class Game:
    
    # E: Una referencia a Pygame, dos strings, un booleano (opcional)
    # S: N/A
    # D: Constructor de la clase e inicializa variables
    def __init__(self, pygame, screen, clock, player1, player2, isIA=False):
        self._player1 = player1
        self._player2 = player2
        self._game_running = True

        self._game_clock = clock
        self._background = pygame.image.load(GAME_BACKGROUND)

        self._screen = screen
        self._pygame = pygame

        
    # E/S: N/A
    # D: Se encarga de iniciar el juego
    def start_game_mode(self):
        self._game_loop()

    # E/S: N/A
    # D: Loop del juego
    def _game_loop(self):
        while self._game_running:
            self._set_background()

            for event in self._pygame.event.get():
                self._close_menu(event)

            self._pygame.display.update()
            self._game_clock.tick(60)

    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Dado un evento, cierra el juego si se oprime el boton de salir
    def _close_menu(self, event):
        if event.type == self._pygame.QUIT:
            self._pygame.quit()
            sys.exit()

    def _set_background(self):
        self._screen.fill((0, 0, 0))
        self._screen.blit(self._background, (200,0))