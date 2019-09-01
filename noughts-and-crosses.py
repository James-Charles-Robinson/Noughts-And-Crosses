import pygame
import os
import random
import operator
import sys
from pygame.locals import*

'''
Noughts and Crosses (X's and O's) game complete with easy, normal and hard ai's.
Has a pygame interface with menus.
Can also be played with 2 people
'''

pygame.init() #initialises game
playersTurn = 1 #who goes first, cross or noughts, by defult cross
usedSegments = [] #segments used
player1Segments = [] #segments cross has
player2Segments = [] #segments nought has
mode = 2 #defult is 2 player
winner = 0
disIntro = 1 #displays option for 1 player or 2 player at start
draw = None
playAgain = "False"
difSelect = 0
difficulty = 2
score = 0
winningCombos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 4, 7, 2, 5, 8, 3, 6, 9, 1, 5, 9, 3, 5, 7]

def resource_path(relative): #used to make importing font in easier
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

winHeight = 550
winWidth = 500
refHeight = 500 #reference hight for calculations
refWidth = 500 #reference width for calculations
win = pygame.display.set_mode((winWidth, winHeight)) #creates window and calls it win
pygame.display.set_caption("Noughts and Crosses - By James Robinson") #the name of the application


segment1 = [(0, 0), ((refWidth/3), 0), (0, (refHeight/3)), ((refWidth/3), (refHeight/3))] #segments cornors, used periodically but may be removed in future
segment2 = [((refWidth/3), 0), (((refWidth/3)*2), 0), ((refWidth/3), (refHeight/3)), (((refWidth/3)*2), (refHeight/3))]
segment3 = [(((refWidth/3)*2), 0), (refWidth, 0), (((refWidth/3)*2), (refHeight/3)), (refWidth, (refHeight/3))]
segment4 = [(0, (refHeight/3)), ((refWidth/3), (refHeight/3)), (0, ((refHeight/3)*2)), ((refWidth/3), ((refHeight/3)*2))]
segment5 = [((refWidth/3), (refHeight/3)), (((refWidth/3)*2), (refHeight/3)), ((refWidth/3), ((refHeight/3)*2)), (((refWidth/3)*2), ((refHeight/3)*2))]
segment6 = [(((refWidth/3)*2), (refHeight/3)), (refWidth, (refHeight/3)), (((refWidth/3)*2), ((refHeight/3)*2)), (refWidth, ((refHeight/3)*2))]
segment7 = [(0, ((refHeight/3)*2)), ((refWidth/3), ((refHeight/3)*2)), (0, refHeight), ((refWidth/3), refHeight)]
segment8 = [((refWidth/3), ((refHeight/3)*2)), (((refWidth/3)*2), ((refHeight/3)*2)), ((refWidth/3), refHeight), (((refWidth/3)*2), refHeight)]
segment9 = [(((refWidth/3)*2), ((refHeight/3)*2)), (refWidth, ((refHeight/3)*2)), (((refWidth/3)*2), refHeight), (refWidth, refHeight)]

def Intro(disIntro, mode, difSelect): #intro screen
    if disIntro == 1:
        disIntro = 1
        mode = 2
        Lfont = pygame.font.Font(resource_path(os.path.join('C:\\Windows\\Fonts', 'Arial.ttf')), 40) #Large font
        Sfont = pygame.font.Font(resource_path(os.path.join('C:\\Windows\\Fonts', 'Arial.ttf')), 30) #Small font
        win.fill((0,0,0)) #removes the board
        label1 = Lfont.render("Welcome To My Game", 1, (255,255,255)) #puts the lables in thier positions
        win.blit(label1, (50, 100))
        label2 = Sfont.render("2 Player      1 Player       QUIT", 1, (255,255,0))
        win.blit(label2, (50, 300))
        xpos, ypos = pygame.mouse.get_pos()
        if xpos > 40 and xpos < 170 and ypos > 270 and ypos < 350: #hover over 1 player
            if pygame.mouse.get_pressed() == (1, 0, 0): #player mode is 2 and displayIntro is 0
                mode = 2
                disIntro = 0
                win.fill((0,0,0))
                difSelect = 0
        if xpos > 200 and xpos < 320 and ypos > 270 and ypos < 350: #hover over 2 player
            if pygame.mouse.get_pressed() == (1, 0, 0): #player mode is 1 and displayIntro is 0
                disIntro = 0
                mode = 1
                difSelect = 1
                win.fill((0,0,0))
        if xpos > 340 and xpos < 460 and ypos > 270 and ypos < 350: #hover over quit
            if pygame.mouse.get_pressed() == (1, 0, 0): #quit
                pygame.quit()
    else:
        disIntro = 0
        difSelect = 0
        mode = mode
    return(disIntro, mode, difSelect)

