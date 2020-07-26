from conecta4.constants import *
from conecta4.game.sprite import Sprite

# E: Una referencia a screen y el background
# S: N/A
# D: Asigna el fondo
def set_background(screen, bg):
    screen.fill((0, 0, 0))
    screen.blit(bg, (200,0))

# E/S: N/A
# D: Setea las posiciones de los botones del menu
def set_game_menu_buttons(pg):
    buttons = []
    button_img = pg.image.load(BUTTON_IMG_PATH)

    buttons.append(Sprite(button_img, 20, 20, 0, 0))
    buttons.append(Sprite(button_img, 20, 120, 0, 0))

    return buttons

# E: Una referencia a pygame y screen, y un entero
# S: N/A
# D: Se encarga de renderizar los indices en x
def render_indices(pygame, screen, lRender, dRender):
    font = pygame.font.Font(GAME_FONT2_PATH, 15)
    x_dis = 270
    y_dis = 520

    for i in range(0, 7):
        txt_x = font.render(str(lRender + i), True, COLOR_WHITE)

        if i < 6:
            txt_y = font.render(str(dRender + i), True, COLOR_WHITE)
            screen.blit(txt_y, (220, y_dis))

            y_dis -= 95

        screen.blit(txt_x, (x_dis, 560))
        x_dis += 110