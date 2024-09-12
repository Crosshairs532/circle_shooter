from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 500, 800

global_E_SE = False
global_cx = 0
global_cy = -240

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

time = 0
dcolor= [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)]
speed = 1
game_over = False
ball_center = 200
random_x = random.randint(-235, 235)
rx = []

move_left = 0
move_right = 0
def randomX():
    global rx, ry
    # rx = [ random.randint(-235, 235) for i in range(5)]
    ry = [random.randint(0, 200) for i in range(len(rx))]

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


# def checkCollision():
#

def animate():
    global randY, time
    # print(randY)
    if(pause):
        return
    if(game_over):
        return
    time+= 0.05
    if(time>=5):
        time = 0
        crandx = random.randint(-235, 235)
        crandy = random.randint(200, 200)
        crandr = random.choice([8, 15])
        rx.append([crandx, crandy, crandr])

    for i in rx:
        print(i[1])
        i[1] -= speed

    glutPostRedisplay()




def diamond():
    global ball_center, rx

    if(len(rx)!=0):
        for i in range(len(rx)):
            x, y , r= rx[i]
            drawcircle2(0, y, r, [1.0, 0.0, 0.0], 0,  x)


def plot_circle_points(x_center, y_center, x, y, color):
    global move_left
    red, green, blue = color
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(red, green, blue)

    glVertex2f(+x+move_left, y_center + y) #zone - 1
    glVertex2f(-x+move_left, y_center + y) #zone - 2
    glVertex2f(+x+move_left, y_center - y) #zone - 6
    glVertex2f(-x+move_left, y_center - y) #zone - 5
    glVertex2f(+y+move_left, y_center + x) #zone - 0
    glVertex2f(-y+move_left, y_center + x) #zone - 3
    glVertex2f(+y+move_left, y_center -  x) #zone - 7
    glVertex2f(-y+move_left, y_center - x) #zone - 4
    glEnd()

def plot_circle_points2(x_center, y_center, x, y, color, ranX):
    red, green, blue = color
    global randY
    print(f"y-center->{y_center}---- y-{y}")
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(red, green, blue)
    glVertex2f(+x+ranX, y_center + y) #zone - 1
    glVertex2f(-x+ranX, y_center + y ) #zone - 2
    glVertex2f(+x+ranX, y_center - y) #zone - 6
    glVertex2f(-x+ranX, y_center - y) #zone - 5
    glVertex2f(+y+ranX, y_center + x) #zone - 0
    glVertex2f(-y+ranX, y_center + x) #zone - 3
    glVertex2f(+y+ranX, y_center - x) #zone - 7
    glVertex2f(-y+ranX, y_center - x) #zone - 4
    glEnd()

def drawcircle(x_center, y_center, radius, color, x):

    y = radius
    d = 1 - radius
    plot_circle_points(x_center, y_center, x, y, color)
    # print(f"x->{x} y->{y}")
    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1

        plot_circle_points(x_center, y_center, x, y, color)


def drawcircle2(x_center, y_center, radius, color, x, ranX):

    y = radius
    d = 1 - radius
    plot_circle_points2(x_center, y_center, x, y, color, ranX)

    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1

        plot_circle_points2(x_center, y_center, x, y, color, ranX)

def reciever():

    drawcircle(0, global_cy, 15, [1.0, 0.0, 0.0], 0)

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
    glPointSize(10)
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(0, 0)
    glEnd()
    crossButton()
    pause_start()
    backButton()
    reciever()
    if(game_over):
        pass
    else:
        diamond()
    # glutPostRedisplay()
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
            print("ballx=>", ballx)
            print("bally=>", bally)
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
    global move_left
    if(pause):
        return
    if not game_over:
        if key==b" ":
            print("space")
        if key == b"a":
            print("left")
            # if(board_left <= -250 ):
            #     return
            move_left -=5
        elif key == b"d":
            print("right")
            # if (pause):
            #     return
            # if( board_right >= 250):
            #     return
            move_left += 5
        glutPostRedisplay()


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"assignment-1 task1")
init()
glutIdleFunc(animate)
glutDisplayFunc(display)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()