def Board():  #draws the board
    if disIntro != 1 and draw != True and (winner == None or winner == 0): #if we arent in the intro or winning/draw menu
        
        #verticle 2 lines
        pygame.draw.rect(win, (255, 255, 255), ((refWidth/3), 0, 5, refHeight))
        pygame.draw.rect(win, (255, 255, 255), (((refWidth/3)*2), 0, 5, refHeight))
        #horizontal 2 lines
        pygame.draw.rect(win, (255, 255, 255), (0, (refHeight/3), refWidth, 5))
        pygame.draw.rect(win, (255, 255, 255), (0, ((refHeight/3)*2), refWidth, 5))

def AI(playersTurn, selectedSegment, winner, score):
    if winner == None or winner == 0: #if theres no ai
        totalMovePoints = 0
        goodMoves = {}
        for i in range(9):
            if i+1 not in usedSegments:#go through each avaliable space to see if its a good choice
                             
                if difficulty == 2: #normal diffulculty analyses if the move will allow them to win and 75% chance it will analyse if the player moves to that
                                    #spot if they will win
                    number = random.randint(1,4)
                    AiPoints = AIWin(i+1, score)
                    if number < 4:
                        PlayerPoints = AIPlayerWin(i+1, score)
                        totalMovePoints = AiPoints + PlayerPoints
                    else:
                        totalMovePoints = AiPoints
                    if totalMovePoints > 0: #if its decided that moveing to that spot would be good it adds it to the goodmoves dictionary
                        goodMoves.update({i+1 : totalMovePoints})


                elif difficulty == 3: #same as normal ai but it will always make the winning move and stop the player from winning.
                    PlayerPoints = AIPlayerWin(i+1, score)
                    AiPoints = AIWin(i+1, score)
                    totalMovePoints = AiPoints + PlayerPoints
                    if totalMovePoints > 0:
                        goodMoves.update({i+1 : totalMovePoints})

        #easy ai will never make a moved to win or stop a win on purpose
                        
        if len(goodMoves) == 0: #if there was no winning or loosing moves avaliable (first half of the game), then rules of the game will be used to determine best move
            
            if difficulty == 1 or difficulty == 2: #if easy or noraml ai, the move will be random
                number = random.randint(1, 9)
                if number not in usedSegments:
                    selectedSegment = number


            if difficulty == 3: #hard ai will use rules of the game to always win or draw
                
                if len(player1Segments) == 1 and player1Segments[0] != 5: #if the player has moved once and not to the middle move there
                    selectedSegment = 5
                elif len(player1Segments) == 1 and player1Segments[0] == 5: #otherwise move to an cornor (always 3)
                    selectedSegment = 3
                elif (len(player1Segments) == 2) and ((player1Segments[0] == 1 and player1Segments[1] == 9) or (player1Segments[0] == 3 and player1Segments[1] == 7)) and player2Segments[0] == 5:
                    selectedSegment = 2          
                else:
                    cornors = [1, 3, 7, 9]
                    sides = [2, 4, 6, 8]
                    for l in range(10):
                        number = cornors[random.randrange(len(cornors))]
                        if number not in usedSegments:#go for cornors first
                            selectedSegment = number
                    if selectedSegment == 0: #then for side
                        for p in range(5):
                            if 5 not in usedSegments:
                                selectedSegment = number
                            number = sides[random.randrange(len(sides))]
                            if number not in usedSegments:
                                selectedSegment = number

        else: #if we did find a winning or loosing move go for that, prorise winning moves
            goodMoves = sorted(goodMoves.items(), key=operator.itemgetter(1), reverse=True)
            bestPosition, bestScore = goodMoves[0]
            selectedSegment = bestPosition
        return(selectedSegment)

    
