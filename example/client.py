import socketio
from easygame import *

with socketio.SimpleClient() as sio:
    open_window('Minecrfat simulator', 800, 600)
    # Začni vykreslovať snímky v cykle (v predvolenej rýchlosti 60fps)
    should_quit = False
    hitboxes.create(0, 0, 20, 20, "Podlaha")
    hitboxes.create(50, 50, 50, 50, "entita1")
    entityID = 1
    vektorx = 0
    vektory = 0
    left = False
    right = False
    sio.connect('http://localhost:8080')
    while not should_quit:
        
        print(sio.receive())

        # Načítaj udalosti pre aktuálnu snímku
        for event in poll_events():
        
            # Napríklad ak hráč spustí CloseEvent
            # prestaň ďalej vykreslovať snímky a zatvor okno 
            if type(event) is CloseEvent:
                should_quit = True
            if type(event) is KeyDownEvent:
                if event.key == "RIGHT":
                    vektorx += 15
                    right = True
                if event.key == "LEFT":
                    vektorx -= 15
                    left = True
                if event.key == "UP" and hitboxes.colision(entityID, 0):
                    vektory += 20
                    #print("[Debug]: key: UP")
                if event.key == "BACKSPACE":
                    hitboxes.pos(entityID, 400, 300)    
            if type(event) is KeyUpEvent:
                if event.key == "RIGHT":
                    right = False
                if event.key == "LEFT":
                    left = False
        ###
        # Tu patrí logika hry, ktorá na obrazovku niečo vykreslí
        ### 
        if left:
            vektorx -= 15
        if right:
            vektorx += 15
        vektorx = floor(vektorx / 1.5)
        #print("[Debug]: " + str(vektorx) + ", " + str(vektorx/2))
        hitboxes.move(entityID, vektorx, vektory)
        if not hitboxes.colision(entityID, 0):
            vektory -= 1
            if hitboxes.get(entityID)[1] < -100:
                vektory = 0
                hitboxes.pos(entityID, 400, 300)
        else:
            vektory = 0
        fill(225,225,225)
        myentity = hitboxes.get(1)
        #draw_polygon((myentity[0], myentity[1]), (myentity[0], myentity[1] + myentity[3]), (myentity[0] + myentity[2], myentity[1] + myentity[3]), (myentity[0] + myentity[2], myentity[1]),  color=(0,0,0,1))
        showhitbox(entityID)
        showhitbox(0)
        draw_text("X: " + str(myentity[0]) + ", Y: " + str(myentity[1]), "Times New Roman", 32, position=(20,500), color=(0,0,0,1))
        # Pokračuj na ďalšiu snímku (a všetko opať prekresli)
        next_frame()
    
    close_window()