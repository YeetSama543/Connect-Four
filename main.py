import pygame
import math
import sys

def display(): #displays the game board
    for row in grid:
        for col in row:
            print(col, end = " ")
        print()
    print("-------------")
    print("0 1 2 3 4 5 6")
def makeBoard(): #displays the board as a 2x2
    grid = [[0 for i in range(NUM_COLS)] for j in range(NUM_ROWS)]
    return grid
def placePiece(grid, col, piece) -> bool: #tries to place a piece. returns bool based on success
    success = False

    if col >= 0 and col < NUM_COLS: #valid column value
        if validColumn(col): #column is not full
            nextRow = getNextValidRow(grid, col)
            grid[nextRow][col] = piece
            success = True
        else: #column is full
            success = False
    else: #invalid column value
        success = False
    return success
def validColumn(col) -> bool: #determines if given col is valid or not
    if grid[0][col] == 0:
        return True
    else:
        return False
def getNextValidRow(grid, col) -> int: #determines the row the piece will fall into
    nextRow = -1
    if not validColumn(col):
        return nextRow
    else:
        for i in range(NUM_ROWS - 1, -1, -1):
            if grid[i][col] == 0:
                nextRow = i
                return nextRow
    return nextRow
def isWin(player) -> bool: #determines if the last move resulted in a win
    isWin = False
    #horizontal
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS - 3):
            if grid[i][j] == player and grid[i][j + 1] == player and grid[i][j + 2] == player and grid[i][j + 3] == player:
                isWin = True
                return isWin
    
    #vertical
    for i in range(NUM_ROWS - 3):
        for j in range(NUM_COLS):
            if grid[i][j] == player and grid[i + 1][j] == player and grid[i + 2][j] == player and grid[i + 3][j] == player:
                isWin = True
                return isWin
    
    #diag forward
    for i in range(NUM_ROWS - 3):
        for j in range(NUM_COLS - 3):
            if grid[i][j] == player and grid[i + 1][j + 1] == player and grid[i + 2][j + 2] == player and grid[i + 3][j + 3] == player:
                isWin = True
                return isWin
    #diag backwards
    for i in range(3, NUM_ROWS):
        for j in range(NUM_COLS - 3):
            if grid[i][j] == player and grid[i - 1][j + 1] == player and grid[i - 2][j + 2] == player and grid[i - 3][j + 3] == player:
                isWin = True
                return isWin
    return isWin
def isDraw(): #checks to see if board is full
    draw = True
    for i in range(NUM_COLS):
        if grid[0][i] == 0:
            draw = False
            return draw
    return draw
def drawBoard(board):
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS, 0, -1): 
            #draw the blue rect
            pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            #draw the black circle
            circle = ((col * SQUARE_SIZE + (SQUARE_SIZE//2), row * SQUARE_SIZE +(SQUARE_SIZE//2)))
            if board[row - 1][col] == 0: #no piece placed
                pygame.draw.circle(screen, BLACK, circle, RADIUS)
            elif board[row - 1][col] == 1: #p1 placed a piece
                pygame.draw.circle(screen, RED, circle, RADIUS)
            else: #p2 placed a piece
                pygame.draw.circle(screen, YELLOW, circle, RADIUS)
#constants
NUM_COLS = 7
NUM_ROWS = 6
BLUE = (0,0,255)
RED = (255,0,0)
BLACK = (0,0,0)
YELLOW = (255,255,0)
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE // 2 - 5

#global vars
grid = makeBoard()
playerTurn = 0
gameOver = False
winner = 0

#building screen
width = NUM_COLS * SQUARE_SIZE
height = (NUM_ROWS + 1) * SQUARE_SIZE
dimensions = (width, height)

pygame.init()
screen = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Connect Four")
font = pygame.font.SysFont("Arial", 75)

while not gameOver:
    for event in pygame.event.get():

        if event.type == pygame.QUIT: #Window is closed
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION: #mouse moves-display the piece about to drop
            #ensure only 1 circle is drawn
            pygame.draw.rect(screen, BLACK, (0, 0, NUM_COLS * SQUARE_SIZE, SQUARE_SIZE))
            #gather x val
            x = event.pos[0]
            y = SQUARE_SIZE //2
            circle = (x,y)
            if playerTurn == 0: #p1 turn
                pygame.draw.circle(screen, RED, circle, RADIUS)
            else: #p2 turn
                pygame.draw.circle(screen, YELLOW, circle, RADIUS)

        if event.type == pygame.MOUSEBUTTONDOWN: #mouse is clicked, try to place a piece
            if playerTurn == 0: #player 1 turn
                position = event.pos[0]
                col = position // SQUARE_SIZE
                
                #place piece
                if not placePiece(grid, col, 1): #don't change turns
                    playerTurn += 1

                #check if win
                if isWin(1):
                    gameOver = True
                    winner = 1
                #check if draw
                if isDraw():
                    gameOver = True
                    winner = 0
                #change turns
                playerTurn += 1
                playerTurn %= 2

            else: #player 2 turn
                if playerTurn == 1: #player 2 turn
                    position = event.pos[0]
                    col = position // SQUARE_SIZE
                
                #place piece
                if not placePiece(grid, col, 2): #don't change turns
                    playerTurn += 1

                #check if win
                if isWin(2):
                    gameOver = True
                    winner = 2
                #check if draw
                if isDraw():
                    gameOver = True
                    winner = 0
                #change turns
                playerTurn += 1
                playerTurn %= 2

        #update and draw the board after any event
        drawBoard(grid)
        pygame.display.update()

    if gameOver:
        pygame.draw.rect(screen, BLACK, (0,0,NUM_COLS * SQUARE_SIZE, SQUARE_SIZE))
        if winner == 0: #draw
            text = font.render("Draw!", 1, BLUE)
            screen.blit(text, (40,10))
        elif winner == 1: #p1 wins
            text = font.render("Player 1 Wins!", 1, BLUE)
            screen.blit(text, (40,10))
        else: #p2 wins
            text = font.render("Player 2 Wins!", 1, BLUE)
            screen.blit(text, (40,10))
            
        pygame.display.update()
        pygame.time.wait(3000)


    
    