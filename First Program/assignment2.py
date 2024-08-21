from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 500, 800
ballx = bally = 0
dinit = 0
dNE = 0
dE = 0
gx1 = 0
gx2= 0
gy1 = 0
gy2 = 0
convertedZone = 0
actualZone = 0
randY = 0
randx = 0
pause = False
score = 0

receiver_position = 0
board_left = -200
board_right = -100

diamondBottom = []
diamondRight = []
diamondLeft = []

reciever_right = []
reciever_left = []

dcolor= [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)]
speed = 1
game_over = False

def convertToPreviousZone(x, y):

    global convertedZone, actualZone

    if (actualZone == 1):
        return [y, x]
    elif (actualZone == 2):
        return [-y , x]
    elif (actualZone == 3):
        return [-x, y]
    elif (actualZone == 4):
        return [-x , -y]
    elif (actualZone == 5):
        return [-y, -x]
    elif(actualZone == 6):
        return [y, -x]
    elif (actualZone == 7):
        return [x, -y]
    else:
        return [x, y]
def drawPoints(gx1, gy1, gx2, gy2, color):
    red , green, blue = color
    global dinit, dNE, dE
    # print(f"drawPoints->{gx1} {gy1} {gx2} {gy2}")
    while(gx1 <= gx2):
        if(dinit <= 0 ):
            dinit += dE
            gx1+=1
        elif(dinit> 0 ):
            dinit += dNE
            gx1 += 1
            gy1 += 1

        glPointSize(2)
        glBegin(GL_POINTS)
        glColor3f(red,green,blue)
        # print(f"x: {gx1}, y: {gy1}")
        x, y = convertToPreviousZone(gx1, gy1)
        glVertex2f(x, y)
        glEnd()

def convertZone(x1, y1, x2, y2, zone):
    # all are converted for zero zone

    if (zone == 1):
        return [y1, x1, y2, x2]
    elif (zone == 2):
        return [y1, abs(x1), y2, abs(x2)]
    elif (zone == 3):
        return [abs(x1), y1, abs(x2), y2]
    elif (zone == 4):
        return [abs(x1), y1, abs(x2), abs(x2)]
    elif (zone == 5):
        return [abs(y1), abs(x1), abs(y2), abs(x2)]
    elif(zone == 6):
        return [abs(y1), abs(x2), abs(y2), abs(x2)]
    elif(zone == 7):
        return [x1, -y1, x2, -y2]

def findZone(x1, y1, x2, y2):
    global dinit, dNE, dE, gx1, gx2, gy1, gy2, convertedZone, actualZone
    #check the zone where the points lies
    dx = x2 - x1
    dy = y2 - y1
    absDx = abs(dx)
    absDy = abs(dy)
    actualZone = 0

    #zone 0
    if (absDx >= absDy) and (dx >= 0 and dy >= 0):
        actualZone = 0
        # print("zone-0")
    # zone 1
    elif (absDy >= absDx) and (dx >= 0 and dy >= 0):
            # print("zone-1")
            actualZone = 1
    # zone 2
    elif (absDx <= absDy) and (dx <= 0 and dy >= 0):

        # print("zone-2")
        actualZone = 2
    # zone 3
    elif (absDy <= absDx) and (dx <= 0 and dy >= 0):
        actualZone = 3
        # print("zone-3")
    # zone 4
    elif (absDx >= absDy) and (dx <= 0 and dy <= 0):
        actualZone = 4
        # print("zone-4")

    # zone 5
    elif (absDy >= absDx) and (dx <= 0 and dy <= 0):
        actualZone = 5
        # print("zone-5")

    # zone 6
    elif (absDx <= absDy) and (dx >= 0 and dy <= 0):
        actualZone = 6
        # print("zone-6")
    # zone 7
    elif (absDy < absDx) and (dx > 0 and dy < 0):
        actualZone = 7
        # print("zone-7")


    if (actualZone != 0):
        x1, y1, x2, y2 = convertZone(x1, y1, x2, y2, actualZone)
        # print("line-118",x1, y1, x2, y2)
        gx1, gy1, gx2, gy2 = x1, y1, x2, y2
        dinit = (2 * (y2-y1)) - (x2-x1)
        dNE = (2 * (y2-y1)) - (2*(x2-x1))
        dE = 2*(y2-y1)
    else:
        gx1, gy1, gx2, gy2 = x1, y1, x2, y2
        # print(gx1, gy1, gx2, gy2)
        dinit  = (2 * (y2-y1)) - (x2-x1)
        dNE = (2 * (y2-y1)) - (2*(x2-x1))
        dE = 2*(y2-y1)

