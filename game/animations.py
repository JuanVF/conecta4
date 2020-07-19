import time 
import sys

sys.path.append("..")

from conecta4.game.physics import calc_velocity
from conecta4.game.sprite import Sprite

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

