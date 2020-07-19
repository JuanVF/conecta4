import sys
import time 
from pprint import pprint

sys.path.append("..")

from conecta4.constants import *
from conecta4.game.sprite import Sprite
from conecta4.utils import *
from conecta4.game.animations import *
from conecta4.game.physics import *

class Game:
    
    # E: Una referencia a Pygame, dos strings, un booleano (opcional)
    # S: N/A
    # D: Constructor de la clase e inicializa variables
    def __init__(self, pygame, screen, clock, player1, player2, isIA=False):
        self.__player1 = player1
        self.__player2 = player2
        self.__game_running = True
        self.__winner = 0
        self.__winner_sound = pygame.mixer.Sound("src/winner (1).ogg")
        self.__winner_sound.set_volume(1.15)
        self.__winner_sound_played = False

        self.__game_clock = clock
        self.__background = pygame.image.load(GAME_BACKGROUND)
        self.__keys_img = pygame.image.load(GAME_KEYS_PATH)
        self.__screen = screen
        self.__pygame = pygame

        # En el primer intento el rLim nunca va ser menor que -99 y el lLim mayor que 99 
        self.__lLim = 99
        self.__rLim = -99
        self.__blLim = 0
        self.__brLim = 6
        self.__lRender = 0
        self.__player_turn = False
        self.__first_try = True
        
        # No multiplique las listas porque me daba errores de direccion de memoria
        # Pasa que todas las listas tenian la misma direccion en memoria
        self.__board = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0], [0,0,0,0,0,0]]
        self.__coins = []

        self.__coin_a = self.__pygame.image.load(COIN_A_PATH)
        self.__coin_b = self.__pygame.image.load(COIN_B_PATH)
        
    # E/S: N/A
    # D: Se encarga de iniciar el juego
    def start_game_mode(self):
        self.__set_game_menu_buttons()
        self.__game_loop()

    # E/S: N/A
    # D: Loop del juego
    def __game_loop(self):
        self.__now = time.time()

        while self.__game_running:
            self.__set_background()

            self.__render_game_menu_buttons()
            self.__render_menu_text()
            self.__screen.blit(self.__keys_img, (25 ,260))
            self.__click = False

            self.__winner = detect_winner(self.__board)

            
            for event in self.__pygame.event.get():
                self.__close_menu(event)
                self.__click = detect_click(self.__pygame, event)

                if self.__winner == 0:
                    self.__detect_game_events(event)
            
            self.__button_events()

            self.__render_coins()
            
            if self.__winner != 0:
                self.__render_winner()

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

    def __render_winner(self):
        # TODO: Refactorizador todo esto
        s = self.__pygame.Surface((800,600))

        s.set_alpha(128)
        s.fill((0,0,0))
        self.__screen.blit(s, (200,0)) 

        font = self.__pygame.font.Font(GAME_FONT_PATH, 22)
        txt = Sprite(font.render("Ganador Jugador: ", True, COLOR_WHITE), 370, 450, 0, 0)
        self.__screen.blit(txt.get_image(), (txt.x, txt.y))
        winner = self.__pygame.image.load("src/winner.png")
        self.__screen.blit(winner, (370,200))

        if not self.__winner_sound_played:
            self.__pygame.mixer.init()
            self.__pygame.mixer.Channel(1).play(self.__winner_sound)

            self.__winner_sound_played = True

    # E/S: N/A
    # D: Se encarga de asignarle un texto a los botones
    def __render_menu_text(self):
        font = self.__pygame.font.Font(GAME_FONT_PATH, 17)

        texts = []
        texts.append(Sprite(font.render("Volver", True, COLOR_WHITE), 42, 45, 0, 0))
        texts.append(Sprite(font.render("Guardar", True, COLOR_WHITE), 38, 145, 0, 0))
        texts.append(Sprite(font.render("Teclas", True, COLOR_WHITE), 48, 230, 0, 0))

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

                play_sound_effect(self.__pygame, GAME_BUTTON_PRESSED, 1)

                if i == 0:
                    self.__game_running = False

                elif i == 1:
                    pass
    
    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Detecta y activa los eventos del juego
    def __detect_game_events(self, event):
        self.__board_events(event)
        self.__player_events(event)

    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Detecta y activa los eventos de movimiento del tablero
    def __board_events(self, event):
        if event.type == self.__pygame.KEYDOWN:
            isRLInBoard = self.__blLim <= self.__lRender-1 and self.__lRender-1 <= self.__brLim
            isRRInBoard = self.__blLim <= self.__lRender+7 and self.__lRender+7 <= self.__brLim

            if event.key == self.__pygame.K_d and isRRInBoard:
                self.__coins = move_coins_x_pos(self.__coins, True)
                self.__lRender += 1

            if event.key == self.__pygame.K_a and isRLInBoard:
                self.__coins = move_coins_x_pos(self.__coins, False)
                self.__lRender -= 1

            if event.key == self.__pygame.K_w:
                pprint(self.__board)
                print("w")
                
            if event.key == self.__pygame.K_s:
                print("s")

    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Detecta y activa los eventos para tirar fichas
    def __player_events(self, event):
        if event.type == self.__pygame.KEYDOWN:
            if event.key == self.__pygame.K_1 or event.key == self.__pygame.K_KP1:
                self.__throw_coin(self.__lRender)
            
            if event.key == self.__pygame.K_2 or event.key == self.__pygame.K_KP2:
                self.__throw_coin(self.__lRender + 1)
                
            if event.key == self.__pygame.K_3 or event.key == self.__pygame.K_KP3:
                self.__throw_coin(self.__lRender + 2)
                
            if event.key == self.__pygame.K_4 or event.key == self.__pygame.K_KP4:
                self.__throw_coin(self.__lRender + 3)

            if event.key == self.__pygame.K_5 or event.key == self.__pygame.K_KP5:
                self.__throw_coin(self.__lRender + 4)
                
            if event.key == self.__pygame.K_6 or event.key == self.__pygame.K_KP6:
                self.__throw_coin(self.__lRender + 5)

            if event.key == self.__pygame.K_7 or event.key == self.__pygame.K_KP7:
                self.__throw_coin(self.__lRender + 6)
    
    # E: Un entero
    # S: N/A
    # D: Se encarga de tirar las monedas
    def __throw_coin(self, pos):
        if self.__player_turn:
            coin = Sprite(self.__coin_b, 0, 0, 0, 0)
        else:
            coin = Sprite(self.__coin_a, 0, 0, 0, 0)

        coin = calc_coin_initial_pos(coin, pos - self.__lRender)

        lim = calc_coin_y_lim(self.__board[pos + abs(self.__blLim)])

        self.__board = add_coin_to_board(self.__board, pos + abs(self.__blLim), self.__player_turn)
        now = time.time()

        play_sound_effect(self.__pygame, COIN_DROP_SOUND, 1)
        drop_coin(self.__screen, coin, now, lim)

        self.__player_turn = not self.__player_turn
        self.__coins.append([coin, now, lim ])
        
        self.__modifyCoinLimits(pos)

    # E: Un entero
    # S: N/A
    # D: Se encarga de determinar los extremos de columnas donde se tiraron monedas
    def __modifyCoinLimits(self, pos):
        left_excess = 7 - abs(pos - self.__blLim)
        right_excess = 7 - abs(self.__brLim - pos)

        if self.__first_try:
            self.__lLim = pos
            self.__rLim = pos
            
            self.__board = add_n_board_cols(self.__board, pos+1, False)
            self.__board = add_n_board_cols(self.__board, 7-pos, True)

            self.__blLim -= left_excess
            self.__brLim += right_excess

            self.__first_try = False

        elif pos < self.__lLim:
            self.__lLim = pos
            
            self.__board = add_n_board_cols(self.__board, left_excess, True)

            self.__blLim -= left_excess

        elif pos > self.__rLim:
            self.__rLim = pos

            self.__board = add_n_board_cols(self.__board, right_excess, False) 

            self.__brLim += right_excess

    # E/S: N/A
    # D: Se encarga de renderizar las monedas
    def __render_coins(self):
        for coin in self.__coins:
            drop_coin(self.__screen, coin[0], coin[1], coin[2])