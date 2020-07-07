import sys
import os  

sys.path.append("..")

from conecta4.services.constants import *
from conecta4.services.sprite import Sprite
from conecta4.utils import is_overlap

class Menu:
    # E: Una referencia a pygame
    # S: N/A
    # D: Constructor
    def __init__(self, pygame):
        self._isRunning = True
        self._click = False

        #Esta funcion se encarga de centrar la ventana
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        icon = pygame.image.load(GAME_LOGO_PATH)

        self._background = pygame.image.load(MENU_BACKGROUND_PATH)
        
        self._screen = pygame.display.set_mode(MENU_WINDOW_SIZE)

        self._pygame = pygame
        self._pygame.display.set_caption("4 en linea")
        self._pygame.display.set_icon(icon)
    
    # E/S: N/A
    # D: Inicia el juego y determina ciertos parametros iniciales
    def start_game(self):
        self._set_background_animations()

        self._set_menu_buttons()

        self._game_loop()

    # E/S: N/A
    # D: Loop
    def _game_loop(self):
        while self._isRunning:
            self._set_background()
            self._background_animation()

            self._render_buttons()
            self._render_buttons_text()

            self._button_events()

            for event in self._pygame.event.get():
                self._close_menu(event)

            self._click = False
            self._detect_click(event)

            self._pygame.display.update()

    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Dado un evento, cierra el juego si se oprime el boton de salir
    def _close_menu(self, event):
        if event.type == self._pygame.QUIT:
            self._isRunning = False

    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Dado un evento, detecta si hay click
    def _detect_click(self, event):
        if event.type == self._pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._click = True

    # E/S: N/A
    # D: Se encarga de asignar el background del menu
    def _set_background(self):
        self._screen.blit(self._background, (0,0))

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

    # E/S: N/A
    # D: Se encarga de asignar los datos inciales del Sprite de los detalles del fondo
    def _set_menu_buttons(self):
        button_img = self._pygame.image.load(BUTTON_XL_IMG_PATH)

        button1 = Sprite(button_img, 100, 150, 0, 0)
        button2 = Sprite(button_img, 100, 230, 0, 0)
        button3 = Sprite(button_img, 100, 310, 0, 0)
        button4 = Sprite(button_img, 100, 390, 0, 0)

        self._menu_buttons = [button1, button2, button3, button4]

    # E/S: N/A
    # D: Se encarga de renderizar los botones
    def _render_buttons(self):
        for button in self._menu_buttons:
            self._screen.blit(button.get_image(), (button.x, button.y))

    # E/S: N/A
    # D: Se encarga de asignarle un texto a los botones
    def _render_buttons_text(self):
        font = self._pygame.font.Font(GAME_FONT_PATH, 20)

        normal_mode_text = font.render("1 vs 1", True, COLOR_WHITE)
        vs_pc_mode = font.render("1 vs PC", True, COLOR_WHITE)
        log_menu = font.render("Puntajes", True, COLOR_WHITE)
        exit_menu = font.render("Salir", True, COLOR_WHITE)

        self._screen.blit(normal_mode_text, (155, 175))
        self._screen.blit(vs_pc_mode, (140, 255))
        self._screen.blit(log_menu, (125, 333))
        self._screen.blit(exit_menu, (150, 410))

    # E/S: N/A
    # D: Detecta que boton se presiono para redirigir a otro menu
    def _button_events(self):
        buttons = self._menu_buttons
        for i in range(0, len(buttons)):
            if self._is_button_pressed(buttons[i]) and self._click:
                if i == 0:
                    print("Juego principal")
                elif i == 1:
                    print("Juego contra IA")
                    pass
                elif i == 2:
                    print("Puntajes")
                    pass
                elif i == 3:
                    self._isRunning = False

    # E: Un Sprite
    # S: Un booleano
    # D: Si el mouse dio click sobre un boton retorna True
    def _is_button_pressed(self, button):
        mx, my = self._pygame.mouse.get_pos()

        pos1 = (button.x, button.y)
        pos2 = (button.x + 200, button.y + 70)
        pos3 = (mx, my)

        overlap = is_overlap(pos1, pos2, pos3)

        return overlap

