
#Reversi imports
import random
import sys
import os
from threading import Timer
import time
def drawBoard(board):
    #Prints out board that is passed. Return None.
    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'
    print  ('    1   2   3   4   5   6   7   8')
    print(HLINE)
    for y in range(8):
        #print(VLINE)
        print (y+1,end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]),end=' ')
        print('|')
        #print(VLINE)
        print(HLINE)

def resetBoard(board):
# boardReset
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '
            
    # starting pieces
    board[3][3]='X'
    board[3][4]='O'
    board[4][3]='O'
    board[4][4]='X'
    

def getNewBoard():
    #create a new blank board 
    board=[]
    for i in range(8):
        board.append([' '] * 8)
        
    return board

def opponent(tile):

    return 'X' if tile is 'O' else 'O'

def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid
    # If it's a valid move, returns a list of spaces that would become the players if they made a move here
    
    if not isOnBoard(xstart,ystart) or board[xstart][ystart] != ' ':
        return False
    board[xstart][ystart] = tile # temporarily set the tile on the board
    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'
    tilesToFlip= []
    #up, up,down,left, right diagonals
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x,y = xstart, ystart
        x += xdirection #first step
        y += ydirection
        #if piece belong to other player next to our
        # the first step in this direction must be 1) on the board and 2) must be occupied by the other player’s tile
        if isOnBoard(x,y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x,y):
                continue
            # if the first space does have the other player’s tile, then check
            #that direction until it reaches one of the player’s tiles. 
            #If it reaches past the end of the board continue back to the for statement and try the next direction.
            while board [x][y] == otherTile:
                x+=xdirection
                y+=ydirection
                #quit while loop and continue in for
                if not isOnBoard(x,y):
                    break
            if not isOnBoard(x,y):
                continue
        #Find out if there are pieces to flip over
        #reverse till we reach original place taking notes
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x,y])
            #restore empty space        
          
    board[xstart][ystart] = ' '
    #if no tiles were flipped, not a valid move        
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip   

def isOnBoard(x, y):
    #Returns True: if on Board else false
    return x>=0 and x<=7 and y >=0 and y <=7

def getBoardWithValidMoves(board, tile):
    dupeBoard = getBoardCopy(board)
    for x,y in getValidMoves(dupeBoard,tile):
        dupeBoard[x][y] = '.'
    return dupeBoard

def getValidMoves(board,tile):
    #Return list of [x,y] array of valid moves for 
    #given player and board
    #checks all spaces and each valid move is appended
    validMoves=[]
    
    for x in range(8):
        for y in range (8):
            if isValidMove(board,tile,x,y) != False:
                #print('this is a valid move: ' +str(x)+ ' '+str(y))
                validMoves.append([x,y])
    return validMoves
def getPlayerScoreOfBoard(player,board):
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    if(player == 'X'):
            return xscore
    else:
            return oscore
def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}

def enterPlayerTile():
    tile =''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()
        if tile == 'X':
            return ['X','O']
        else:
            return ['O','X']

def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'
        

def playAgain():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

def makeMove(board,tile,xstart,ystart):
    tilesToFlip = isValidMove(board,tile,xstart,ystart)
    if tilesToFlip == False:
        return False,board
    board[xstart][ystart] = tile
    for x,y in tilesToFlip:
        board[x][y] = tile
    return True,board

def getBoardCopy(board):
    dupeBoard= getNewBoard()
    
    for x in range (8):
        for y in range (8):
            dupeBoard[x][y]= board[x][y]
    return dupeBoard

def isOnCorner(x, y):
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def getPlayerMove(board, playerTile,cyborg,timer):
    if(cyborg=='cyborg'):
        copy = getBoardCopy(board)

        bestMove = minimax(copy,playerTile, int(depthplayer),float('-inf'),float('inf'), timer)[1]
        
        return bestMove
        
    DIGITS1T08 = '1 2 3 4 5 6 7 8'.split()
    def stop():
        print('sorry, timeout quitting...')
        os._exit(0)
        
    t = Timer(timer, stop)
    t.start()
    prompt = ("You have %d seconds to choose an option...\n" % timer)
          
        
            
    while True:
 
        print('Enter your move, or type quit to end the game, or hints to turn on/off hints')
        move = input(prompt).lower()
        t.cancel()
        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'
        if len(move) == 2 and move[0] in DIGITS1T08 and move [1] in DIGITS1T08:
            x= int(move [0]) -1
            y = int(move[1]) -1
            if isValidMove(board, playerTile,x,y)==False:
                continue
            else:
                break
        else:
            print ('That is not a valid move. Type the x digit (1-8) then y digit (1-8). ex: 76')
    return [x,y]
            

