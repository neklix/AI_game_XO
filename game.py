import argparse
import math
parser = argparse.ArgumentParser()
n = 3
k = 3
parser.add_argument('-n', action='store', dest='n', default=3, help='Field size')
parser.add_argument('-k', action='store', dest='k', default=3, help='Win row size')
parser.add_argument('-gamemode', action='store', dest='mode', default='PvsAI', help='PvsP for Player vs Player, PvsAI for Player vs AI, AIvsAI for AI vs AI')
parser.add_argument('-turn', action='store', dest='turn', default='First', help='First for playing for x, Second for playing for o. Works in PvsAI mode only')
args = parser.parse_args()
n = int(args.n)
k = int(args.k)
mode_name = args.mode
mode = 0
if mode_name == 'PvsAI':
    mode = 1
if mode_name == 'AIvsAI':
    mode = 2
is_playing_for_first = True
if args.turn == 'Second':
    is_playing_for_first = False
field = []
MAXN = 10000000 # You can change this value to speed up/slow down AI decision
depth = max(int(math.log(MAXN, n) / 2) - 1, 1)

def parse_input(input_string):
    input_string = input_string.replace('(', '').replace(')', '').replace(',', '')
    input_list = input_string.split()
    return int(input_list[0]), int(input_list[1])

def initialize(field):
    field = [['.' for i in range(n)] for j in range(n)]
    return field

def turn_symbol(is_turn_first):
    if is_turn_first:
        return 'x'
    else:
        return 'o'

def player_turn(field, n, is_turn_first):
    x = -1
    y = -1
    is_try_first = True
    while (x < 0 or x >= n) or (y < 0 or y >= n) or (field[x][y] != '.'):
        if not is_try_first:
            print('Wrong input, try again. ', end='')
        print('Player {0}, your turn'.format(turn_symbol(is_turn_first)), end=' ');
        raw_input = input()
        x, y = parse_input(raw_input)
        x -= 1
        y -= 1
        is_try_first = False
    field[x][y] = turn_symbol(is_turn_first)
    return field

def is_game_over(field, n, k):
    for i in range(n - k + 1):
        for j in range(n):
            if field[i][j] == '.':
                continue
            is_row_correct = True
            for l in range(k):
                if field[i + l][j] != field[i][j]:
                    is_row_correct = False
                    break
            if is_row_correct:
                #print('Game ended with player  {0}  win'.format(field[i][j]))
                return field[i][j]
    
    for i in range(n - k + 1):
        for j in range(n):
            if field[j][i] == '.':
                continue
            is_row_correct = True
            for l in range(k):
                if field[j][i + l] != field[j][i]:
                    is_row_correct = False
                    break
            if is_row_correct:
                #print('Game ended with player  {0}  win'.format(field[j][i]))
                return field[j][i]
    for i in range(n - k + 1):
        for j in range(n - k + 1):
            if field[j][i] == '.':
                continue
            is_row_correct = True
            for l in range(k):
                if field[j + l][i + l] != field[j][i]:
                    is_row_correct = False
                    break
            if is_row_correct:
                #print('Game ended with player  {0}  win'.format(field[j][i]))
                return field[j][i]
    for i in range(n - k + 1):
        for j in range(k - 1, n):
            if field[j][i] == '.':
                continue
            is_row_correct = True
            for l in range(k):
                if field[j - l][i + l] != field[j][i]:
                    is_row_correct = False
                    break
            if is_row_correct:
                #print('Game ended with player  {0}  win'.format(field[j][i]))
                return field[j][i]
    
    is_draw = True
    for i in range(n):
        for j in range(n):
            if field[i][j] == '.':
                is_draw = False
    if is_draw:
        #print('Game ended with Draw')
        return 'draw'
    return 'no'

def print_field(field, n, k):
    # You can uncomment lines to make output more beautiful
    print('\n', end='')
    # print('\t', end='')
    # for i in range(n):
    #     print(i + 1, end='\t')
    print()
    for i in range(n):
        # print(i + 1, end='\t')
        for j in range(n):
            print(field[j][i], end='')
            # print('\t', end='')
        print()
    print()

def is_move_good(field, n, k, is_turn_first, level):
    game_result = is_game_over(field, n, k)
    if game_result == turn_symbol(not is_turn_first):
        return 'lose'
    if game_result == 'draw' or level == 0:
        return 'draw'
    if game_result == turn_symbol(is_turn_first):
        return 'win'
    result = 'lose'
    for i in range(n):
        for j in range(n):
            if field[i][j] != '.':
                continue
            field[i][j] = turn_symbol(is_turn_first)
            next_result = is_move_good(field, n, k, not is_turn_first, level - 1)
            field[i][j] = '.'
            if next_result == 'lose':
                result = 'win'
            if next_result == 'win':
                continue
            if next_result == 'draw' and result == 'lose':
                result = 'draw'
    return result

def ai_turn(field, n, k, is_turn_first):
    x = -1
    y = -1
    is_win_move_found = False
    for i in range(n):
        for j in range(n):
            if field[i][j] != '.':
                continue
            if x == -1:
                x = i
                y = j
            field[i][j] = turn_symbol(is_turn_first)
            result = is_move_good(field, n, k, not is_turn_first, depth)
            field[i][j] = '.'
            if result == 'win':
                continue
            if result == 'lose':
                x = i
                y = j
                is_win_move_found = True
            if result == 'draw' and not is_win_move_found:
                x = i
                y = j
    field[x][y] = turn_symbol(is_turn_first)
    return field

field = initialize(field)
is_turn_first = True
game_result = 'no'
while game_result == 'no':
    if mode == 0:
        field = player_turn(field, n, is_turn_first)
    elif mode == 1:
        if is_turn_first == is_playing_for_first:
            field = player_turn(field, n, is_turn_first)
        else:
            field = ai_turn(field, n, k, is_turn_first)
    else:
        field = ai_turn(field, n, k, is_turn_first)
    is_turn_first = not is_turn_first
    print_field(field, n, k)
    game_result = is_game_over(field, n, k)
if game_result == 'draw':
    print('Game ended with Draw')
else:
    print('Player {0} wins'.format(game_result))
