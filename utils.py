# E: Una lista de tuplas
# S: Un booleano
# D: Detecta si hay traslape
def is_overlap(pos1, pos2, pos3):
    if pos1[0] <= pos3[0] and pos3[0] <= pos2[0]:
        if pos1[1] <= pos3[1] and pos3[1] <= pos2[1]:
            return True

    return False