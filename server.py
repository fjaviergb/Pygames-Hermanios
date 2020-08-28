import socket
from _thread import *

server_ip = "192.168.1.36"

server = server_ip
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

players = {}

def threaded_client(conn, player):
    global currentPlayer
    reply = ""
    while True:
        try:
            databit = conn.recv(2048)
            data = eval(databit.decode("utf-8"))
            players[player] = data
            for p_index in players:
                if not players[p_index]:
                    #players[player] = (0,0,0,0,0,0,0,0,0,0)
                    players.pop(p_index)
            reply = list(players.values())
            print(reply)
            conn.send(str.encode(str(reply)))

        except:
            break

    print("Lost connection")
    conn.close()


global currentPlayer
currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
