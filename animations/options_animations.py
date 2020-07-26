from conecta4.gui.input import Input
from conecta4.utils import *

p2_hint = "Escriba el nombre del jugador 2..."

# E: Una referencia a pygame y screen, y un boolenao
# S: Una referencia a un input
# D: Devuelve el valor del input del player 2
def set_input_p2(pg, screen, isIa):
    if not isIa:
        return Input(pg, screen, 20, 260, p2_hint)
    
    return None

# E: Una referencia a screen, un booleano y dos render de fonts
# S: N/A
# D: Se encarga de renderizar los titulos de los inputs
def render_input_title(screen, isIA, input_p1_title, input_p2_title):
    screen.blit(input_p1_title, (40, 80))

    if not isIA:
        screen.blit(input_p2_title, (40, 210))

# E: Una referencia a screen, un booleano y dos Inputs
# S: N/A
# D: Se encarga de renderizar los inputs
def render_inputs(screen, isIA, input_p1, input_p2, ):
    input_p1.render()

    if not isIA:
        input_p2.render()

# E: Una referencia a screen y 4 botones
# S: N/A
# D: Renderiza los principales botones del menu
def render_buttons(screen, back_button_title, back_button, button_img, play_button):
    screen.blit(back_button_title, (100, 25))
    screen.blit(back_button.get_image(), (back_button.x, back_button.y))
    screen.blit(button_img, (720, 272))
    screen.blit(play_button, (762, 295))

# E: Un booleano, una lista y una fuente
# S: Dos listas y un render de font
# D: Retorna las variables iniciales
def set_saved_games(isIA, saved_games, font):
    length = get_mode_length(isIA, saved_games)
    mode = get_game_mode(isIA)

    p1s = []
    p2s = []

    vs = font.render("VS", True, (255, 234, 55))

    for i in range(0, length):
        current_game = saved_games[mode][i]

        p1s.append(font.render(current_game["player1"], True, COLOR_WHITE))
        p2s.append(font.render(current_game["player2"], True, COLOR_WHITE))

    return p1s, p2s, vs

# E: Una referencia a screen, un entero, dos listas y un render de font
# S: N/A
# D: Renderiza la lista de partidas guardadas
def render_saved_games(screen, x_move, p1s, p2s, vs, game_container):
    x_cont = 90

    for i in range(0, len(p1s)):
        current_x = 30 + x_cont + x_move

        pos = (x_cont + x_move, 400)

        p1_pos = ((current_x, 400))
        p2_pos = ((current_x, 480))
        vs_pos = ((current_x, 440))

        screen.blit(game_container, pos)

        screen.blit(p1s[i], p1_pos)
        screen.blit(p2s[i], p2_pos)
        screen.blit(vs, vs_pos)

        x_cont += 320

# E: Un entero y un booleano
# S: Un entero
# D: Mueve la lista de partidas hacia la izquierda
def move_list_to_left(x_move, pressed):
    if pressed and x_move < 0:
        return x_move + 70

    return x_move

# E: Dos enteros y un booleano
# S: Un entero
# D: Mueve la lista de partidas hacia la derecha
def move_list_to_right(x_move, length, pressed):
    if pressed and x_move >= length:
        return x_move - 70

    return x_move