import random 

from conecta4.game.physics import get_pos_last_space

# E: Una matriz y un entero
# S: Un entero
# D: Predice el siguiente movimiento por parte de la PC
def predict_movement(board):
    possible_movementes = get_possible_movements(board)

    for movement in possible_movementes:
        max_height = get_pos_last_space(board[movement[1][0]])

        if abs(movement[1][1] - max_height) % 2 == 0:
            return movement[1][0]

    if len(possible_movementes) == 0:
        return random.randint(0, 5)

    return possible_movementes[0][1][0]

# E: Una matriz
# S: Una lista
# D: Obtiene las maximos posibles movimientos dada una matriz
def get_possible_movements(board):
    pos_wins = []

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == 1:
                highest_i = find_line(board, i, j, 1)

                for code in range(2, 8):
                    case = find_line(board, i, j, code)

                    if case[0] > highest_i[0]:
                        highest_i = case
    
                pos_wins.append(highest_i)

    pos_wins.sort()

    return pos_wins[::-1]
                

# E: Una matriz y tres enteros
# S: Un entero
# D: Encuentra la n cantida de lineas seguidas
def find_line(board, i, j, cod):
    n = 1
    nxt = 1

    while n == nxt:
        limits = len(board) == i + 1 or len(board[0]) == j + 1

        if limits:
            n = -1
        else:
            if i - 1 >= 0:
                if j - 1 >= 0:
                    # Derecha-abajo
                    if cod == 1 and board[i][j] == board[i+1][j-1]:
                        nxt += 1
                        i += 1
                        j -= 1
                    elif cod == 1:
                        i += 1
                        j -= 1

                    # Izquierda-abajo
                    if cod == 7 and board[i][j] == board[i-1][j-1]:
                        nxt += 1
                        i -= 1
                        j -= 1
                    elif cod == 7:
                        i -= 1
                        j -= 1

                # Izquierda-arriba
                if cod == 5 and board[i][j] == board[i-1][j+1]:
                    nxt += 1
                    j += 1
                    i -= 1
                elif cod == 5:
                    j += 1
                    i -= 1
                
                # Izquierda
                if cod == 6 and board[i][j] == board[i-1][j]:
                    nxt += 1
                    i -= 1
                elif cod == 6:
                    i -= 1

            # Derecha
            if cod == 2 and board[i][j] == board[i+1][j]:
                nxt += 1
                i += 1
            elif cod == 2:
                i += 1
            
            # Derecha-arriba
            if cod == 3 and board[i][j] == board[i+1][j+1]:
                nxt += 1
                j += 1
                i += 1
            elif cod == 3:
                j += 1
                i += 1
            
            # Arriba
            if cod == 4 and board[i][j] == board[i][j+1]:
                nxt += 1
                j += 1
            elif cod == 4:
                j += 1
        
            n += 1
    
    return [nxt, [i, j]]

# E/S: Una lista
# D: Ordena la lista de wins
def sort_wins(wins):
    sort = [wins[0]]
    
    return sort