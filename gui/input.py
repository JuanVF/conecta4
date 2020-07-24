import sys
import os  
import time

sys.path.append("..")

from conecta4.game.sprite import Sprite
from conecta4.constants import *
from conecta4.utils import *

class Input:

    # E: Una referencia a pygame, screen, dos enteros y un string opcional
    # S: N/A
    # D: Constructor de la clase
    def __init__(self, pygame, screen, x, y, hint=""):
        image = pygame.image.load(INPUT_IMG)
        font = pygame.font.Font(GAME_FONT2_PATH, 15)

        self.__pygame = pygame
        self.__screen = screen
        self.__sprite = Sprite(image, x, y, 0, 0)
        self.__is_active = False
        self.__text = ""
        self.__input = Sprite(font, x+30, y+20, 0, 0)
        self.__cursor = Sprite(None, x+35, y+25, 0, 0)
        self.__cursor_time = time.time() * 1000.0
        self.__hint = hint

    # E/S: N/A
    # D: Se encarga de renderizar el input
    def render(self):
        self.__screen.blit(self.__sprite.get_image(), (self.__sprite.x, self.__sprite.y))

        if self.__text != "":
            self.__screen.blit(self.__input.get_image().render(self.__text, True, COLOR_WHITE), (self.__input.x, self.__input.y))
        elif not self.__is_active:
            self.__screen.blit(self.__input.get_image().render(self.__hint, True, (174, 174, 174)), (self.__input.x, self.__input.y))

        if self.__is_active:
            self.__animate_cursor()

    # E/S: N/A
    # D: Se encarga de hacer la animacion del cursor
    def __animate_cursor(self):
        cursor = self.__pygame.Rect((self.__cursor.x, self.__cursor.y, 2, 50))

        start_pos = (self.__cursor.x, self.__cursor.y)
        end_pos = (self.__cursor.x, self.__cursor.y+40)

        time_since = time.time() * 1000.0 - self.__cursor_time

        if time_since <= 500:
            self.__pygame.draw.line(self.__screen, COLOR_WHITE, start_pos, end_pos, 3)
        elif 500 < time_since and time_since <= 1000:
            self.__pygame.draw.line(self.__screen, (0,0,0), start_pos, end_pos, 3)
        else:
            self.__cursor_time = time.time() * 1000

    # E: Una referencia a un evento y un booleano
    # S: N/A
    # D: Se encarga de detectar los eventos
    def detect_events(self, event, click):
        self.__detect_click(click)

        if self.__is_active:
            self.__detect_keyboard(event)

    # E: Una referencia a un evento
    # S: N/A
    # D: Detecta cuando un usuario escribe y a la vez mueve el cursor
    def __detect_keyboard(self, event):
        if event.type == self.__pygame.KEYDOWN:
            valid_ascii = event.unicode.isalpha() or event.unicode.isnumeric() or event.key == self.__pygame.K_SPACE
            
            if event.key == self.__pygame.K_RETURN:
                self.__is_active = False

            elif event.key == self.__pygame.K_BACKSPACE:
                self.__text = self.__text[:-1]

                if len(self.__text) > 0:
                    self.__cursor.x -= 14

            elif valid_ascii and len(self.__text) <= 40:
                self.__cursor.x += 14
                self.__text += str(event.unicode)

    # E: Un booleano
    # S: N/A
    # D: Se encarga de detectar si se dio click al input y activarlo
    def __detect_click(self, click):
        mx, my = self.__pygame.mouse.get_pos()

        pos1 = (self.__sprite.x, self.__sprite.y)
        pos2 = (self.__sprite.x + 700, self.__sprite.y + 90)
        pos3 = (mx, my)

        if click:
            self.__toggle_status(is_overlap(pos1, pos2, pos3))
    
    # E: N/A
    # S: Un string
    # D: Retorna el texto del input
    def get_text(self):
        return self.__text

    # E: Un booleano
    # S: N/A
    # D: Se encarga de setear el estado del input
    def __toggle_status(self, mode):
        self.__is_active = mode