def AIPlayerWin(i, score): #calcualtes if the player would win if they went to that move
    movePoints = 0
    player1Segments.append(i)
    winningMove, score = Win(1, score)
    if winningMove == 1:
        movePoints = 10
    player1Segments.remove(i)
    return(movePoints)

def AIWin(i, score): #calculates if making that move would make the ai win
    movePoints = 0
    player2Segments.append(i)
    winningMove, score = Win(2, score)
    if winningMove == 2:
        movePoints = 100
    player2Segments.remove(i)
    return(movePoints)


def AiDif(difSelect, difficulty): #select ai difficulty screen
    if difSelect == 1:
        Lfont = pygame.font.Font(resource_path(os.path.join('C:\\Windows\\Fonts', 'Arial.ttf')), 40) #Large font
        Sfont = pygame.font.Font(resource_path(os.path.join('C:\\Windows\\Fonts', 'Arial.ttf')), 30) #Small font
        win.fill((0,0,0)) #removes the board
        label1 = Lfont.render("     Which Difficulty", 1, (255,255,255)) #puts the lables in thier positions
        win.blit(label1, (50, 100))
        label2 = Sfont.render("    Easy      Normal       Hard", 1, (255,255,0))
        win.blit(label2, (50, 300))
        xpos, ypos = pygame.mouse.get_pos()
        if xpos > 75 and xpos < 155 and ypos > 270 and ypos < 350: #hover over easy
            if pygame.mouse.get_pressed() == (1, 0, 0):
                difficulty = 1
                difSelect = 0
                win.fill((0,0,0))
        if xpos > 180 and xpos < 310 and ypos > 270 and ypos < 350: #hover over normal
            if pygame.mouse.get_pressed() == (1, 0, 0):
                difficulty = 2
                difSelect = 0
                win.fill((0,0,0))
        if xpos > 330 and xpos < 430 and ypos > 270 and ypos < 350: #hover over hard
            if pygame.mouse.get_pressed() == (1, 0, 0):
                difficulty = 3
                difSelect = 0
                win.fill((0,0,0))
    else:
        difSelect = 0
    return(difSelect, difficulty)    


