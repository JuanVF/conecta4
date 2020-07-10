import time 
import sys

sys.path.append("..")

from conecta4.game.physics import calc_velocity
from conecta4.game.sprite import Sprite

# E: Una referencia a screen, pygame y un sprite
# S: N/A
# D: Hace la animacion de dejar caer la moneda
def drop_coin(screen, coin, start_time):
    screen.blit(coin.get_image(), (coin.x, coin.y))

    if coin.y >= 500:
        coin.y = 500
        return

    now = time.time()
    dif = now - start_time

    coin.y_change = calc_velocity(dif)
    coin.y += coin.y_change

