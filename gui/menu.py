import sys
import os  

sys.path.append("..")

from conecta4.constants import *
from conecta4.game.sprite import Sprite
from conecta4.utils import *
from conecta4.gui.game import Game
from pygame import mixer

class Menu:
    # E: Una referencia a pygame
    # S: N/A
    # D: Constructor
    def __init__(self, pygame):
        self.__isRunning = True
        self.__click = False

        #Esta funcion se encarga de centrar la ventana
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        self.__main_clock = pygame.time.Clock()

        icon = pygame.image.load(GAME_LOGO_PATH)

        mixer.music.load(GAME_BACKGROUND_MUSIC)
        mixer.music.set_volume(0.0)
        mixer.music.play(-1)

        self.__background = pygame.image.load(MENU_BACKGROUND_PATH)
        
        self.__screen = pygame.display.set_mode(MENU_WINDOW_SIZE)

        self.__pygame = pygame
        self.__pygame.display.set_caption("4 en linea")
        self.__pygame.display.set_icon(icon)
    
    # E/S: N/A
    # D: Inicia el juego y determina ciertos parametros iniciales
    def start_game(self):
        self.__set_background_animation_1()
        self.__set_background_animation_2()

        self.__set_menu_buttons()

        self.__game_loop()

    # E/S: N/A
    # D: Loop
    def __game_loop(self):
        while self.__isRunning:
            self.__set_background()

            self.__background_animation_2_base()
            self.__background_animation_2()
            self.__background_animation_1()

            self.__render_buttons()
            self.__render_buttons_text()

            self.__button_events()

            self.__click = False

            for event in self.__pygame.event.get():
                self.__close_menu(event)
                self.__click = detect_click(self.__pygame, event)


            self.__pygame.display.update()
            self.__main_clock.tick(60)

    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Dado un evento, cierra el juego si se oprime el boton de salir
    def __close_menu(self, event):

        if event.type == self.__pygame.QUIT:

            self.__pygame.quit()
            sys.exit()

    # E/S: N/A
    # D: Se encarga de asignar el background del menu
    def __set_background(self):

        self.__screen.fill((16, 15, 15))
        self.__screen.blit(self.__background, (300,0))

    # E/S: N/A
    # D: Se encarga de asignar los datos inciales del Sprite de los detalles del fondo
    def __set_background_animation_1(self):

        background_detail = self.__pygame.image.load(MENU_BG_DETAILS_PATH)

        bg_detail1 = Sprite(background_detail, -245, 0, MENU_BG_DETAILS_SPEED, 0)
        bg_detail2 = Sprite(background_detail, 940, 0, MENU_BG_DETAILS_SPEED, 0)

        self.__bg_details = [bg_detail1, bg_detail2]

    # E/S: N/A
    # D: Se encarga de animar los Sprites de los detalles del fondo
    def __background_animation_1(self):

        x = self.__bg_details[0].x
        x_change = self.__bg_details[0].x_change

        if x > -235:
            x_change = -MENU_BG_DETAILS_SPEED

        elif x < -255:
            x_change = MENU_BG_DETAILS_SPEED
        
        for i in range(0, len(self.__bg_details)):
            self.__bg_details[i].x_change = x_change
            self.__bg_details[i].x += x_change

            img = self.__bg_details[i].get_image()

            x = self.__bg_details[i].x
            y = self.__bg_details[i].y

            self.__screen.blit(img, (x,y))

    # E/S: N/A
    # D: Se encarga de dibujar la base para la animacion 2
    def __background_animation_2_base(self):
        rects = []
        lines = []
        blue_lines = []
        red_lines = []

        rects.append(self.__pygame.Rect((0, 300, 1000, 2)))
        rects.append(self.__pygame.Rect((500, 300, 2, 600)))

        y1 =  300
        y2 = 600
        x1 = 450
        x2 = 550

        while x1 != 0:
            lines.append([(x1,y1),(retro_menu_rect(x1),y2)])
            blue_lines.append([(x1+2,y1),(retro_menu_rect(x1+2),y2)])
            red_lines.append([(x1-2,y1),(retro_menu_rect(x1-2),y2)])

            lines.append([(x2,y1),(retro_menu_rect(x2),y2)])
            blue_lines.append([(x2+2,y1),(retro_menu_rect(x2+2),y2)])
            red_lines.append([(x2-2,y1),(retro_menu_rect(x2-2),y2)])

            x1-=50
            x2+=50

        for rect in rects:
            self.__pygame.draw.rect(self.__screen, COLOR_WHITE, rect)

        for i in range(0, len(blue_lines)):
            self.__pygame.draw.line(self.__screen, COLOR_BLUE, blue_lines[i][0], blue_lines[i][1], 2)
            self.__pygame.draw.line(self.__screen, COLOR_RED, red_lines[i][0], red_lines[i][1], 2)
            self.__pygame.draw.line(self.__screen, COLOR_WHITE, lines[i][0], lines[i][1], 2)

    # E/S: N/A
    # D: Se encarga de asignar los datos inciales de la animacion de fondo
    def __set_background_animation_2(self):
        bg_rects = []
        y = 300

        for i in range(0, 5):
            rect = Sprite(None, 0, y, 0, 1)
            bg_rects.append(rect)
            y += 60
            

        self.__bg_rects = bg_rects

    # E/S: N/A
    # D: Se encarga de animar los Sprites de los detalles del fondo
    def __background_animation_2(self):
        line = self.__bg_rects[4]

        if line.y > 600:
            self.__bg_rects = []
            self.__set_background_animation_2()
        
        for i in range(0, 5):
            self.__bg_rects[i].y += self.__bg_rects[i].y_change
            rect = self.__pygame.Rect((self.__bg_rects[i].x, self.__bg_rects[i].y, 1000, 2))
            self.__pygame.draw.rect(self.__screen, COLOR_WHITE, rect)


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
        font = self.__pygame.font.Font(GAME_FONT_PATH, 20)

        texts = []

        texts.append(Sprite(font.render("1 vs 1", True, COLOR_WHITE), 455, 175, 0, 0))
        texts.append(Sprite(font.render("1 vs PC", True, COLOR_WHITE), 440, 255, 0, 0))
        texts.append(Sprite(font.render("Puntajes", True, COLOR_WHITE), 425, 333, 0, 0))
        texts.append(Sprite(font.render("Salir", True, COLOR_WHITE), 450, 410, 0, 0))

        for text in texts:
            self.__screen.blit(text.get_image(), (text.x, text.y))

    # E/S: N/A
    # D: Detecta que boton se presiono para redirigir a otro menu
    def __button_events(self):
        buttons = self.__menu_buttons

        for i in range(0, len(buttons)):

            if is_sprite_pressed(self.__pygame, buttons[i]) and self.__click:
                play_sound_effect(self.__pygame, GAME_BUTTON_PRESSED, 1)

                if i == 0:
                    # TODO: Pedir nombres a los usuarios
                    game = Game(self.__pygame, self.__screen, self.__main_clock,"Juan", "Gerald")
                    game.start_game_mode()

                elif i == 1:
                    print("Juego contra IA")
                    pass

                elif i == 2:
                    print("Puntajes")
                    pass
                
                elif i == 3:
                    self.__pygame.quit()
                    sys.exit()

