import sys
import os  

sys.path.append("..")

from conecta4.gui.input import Input
from conecta4.constants import *
from conecta4.utils import *
from conecta4.game.sprite import Sprite

class Options:
    def __init__(self, pygame, screen, clock, isIa):
        self.__pygame = pygame
        self.__clock = clock
        self.__screen = screen
        self.__isIa = isIa

        self.__running = True
        self.__click = False

        self.__font2 = pygame.font.Font(GAME_FONT2_PATH, 22)
        self.__font = pygame.font.Font(GAME_FONT_PATH, 22)

        self.__input_p1_txt = self.__font2.render("Jugador 1", True, COLOR_WHITE)
        self.__input_p2_txt = self.__font2.render("Jugador 2", True, COLOR_WHITE)
        self.__back_button_txt = self.__font.render("Volver", True, COLOR_WHITE)

        self.__saved_games = {}
        self.__game_container_img = pygame.image.load(GAME_SAVE_CONTAINER)

        self.__game_move_left = Sprite(pygame.image.load(GAME_MOVE_LEFT), 0, 400, 0, 0)
        self.__game_move_right = Sprite(pygame.image.load(GAME_MOVE_RIGHT), 930, 400, 0, 0)

        self.__game_container_x_move = 0

        self.__back_button = Sprite(pygame.image.load(GAME_BACK_BUTTON), 10, 10, 0, 0)

    def start_options(self):
        self.__input_p1 = Input(self.__pygame, self.__screen, 20, 130, "Escriba el nombre del jugador 1...")
        self.__input_p2 = Input(self.__pygame, self.__screen, 20, 260, "Escriba el nombre del jugador 2...")

        self.__load_saved_games()

        self.__loop()

    def __loop(self):
        while self.__running:
            self.__screen.fill((0, 0, 0))
            
            self.__screen.blit(self.__input_p1_txt, (40, 80))
            self.__screen.blit(self.__input_p2_txt, (40, 210))
            self.__screen.blit(self.__back_button_txt, (100, 25))
            self.__screen.blit(self.__back_button.get_image(), (self.__back_button.x, self.__back_button.y))

            self.__input_p1.render()   
            self.__input_p2.render()

            self.__render_saved_games()

            self.__screen.blit(self.__game_move_left.get_image(), (self.__game_move_left.x, self.__game_move_left.y))
            self.__screen.blit(self.__game_move_right.get_image(), (self.__game_move_right.x, self.__game_move_right.y))

            self.__click = False
            
            for event in self.__pygame.event.get():
                self.__close_menu(event)
                self.__click = detect_click(self.__pygame, event)

                self.__input_p1.detect_events(event, self.__click)
                self.__input_p2.detect_events(event, self.__click)

                self.__back_button_click(self.__click)

                self.__move_left_saved_games()
                self.__move_right_saved_games()
                self.__detect_saved_game_click()

            self.__pygame.display.update()
            self.__clock.tick(60)

    def __load_saved_games(self):
        saved_games = eval(read(SAVED_GAMES))
        length = 0
        if saved_games != "":
            self.__saved_games = saved_games

    def __move_left_saved_games(self):
        pressed = is_sprite_pressed(self.__pygame, self.__game_move_left, x=70, y=150)

        if self.__click and pressed and self.__game_container_x_move < 0:
            self.__game_container_x_move += 70

    def __move_right_saved_games(self):
        length = self.__get_mode_length() * -90

        pressed = is_sprite_pressed(self.__pygame, self.__game_move_right, x=70, y=150)

        if self.__click and pressed and self.__game_container_x_move >= length:
            self.__game_container_x_move -= 70

    def __render_saved_games(self):
        x_cont = 90
        length = self.__get_mode_length()

        mode = "PVP"

        if self.__isIa:
            mode = "PV1"

        for i in range(0, length):
            pos = (x_cont + self.__game_container_x_move, 400)

            p1 = self.__font2.render(self.__saved_games[mode][i]["player1"], True, COLOR_WHITE)
            p1_pos = ((30 + x_cont + self.__game_container_x_move, 400))

            p2 = self.__font2.render(self.__saved_games[mode][i]["player2"], True, COLOR_WHITE)
            p2_pos = ((30 + x_cont + self.__game_container_x_move, 480))

            vs = self.__font2.render("VS", True, (255, 234, 55))
            vs_pos = ((30 + x_cont + self.__game_container_x_move, 440))

            self.__screen.blit(self.__game_container_img, pos)

            self.__screen.blit(p1, p1_pos)
            self.__screen.blit(p2, p2_pos)
            self.__screen.blit(vs, vs_pos)

            x_cont += 320

    def __detect_saved_game_click(self):
        if self.__click:
            x_cont = 90
            y = 400
            mx, my = self.__pygame.mouse.get_pos()
            rest_x = (0 <= mx and mx <= 70) or (930 <= mx and mx <= 1000)

            pos3 = (mx, my)

            length = self.__get_mode_length()

            mode = "PVP"

            if self.__isIa:
                mode = "PV1"

            for i in range(0, length):
                pos1 = (x_cont + self.__game_container_x_move, y)
                pos2 = (x_cont + self.__game_container_x_move + 300, y+150)

                if is_overlap(pos1, pos2, pos3) and not rest_x:
                    pass
                    # TODO: Conexion con el juego

                x_cont += 320

    def __get_mode_length(self):
        mode = "PVP"
        length = 0 

        if self.__isIa:
            mode = "PV1"
            length = len(self.__saved_games[mode])
        else:
            length = len(self.__saved_games[mode])

        return length


    # E: Un booleano
    # S: N/A
    # D: Se encarga de regresar al menu principal
    def __back_button_click(self, click):
        if click and is_sprite_pressed(self.__pygame, self.__back_button, x=80, y=60):
            play_sound_effect(self.__pygame, GAME_BUTTON_PRESSED, 1)

            self.__running = False

    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Dado un evento, cierra el juego si se oprime el boton de salir
    def __close_menu(self, event):
        if event.type == self.__pygame.QUIT:
            self.__pygame.quit()
            sys.exit()