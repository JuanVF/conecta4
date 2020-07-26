import sys
import os

sys.path.append("..")

from pygame import mixer

from conecta4.animations.menu_animations import *

from conecta4.gui.scores import Score
from conecta4.gui.options import Options
from conecta4.game.sprite import Sprite

from conecta4.constants import *
from conecta4.utils import *

class Menu:

    # E: Una referencia a pygame
    # S: N/A
    # D: Constructor
    def __init__(self, pygame):
        # Esta funcion se encarga de centrar la ventana
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        self.__background = pygame.image.load(MENU_BACKGROUND_PATH)
        self.__font = pygame.font.Font(GAME_FONT_PATH, 20)

        icon = pygame.image.load(GAME_LOGO_PATH)

        mixer.music.load(GAME_BACKGROUND_MUSIC)
        mixer.music.set_volume(0.0)
        mixer.music.play(-1)

        self.__isRunning = True
        self.__click = False
        self.__main_clock = pygame.time.Clock()

        self.__screen = pygame.display.set_mode(MENU_WINDOW_SIZE)

        self.__pygame = pygame
        self.__pygame.display.set_caption("4 en linea")
        self.__pygame.display.set_icon(icon)

    # E/S: N/A
    # D: Inicia el juego y determina ciertos parametros iniciales
    def start_game(self):
        self.__bg_details = set_bg_details(self.__pygame)
        self.__button_text = set_button_list(self.__font)

        self.__lines = set_lines()
        self.__rects = set_rects(self.__pygame)
        self.__base_lines = set_line_bases()

        self.__set_menu_buttons()

        self.__game_loop()

    # E/S: N/A
    # D: Loop
    def __game_loop(self):
        while self.__isRunning:
            self.__set_background()

            draw_base_lines(self.__pygame, self.__screen, self.__rects, self.__base_lines)
            self.__lines = move_lines(self.__pygame, self.__screen, self.__lines)

            self.__bg_details = animate_bg_details(self.__screen, self.__bg_details)

            self.__render_buttons()
            self.__render_buttons_text()

            self.__button_events()

            self.__click = False

            for event in self.__pygame.event.get():
                close_menu(self.__pygame, event)
                self.__click = detect_click(self.__pygame, event)

            self.__pygame.display.update()
            self.__main_clock.tick(60)

    # E/S: N/A
    # D: Se encarga de asignar el background del menu
    def __set_background(self):
        self.__screen.fill((16, 15, 15))
        self.__screen.blit(self.__background, (300, 0))

    # E/S: N/A
    # D: Se encarga de asignar los datos inciales del Sprite de los detalles del fondo

    def __set_menu_buttons(self):
        buttons = []
        button_img = self.__pygame.image.load(BUTTON_XL_IMG_PATH)

        buttons.append(Sprite(button_img, 400, 150, 0, 0))
        buttons.append(Sprite(button_img, 400, 230, 0, 0))
        buttons.append(Sprite(button_img, 400, 310, 0, 0))
        buttons.append(Sprite(button_img, 400, 390, 0, 0))

        self.__menu_buttons = buttons

    # E/S: N/A
    # D: Se encarga de renderizar los botones
    def __render_buttons(self):

        for button in self.__menu_buttons:
            self.__screen.blit(button.get_image(), (button.x, button.y))

    # E/S: N/A
    # D: Se encarga de asignarle un texto a los botones
    def __render_buttons_text(self):
        for text in self.__button_text:
            self.__screen.blit(text.get_image(), (text.x, text.y))

    # E/S: N/A
    # D: Detecta que boton se presiono para redirigir a otro menu
    def __button_events(self):
        buttons = self.__menu_buttons

        for i in range(0, len(buttons)):

            if is_sprite_pressed(self.__pygame, buttons[i]) and self.__click:
                play_sound_effect(self.__pygame, GAME_BUTTON_PRESSED, 1)

                if i == 0:
                    opts = Options(self.__pygame, self.__screen,
                                   self.__main_clock, False)

                    opts.start_options()

                elif i == 1:
                    opts = Options(self.__pygame, self.__screen,
                                   self.__main_clock, True)

                    opts.start_options()

                elif i == 2:
                    score = Score(self.__pygame, self.__screen,
                                  self.__main_clock)

                    score.open_scores()

                elif i == 3:
                    self.__pygame.quit()
                    sys.exit()
