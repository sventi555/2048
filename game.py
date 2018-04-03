import random
import copy

start_board = [[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]


def display_grid(grid):
    print('_________________')
    for row in grid[:-1]:
        for item in row:
            print('|', end=' ')
            if item == 0:
                print(' ', end=' ')
            else:
                print('{0}'.format(item), end=' ')
        print('|')
        print('| -   -   -   - |')
    for item in grid[-1]:
        print('|', end=' ')
        if item == 0:
            print(' ', end=' ')
        else:
            print('{0}'.format(item), end=' ')
    print('|')
    print(chr(0x00af)*17)


def add_number(board):
    new_board = copy.deepcopy(board)
    open_spots = []
    for i in range(4):
        for j in range(4):
            if new_board[i][j] == 0:
                open_spots.append([i, j])
    if len(open_spots) == 0:
        return False
    spot = random.randint(0, len(open_spots) - 1)
    space = open_spots[spot]
    new_board[space[0]][space[1]] = random.choices([2, 4], [0.7, 0.3])[0]
    return new_board


def make_transpose(board):
    new_board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(4):
        for j in range(4):
            new_board[i][j] = board[j][i]
            new_board[j][i] = board[i][j]
    return new_board


def slide(dir, board):
    if dir == 'd' or dir == 'a':
        new_board = copy.deepcopy(board)
        for row in new_board:
            num_zeros = row.count(0)
            for i in range(num_zeros):
                row.remove(0)
            for i in range(num_zeros):
                if dir == 'a':
                    row.append(0)
                else:
                    row.insert(0, 0)
        return new_board
    if dir == 'w' or dir == 's':
        transpose = make_transpose(board)
        for row in transpose:
            num_zeros = row.count(0)
            for i in range(num_zeros):
                row.remove(0)
            for i in range(num_zeros):
                if dir == 'w':
                    row.append(0)
                else:
                    row.insert(0, 0)
        return make_transpose(transpose)


def combine(dir, board):
    new_board = copy.deepcopy(board)
    if dir == 'd':
        i = 3
        while i >= 1:
            for row in new_board:
                if row[i] == row[i-1]:
                    row[i] *= 2
                    row[i-1] = 0
            i -= 1
        return new_board
    if dir == 'a':
        i = 0
        while i <= 2:
            for row in new_board:
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    row[i + 1] = 0
            i += 1
        return new_board
    transpose = make_transpose(board)
    if dir == 's':
        i = 3
        while i >= 1:
            for row in transpose:
                if row[i] == row[i - 1]:
                    row[i] *= 2
                    row[i - 1] = 0
            i -= 1
        return make_transpose(transpose)
    if dir == 'w':
        i = 0
        while i <= 2:
            for row in transpose:
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    row[i + 1] = 0
            i += 1
        return make_transpose(transpose)


def operate(board):
    dir = input('provide a direction to swipe: one of "w", "a", "s", or "d". Press "q" to quit')
    if dir == 'q':
        return
    elif dir == 'w' or dir == 'a' or dir == 's' or dir == 'd':
        old_board = copy.deepcopy(board)
        new_board = slide(dir, combine(dir, slide(dir, old_board)))
        if not add_number(new_board):
            print('game over!')
            display_grid(new_board)
            return
        elif new_board != old_board:
            new_board = add_number(new_board)
            display_grid(new_board)
            return new_board
        else:
            display_grid(new_board)
            return new_board
    else:
        display_grid(board)
        return board


def play_game():
    current_board = add_number(add_number(start_board))
    display_grid(current_board)
    while current_board:
        current_board = operate(current_board)



