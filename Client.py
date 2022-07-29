from tkinter import *
import threading
import socket

FORMAT = "utf-8"
HEADER = 4
DISCONNECT = "!D"

counter = 0
myFont = ("Helvetica", 20)
state_check = True


def disconnect():
    send_msg = DISCONNECT.encode(FORMAT)
    client.send(send_msg)
    client.close()
    root.withdraw()


def rematch():
    return "done"


def receive():
    global state_check
    while state_check:
        try:
            msg = client.recv(HEADER).decode(FORMAT)
        except:
            break
        Button(root, text=msg[2], width=10, height=4, font=myFont, state="disabled", disabledforeground="black").grid(row=(int(msg[0]) + 1), column=msg[1])
        if (msg[2] == "X" and player[0] == "1") or (msg[2] == "O" and player[0] == "2"):
            if msg[3] == "W":
                Label(root, text="You Won", font=myFont, bg="white").grid(column=0, row=0, columnspan=3, sticky="nsew", pady=10)
                state_check = False
            else:
                Label(root, text="Your Opponent's Turn", font=myFont, bg="white").grid(column=0, row=0, columnspan=3, sticky="nsew", pady=10)
        else:
            if msg[3] == "W":
                Label(root, text="You Lost", font=myFont, bg="white").grid(column=0, row=0, columnspan=3, sticky="nsew", pady=10)
                state_check = False
            else:
                Label(root, text="Your Turn", font=myFont, bg="white").grid(column=0, row=0, columnspan=3, sticky="nsew", pady=10)

        if msg[3] == "S":
            state_check = False
            Label(root, text="Draw", font=myFont, bg="white").grid(column=0, row=0, columnspan=3, sticky="nsew", pady=10)
    Button(root, text="Rematch", font=myFont, command=lambda: rematch()).grid(row=5, column=0, columnspan=3, sticky="nsew", pady=10)


def send_pos(posy, posx):
    send_msg = str(posy) + str(posx)
    send_msg = send_msg.encode(FORMAT)
    client.send(send_msg)


def board_generation():
    if player[0] == "1":
        Label(root, text="Your Turn", font=myFont, bg="white").grid(column=0, row=0, columnspan=3, sticky="nsew", pady=10)
    else:
        Label(root, text="Your Opponent's Turn", font=myFont, bg="white").grid(column=0, row=0, columnspan=3, sticky="nsew", pady=10)
    for Col in range(3):
        for Row in range(3):
            action = lambda x=Col, y=Row: send_pos(y, x)
            Button(root, command=action, width=10, height=4, font=myFont, bg="white").grid(row=(Row + 1), column=Col)
    Button(root, text="Quit", bg="white", font=myFont, command=disconnect, bd=0, highlightthickness=0)\
        .grid(row=7, column=0, columnspan=3, rowspan=2, sticky="nsew ")
    receive_messages = threading.Thread(target=receive)
    receive_messages.start()


def main(SERVER, PORT):
    global client, player, root, port, ip, wait

    ADDR = (SERVER, PORT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    root = Tk()
    root.title("Xs and Os")
    root.resizable(width=False, height=False)
    root.config(bg="white")

    player = client.recv(2).decode(FORMAT)
    if player[1] == "h":
        wait = Label(root, text="Waiting For Opponent...", font=myFont, bg="white")
        ip = Label(root, text=("Your Server IP Address Is: " + SERVER), font=myFont, bg="white")
        port = Label(root, text=("Your Server Port Address Is: " + str(PORT)), font=myFont, bg="white")
        wait.grid(column=0, row=0, pady=10, padx=10)
        ip.grid(column=0, row=1, pady=10, padx=10)
        port.grid(column=0, row=2, pady=10, padx=10)
        root.update()

    client.recv(HEADER).decode(FORMAT)
    if player[1] == "h":
        wait.destroy()
        ip.destroy()
        port.destroy()

    board_generation()
    root.mainloop()
