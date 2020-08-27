import socket
from _thread import *
import pickle

server_ip = "192.168.43.78"

server = server_ip
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


players = []


def threaded_client(conn, player):
    global currentPlayer
    reply = ""
    while True:
        try:
            databit = conn.recv(2048)
            data = eval(databit.decode("utf-8"))

            try:
                players[player] = data
            except IndexError:
                players.append(data)
            for p in players:
                if not p:
                    players.remove(p)
                    reply = players
                else:
                    reply = players
                    print(reply)
            conn.send(str.encode(str(reply)))

        except:
            break

    currentPlayer -= 1
    print("Lost connection")
    conn.close()


global currentPlayer
currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
