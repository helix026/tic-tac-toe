from ticTacToe import *
from time import sleep

board = {
    (1,1) : empty,  (1,2) : empty,  (1,3) : empty,
    (2,1) : empty,  (2,2) : empty,  (2,3) : empty,
    (3,1) : empty,  (3,2) : empty,  (3,3) : empty
}

playerMark = chooseMark()
if playerMark == 'X':
    cpuMark = 'O'
    isMaxTurn = False

else:
    cpuMark = 'X'
    isMaxTurn = True

cpuTurn = isMaxTurn

print('Wait a second... Preparing to defeat you...')
duration=0.5
for i in range(10):
    sleep(duration)
    print('.',end='',flush=True)
    duration -= 0.05
sleep(0.5)
print()

printBoard(board)

for turn in range(9):
    if cpuTurn :
        print("CPU's move:\n")
        moveSet = minimax(board,isMaxTurn)
        markBox(board,moveSet['move'],cpuMark)
    else:
        move = acceptValidMove(board)
        markBox(board,move,playerMark)

    cpuTurn = not cpuTurn

    printBoard(board)

    score = evaluateBoard(board)
    if score < 0:
        print("\n'O' wins the game!")
        sleep(3)
        exit()
    elif score > 0:
        print("\n'X' wins the game!")
        sleep(3)
        exit()

    print()

print('\nAww.. It was a draw!\n')
sleep(3)
