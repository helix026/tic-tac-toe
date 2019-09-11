
empty = ' '

def chooseMark():
    valid = False
    while not valid:
        mark = input("Choose mark, 'X' or 'O' :")
        if mark == 'X' or mark == 'O':
            valid = True
        else:
            print('Invalid choice!')
    return mark

def fetchEmptyBoxes(board):
    emptyBoxes = []
    for box in board:
        if board[box] == empty:
            emptyBoxes.append(box)
    return emptyBoxes

def markBox(board,box,mark): # *box* is a Tuple containing index of box, mark is either 'X' or 'O'
    board[box] = mark

def printBoard(board):
    '''
    for row in range(1,4):
        for col in range(1,4):
            print(board[(row,col)],end='\t')
        print()
    '''
    print(' -------------')
    print(' |',board[(1,1)],'|',board[(1,2)],'|',board[(1,3)],'|')
    print(' -------------')
    print(' |',board[(2,1)],'|',board[(2,2)],'|',board[(2,3)],'|')
    print(' -------------')
    print(' |',board[(3,1)],'|',board[(3,2)],'|',board[(3,3)],'|')
    print(' -------------')

def acceptValidMove(board):
    valid=False
    emptyBoxes = fetchEmptyBoxes(board)

    while not valid :
        move = input("Enter your move:")
        move = tuple( int(n) for n in move.split() )
        if ( move in emptyBoxes ) and ( len(move) is 2 ) :
            valid = True
        else:
            print("Invalid move!")
    return move


def evaluateBoard(board):
    bonus = len(fetchEmptyBoxes(board))
    #rows
    for i in range(1,4):
        if board[(i,1)]==board[(i,2)]==board[(i,3)]:
            score =  int(board[(i,1)]=='X') * ( 50 + bonus ) - int(board[(i,1)]=='O') * ( 50 + bonus )
            if( score != 0 ):
                return score


    #cols
    for i in range(1,4):
        if board[(1,i)]==board[(2,i)]==board[(3,i)]:
            score = int(board[(1,i)]=='X') * ( 50 + bonus)  - int(board[(1,i)]=='O') *  ( 50 + bonus )
            if( score != 0):
                return score

    #diagonals
    if board[(1,1)]==board[(2,2)]==board[(3,3)] or board[(1,3)]==board[(2,2)]==board[(3,1)]:
        score = int(board[(2,2)]=='X') *  ( 50 + bonus) - int(board[(2,2)]=='O') *  ( 50 + bonus )
        if( score != 0):
            return score

    return 0

def minimax( board, isMaxTurn):
    possibleMoveSets = []
    score = evaluateBoard(board)
    emptyBoxes = fetchEmptyBoxes(board)

    if score != 0 or len(emptyBoxes) == 0 :
        return { 'move':(0,0),'score':score }
    else:
        if isMaxTurn:
            for box in emptyBoxes:
                boardCopy = board.copy()
                markBox(boardCopy,box,'X')
                set = minimax(boardCopy, not isMaxTurn)
                possibleMoveSets.append( {'move':box,'score':set['score']} )

            bestMoveSet = possibleMoveSets[0]
            for set in possibleMoveSets:
                if(set['score'] > bestMoveSet['score']):
                    bestMoveSet = set
        else:
            for box in emptyBoxes:
                boardCopy = board.copy()
                markBox(boardCopy,box,'O')
                set = minimax(boardCopy, not isMaxTurn)
                possibleMoveSets.append(  {'move':box,'score':set['score']} )

            bestMoveSet = possibleMoveSets[0]
            for set in possibleMoveSets:
                if(set['score'] < bestMoveSet['score']):
                    bestMoveSet = set

    return bestMoveSet
