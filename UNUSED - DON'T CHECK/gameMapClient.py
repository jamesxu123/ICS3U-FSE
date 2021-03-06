import socket, threading
from pygame import *
from math import*
#TCP_IP = '10.88.214.97'
TCP_IP = '192.227.178.111'
TCP_PORT = 5005
BUFFER_SIZE = 200
running = True
screen = display.set_mode((800,600))
otherPlayers = {}
background = image.load('OutcastMap.png')
person = image.load("Default Person.png")
deg = 90
playerList = ['admin',[400,300],deg]
def getData():
    global BUFFER_SIZE
    global running
    global playerList
    global otherPlayers
    global deg
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    while running:
        s.send(str(playerList).encode('utf-8'))
        data = eval(s.recv(BUFFER_SIZE).decode('utf-8'))
        try:
            otherPlayers = data
        except:
            pass
    s.close()

threading.Thread(target=getData).start()
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False




    #Movement and Blitting    
    try:
        portion = background.subsurface(Rect(playerList[1][0]-screen.get_width()//2,playerList[1][1]-screen.get_height()//2,800,600))
        screen.blit(portion,(0,0))
    except:
        print(playerList)
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    keysPressed = key.get_pressed()
    #UP
    if keysPressed[K_w] and 300<playerList[1][1]-5:
        playerList[1][1] -= 5
    #DOWN
    if keysPressed[K_s] and playerList[1][1]+5<background.get_height()-300:
        playerList[1][1] += 5
    #LEFT
    if keysPressed[K_a] and 400<playerList[1][0]-5:
        playerList[1][0] -= 5
    #RIGHT
    if keysPressed[K_d] and playerList[1][0]+5<background.get_width()-400:
        playerList[1][0] += 5
    
    length=(400-mx),(300-my)
    deg = atan2(length[0],length[1])
    length=degrees(deg)
    rotated = transform.rotate(person,(length))
    screen.blit(rotated,(screen.get_width()//2-rotated.get_width()//2,screen.get_height()//2-rotated.get_height()//2))
    #draw.circle(screen, (255,255,0), playerList[1],5)
    for p in otherPlayers:
        if p != playerList[0]:
            px,py = playerList[1]
            nx,ny = otherPlayers[p][0]
            if px-screen.get_width()//2<nx<px+screen.get_width() and py-screen.get_height()//2<ny<py+screen.get_height()//2:
                nx = nx-px +400
                ny = ny-py +300
                rotated = transform.rotate(person,(length))
                screen.blit(rotated,(nx-rotated.get_width()//2,ny-rotated.get_height()//2))
    display.flip()
quit()

