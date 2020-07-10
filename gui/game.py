import sys
import time 

sys.path.append("..")

from conecta4.constants import *
from conecta4.game.sprite import Sprite
from conecta4.utils import *
from conecta4.game.animations import drop_coin

class Game:
    
    # E: Una referencia a Pygame, dos strings, un booleano (opcional)
    # S: N/A
    # D: Constructor de la clase e inicializa variables
    def __init__(self, pygame, screen, clock, player1, player2, isIA=False):
        self.__player1 = player1
        self.__player2 = player2
        self.__game_running = True

        self.__game_clock = clock
        self.__background = pygame.image.load(GAME_BACKGROUND)

        self.__screen = screen
        self.__pygame = pygame

        
    # E/S: N/A
    # D: Se encarga de iniciar el juego
    def start_game_mode(self):
        self.__set_game_menu_buttons()
        self.__coin = Sprite(self.__pygame.image.load(COIN_A_PATH), 235, 0, 0, 0)
        self.__now = time.time()
        play_sound_effect(self.__pygame, COIN_DROP_SOUND)
        self.__game_loop()

    # E/S: N/A
    # D: Loop del juego
    def __game_loop(self):
        self.__now = time.time()

        while self.__game_running:
            self.__set_background()
            drop_coin(self.__screen, self.__coin, self.__now)

            self.__render_game_menu_buttons()
            self.__render_buttons_text()

            self.__click = False
            

            for event in self.__pygame.event.get():
                self.__close_menu(event)
                self.__click = detect_click(self.__pygame, event)

            self.__button_events()
            self.__pygame.display.update()
            self.__game_clock.tick(60)

    # E/S: N/A
    # D: Setea las posiciones de los botones del menu
    def __set_game_menu_buttons(self):
        buttons = []
        button_img = self.__pygame.image.load(BUTTON_IMG_PATH)

        buttons.append(Sprite(button_img, 20, 20, 0, 0))
        buttons.append(Sprite(button_img, 20, 120, 0, 0))

        self.__game_menu_buttons = buttons

    # E/S: N/A
    # D: Renderiza los botones del menu
    def __render_game_menu_buttons(self):
        for button in self.__game_menu_buttons:
            self.__screen.blit(button.get_image(),(button.x, button.y))


    # E/S: N/A
    # D: Se encarga de asignarle un texto a los botones
    def __render_buttons_text(self):
        font = self.__pygame.font.Font(GAME_FONT_PATH, 17)

        texts = []
        texts.append(Sprite(font.render("Volver", True, COLOR_WHITE), 42, 45, 0, 0))
        texts.append(Sprite(font.render("Guardar", True, COLOR_WHITE), 38, 145, 0, 0))

        for text in texts:
            self.__screen.blit(text.get_image(), (text.x, text.y))

    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Dado un evento, cierra el juego si se oprime el boton de salir
    def __close_menu(self, event):
        if event.type == self.__pygame.QUIT:
            self.__pygame.quit()
            sys.exit()

    # E/S: N/A
    # D: Asigna el fondo
    def __set_background(self):
        self.__screen.fill((0, 0, 0))
        self.__screen.blit(self.__background, (200,0))

    # E/S: N/A
    # D: Detecta que boton se presiono para redirigir a otro menu
    def __button_events(self):
        buttons = self.__game_menu_buttons

        for i in range(0, len(buttons)):
            if is_sprite_pressed(self.__pygame, buttons[i]) and self.__click:

                play_sound_effect(self.__pygame, GAME_BUTTON_PRESSED)

                if i == 0:
                    self.__game_running = False

                elif i == 1:
                    pass