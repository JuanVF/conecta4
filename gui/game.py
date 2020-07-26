import time

from conecta4.constants import *
from conecta4.game.animations import *
from conecta4.game.pc import *
from conecta4.game.physics import *
from conecta4.game.sprite import Sprite
from conecta4.utils import *
from conecta4.animations.game_animations import *

class Game:
    
    # E: Una referencia a Pygame, dos strings, un booleano (opcional) y un diccionario opcional
    # S: N/A
    # D: Constructor de la clase e inicializa variables
    def __init__(self, pygame, screen, clock, player1, player2, isIA=False, prev_game={}):
        # Carga de recursos multimedia
        self.__winner_sound = pygame.mixer.Sound(GAME_WIN_SOUND)
        self.__winner_sound.set_volume(1.15)

        self.__background = pygame.image.load(GAME_BACKGROUND)
        self.__keys_img = pygame.image.load(GAME_KEYS_PATH)
        self.__font = pygame.font.Font(GAME_FONT_PATH, 15)
        self.__coin_a = pygame.image.load(COIN_A_PATH)
        self.__coin_b = pygame.image.load(COIN_B_PATH)

        # Inicializacion de variables
        self.__game_clock = clock
        self.__screen = screen
        self.__pygame = pygame
        self.__isIa = isIA

        self.__mode = get_game_mode(isIA)

        self.__prev_game = prev_game

        self.__game_running = True

        self.__winner = 0
        self.__winner_loop_passed = False
        
        self.__turn_text = self.__font.render("Turno", True, COLOR_WHITE)
        self.__p1_turn_text = self.__font.render(player1, True, COLOR_WHITE)
        self.__p2_turn_text = self.__font.render(player2, True, COLOR_WHITE)
        
        self.__game_menu_buttons = set_game_menu_buttons(self.__pygame)

        self.__now = time.time()
        
        self.__current_game = eval(str(DEFAULT_GAME_STATUS))

        self.__current_game["player1"] = player1
        self.__current_game["player2"] = player2
        self.__current_game["id"] = get_latest_id(self.__mode)

    # E/S: N/A
    # D: Se encarga de iniciar el juego
    def start_game_mode(self):
        self.__load_prev_game()
        self.__game_loop()

    # E/S: N/A
    # D: Loop del juego
    def __game_loop(self):
        while self.__game_running:
            set_background(self.__screen, self.__background)

            self.__click = False
            self.__winner = detect_winner(self.__current_game["board"])
            
            self.__game_renders()

            for event in self.__pygame.event.get():
                self.__loop_events(event)

            self.__on_win()

            self.__pygame.display.update()
            self.__game_clock.tick(60)
    
    # E: Un evento de pygame
    # S: N/A
    # D: Detecta los eventos del loop
    def __loop_events(self, event):
        close_menu(self.__pygame, event)
        self.__click = detect_click(self.__pygame, event)

        if self.__winner == 0:
            self.__detect_game_events(event)

        self.__button_events()

    # E/S: N/A
    # D: Detecta que boton se presiono para redirigir a otro menu
    def __button_events(self):
        buttons = self.__game_menu_buttons

        for i in range(0, len(buttons)):
            if is_sprite_pressed(self.__pygame, buttons[i]) and self.__click:
                self.__button_pressed(i)
                
    
    # E: Un entero
    # S: N/A
    # D: Activa las funciones de cada respectivo boton
    def __button_pressed(self, index):
        play_sound_effect(self.__pygame, GAME_BUTTON_PRESSED, 1)

        if index == 0:
            self.__game_running = False

        elif index == 1:
            if self.__winner == 0:
                self.__save_current_game()
                self.__game_running = False

    # E/S: N/A
    # D: Se encarga de realizar todos los renders del juego
    def __game_renders(self):
        coins = self.__current_game["coins"]
        turn = self.__current_game["playerTurn"]

        lRender = self.__current_game["lRender"]
        dRender = self.__current_game["dRender"]

        render_indices(self.__pygame, self.__screen, lRender, dRender)

        render_coins(self.__screen, coins)
        render_coin_hider(self.__pygame, self.__screen)

        render_game_menu_buttons(self.__game_menu_buttons, self.__screen)
        render_menu_text(self.__pygame, self.__screen)

        self.__screen.blit(self.__keys_img, (25 ,260))
        self.__screen.blit(self.__turn_text, (25, 400))

        if turn:
            self.__screen.blit(self.__p2_turn_text, (25, 450))
        else:
            self.__screen.blit(self.__p1_turn_text, (25, 450))
    
    # E/S: N/A
    # D: Si un jugador gana, activa eventos del ganador
    def __on_win(self):
        if self.__winner != 0:
            p1_won = not self.__winner_loop_passed and self.__winner == 1
            p2_won = not self.__winner_loop_passed and self.__winner == 2
            is_a_previous_game = not self.__winner_loop_passed and len(self.__prev_game) != 0

            p1 = self.__current_game["player1"]
            p2 = self.__current_game["player2"]

            if p1_won:
                update_scores(p1)

            elif p2_won:
                update_scores(p2)

            if is_a_previous_game:
                game_id = self.__current_game["id"]
                mode = get_game_mode(self.__isIa)

                delete_game_by_id(game_id, mode)

            self.__winner_loop_passed = render_winner(self.__pygame, self.__screen, self.__winner_sound, self.__winner_loop_passed)
            render_winner_text(self.__pygame, self.__screen, self.__winner, p1, p2)

    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Detecta y activa los eventos del juego
    def __detect_game_events(self, event):
        player_turn = self.__current_game["playerTurn"]
        ia_playing = self.__isIa and player_turn

        self.__board_events(event)

        if ia_playing:
            ia_turn = predict_movement(self.__current_game["board"])

            self.__throw_coin(ia_turn)
        else:
            self.__player_events(event)

    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Detecta y activa los eventos de movimiento del tablero
    def __board_events(self, event):
        if event.type == self.__pygame.KEYDOWN:
            lRender = self.__current_game["lRender"]

            blLim = self.__current_game["blLim"]
            brLim = self.__current_game["brLim"]

            isRLInBoard = blLim <= lRender-1 <= brLim
            isRRInBoard = blLim <= lRender+7 <= brLim

            if event.key == self.__pygame.K_d and isRRInBoard:
                self.__current_game["coins"] = move_coins_x_pos(self.__current_game["coins"], True)
                self.__current_game["lRender"] += 1

            if event.key == self.__pygame.K_a and isRLInBoard:
                self.__current_game["coins"] = move_coins_x_pos(self.__current_game["coins"], False)
                self.__current_game["lRender"] -= 1

            if event.key == self.__pygame.K_w:
                if self.__current_game["dRender"] + 1 < self.__current_game["upLimit"] :
                    self.__current_game["coins"] = move_coins_y_pos(self.__current_game["coins"], True)
                    self.__current_game["dRender"] += 1

            if event.key == self.__pygame.K_s:
                if self.__current_game["dRender"] >= 1:
                    self.__current_game["coins"] = move_coins_y_pos(self.__current_game["coins"], False)
                    self.__current_game["dRender"] -= 1


    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Detecta y activa los eventos para tirar fichas
    def __player_events(self, event):
        if event.type == self.__pygame.KEYDOWN:
            lRender = self.__current_game["lRender"]
            blLim = self.__current_game["blLim"]
            
            pos = lRender + abs(blLim)
            
            if event.key == self.__pygame.K_1 or event.key == self.__pygame.K_KP1:
                self.__throw_coin(pos)
            
            if event.key == self.__pygame.K_2 or event.key == self.__pygame.K_KP2:
                self.__throw_coin(pos + 1)
                
            if event.key == self.__pygame.K_3 or event.key == self.__pygame.K_KP3:
                self.__throw_coin(pos + 2)
                
            if event.key == self.__pygame.K_4 or event.key == self.__pygame.K_KP4:
                self.__throw_coin(pos + 3)

            if event.key == self.__pygame.K_5 or event.key == self.__pygame.K_KP5:
                self.__throw_coin(pos + 4)
                
            if event.key == self.__pygame.K_6 or event.key == self.__pygame.K_KP6:
                self.__throw_coin(pos + 5)

            if event.key == self.__pygame.K_7 or event.key == self.__pygame.K_KP7:
                self.__throw_coin(pos + 6)
    
    # E: Un entero
    # S: N/A
    # D: Se encarga de tirar las monedas
    def __throw_coin(self, pos):
        player_turn = self.__current_game["playerTurn"]
        lRender = self.__current_game["lRender"]
        board = self.__current_game["board"]
        bLim = self.__current_game["blLim"]

        pos_in_board = (pos - abs(bLim)) - lRender

        coin = get_coin_sprite(player_turn, self.__coin_a, self.__coin_b)
        coin = calc_coin_initial_pos(coin, pos_in_board)

        height = get_pos_last_space(self.__current_game["board"][pos])
        lim = calc_coin_y_lim(self.__current_game["board"][pos])

        lim += self.__current_game["dRender"] * 95

        self.__current_game["board"] = add_coin_to_board(board, pos, player_turn)
        now = time.time()

        play_sound_effect(self.__pygame, COIN_DROP_SOUND, 1)
        drop_coin(self.__screen, coin, now, lim)

        self.__current_game["playerTurn"] = not player_turn
        self.__current_game["coins"].append([coin, now, lim])
        
        self.__modifyCoinLimits(pos - abs(bLim))
        self.__current_game["upLimit"] = get_highest_coin(self.__current_game["board"])
    
    # E: Un entero
    # S: N/A
    # D: Se encarga de determinar los extremos de columnas donde se tiraron monedas
    def __modifyCoinLimits(self, pos):
        left_excess = 7 - abs(pos - self.__current_game["blLim"])
        right_excess = 7 - abs(self.__current_game["brLim"] - pos)

        if self.__current_game["first_try"]:
            self.__current_game["lLim"] = pos
            self.__current_game["rLim"] = pos
            
            self.__current_game["board"] = add_n_board_cols(self.__current_game["board"], pos+1, False)
            self.__current_game["board"] = add_n_board_cols(self.__current_game["board"], 7-pos, True)

            self.__current_game["blLim"] -= left_excess
            self.__current_game["brLim"] += right_excess

            self.__current_game["first_try"] = False

        elif pos < self.__current_game["lLim"]:
            self.__current_game["lLim"] = pos
            
            self.__current_game["board"] = add_n_board_cols(self.__current_game["board"], left_excess, True)

            self.__current_game["blLim"] -= left_excess

        elif pos > self.__current_game["rLim"]:
            self.__current_game["rLim"] = pos

            self.__current_game["board"] = add_n_board_cols(self.__current_game["board"], right_excess, False) 

            self.__current_game["brLim"] += right_excess

    # E/S: N/A
    # D: Permite restaurar una partida anterior
    def __load_prev_game(self):
        pg = self.__prev_game

        if len(pg) > 0:
            self.__current_game = eval(str(pg))
            self.__current_game["coins"] = []

            for coin in pg["coins"]:
                current_coin = []
                if coin[0]["type"] == True:
                    current_coin = Sprite(self.__coin_b, coin[0]["x"], coin[0]["y"], coin[0]["x_change"], coin[0]["y_change"], desc="b")
                else:
                    current_coin = Sprite(self.__coin_a, coin[0]["x"], coin[0]["y"], coin[0]["x_change"], coin[0]["y_change"], desc="a")

                self.__current_game["coins"].append([current_coin, coin[1], coin[2]])

    # E/S: N/A
    # D: Guarda un juego actual
    def __save_current_game(self):
        new_game = self.__current_game
        
        coins = []

        for coin in self.__current_game["coins"]:
            dic = {
                    "type"    : True, 
                    "x"       : coin[0].x, 
                    "y"       : coin[0].y,
                    "x_change": coin[0].x_change,
                    "y_change": coin[0].y_change
                }

            current_coin = [
                eval(str(dic)), 
                coin[1], 
                coin[2]
            ]

            if coin[0].desc == "a":
                current_coin[0]["type"] = False
            else:
                current_coin[0]["type"] = True
                
            coins.append(current_coin)

        new_game["coins"] = coins
        mode = get_game_mode(self.__isIa)

        save_current_game(self.__prev_game, new_game, mode)
        
