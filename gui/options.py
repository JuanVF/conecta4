from conecta4.game.sprite import Sprite

from conecta4.utils import *
from conecta4.constants import *

from conecta4.gui.game import Game
from conecta4.gui.input import Input

from conecta4.animations.options_animations import *

p1_hint = "Escriba el nombre del jugador 1..."

new_game_pos1 = (720, 272)
new_game_pos2 = (920, 342)

class Options:

    # E: Una referencia a pygame y screen, y dos booleanos
    # S: N/A
    # D: Constructor de la clase
    def __init__(self, pygame, screen, clock, isIa):

        # Recursos multimedia
        self.__font2 = pygame.font.Font(GAME_FONT2_PATH, 22)
        self.__font = pygame.font.Font(GAME_FONT_PATH, 22)

        self.__button_img = pygame.image.load(BUTTON_XL_IMG_PATH)

        self.__game_container_img = pygame.image.load(GAME_SAVE_CONTAINER)
        self.__button_move_left = Sprite(pygame.image.load(GAME_MOVE_LEFT), 0, 400, 0, 0)
        self.__button_move_right = Sprite(pygame.image.load(GAME_MOVE_RIGHT), 930, 400, 0, 0)

        self.__back_button = Sprite(pygame.image.load(GAME_BACK_BUTTON), 10, 10, 0, 0)

        # Variables iniciales
        self.__mode = get_game_mode(isIa)
        self.__pygame = pygame
        self.__clock = clock
        self.__screen = screen
        self.__isIa = isIa

        self.__running = True
        self.__click = False

        self.__input_p1_title = self.__font2.render("Jugador 1", True, COLOR_WHITE)
        self.__input_p2_title = self.__font2.render("Jugador 2", True, COLOR_WHITE)

        self.__back_button_title = self.__font.render("Volver", True, COLOR_WHITE)

        self.__play_button_title = self.__font.render("Jugar", True, COLOR_WHITE)

        self.__game_container_x_move = 0

        self.__input_p1 = Input(pygame, screen, 20, 130, p1_hint)

        self.__input_p2 = set_input_p2(pygame, screen, isIa)

        self.__load_games()

    # E/S: N/A
    # D: Inicia el menu de opciones
    def start_options(self):
        self.__loop()

    # E/S: N/A
    # D: Loop de la clase
    def __loop(self):
        while self.__running:
            self.__screen.fill((0, 0, 0))
            
            render_buttons(self.__screen, self.__back_button_title, self.__back_button, self.__button_img, self.__play_button_title)
            render_input_title(self.__screen, self.__isIa, self.__input_p1_title, self.__input_p2_title)
            render_inputs(self.__screen, self.__isIa, self.__input_p1, self.__input_p2)
            render_saved_games(self.__screen, self.__game_container_x_move, self.__p1s, self.__p2s, self.__vs, self.__game_container_img)
            
            self.__screen.blit(self.__button_move_left.get_image(), (self.__button_move_left.x, self.__button_move_left.y))
            self.__screen.blit(self.__button_move_right.get_image(), (self.__button_move_right.x, self.__button_move_right.y))

            self.__click = False

            for event in self.__pygame.event.get():
                self.__loop_events(event)

            self.__pygame.display.update()
            self.__clock.tick(60)

    # E: Un evento de pygame
    # S: N/A
    # D: Detecta los eventos del juego
    def __loop_events(self, event):
        close_menu(self.__pygame, event)
        self.__click = detect_click(self.__pygame, event)

        self.__input_p1.detect_events(event, self.__click)

        if not self.__isIa:
            self.__input_p2.detect_events(event, self.__click)

        self.__back_button_click(self.__click)

        self.__list_events()
        self.__start_game()

    # E/S: N/A
    # D: Detecta los eventos para mover la lista
    def __list_events(self):
        if self.__click:
            length = get_mode_length(self.__isIa, self.__saved_games) * -90
            r_pressed = is_sprite_pressed(self.__pygame, self.__button_move_right, x=70, y=150)
            l_pressed = is_sprite_pressed(self.__pygame, self.__button_move_left, x=70, y=150)

            self.__game_container_x_move = move_list_to_right(self.__game_container_x_move, length, r_pressed)
            self.__game_container_x_move = move_list_to_left(self.__game_container_x_move, l_pressed)

    # E/S: N/A
    # D: Inicia el juego
    def __start_game(self):
        mx, my = self.__pygame.mouse.get_pos()
        mouse_pos = (mx, my)

        new_game_pressed = is_overlap(new_game_pos1, new_game_pos2, mouse_pos)

        if self.__click and new_game_pressed:
            self.__new_game_event({})

        elif self.__click:
            game = self.__detect_saved_game_click(mouse_pos)

            if len(game) != 0:
                self.__new_game_event(game)

    # E: Un diccionario
    # S: N/A
    # D: Inicia un nuevo juego
    def __new_game_event(self, prev_game):
        p1 = get_p1_name(self.__input_p1)
        p2 = get_p2_name(self.__input_p2, self.__isIa)

        game = Game(self.__pygame, self.__screen, self.__clock, p1, p2, self.__isIa, prev_game=prev_game)

        play_sound_effect(self.__pygame, GAME_BUTTON_PRESSED, 1)
        game.start_game_mode()

        self.__load_games()
    
    # E: Una tupla
    # S: Un diccionario
    # D: Retorna la partida si se detecta un click sobre alguna de ellas
    def __detect_saved_game_click(self, mouse_pos):
        mx = mouse_pos[0]
        x_cont = 90
        y = 400

        rest_x = (0 <= mx and mx <= 70) or (930 <= mx and mx <= 1000)

        length = get_mode_length(self.__isIa, self.__saved_games)

        for i in range(0, length):
            pos1 = (x_cont + self.__game_container_x_move, y)
            pos2 = (x_cont + self.__game_container_x_move + 300, y+150)

            if is_overlap(pos1, pos2, mouse_pos) and not rest_x:
                return self.__saved_games[self.__mode][i]

            x_cont += 320

        return {}
    
    # E/S: N/A
    # D: Carga las partidas guardadas
    def __load_games(self):
        self.__saved_games = find_games()
        self.__p1s, self.__p2s, self.__vs = set_saved_games(self.__isIa, self.__saved_games, self.__font2)

    # E: Un booleano
    # S: N/A
    # D: Se encarga de regresar al menu principal
    def __back_button_click(self, click):
        if click and is_sprite_pressed(self.__pygame, self.__back_button, x=80, y=60):
            play_sound_effect(self.__pygame, GAME_BUTTON_PRESSED, 1)

            self.__running = False
