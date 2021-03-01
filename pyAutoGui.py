import pyautogui as pg
import autopy as ap

sizeX = pg.size().width
sizeY = pg.size().height

curPosX = pg.position().x
curPosY = pg.position().y

x1 = 100
y1 = 50

pg.FAILSAFE = False

def mouseMovement(i,j):
    # print(curPosX + i*(x/x1), curPosY + j*(y/y1))
    x = curPosX + i*(sizeX/x1)
    y = curPosY + j*(sizeY/y1)
    if(x>=1366):
        x = sizeX - 1
    elif(x < 0):
        x = 0
    if (y>= 768):
        x = sizeX - 1
    elif(y<0):
        y = 0  
    ap.mouse.smooth_move(x, y)
    

# mouseMovement(10,0)