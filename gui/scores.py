import sys

from conecta4.game.sprite import Sprite
from conecta4.constants import *
from conecta4.utils import *


class Score:

    def __init__(self, pygame, screen, clock):
        self.__pygame = pygame
        self.__screen = screen
        self.__clock = clock
        self.__running = True
        self.__click = False

        self.__font = pygame.font.Font(GAME_FONT_PATH, 22)

        self.__background = pygame.image.load(SCORE_BACKGROUND)
        self.__back_button_img = pygame.image.load(GAME_BACK_BUTTON)
        self.__scroll_button_img = pygame.image.load(SCROLL_BUTTON)

        self.__back_button = Sprite(self.__back_button_img, 20, 20, 0, 0)
        self.__scroll_button = Sprite(self.__scroll_button_img, 820, 250, 0, 0)
        self.__current_scroll = 0

    def open_scores(self):
        self.__scores = find_scores()
        self.__scores = sort_scores(self.__scores)

        self.__loop()

    def __render_background(self):
        self.__screen.blit(self.__background, (0, 0))

        self.__screen.blit(self.__back_button.get_image(),
                           (self.__back_button.x, self.__back_button.y))

    def __loop(self):
        while self.__running:
            self.__screen.fill((0, 0, 0))
            self.__render_scores()
            self.__render_background()
            self.__screen.blit(self.__scroll_button.get_image(
            ), (self.__scroll_button.x, self.__scroll_button.y))

            for event in self.__pygame.event.get():
                self.__click = detect_click(self.__pygame, event)
                self.__close_menu(event)

            self.__scroll_scores()
            self.__back_button_event()

            self.__pygame.display.update()
            self.__clock.tick(60)

    # E: Una referencia a un evento de Pygame
    # S: N/A
    # D: Dado un evento, cierra el juego si se oprime el boton de salir
    def __close_menu(self, event):
        if event.type == self.__pygame.QUIT:
            self.__pygame.quit()
            sys.exit()

    # E/S: N/A
    # D: Cierra la ventana de puntajes
    def __back_button_event(self):
        if self.__click and is_sprite_pressed(self.__pygame, self.__back_button, x=80, y=60):
            play_sound_effect(self.__pygame, GAME_BUTTON_PRESSED, 1)
            self.__running = False

    def __render_scores(self):
        x = 200
        y = 100

        for score in self.__scores:
            player = "Jugador " + score["player"]
            points = str(score["points"]) + " puntos"

            txt_player = self.__font.render(player, True, COLOR_WHITE)
            txt_points = self.__font.render(points, True, COLOR_WHITE)

            self.__screen.blit(txt_player, (x, y + self.__current_scroll))
            self.__screen.blit(txt_points, (x, y + self.__current_scroll + 40))
            self.__pygame.draw.line(self.__screen, COLOR_WHITE, (
                0, y + self.__current_scroll + 80), (1000, y + self.__current_scroll + 80), 2)

            y += 100

    def __scroll_scores(self):
        up_pressed = is_sprite_pressed(
            self.__pygame, self.__scroll_button, 70, 75)
        down_pressed = is_sprite_pressed(
            self.__pygame, self.__scroll_button, 70, 150)

        length = (len(self.__scores)-1) * 100

        if self.__click and up_pressed and self.__current_scroll <= 0:
            self.__current_scroll += 20
        elif self.__click and up_pressed and self.__current_scroll > 0:
            self.__current_scroll = 1
        elif self.__click and down_pressed and -length <= self.__current_scroll:
            self.__current_scroll -= 20
