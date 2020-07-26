from conecta4.constants import *
from conecta4.utils import retro_menu_rect

from conecta4.game.sprite import Sprite

# E: Una referencia a Pygame
# S: Una lista
# D: Se encarga de asignar los datos inciales del Sprite de los detalles del fondo
def set_bg_details(pg):
    background_detail = pg.image.load(MENU_BG_DETAILS_PATH)

    bg_detail1 = Sprite(background_detail, -245, 0,
                        MENU_BG_DETAILS_SPEED, 0)
    bg_detail2 = Sprite(background_detail, 940, 0,
                        MENU_BG_DETAILS_SPEED, 0)

    return [bg_detail1, bg_detail2]

# E: Una referencia a screen y una lista
# S: Una lista
# D: Se encarga de animar los Sprites de los detalles del fondo
def animate_bg_details(screen, bg_details):
    x = bg_details[0].x
    x_change = bg_details_x_direction(x, bg_details[0].x_change)

    for i in range(0, len(bg_details)):
        bg_details[i].x_change = x_change
        bg_details[i].x += x_change

        img = bg_details[i].get_image()

        x = bg_details[i].x
        y = bg_details[i].y

        screen.blit(img, (x, y))

    return bg_details

# E: Dos flotantes
# S: Un flotante
# D: Determina la direccion de movimiento de la animacion de bg_details
def bg_details_x_direction(x, x_change):
    if x > -235:
        return -MENU_BG_DETAILS_SPEED

    elif x < -255:
        return MENU_BG_DETAILS_SPEED
    
    return x_change

# E: N/A
# S: Una lista
# D: Se encarga de asignar los datos inciales de la animacion de lineas
def set_lines():
    lines = []
    y = 300

    for i in range(0, 5):
        rect = Sprite(None, 0, y, 0, 1)
        lines.append(rect)
        y += 60

    return lines

# E: Una referencia a Pygame y screen, y una lista
# S: Una lista
# D: Se encarga de animar los Sprites de los detalles del fondo
def move_lines(pg, screen, lines):
    line = lines[4]

    if line.y > 600:
        lines = []
        lines = set_lines()

    for i in range(0, 5):
        lines[i].y += lines[i].y_change

        rect = pg.Rect((lines[i].x, lines[i].y, 1000, 2))

        pg.draw.rect(screen, COLOR_WHITE, rect)
    
    return lines

# E: N/A
# S: Una lista
# D: Retorna las lineas para la base de la animacion
def set_line_bases():
    lines = []
    blue_lines = []
    red_lines = []

    y1 = 300
    y2 = 600
    x1 = 450
    x2 = 550

    while x1 > 0:
        lines.append([(x1, y1), (retro_menu_rect(x1), y2)])
        blue_lines.append([(x1+2, y1), (retro_menu_rect(x1+2), y2)])
        red_lines.append([(x1-2, y1), (retro_menu_rect(x1-2), y2)])

        lines.append([(x2, y1), (retro_menu_rect(x2), y2)])
        blue_lines.append([(x2+2, y1), (retro_menu_rect(x2+2), y2)])
        red_lines.append([(x2-2, y1), (retro_menu_rect(x2-2), y2)])

        x1 -= 50
        x2 += 50
    
    return [lines, blue_lines, red_lines]

# E: Una referencia a pygame
# S: Una lista
# D: Determina las lineas bases de la animacion
def set_rects(pg):
    rects = []

    rects.append(pg.Rect((0, 300, 1000, 2)))
    rects.append(pg.Rect((500, 300, 2, 600)))

    return rects


# E/S: N/A
# D: Se encarga de dibujar la base para la animacion
def draw_base_lines(pg, screen, rects, lines):
    white_lines = lines[0]
    blue_lines = lines[1]
    red_lines = lines[2]


    for rect in rects:
        pg.draw.rect(screen, COLOR_WHITE, rect)

    for i in range(0, len(blue_lines)):
        pg.draw.line(screen, COLOR_BLUE, blue_lines[i][0], blue_lines[i][1], 2)

        pg.draw.line(screen, COLOR_RED, red_lines[i][0], red_lines[i][1], 2)

        pg.draw.line(screen, COLOR_WHITE, white_lines[i][0], white_lines[i][1], 2)

# E: Una referencia a una fuente de texto
# S: Una lista
# D: Setea la lista de botones del menu principal
def set_button_list(font):
    texts = []

    texts.append(
        Sprite(font.render("1 vs 1", True, COLOR_WHITE), 455, 175, 0, 0))
    texts.append(
        Sprite(font.render("1 vs PC", True, COLOR_WHITE), 440, 255, 0, 0))
    texts.append(
        Sprite(font.render("Puntajes", True, COLOR_WHITE), 425, 333, 0, 0))
    texts.append(
        Sprite(font.render("Salir", True, COLOR_WHITE), 450, 410, 0, 0))

    return texts