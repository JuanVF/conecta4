import sys
import os  

sys.path.append("..")

from conecta4.services.constants import *
from conecta4.services.sprite import Sprite

class Menu:
    # E: Una referencia a pygame
    # S: N/A
    # D: Constructor
    def __init__(self, pygame):
        self._pygame = pygame
        self._isRunning = True
    
    # E/S: N/A
    # D: Inicia el juego y determina ciertos parametros iniciales
    def start_game(self):
        self._set_default_configs()
        self._set_background_animations()
        self._set_menu_buttons()
        self._game_loop()

    # E/S: N/A
    # D: Se encarga de configurar valores por defecto del menu
    def _set_default_configs(self):
        #Esta funcion se encarga de centrar la ventana
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        icon = self._pygame.image.load(GAME_LOGO_PATH)

        self._background = self._pygame.image.load(MENU_BACKGROUND_PATH)

        self._screen = self._pygame.display.set_mode(MENU_WINDOW_SIZE)
        self._pygame.display.set_caption("4 en linea")
        self._pygame.display.set_icon(icon)

    # E/S: N/A
    # D: Loop
    def _game_loop(self):
        while self._isRunning:
            self._set_background()
            self._background_animation()

            self._screen.blit(self._menu_buttons[0].get_image(), (self._menu_buttons[0].x, self._menu_buttons[0].y))
            self._screen.blit(self._menu_buttons[1].get_image(), (self._menu_buttons[1].x, self._menu_buttons[1].y))

            for event in self._pygame.event.get():
                self._close_menu(event)

            self._pygame.display.update()

    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Dado un evento, cierra el juego si se oprime el boton de salir
    def _close_menu(self, event):
        if event.type == self._pygame.QUIT:
            self._isRunning = False

    # E/S: N/A
    # D: Se encarga de asignar el background del menu
    def _set_background(self):
        self._screen.blit(self._background, (0,0))
    
    # E/S: N/A
    # D: Se encarga de asignar los datos inciales del Sprite de los detalles del fondo
    def _set_menu_buttons(self):
        button_img = self._pygame.image.load(BUTTON_IMG_PATH)

        button1 = Sprite(button_img, 120, 150, 0, 0)
        button2 = Sprite(button_img, 120, 230, 0, 0)

        self._menu_buttons = [button1, button2]

    # E/S: N/A
    # D: Se encarga de asignar los datos inciales del Sprite de los detalles del fondo
    def _set_background_animations(self):
        background_detail = self._pygame.image.load(MENU_BG_DETAILS_PATH)

        bg_detail1 = Sprite(background_detail, -245, 0, MENU_BG_DETAILS_SPEED, 0)
        bg_detail2 = Sprite(background_detail, 340, 0, MENU_BG_DETAILS_SPEED, 0)

        self._bg_details = [bg_detail1, bg_detail2]

    # E/S: N/A
    # D: Se encarga de animar los Sprites de los detalles del fondo
    def _background_animation(self):
        x = self._bg_details[0].x
        x_change = self._bg_details[0].x_change

        if x > -235:
            x_change = -MENU_BG_DETAILS_SPEED
        elif x < -255:
            x_change = MENU_BG_DETAILS_SPEED
        
        for i in range(0, len(self._bg_details)):
            self._bg_details[i].x_change = x_change
            self._bg_details[i].x += x_change

            img = self._bg_details[i].get_image()
            x = self._bg_details[i].x
            y = self._bg_details[i].y

            self._screen.blit(img, (x,y))
