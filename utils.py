from os import path

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
def is_sprite_pressed(pygame, button):
    mx, my = pygame.mouse.get_pos()

    pos1 = (button.x, button.y)
    pos2 = (button.x + 200, button.y + 70)
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