def pause_start():
    global pause
    color= [1.0, 1.0,0.0]
    if(pause):
        # play button
        findZone(-10, 220, 10, 235)
        drawPoints(gx1, gy1, gx2, gy2, color)

        findZone(-10, 248, 10, 235)
        drawPoints(gx1, gy1, gx2, gy2, color)

        findZone(-10, 220, -10, 248)
        drawPoints(gx1, gy1, gx2, gy2, color)

        # play button
    else:
        # Pause
        findZone(-10, 230, -10, 250)
        drawPoints(gx1, gy1, gx2, gy2, color)

        findZone(10, 230, 10, 250)
        drawPoints(gx1, gy1, gx2, gy2, color)

        # Pause


def backButton():
    color = [0.0,1.0,1.0]
    findZone(-250, 240, -240, 250)
    drawPoints(gx1, gy1, gx2, gy2, color)

    findZone(-250, 240, -230, 240)
    drawPoints(gx1, gy1, gx2, gy2, color)

    findZone(-240, 230, -250, 240)
    drawPoints(gx1, gy1, gx2, gy2, color)


def checkCollision():

    global randY, diamondBottom, receiver_position, board_left, board_right, score, diamondLeft, reciever_left, reciever_right, dcolor


    #diamond x and y destructure

    diamond_x_bottom = diamondBottom[0]
    diamond_y_bottom = diamondBottom[1]

    diamond_x_right = diamondRight[0]
    diamond_y_right = diamondRight[1]

    diamond_x_left = diamondLeft[0]
    diamond_y_left = diamondLeft[1]

    # reciever

    reciever_x_l = reciever_left[0]
    reciever_y_l = reciever_left[1]

    reciever_x_r = reciever_right[0]
    reciever_y_r = reciever_right[1]

    # print("diaamon y => ", diamond_y_bottom)
    if(((reciever_x_r >= diamond_x_bottom >= reciever_x_l) and ( -240 >= diamond_y_bottom >= -250 )) or ( (reciever_x_r >= diamond_x_left >= reciever_x_l) and ( -240 >= diamond_y_bottom >= -250 ) ) or ( (reciever_x_l <= diamond_x_right <= reciever_x_r) and ( -240 >= diamond_y_bottom >= -250 ) ) ):
        # print("bottom touched reciever...")
        dcolor = [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)]

        return True
    else:
        return False

def animate():
    global randY, randx, receiver_position, score, game_over, diamondBottom, dcolor, speed
    # print(randY)
    if(pause):
        return
    if(game_over):
        return

    diamond_y_bottom = diamondBottom[1]
    randY -= random.choice([-1, -1])-speed

    if(randY >= 425):
        randY = 0
        dcolor = [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)]
        randx = random.randint(-200, 200)

    if checkCollision():
        score += 1
        print("score:", score)
        randY = 0
        randx = random.randint(-200, 200)
        game_over = False
        speed += 0.2

    elif( -260 >= diamond_y_bottom ):

        game_over = True
        print("Game Over! score:", score)
    glutPostRedisplay()
