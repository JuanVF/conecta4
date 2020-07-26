import sys

from conecta4.constants import *

# E: Una referencia a pygame y un evento de Pygame
# S: N/A
# D: Dado un evento, cierra el juego si se oprime el boton de salir
def close_menu(pg, event):
    if event.type == pg.QUIT:
        pg.quit()
        sys.exit()

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
def is_sprite_pressed(pygame, button, x=200, y=70):
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
    return 2*x - 500

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

# E: N/A
# S: Un diccionario
# D: Retorna las partidas guardadas
def find_games():
    saved_games = eval(read(SAVED_GAMES))

    if saved_games != "":
        print("so?")
        return saved_games

    return {}

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
def update_game_by_id(mode, games, game, game_id):
    for i in range(0, len(games[mode])):
        if games[mode][i]["id"] == game_id:
            games[mode][i] = game

    return save(SAVED_GAMES, str(games))

# E: Un entero y un string
# S: Un booleano
# D: Borra una partida guardada por su id
def delete_game_by_id(game_id, mode):
    saved_games = eval(read(SAVED_GAMES))
    new_games = []

    for i in range(0, len(saved_games[mode])):
        if saved_games[mode][i]["id"] != game_id:
            new_games.append(saved_games[mode][i])

    saved_games[mode] = new_games

    return save(SAVED_GAMES, str(saved_games))

# E: N/A
# S: Una lista
# D: Retorna todos los scores guardados
def find_scores():
    scores = read(SCORE_FILE)

    if scores == "":
        return []

    return eval(scores)

# E: Un string
# S: Un booleano
# D: Actualiza la tabla de puntajes
def update_scores(player):
    scores = find_scores()
    isIn = False

    for i in range(0, len(scores)):
        if scores[i]["player"] == player:
            scores[i]["points"] += 1
            isIn = True

    if not isIn:
        scores.append({"player": player, "points": 1})

    return save(SCORE_FILE, str(scores))


# E/S: Una lista
# D: Ordena una lista por el metodo iterativo, mayor a menor
def sort_scores(scores):
    for i in range(0, len(scores)-1):
        mini = i

        for j in range(i+1, len(scores)):
            if scores[j]["points"] < scores[mini]["points"]:
                mini = j
        
        scores[i], scores[mini] = scores[mini], scores[i]

    return scores[::-1]

# E: Un booleano
# S: Un string
# D: Retorna el modo de juego
def get_game_mode(isIa):
    if isIa:
        return "PV1"
    return "PVP"

# E: Un booleano y una lista
# S: Un entero
# D: Retorna el largo de las partidas guardadas dado su modo de juego
def get_mode_length(isIa, saved_games):
    mode = get_game_mode(isIa)

    return len(saved_games[mode])

# E: Un Input y un booleano
# S: Un string
# D: Retorna el nombre del player 2
def get_p2_name(p2_input, isIa):
    if not isIa:
        p2 = p2_input.get_text()
                
        if p2.lstrip() == "":
            return "Player 2"

        return p2

    return "PC"

# E: Un Input
# S: Un string
# D: Retorna el nombre del player 1
def get_p1_name(p1_input):
    p1 = p1_input.get_text()

    if p1.lstrip() == "":
        return "Player 1"
    
    return p1
