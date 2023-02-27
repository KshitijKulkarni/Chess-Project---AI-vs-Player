import socket

def NewMatch():
    print("New match started")

def Start():
    global Game_Manager
    # print("Starting with skill: " + str(skill))
    import time
    time.sleep(5)
    import Game_Manager
    Game_Manager.Start()

InvalidMove = False;

def ConfirmMove():
    global Game_Manager, InvalidMove
    error = Game_Manager.OnUserPlayed()#play the move and record error code
    return error


def RetakeReferenceFrame():
    global Game_Manager, InvalidMove
    Game_Manager.ReTakePicture()

HOST = ''  # The server's hostname or IP address
PORT = 6969        # The port used by the server

def subtract(a, b):                              
    return "".join(a.rsplit(b))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server listening on {HOST}:{PORT}...')

    conn, addr = s.accept()
    with conn:
        print(f'Connected by {addr}')
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            if data[:5] == "Start":
                Start()
            elif data[:7] == "Confirm":
                conn.send(str(ConfirmMove()).encode())
            elif data[:3] == "RRF":
                RetakeReferenceFrame()


            
