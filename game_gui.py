from tkinter import *
import random
import copy

current_board = [[0, 0, 0, 0],
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
    board[space[0]][space[1]] = random.choices([2, 4], [0.7, 0.3])[0]
    return True


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
        for i in range(4):
            board[i] = new_board[i]
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
        for i in range(4):
            board[i] = make_transpose(transpose)[i]


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
        for i in range(4):
            board[i] = new_board[i]
    if dir == 'a':
        i = 0
        while i <= 2:
            for row in new_board:
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    row[i + 1] = 0
            i += 1
        for i in range(4):
            board[i] = new_board[i]
    transpose = make_transpose(new_board)
    if dir == 's':
        i = 3
        while i >= 1:
            for row in transpose:
                if row[i] == row[i - 1]:
                    row[i] *= 2
                    row[i - 1] = 0
            i -= 1
        for i in range(4):
            board[i] = make_transpose(transpose)[i]
    if dir == 'w':
        i = 0
        while i <= 2:
            for row in transpose:
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    row[i + 1] = 0
            i += 1
        for i in range(4):
            board[i] = make_transpose(transpose)[i]


def operate(dir, board):
    old_board = copy.deepcopy(board)
    if dir == 'w' or dir == 'a' or dir == 's' or dir == 'd':
        slide(dir, board)
        combine(dir, board)
        slide(dir, board)
        if old_board != board:
            add_number(board)
    else:
        return


def game_over(board):
    for row in board:
        for item in row:
            if item == 0:
                return False
    board1 = copy.deepcopy(board)
    board2 = copy.deepcopy(board)
    board3 = copy.deepcopy(board)
    board4 = copy.deepcopy(board)
    operate('w', board1)
    operate('d', board2)
    operate('s', board3)
    operate('a', board4)
    if board1 == board2 == board3 == board4 == board:
        return True
    else:
        return False




class Cell:
    def __init__(self, row, col, num):
        self.x = row
        self.y = col
        self.num = num


def make_cells(board):
    cells = []
    for i in range(4):
        for j in range(4):
            cells.append(Cell(i, j, board[i][j]))
    return cells


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        add_number(current_board)
        self.board = current_board
        self.cells = make_cells(self.board)
        self.display()

    def display(self, master=None):
        self.destroy()
        Frame.__init__(self, master)
        self.pack()
        for i in range(4):
            self.columnconfigure(i, minsize=100)
            self.rowconfigure(i, minsize=100)
        for cell in self.cells:
            square = Button(self)
            if cell.num != 0:
                square['text'] = cell.num
                square['font'] = ('Helvetica', '30')
            square.grid(row=cell.x, column=cell.y, sticky=W+N+E+S)
        if game_over(self.board):
            self.destroy()
            Frame.__init__(self, master)
            self.pack()
            GO = Label(self, text='Game over')
            GO.pack()


def change_board(event):
    operate(event.char, app.board)
    app.cells = make_cells(app.board)
    app.display()


root = Tk()
root.geometry("400x400")
app = Application(master=root)
root.bind("<Key>", change_board)
app.mainloop()