def Select(playersTurn, mode, score): #select a box
    if (mode == 2) or (mode == 1 and playersTurn == 1):
        if pygame.mouse.get_pressed() == (1, 0, 0): #if button pressed
            pos = pygame.mouse.get_pos()
            xPos, yPos = pygame.mouse.get_pos() #gets the x and y pos of mouse
            for i in range(9):#goes through all nine segments
                segment = 0
                segment = i + 1
                if segment == 1:#checks if the mouse press was in the boundaries of each box, if it is it returns that segment
                    xTopLeft, yTopLeft = segment1[0]
                    xTopRight, yTopRight = segment1[1]
                    xBottomLeft, yBottomLeft = segment1[2]
                    if xPos >= xTopLeft and xPos <= xTopRight and yPos >= yTopLeft and yPos <= yBottomLeft:
                        selectedSegment = i+1
                if segment == 2:
                    xTopLeft, yTopLeft = segment2[0]
                    xTopRight, yTopRight = segment2[1]
                    xBottomLeft, yBottomLeft = segment2[2]
                    if xPos >= xTopLeft and xPos <= xTopRight and yPos >= yTopLeft and yPos <= yBottomLeft:
                        selectedSegment = i+1
                if segment == 3:
                    xTopLeft, yTopLeft = segment3[0]
                    xTopRight, yTopRight = segment3[1]
                    xBottomLeft, yBottomLeft = segment3[2]
                    if xPos >= xTopLeft and xPos <= xTopRight and yPos >= yTopLeft and yPos <= yBottomLeft:
                        selectedSegment = i+1
                if segment == 4:
                    xTopLeft, yTopLeft = segment4[0]
                    xTopRight, yTopRight = segment4[1]
                    xBottomLeft, yBottomLeft = segment4[2]
                    if xPos >= xTopLeft and xPos <= xTopRight and yPos >= yTopLeft and yPos <= yBottomLeft:
                        selectedSegment = i+1
                if segment == 5:
                    xTopLeft, yTopLeft = segment5[0]
                    xTopRight, yTopRight = segment5[1]
                    xBottomLeft, yBottomLeft = segment5[2]
                    if xPos >= xTopLeft and xPos <= xTopRight and yPos >= yTopLeft and yPos <= yBottomLeft:
                        selectedSegment = i+1
                if segment == 6:
                    xTopLeft, yTopLeft = segment6[0]
                    xTopRight, yTopRight = segment6[1]
                    xBottomLeft, yBottomLeft = segment6[2]
                    if xPos >= xTopLeft and xPos <= xTopRight and yPos >= yTopLeft and yPos <= yBottomLeft:
                        selectedSegment = i+1
                if segment == 7:
                    xTopLeft, yTopLeft = segment7[0]
                    xTopRight, yTopRight = segment7[1]
                    xBottomLeft, yBottomLeft = segment7[2]
                    if xPos >= xTopLeft and xPos <= xTopRight and yPos >= yTopLeft and yPos <= yBottomLeft:
                        selectedSegment = i+1
                if segment == 8:
                    xTopLeft, yTopLeft = segment8[0]
                    xTopRight, yTopRight = segment8[1]
                    xBottomLeft, yBottomLeft = segment8[2]
                    if xPos >= xTopLeft and xPos <= xTopRight and yPos >= yTopLeft and yPos <= yBottomLeft:
                        selectedSegment = i+1
                if segment == 9:
                    xTopLeft, yTopLeft = segment9[0]
                    xTopRight, yTopRight = segment9[1]
                    xBottomLeft, yBottomLeft = segment9[2]
                    if xPos >= xTopLeft and xPos <= xTopRight and yPos >= yTopLeft and yPos <= yBottomLeft:
                        selectedSegment = i+1
            return(selectedSegment)#returns the segment
    else:
        selectedSegment = AI(playersTurn, 5, winner, score)
        return(selectedSegment)

def WhosGo(playersTurn): #simple function which swaps the go each turn
    if playersTurn == 1:
        playersTurn = 2
        pygame.time.delay(100) #wait time
    else:
        playersTurn = 1
        pygame.time.delay(100) #wait time
    return(playersTurn)

def Cross(topLeft, topRight, bottomLeft, bottomRight): #used so theres no images, just draws a box in the right position using the parameters given
    
    xtopLeft, ytopLeft = topLeft #changes must be done to the co-ordinates so the cross doesnt go right the edge and looks nice
    xtopLeft = xtopLeft + 20
    ytopLeft = ytopLeft + 20
    topLeft = (xtopLeft, ytopLeft)
    
    xtopRight, ytopRight = topRight
    xtopRight = xtopRight - 20
    ytopRight = ytopRight + 20
    topRight = (xtopRight, ytopRight)

    xbottomLeft, ybottomLeft = bottomLeft
    xbottomLeft = xbottomLeft + 20
    ybottomLeft = ybottomLeft - 20
    bottomLeft = (xbottomLeft, ybottomLeft)

    xbottomRight, ybottomRight = bottomRight
    xbottomRight = xbottomRight - 20
    ybottomRight = ybottomRight - 20
    bottomRight = (xbottomRight, ybottomRight)
    
    pygame.draw.line(win, (255, 255, 255), (topLeft), (bottomRight), 10)
    pygame.draw.line(win, (255, 255, 255), (topRight), (bottomLeft), 10)

def Nought(x, y): #noughts are much easier as there are only 2 x and y values.
    x = x + 20
    y = y + 20
    pygame.draw.ellipse(win, (255, 255, 255), (x, y, 130, 130), 10)

