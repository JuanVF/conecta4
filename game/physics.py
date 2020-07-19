# E/S: Un numero real
# D: Dado el tiempo actual retorna la veloidad
def calc_velocity(time_rnow):
    a = 25
    vel = (time_rnow ** 3) * a

    return vel

# E: Una matriz y un booleano
# S: Una matriz
# D: Agrega una posiion a la matriz
def add_board_col(board ,left):
    if left:
        board.insert(0, [0,0,0,0,0,0])
    else:
        board.append([0,0,0,0,0,0])

    return board

# E: Una matriz, un entero y un booleano
# S: Una matriz
# D: Agrega 7 columnas
def add_n_board_cols(board, n, left):
    for i in range(0, n):
        board = add_board_col(board, left)

    return board

# E: Una matriz, un entero y un booleano
# S: Una matriz
# D: Dada una posiion y el turno, agrega una nueva moneda
def add_coin_to_board(board, pos, player_turn):
    coins = get_pos_last_space(board[pos])

    if coins == len(board[pos]):
        if player_turn:
            board[pos].append(2)
        else:
            board[pos].append(1)
    else:
        if player_turn:
            board[pos][coins] = 2
        else:
            board[pos][coins] = 1
    
    return board

# E: Un sprite, un entero y una matriz
# S: Un sprite
# D: Calcula la posiion iniial de una moneda dada su posiion de tablero
def calc_coin_initial_pos(coin, pos):
    coin_x_distance = 35
    coin_width = 75

    dis_y = 5
    dis_x = 235 + pos * (coin_x_distance + coin_width)

    coin.x = dis_x
    coin.y = dis_y

    return coin

# E: Un entero y un vector
# S: Un entero
# D: Calcula el limite en y para que una moneda no caiga haia el infinito
def calc_coin_y_lim(col):
    coin_y_distance = 20
    coin_height = 75
    
    pos = get_pos_last_space(col) + 1

    lim = 600 - (coin_height+coin_y_distance)*pos
    return lim

# E: Un vector
# S: Un entero
# D: Dado un vector, devuelve la posiion donde es 0, si no existe, la posiion nueva
def get_pos_last_space(col):
    for i in range(0, len(col)):
        if col[i] == 0:
            return i
    
    return len(col)

# E/S: Una lista y un booleano
# D: Se encarga de mover la posiion x de render de las monedas
#    Si left es True las mueve haia la izquierda, de lo contrario, haia la derecha
def move_coins_x_pos(coins, left):
    coin_x_distance = 35
    coin_width = 75
    x_move = coin_x_distance + coin_width

    for i in range(0, len(coins)):
        if left:
            coins[i][0].x -= x_move
        else:
            coins[i][0].x += x_move

    return coins

# E: Una matriz
# S: Un entero entre 0 - 2
# D: Detecta si hay un ganador
def detect_winner(board):
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            point = board[i][j]

            if point != 0 and detect_lines(board, i, j):
                return board[i][j]

    return 0

# E: Una matriz y dos enteros
# S: Un booleano
# D: Retorna True si encuentra ganador
def detect_lines(board, i, j):
    for code in range(1, 5):
        case = detect_line(board, code, i, j)

        if case:
            return True

    return False

# E: Una matriz y tres enteros
# S: Un booleano
# D: Detecta si hay una linea seguida
def detect_line(board, cod, i, j):
    n = 1
    nxt = 1
    i = i
    j = j

    while n == nxt or n == 4:
        nI = i + 1
        nJ = j + 1

        cond = (cod == 4 and (i-1 < 0 or j-1 < 0))

        if len(board) == nI or len(board[j]) == nJ or cond:
            n = -1
        else:
            # Derecha
            if cod == 1 and board[i][j] == board[nI][j]:
                nxt += 1
                i += 1

            # Derecha-arriba
            elif cod == 2 and board[i][j] == board[nI][nJ]:
                nxt += 1
                i += 1
                j += 1

            # Arriba
            elif cod == 3 and board[i][j] == board[i][nJ]:
                nxt += 1
                j += 1

            # Derecha-abajo
            elif cod == 4 and board[i][j] == board[i+1][j-1]:
                nxt += 1
                i += 1
                j -= 1
            
            n += 1

    return nxt == 4