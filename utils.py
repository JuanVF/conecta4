from os import path
from conecta4.constants import *

# E: Una lista de tuplas
# S: Un booleano
# D: Detecta si hay traslape
def is_overlap(pos1, pos2, pos3):
    if pos1[0] <= pos3[0] and pos3[0] <= pos2[0]:
        if pos1[1] <= pos3[1] and pos3[1] <= pos2[1]:
            return True

    return False

# E: Una referencia a Pygame, un string y dos enteros
# S: N/A
# D: Dado el path de un sonido, lo reproduce
def play_sound_effect(pygame, sound_path, chn, volume=0.3):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(sound_path)
    sound.set_volume(volume)
    pygame.mixer.Channel(chn).play(sound)

# E: Una referecia a pygame y un Sprite
# S: Un booleano
# D: Si el mouse dio click sobre un boton retorna True
def is_sprite_pressed(pygame, button, x=200, y =70):
    mx, my = pygame.mouse.get_pos()

    pos1 = (button.x, button.y)
    pos2 = (button.x + x, button.y + y)
    pos3 = (mx, my)

    overlap = is_overlap(pos1, pos2, pos3)

    return overlap

# E: Una referencia a un evento de Pygame
# S: Un booleano
# D: Dado un evento, detecta si hay click
def detect_click(pygame, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            return True

    return False

# E/S: Un numero real
# D: Dado un x retorna su valor en la funcion F(x)=2x-500
def retro_menu_rect(x):
    return (2*x - 500)

# E: Dos strings
# S: Booleano
# D: Guarda los datos de un string sobre un archivo
def save(path, string):
    try:
        file = open(path, 'w')
        file.write(string)
        file.close()
    except:
        return False
    return True

# E/S: Un string
# D: Dada la ubicacion de un archivo, lo lee y retorna sus datos
def read(path):
    datos = ""
    try:
        file = open(path, 'r')

        datos = file.read()

        file.close()
        return datos
    except:
        return datos

# E: Un string
# S: Un entero
# D: Retorna una id disponible de un modo de juego
def get_latest_id(mode):
    saved_games = eval(read(SAVED_GAMES))
    highest_id = 0

    for game in saved_games[mode]:
        if game["id"] > highest_id:
            highest_id = game["id"]

    return highest_id + 1

# E: Un string y un entero
# S: Un diccionario
# D: Busca en las partidas un diccionario por su id
def find_game_by_id(mode, game_id):
    saved_games = eval(read(SAVED_GAMES))

    for game in saved_games[mode]:
        if game["id"] == game_id:
            return game
        
    return {}

# E: Un string, dos diccionarios y una id
# S: Un booleano
# D: Actualiza una partida por su id
def update_game_by_id(mode, games, game, id):
    for i in range(0, len(games[mode])):
        if games[mode][i]["id"] == id:
            games[mode][i] = game
    
    return save(SAVED_GAMES, str(games))
