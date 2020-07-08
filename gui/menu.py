import sys
import os  

sys.path.append("..")

from conecta4.constants import *
from conecta4.game.sprite import Sprite
from conecta4.utils import is_overlap
from conecta4.gui.game import Game
from pygame import mixer

class Menu:
    # E: Una referencia a pygame
    # S: N/A
    # D: Constructor
    def __init__(self, pygame):
        self._isRunning = True
        self._click = False

        #Esta funcion se encarga de centrar la ventana
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        self._main_clock = pygame.time.Clock()

        icon = pygame.image.load(GAME_LOGO_PATH)

        mixer.music.load(GAME_BACKGROUND_MUSIC)
        mixer.music.set_volume(0.15)
        mixer.music.play(-1)

        self._background = pygame.image.load(MENU_BACKGROUND_PATH)
        
        self._screen = pygame.display.set_mode(MENU_WINDOW_SIZE)

        self._pygame = pygame
        self._pygame.display.set_caption("4 en linea")
        self._pygame.display.set_icon(icon)
    
    # E/S: N/A
    # D: Inicia el juego y determina ciertos parametros iniciales
    def start_game(self):
        self._set_background_animation_1()
        self._set_background_animation_2()
        self._set_menu_buttons()

        self._game_loop()

    # E/S: N/A
    # D: Loop
    def _game_loop(self):
        while self._isRunning:
            self._set_background()

            self._background_animation_2_base()
            self._background_animation_2()
            self._background_animation_1()

            self._render_buttons()
            self._render_buttons_text()

            self._button_events()

            for event in self._pygame.event.get():
                self._close_menu(event)

            self._click = False
            self._detect_click(event)

            self._pygame.display.update()
            self._main_clock.tick(60)

    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Dado un evento, cierra el juego si se oprime el boton de salir
    def _close_menu(self, event):
        if event.type == self._pygame.QUIT:
            self._pygame.quit()
            sys.exit()

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
        self._screen.fill((16, 15, 15))
        self._screen.blit(self._background, (300,0))

    # E/S: N/A
    # D: Se encarga de asignar los datos inciales del Sprite de los detalles del fondo
    def _set_background_animation_1(self):
        background_detail = self._pygame.image.load(MENU_BG_DETAILS_PATH)

        bg_detail1 = Sprite(background_detail, -245, 0, MENU_BG_DETAILS_SPEED, 0)
        bg_detail2 = Sprite(background_detail, 940, 0, MENU_BG_DETAILS_SPEED, 0)

        self._bg_details = [bg_detail1, bg_detail2]

    # E/S: N/A
    # D: Se encarga de animar los Sprites de los detalles del fondo
    def _background_animation_1(self):
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
    # D: Se encarga de dibujar la base para la animacion 2
    def _background_animation_2_base(self):
        rects = []
        lines = []
        blue_lines = []
        red_lines = []

        rects.append(self._pygame.Rect((0, 300, 1000, 2)))
        rects.append(self._pygame.Rect((500, 300, 2, 600)))
        y1 =  300
        y2 = 600
        x1 = 450
        x2 = 550

        while x1 != 0:
            lines.append([(x1,y1),(2*x1-500,y2)])
            blue_lines.append([(x1+2,y1),(2*(x1+2)-500,y2)])
            red_lines.append([(x1-2,y1),(2*(x1-2)-500,y2)])
            lines.append([(x2,y1),(2*x2-500,y2)])
            blue_lines.append([(x2+2,y1),(2*(x2+2)-500,y2)])
            red_lines.append([(x2-2,y1),(2*(x2-2)-500,y2)])

            x1-=50
            x2+=50

        for rect in rects:
            self._pygame.draw.rect(self._screen, COLOR_WHITE, rect)

        for i in range(0, len(blue_lines)):
            self._pygame.draw.line(self._screen, COLOR_BLUE, blue_lines[i][0], blue_lines[i][1], 2)
            self._pygame.draw.line(self._screen, COLOR_RED, red_lines[i][0], red_lines[i][1], 2)
            self._pygame.draw.line(self._screen, COLOR_WHITE, lines[i][0], lines[i][1], 2)

    # E/S: N/A
    # D: Se encarga de asignar los datos inciales de la animacion de fondo
    def _set_background_animation_2(self):
        bg_rects = []
        y = 300

        for i in range(0, 5):
            rect = Sprite(None, 0, y, 0, 1)
            bg_rects.append(rect)
            y += 60
            

        self._bg_rects = bg_rects

    # E/S: N/A
    # D: Se encarga de animar los Sprites de los detalles del fondo
    def _background_animation_2(self):
        line = self._bg_rects[4]

        if line.y > 600:
            self._bg_rects = []
            self._set_background_animation_2()
        
        for i in range(0, 5):
            self._bg_rects[i].y += self._bg_rects[i].y_change
            rect = self._pygame.Rect((self._bg_rects[i].x, self._bg_rects[i].y, 1000, 2))
            self._pygame.draw.rect(self._screen, COLOR_WHITE, rect)


    # E/S: N/A
    # D: Se encarga de asignar los datos inciales del Sprite de los detalles del fondo
    def _set_menu_buttons(self):
        button_img = self._pygame.image.load(BUTTON_XL_IMG_PATH)

        button1 = Sprite(button_img, 400, 150, 0, 0)
        button2 = Sprite(button_img, 400, 230, 0, 0)
        button3 = Sprite(button_img, 400, 310, 0, 0)
        button4 = Sprite(button_img, 400, 390, 0, 0)

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

        self._screen.blit(normal_mode_text, (455, 175))
        self._screen.blit(vs_pc_mode, (440, 255))
        self._screen.blit(log_menu, (425, 333))
        self._screen.blit(exit_menu, (450, 410))

    # E/S: N/A
    # D: Detecta que boton se presiono para redirigir a otro menu
    def _button_events(self):
        buttons = self._menu_buttons
        for i in range(0, len(buttons)):
            if self._is_button_pressed(buttons[i]) and self._click:
                if i == 0:
                    # TODO: Pedir nombres a los usuarios
                    game = Game(self._pygame, self._screen, self._main_clock,"Juan", "Gerald")
                    game.start_game_mode()
                elif i == 1:
                    print("Juego contra IA")
                    pass
                elif i == 2:
                    print("Puntajes")
                    pass
                elif i == 3:
                    self._pygame.quit()
                    sys.exit()

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