def diamond():

    global randY, randx, diamondBottom, diamondRight, diamondLeft, dcolor

    if not game_over:
        dcolor

    else:
        dcolor = [0.0,0.0,0.0]

    findZone(-25 + randx , 180-randY , 0+randx, 200-randY )
    drawPoints(gx1, gy1, gx2, gy2, dcolor)

    findZone(0+ randx, 200-randY, 25 + randx, 180-randY)
    drawPoints(gx1, gy1, gx2, gy2,dcolor)

    #left
    findZone(-25+ randx, 180-randY,0+ randx, 160-randY)
    drawPoints(gx1, gy1, gx2, gy2, dcolor)

    #right
    findZone(0 + randx, 160-randY, 25 + randx, 180-randY)
    drawPoints(gx1, gy1, gx2, gy2, dcolor)

    diamondBottom = [0 + randx, 160-randY]
    diamondRight = [25 + randx, 180-randY]
    diamondLeft = [-25 + randx, 180-randY]

def reciever():

    global board_right, board_left, receiver_position,reciever_right, reciever_left, game_over

    color = [1.0, 1.0, 1.0]
    if game_over:
        color = [1.0, 0.0, 0.0]




    findZone(-200 + receiver_position, -240, -100 + receiver_position, -240)
    drawPoints(gx1, gy1, gx2, gy2, color)

    findZone(receiver_position - 180 , -250, receiver_position -120, -250)
    drawPoints(gx1, gy1, gx2, gy2, color)

    #bottomlEft
    findZone(receiver_position-200, -240,receiver_position-180, -250)
    drawPoints(gx1, gy1, gx2, gy2, color)

    #bottomRight
    findZone(receiver_position - 120, -250, receiver_position - 100, -240)
    drawPoints(gx1, gy1, gx2, gy2, color)

    glutPostRedisplay()

    reciever_right = [receiver_position - 100, -240]
    reciever_left = [receiver_position-200, -240]

def crossButton():
    # cross start
    color = [1.0, 0.0,0.0]
    findZone(200, 230, 250, 250)
    drawPoints(gx1,
               gy1,
               gx2,
               gy2, color)
    findZone(200, 250, 250, 230)
    drawPoints(gx1,
               gy1,
               gx2,
               gy2, color)

    # cross end
def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    # glPointSize(10)
    # glBegin(GL_POINTS)
    # glColor3f(1.0, 1.0, 0.0)
    # glVertex2f(0, 0)
    # glEnd()
    crossButton()
    pause_start()
    backButton()
    reciever()
    if(game_over):
        pass
    else:
        diamond()
    glutPostRedisplay()
    glutSwapBuffers()


def init():

    glClearColor(1, 1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1 , 1, 1000.0)
def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y
    return a,b
def mouseListener(button, state, x, y):
    global ballx, bally, pause, score, game_over, randY, speed


    if button == GLUT_LEFT_BUTTON:

        if (state == GLUT_DOWN):
            c_X, c_y = convert_coordinate(x, y)
            ballx, bally = c_X, c_y
            # print("ballx=>", ballx)
            # print("bally=>", bally)
            # -25, 250
            if not game_over:
                if((ballx >= -25 and bally >= 340) and (ballx <= 25 and bally <= 400)):
                    pause = not(pause)
            if ((ballx >=180 and bally >= 340) and (ballx <= 250 and bally <= 400)):
                glutLeaveMainLoop()
                print("GoodBye! score:", score)

            if(( -221>= ballx >=-250 and 400>= bally >=360 )):

                game_over = False
                randY = 0
                score = 0
                speed = 0
                print("starting over...")
    glutPostRedisplay()
def keyboardListener(key, x, y):
    global receiver_position, board_left, board_right
    if(pause):
        return
    if not game_over:
        if key == GLUT_KEY_LEFT:
            # print("left")
            if(board_left <= -250 ):
                return
            receiver_position -= 10
            board_left -= 10
            board_right -= 10
        elif key == GLUT_KEY_RIGHT:
            if (pause):
                return
            if( board_right >= 250):
                return
            receiver_position += 10
            board_right += 10
            board_left += 10
        glutPostRedisplay()


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"assignment-1 task1")
init()
glutIdleFunc(animate)
glutDisplayFunc(display)
glutSpecialFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()
