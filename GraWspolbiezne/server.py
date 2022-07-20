import socket
from _thread import *


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '192.168.56.1'
port = 5555
BOARD_WIDTH, BOARD_HEIGHT = 5, 4

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"

board = []
for row in range(BOARD_HEIGHT):
    board.append([])
    for column in range(BOARD_WIDTH):
        board[row].append(1)
board[0][0] = -1

def threaded_client(conn):
    global currentId, board
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + reply)
            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))