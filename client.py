from easygame import *
import socket
import select
import errno
import sys

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")
#my_username = "Hacaric"
open_window('Panda simulator', 800, 600)
 
# Začni vykreslovať snímky v cykle (v predvolenej rýchlosti 60fps)
should_quit = False

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
senddata = ""
receiveddata = []
 
# Začni vykreslovať snímky v cykle (v predvolenej rýchlosti 60fps)
should_quit = False
hitboxes.create(0, 0, 20, 20, "Podlaha")
hitboxes.create(50, 50, 50, 50, "entita1")
entityID = 1
vektorx = 0
vektory = 0
left = False
right = False
while True:
 
# Otvor okno s nadpisom "Panda simulator"
# vo veľkosti 800px na šírku a 600px na výš
    # Wait for user to input a message
    message = senddata
    # Načítaj udalosti pre aktuálnu snímku
    for event in poll_events():
    
        # Napríklad ak hráč spustí CloseEvent
        # prestaň ďalej vykreslovať snímky a zatvor okno 
        if type(event) is CloseEvent:
            close_window()
            sys.exit()
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
    senddata = my_username + "," + str(myentity[0]) + "," + str(myentity[1]) + "," + str(myentity[2]) + "," + str(myentity[3])
    redvicedata = receiveddata
    for i in range(math.floor(len(redvicedata)/5)):
        if hitboxes.getID(redvicedata[i * 5]) == -1 :
            hitboxes.create(int(redvicedata[i * 5 + 1]),int(redvicedata[i * 5 + 2]),int(redvicedata[i * 5 + 3]),int(redvicedata[i * 5 + 4]), redvicedata[i*5])
        #hitboxes.colision(hitboxes.getID(), entityID)
        showhitbox(hitboxes.getID(redvicedata[i*5]))

    next_frame()






    # If message is not empty - send it
    if message != "":
        senddata = ""
        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                close_window()
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Print message
            receiveddata = message.split(",")
            print(f'{username} > {message}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            close_window()
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        close_window()
        sys.exit()