def PlaceSymbol(playersTurn, selectedSegment,):#using the nought and cross functions a symbol is draw in a selected box
    if selectedSegment != None and (selectedSegment in usedSegments) == False: #if there is a selected segments and the segment hasnt been used before we draw in it
        if playersTurn == 1:
            
            if selectedSegment == 1:
                Cross((0, 0), ((refWidth/3), 0), (0, (refHeight/3)), ((refWidth/3), (refHeight/3)))
            if selectedSegment == 2:
                Cross(((refWidth/3), 0), (((refWidth/3)*2), 0), ((refWidth/3), (refHeight/3)), (((refWidth/3)*2), (refHeight/3)))
            if selectedSegment == 3:
                Cross((((refWidth/3)*2), 0), (refWidth, 0), (((refWidth/3)*2), (refHeight/3)), (refWidth, (refHeight/3)))
            if selectedSegment == 4:
                Cross((0, (refHeight/3)), ((refWidth/3), (refHeight/3)), (0, ((refHeight/3)*2)), ((refWidth/3), ((refHeight/3)*2)))
            if selectedSegment == 5:
                Cross(((refWidth/3), (refHeight/3)), (((refWidth/3)*2), (refHeight/3)), ((refWidth/3), ((refHeight/3)*2)), (((refWidth/3)*2), ((refHeight/3)*2)))
            if selectedSegment == 6:
                Cross((((refWidth/3)*2), (refHeight/3)), (refWidth, (refHeight/3)), (((refWidth/3)*2), ((refHeight/3)*2)), (refWidth, ((refHeight/3)*2)))
            if selectedSegment == 7:
                Cross((0, ((refHeight/3)*2)), ((refWidth/3), ((refHeight/3)*2)), (0, refHeight), ((refWidth/3), refHeight))
            if selectedSegment == 8:
                Cross(((refWidth/3), ((refHeight/3)*2)), (((refWidth/3)*2), ((refHeight/3)*2)), ((refWidth/3), refHeight), (((refWidth/3)*2), refHeight))
            if selectedSegment == 9:
                Cross((((refWidth/3)*2), ((refHeight/3)*2)), (refWidth, ((refHeight/3)*2)), (((refWidth/3)*2), refHeight), (refWidth, refHeight))
            player1Segments.append(selectedSegment) 
        elif playersTurn == 2:
            if selectedSegment == 1:
                Nought(0, 0)
            if selectedSegment == 2:
                Nought((refWidth/3), 0)
            if selectedSegment == 3:
                Nought(((refWidth/3)*2), 0)
            if selectedSegment == 4:
                Nought(0, (refHeight/3))
            if selectedSegment == 5:
                Nought((refWidth/3), (refHeight/3))
            if selectedSegment == 6:
                Nought(((refWidth/3)*2), (refHeight/3))
            if selectedSegment == 7:
                Nought(0, ((refHeight/3)*2))
            if selectedSegment == 8:
                Nought((refWidth/3), ((refHeight/3)*2))
            if selectedSegment == 9:
                Nought(((refWidth/3)*2), ((refHeight/3)*2))
            player2Segments.append(selectedSegment) #adds the segment to the used list for each player
        usedSegments.append(selectedSegment) #adds the segment to the used list
        turnDone = True            
        return(turnDone)

def Win(playersTurn, score): #checks to see if either players has one of the winning combos, theres 8 waays to win
    player1Segments.sort()
    score = score
    player2Segments.sort()
    winner = 0
    for c in range(0, 8):
        if winningCombos[c*3] in player1Segments and winningCombos[c*3+1] in player1Segments and winningCombos[c*3+2] in player1Segments:
            winner = 1
    for c in range(0, 8):
        if winningCombos[c*3] in player2Segments and winningCombos[c*3+1] in player2Segments and winningCombos[c*3+2] in player2Segments:
            winner = 2
    return(winner, score)
    print(score, winner)