def getComputerMove(board,computerTile,strategy,dept,t):
    if(strategy == 'minimax'):
        copy = getBoardCopy(board)

        bestMove = minimax(copy,computerTile,int(depth),float('-inf'),float('inf'),t)[1]
        
        return bestMove
    else:    
        possibleMoves = getValidMoves(board, computerTile)
        print(possibleMoves)
        random.shuffle(possibleMoves)
    
        for x, y in possibleMoves:
            if isOnCorner(x,y):
                return [x,y]
   
        bestScore = -1
        for x,y in possibleMoves:
            dupeBoard = getBoardCopy(board)
            makeMove(dupeBoard, computerTile,x,y)
            score = getScoreOfBoard(dupeBoard)[computerTile]
            print('bestScore '+str(bestScore))
            print('score: '+str(score))
            if score > bestScore:
                bestMove = [x, y]
                bestScore = score
    return bestMove


def showPoints(playerTile, computerTile):
    scores = getScoreOfBoard(mainBoard)
    print(scores)
    print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))

#player here is equal to tile elsewhere


def minimax(evalboard,player, depth,alpha,beta,t):
    print(depth)
    def value(board,alpha,beta):
        opp = opponent(player)
        newDepth = depth-1;
        #define value as opposite of us, computed recursively by applying minimax
        value = -minimax(board[1],opp,newDepth,-beta,-alpha,t)[0]

        return value
    
    #if depth 0 just return value
    if depth == 0 or time.time() > t:
        score = getPlayerScoreOfBoard(player,evalboard)
        return score,None
    #evaluate all moves by their IMPLICATION DEPTH
    #first get all valid moves
    moves = getValidMoves(evalboard,player)

    #no valid moves
    if not moves:
        #print('No moves')
        return float('-inf'),None
    #if serveral moves, take the one with max value (aka best choise)
    #FIX THIS!!!
    
    best_move=moves[0];
    for m in moves:
        #print('depth'+str(depth))
        #print('The move: ')
        #print(m[0],m[1])
        
        #if alpha move gives a better scora than beta, stop looking
        #since opponent will avoid this branch 
        if alpha >= beta:
            break;
            
        newAlpha = value(makeMove(getBoardCopy(evalboard),player,m[0],m[1]),alpha,beta)
        if newAlpha > alpha:
            
            best_move=m
            alpha=newAlpha
                  
    return [alpha,best_move]
def getInputDepth():
     print('Input max search depth:')
     depth = input()
     return depth
 
print('Welcome to Reversi!')


while True:

    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    
    print('Set timeout!:')
    timer = int(input())
    print('Set max runningtime for minimax: ')
    t=int(input())
    playerTile, computerTile = enterPlayerTile()
    depth = getInputDepth()
    showHints = False
    turn = whoGoesFirst()
    #playerTile, computerTile=['X','O']
    #turn = 'computer'
    #depth=10
    depthplayer = 2
    print('The '+ turn + ' will go first')
    
    while True:
        if turn == 'player':
            if showHints:
                validMovesBoard = getBoardWithValidMoves(mainBoard,playerTile)
                
                drawBoard(validMovesBoard)
            else:
                drawBoard(mainBoard)
                
            showPoints(playerTile,computerTile)
         
          
            move = getPlayerMove(mainBoard, playerTile,'notcyborg',timer)  
           
              
            if move == 'quit':
                print('Bye, thanks for playing')
                sys.exit()
            elif move == 'hints':
                    showHints = not showHints
                    continue
            else:
                makeMove(mainBoard, playerTile, move[0],move[1])
                
            if getValidMoves(mainBoard,computerTile)==[]:
                 break
            else:
                turn = 'computer'
            
        else:
             #computerturn
            drawBoard(mainBoard)
            showPoints(playerTile,computerTile)
            input('Press Enter to see the Computers move')
            x,y = getComputerMove(mainBoard,computerTile,'minimax',depth,time.time() + t)
            makeMove(mainBoard,computerTile,x,y)    
            if getValidMoves(mainBoard,playerTile) == []:
                break
            else:
                turn ='player'
    #display final score
    drawBoard(mainBoard)
    
    scores=getScoreOfBoard(mainBoard)
    print('X score %s points, O scored %s points' % (scores['X'],scores['O']))
                
    if not playAgain():
           break
       
