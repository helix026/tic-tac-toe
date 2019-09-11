from tkinter import *
from tkinter import messagebox


def evaluateBoard(board):
    bonus = len(fetchEmptyBoxes(board))
    # rows
    for i in range(1, 4):
        if board[(i, 1)] == board[(i, 2)] == board[(i, 3)]:
            score = int(board[(i, 1)] == 'X') * (50 + bonus) - int(board[(i, 1)] == 'O') * (50 + bonus)
            if score != 0:
                return score

    # cols
    for i in range(1, 4):
        if board[(1, i)] == board[(2, i)] == board[(3, i)]:
            score = int(board[(1, i)] == 'X') * (50 + bonus) - int(board[(1, i)] == 'O') * (50 + bonus)
            if score != 0:
                return score

    # diagonals
    if board[(1, 1)] == board[(2, 2)] == board[(3, 3)] or board[(1, 3)] == board[(2, 2)] == board[(3, 1)]:
        score = int(board[(2, 2)] == 'X') * (50 + bonus) - int(board[(2, 2)] == 'O') * (50 + bonus)
        if score != 0:
            return score

    return 0


def markBox(board, box, mark):  # *box* is a Tuple containing index of box, mark is either 'X' or 'O'
    board[box] = mark


def minimax(board, isMaxTurn):
    possibleMoveSets = []
    score = evaluateBoard(board)
    emptyBoxes = fetchEmptyBoxes(board)

    if score != 0 or len(emptyBoxes) == 0:
        return {'move': (0, 0), 'score': score}
    else:
        if isMaxTurn:
            for box in emptyBoxes:
                boardCopy = board.copy()
                markBox(boardCopy, box, 'X')
                set = minimax(boardCopy, not isMaxTurn)
                possibleMoveSets.append({'move': box, 'score': set['score']})

            bestMoveSet = possibleMoveSets[0]
            for set in possibleMoveSets:
                if (set['score'] > bestMoveSet['score']):
                    bestMoveSet = set
        else:
            for box in emptyBoxes:
                boardCopy = board.copy()
                markBox(boardCopy, box, 'O')
                set = minimax(boardCopy, not isMaxTurn)
                possibleMoveSets.append({'move': box, 'score': set['score']})

            bestMoveSet = possibleMoveSets[0]
            for set in possibleMoveSets:
                if (set['score'] < bestMoveSet['score']):
                    bestMoveSet = set

    return bestMoveSet


def showAbout():
    messagebox.showinfo('About', 'Created by: Kashinath Patekar, student at NITG\n\nSpeacial thanks to Stack Overflow')


def resetBoard():
    global board
    global empty
    for box in board:
        board[box] = empty


def resetGuiButtons():
    global buttons
    for button in buttons:
        button.config(text='', relief=SUNKEN)


def resetAll():
    global moves
    moves = 0
    resetBoard()
    resetGuiButtons()


def fetchEmptyBoxes(board):
    emptyBoxes = []
    for box in board:
        if board[box] == empty:
            emptyBoxes.append(box)
    return emptyBoxes


def onClick(event):
    global board
    global playerMark
    global cpuMark
    global moves

    button = event.widget
    frame = button.master
    info = frame.grid_info()
    idx = (info['row'] + 1, info['column'] + 1)

    if idx in fetchEmptyBoxes(board):
        # player's Move
        button.config(text=playerMark, font=('default', 50))
        board[idx] = playerMark
        moves += 1
        score = evaluateBoard(board)
        if score > 0:
            messagebox.showinfo('Congrats!', 'You Win!')
            resetAll()
        elif moves == 9:
            messagebox.showinfo('Genius!', 'It was a draw...')
            resetAll()
        else:
            # CPU's move
            moveSet = minimax(board, isMaxTurn=False)
            row = moveSet['move'][0] - 1
            col = moveSet['move'][1] - 1
            buttons[3 * row + col].config(text=cpuMark, font=('default', 50))
            markBox(board, moveSet['move'], cpuMark)
            moves += 1

            score = evaluateBoard(board)
            if score < 0:
                messagebox.showinfo('Oops!', 'Better luck next time!')
                resetAll()
    else:
        messagebox.showinfo('Alert', 'Already marked!')


# Board
empty = ' '

board = {
    (1, 1): empty, (1, 2): empty, (1, 3): empty,
    (2, 1): empty, (2, 2): empty, (2, 3): empty,
    (3, 1): empty, (3, 2): empty, (3, 3): empty
}

# Window
root = Tk()
root.geometry('320x320')
root.resizable(0, 0)
root.title('Tic Tac Toe')

# Menu for Window
menu_bar = Menu(root)
root.config(menu=menu_bar)

menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Menu', menu=menu)

menu.add_command(label='New Game', command=resetAll)

'''
markMenu = Menu(menu)
menu.add_cascade(label='Choose Mark',menu=markMenu)
markMenu.add_command(label='X',command=playerChoiceX)
'''

menu.add_command(label='Quit', command=root.destroy)
menu.add_command(label='About', command=showAbout)

# Container frame for button frames
mainFrame = Frame(root, width=300, height=300, padx=10, pady=10)

buttonFrames = []
for i in range(9):
    buttonFrames.append(Frame(mainFrame, width=100, height=100, padx=3, pady=3))
    buttonFrames[i].grid(row=int(i / 3), column=i % 3)
    buttonFrames[i].pack_propagate(0)

buttons = []
for i in range(9):
    buttons.append(Button(buttonFrames[i], text=None, relief=SUNKEN))
    buttons[i].bind('<Button-1>', onClick)
    buttons[i].pack(side=TOP, fill=BOTH, expand=1)

mainFrame.pack()

cpuMark = 'O'
playerMark = 'X'
moves = 0

root.mainloop()