def DisplayWin(winner): #takes us to the winner display, shows us the winner and asks if we want to play again
    font = pygame.font.Font(resource_path(os.path.join('C:\\Windows\\Fonts', 'Arial.ttf')), 40) #my selected font, can be changed easily
    posX, posY = pygame.mouse.get_pos()
    playAgain = "False"
    run = True
    if winner != None and winner != 0:
        win.fill((0,0,0)) #removes the board
        if winner == 1:
            label1 = font.render("PLAYER 1 WINS", 1, (255,255,255)) #puts the lables in thier positions
        elif winner == 2 and mode == 2:
            label1 = font.render("PLAYER 2 WINS", 1, (255,255,255)) #puts the lables in thier positions
        elif winner == 2 and mode == 1:
            label1 = font.render(" THE AI WINS", 1, (255,255,255)) #puts the lables in thier positions
        win.blit(label1, (110, 100))
        label2 = font.render("PLAY      QUIT", 1, (255,255,0))
        win.blit(label2, (130, 300))
        if posX > 100 and posX < 220 and posY > 270 and posY < 350:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                playAgain = "True" #if they click near the play label then we make the play again varibale true
        elif posX > 275 and posX < 395 and posY >270 and posY < 350:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                run = False
                playAgain = "False" #other wise if they click near exit we quit the game
                pygame.quit()

        else:
            run = True
            playAgain = "False"
    else:
        run = True
        playAgain = "False"
    return((str(playAgain)), (str(run)))

def Draw(): #if all segments are used its a draw
    if len(usedSegments) == 9:
        draw = True
        return(draw)

def Score(score): #displays the score at the bottom of the screen
    font=pygame.font.Font(None,40)
    if mode == 1:
        if difficulty == 1:
            scoreMessage = " Easy Score = " + str(score)
        if difficulty == 2:
            scoreMessage = "Normal Score = " + str(score)
        if difficulty == 3:
            scoreMessage = " Hard Score = " + str(score)
        label = font.render(scoreMessage, 1, (255,255,255))
        win.blit(label, (140, 510))


def DisplayDraw(draw, winner, playAgain, run): #almost the same as the winner display just different lables
    if draw == True and (winner == None or winner == 0):
        posX, posY = pygame.mouse.get_pos()
        font=pygame.font.Font(None,40)
        playAgain = "False"
        run = True
        win.fill((0,0,0))
        label1 = font.render("DRAW", 1, (255,255,255))
        win.blit(label1, (180, 100))
        label2 = font.render("PLAY      QUIT", 1, (255,255,0))
        win.blit(label2, (130, 300))
        if posX > 100 and posX < 220 and posY > 270 and posY < 350:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                playAgain = "True"
                run = True
        elif posX > 275 and posX < 395 and posY >270 and posY < 350:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                run = False
                playAgain = "False"
                pygame.quit()
        else:
            run = True
            playAgain = "False"
    elif draw != True and (winner == None or winner == 0):
        run = True
        playAgain = "False"
    
    return(str(playAgain), str(run))

######   MAIN LOOP   #######

run = True
while run: #main loop, i tried to make it as short as possible to keep it simple using functions
    pygame.time.delay(100) #tick speed
    for event in pygame.event.get(): #quit if you click the X
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
    if disIntro != 1: #if we arent in intro
        if difSelect == 1:
            difSelect, difficulty = AiDif(difSelect, 2)
            score = 0
        else:
            turnDone = False
            Board() #draw board
            selectedSegment = Select(playersTurn, mode, score)#player selects a segment
            turnDone = PlaceSymbol(playersTurn, selectedSegment)#places a symbol in that segment
            winner, score = Win(playersTurn, score) #detects if someone wins
            draw = Draw() #detects if its a draw
            playAgain, run = DisplayWin(winner) #displays win page if omeone winns
            Score(score)
            playAgain, run = DisplayDraw(draw, winner, playAgain, run) #displays draw page if someone draws
            if playAgain == "True": #if the game is ended this restarts it
                        winner = 0
                        score = score + 1
                        playersTurn = 1
                        usedSegments = []
                        player1Segments = []
                        player2Segments = []
                        draw = None
                        win.fill((0,0,0))
                        pygame.time.delay(100)
            if turnDone == True: #swaps the turn
                playersTurn = WhosGo(playersTurn)
    else:
        disIntro, mode, difSelect = Intro(disIntro, mode, difSelect)
    pygame.display.update() #end of main loop, update display 
pygame.quit()# if loop left game stops
