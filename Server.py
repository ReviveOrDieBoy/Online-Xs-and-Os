import socket
import threading
import random


FORMAT = "utf-8"
HEADER = 2
DISCONNECT = "!D"


player_names = {}
counter = 0
players = ["1", "2"]
role = ["h", "j"]
wins = [["X", "X", "X"], ["O", "O", "O"]]
grid = [[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]]


def check_win():
    for i in range(2):
        for r in range(3):
            if grid[r] == wins[i]:
                return True
            elif [str(grid[0][r]), str(grid[1][r]), str(grid[2][r])] == wins[i]:
                return True
        if [grid[0][0], grid[1][1], grid[2][2]] == wins[i]:
            return True
        if [grid[0][2], grid[1][1], grid[2][0]] == wins[i]:
            return True


def handle_client(conn, addr):
    player = random.choice(players)
    players.remove(player)
    player += role[len(clients) - 2]
    conn.send(player.encode())
    global msg, player_names
    with client_lock:
        clients.add(conn)
        player_names[addr] = "Player " + player
    connected = True
    if not players:
        for i in clients:
            i.send("good".encode(FORMAT))
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        if msg == DISCONNECT:
            connected = False
            print(threading.activeCount() - 1)
            if (threading.activeCount() - 1) == 0:
                server.close()
                print("closed")
        else:
            check(msg[0], msg[1], addr)

    conn.close()
    clients.remove(conn)


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr,))
        thread.start()


def send_pos(posx, posy, sign, win):
    global counter
    send_msg = str(posx) + str(posy) + sign
    counter += 1
    if counter == 9 and not win:
        send_msg += "S"
    elif win:
        send_msg += "W"
    else:
        send_msg += "P"
    for i in clients:
        i.send(send_msg.encode(FORMAT))


def check(posy, posx, addr):
    global grid
    if counter % 2 == 0 and (player_names[addr].rstrip(player_names[addr][-1])) == "Player 1":
        sign = "X"
        grid[int(posy)][int(posx)] = sign
        win = check_win()
        send_pos(posy, posx, sign, win)
    elif counter % 2 != 0 and (player_names[addr].rstrip(player_names[addr][-1])) == "Player 2":
        sign = "O"
        grid[int(posy)][int(posx)] = sign
        win = check_win()
        send_pos(posy, posx, sign, win)


def main(SERVER, PORT):
    global server, clients, client_lock
    clients = set()
    client_lock = threading.Lock()
    ADDR = (SERVER, PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    start()
