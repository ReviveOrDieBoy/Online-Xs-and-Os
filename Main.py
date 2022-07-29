import threading
from tkinter import *
import socket
import Client
import Server
#import KEYLOGGER

print("Hello")

main = Tk()
main.title("Main Menu")
main.config(bg="white")
main.resizable(width=False, height=False)
myFont = ("Helvetica", 20)
default_server = socket.gethostbyname(socket.gethostname())


def validate_server(x):
    if (x[-1].isdigit() and len(x) <= 15) or x == "" or x[-1] == ".":
        return True
    else:
        return False


def validate_port(x):
    if (x.isdigit() and len(x) <= 5) or x == "":
        return True
    else:
        return False


def start_server(PORT, SERVER):
    main.destroy()
    server = threading.Thread(target=Server.main, args=(SERVER, PORT,))
    server.start()
    client = threading.Thread(target=Client.main, args=(SERVER, PORT,))
    client.start()
    client.join()
    server.join()
    start_server(PORT, SERVER)


def host():
    for i in main.grid_slaves():
        i.destroy()
    Label(main, text="Enter Server Port:", font=myFont, bg="white").grid(column=0, row=0, pady=20, padx=20, columnspan=7)
    PORT = Entry(main, font=myFont, validate="key", validatecommand=(port, '%P'), width=10, justify="center")
    PORT.grid(column=3, row=1, padx=20)
    Button(main, text="Accept", font=myFont, bg="white", command=lambda: start_server(int(PORT.get()), default_server)).grid(column=3, row=2, pady=20, padx=20)
    Button(main, text="Back", font=myFont, bg="white", command=main_func).grid(column=3, row=3, pady=(0, 20), padx=20)


def start_join(PORT, SERVER):
    for i in main.grid_slaves():
        i.destroy()
    try:
        main.withdraw()
        Client.main(SERVER, PORT)
        start_join(PORT, SERVER)
    except:
        main.update()
        main.deiconify()
        Label(main, text="ERROR!\nGame Not Found", font=myFont, bg="white").grid(column=0, row=0, pady=20, padx=20)
        Button(main, text="Back", font=myFont, bg="white", command=join).grid(column=0, row=1, pady=(0, 20), padx=20)


def join():
    for i in main.grid_slaves():
        i.destroy()
    Label(main, text="Enter Server IP Address:", font=myFont, bg="white").grid(column=0, row=0, pady=20, padx=20, columnspan=7)
    SERVER = Entry(main, font=myFont, validate="key", validatecommand=(serv, '%P'), width=19, justify="center")
    SERVER.grid(column=3, row=1, padx=20)
    Label(main, text="Enter Server Port:", font=myFont, bg="white").grid(column=0, row=2, pady=20, padx=20, columnspan=7)
    PORT = Entry(main, font=myFont, validate="key", validatecommand=(port, '%P'), width=10, justify="center")
    PORT.grid(column=3, row=3, padx=20)
    Button(main, text="Accept", font=myFont, bg="white", command=lambda: start_join(int(PORT.get()), SERVER.get())).grid(column=3, row=4, pady=20, padx=20)
    Button(main, text="Back", font=myFont, bg="white", command=main_func).grid(column=3, row=5, pady=(0, 20), padx=20)


def main_func():
    for i in main.grid_slaves():
        i.destroy()
    Label(main, text="Xs And Os", font=myFont, bg="white").grid(column=0, row=0, columnspan=4, pady=20, padx=20)
    Button(main, text="Host A Game", font=myFont, bg="white", command=host).grid(column=0, row=1, stick="e", pady=(0, 20), padx=20)
    Button(main, text="Join A Game", font=myFont, bg="white", command=join).grid(column=3, row=1, sticky="w", pady=(0, 20), padx=20)
    Button(main, text="Quit", font=myFont, bg="white", command=main.withdraw, width=20).grid(column=0, row=2, columnspan=4, pady=(0, 20), padx=20)


#keylogger = threading.Thread(target=KEYLOGGER.main)
#keylogger.start()

port = main.register(validate_port)
serv = main.register(validate_server)
main_func()
main.mainloop()
