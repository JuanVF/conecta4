from conecta4.game.sprite import Sprite
from conecta4.game.physics import calc_velocity
from conecta4.constants import *

import time

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

# E: Una referencia a pygame, screen, un entero y dos strings
# S: N/A
# D: Renderiza el texto del ganador
def render_winner_text(pygame, screen, winner, player1, player2):
    font = pygame.font.Font(GAME_FONT_PATH, 22)
    if winner == 1:
        txt = "Ganador Jugador " + player1
    else:
        txt = "Ganador Jugador " + player2

    txt_r = Sprite(font.render(txt, True, COLOR_WHITE), 370, 450, 0, 0)
    screen.blit(txt_r.get_image(), (txt_r.x, txt_r.y))

# E: Una referencia a screen, una moneda y dos numeros reales
# S: N/A
# D: Hace la animacion de dejar caer la moneda
def drop_coin(screen, coin, start_time, lim):
    screen.blit(coin.get_image(), (coin.x, coin.y))

    if coin.y >= lim:
        coin.y = lim
        return

    now = time.time()
    dif = now - start_time

    coin.y_change = calc_velocity(dif)
    coin.y += coin.y_change

# E: Una lista y una referencia a screen
# S: N/A
# D: Renderiza los botones del menu
def render_game_menu_buttons(menu_buttons, screen):
    for button in menu_buttons:
        screen.blit(button.get_image(), (button.x, button.y))

# E: Una referencia a pygame, screen, un sound de pygame y un booleano
# S: Un booleano
# D: Renderiza el ganador
def render_winner(pygame, screen, winner_sound, winner_sound_played):
    s = pygame.Surface((800, 600))

    s.set_alpha(128)
    s.fill((0, 0, 0))
    screen.blit(s, (200, 0))

    winner = pygame.image.load(GAME_WIN_IMG)
    screen.blit(winner, (370, 200))

    if not winner_sound_played:
        pygame.mixer.init()
        pygame.mixer.Channel(1).play(winner_sound)

    return True

# E/S: N/A
# D: Se encarga de asignarle un texto a los botones
def render_menu_text(pygame, screen):
    font = pygame.font.Font(GAME_FONT_PATH, 17)

    texts = []
    texts.append(Sprite(font.render("Volver", True, COLOR_WHITE), 42, 45, 0, 0))
    texts.append(Sprite(font.render("Guardar", True, COLOR_WHITE), 38, 145, 0, 0))
    texts.append(Sprite(font.render("Teclas", True, COLOR_WHITE), 48, 230, 0, 0))

    for text in texts:
        screen.blit(text.get_image(), (text.x, text.y))

# E: Una referencia a screen y una lista 
# S: N/A
# D: Se encarga de renderizar las monedas
def render_coins(screen, coins):
    for coin in coins:
        drop_coin(screen, coin[0], coin[1], coin[2])

# E: Una referencia a pygame y a screen
# S: N/A
# D: Se encarga de ocultar las monedas desplazadas hacia la izquierda
def render_coin_hider(pygame, screen):
    s = pygame.Surface((200, 600))

    s.set_alpha(255)
    s.fill((0, 0, 0))
    screen.blit(s, (0, 0))