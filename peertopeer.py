import socket
from threading import *
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import time


global chat_row, data, reset
global filepath, filedata_wait
filedata_wait = chat_row = 0
filepath = data = None


def invalidMachineAddress():
    messagebox.showerror(
        title="Invalid Machine Address !!",
        message="We canot proceed without a valid IP address.\nTry giving a valid IP/port",
    )


# SupportiveFunctions
def getIP():
    ipadrds = list(map(str, ip.get().split("/")))
    try:
        ipadrds[1] = int(ipadrds[1])
    except IndexError as IE:
        invalidMachineAddress()
    return [ipadrds[0], ipadrds[1]]


# remove data from a entryBox
def cleanbox(obj):
    obj.delete(0, END)


class lightmodeTheme1:
    def __init__(self) -> None:
        self.snd_chat_bg = "#4CEE17"
        self.snd_chat_fg = "#00203f"
        self.rcv_chat_fg = "#fff"
        self.rcv_chat_bg = "#000"
        self.beside_fg = "#ced"
        self.beside_bg = "#ced"


class buttonColor:
    def __init__(self) -> None:
        self.fgCol = "#000"
        self.bgCol = "#388ef9"
        self.actfgCol = "#000"
        self.actbgCol = "#3849f9"


class Message(Thread):
    def __init__(self):
        Thread.__init__(self)

    def binder(self, con, name1):
        self.con = con
        self.name1 = name1

    def run(self):
        chatobj = lightmodeTheme1()

        def chatsender():
            global filepath
            global chat_row
            global data
            if data != None and len(data) > 0 and data != "\n":
                data = self.name1 + ": " + data
                self.con.send(bytes(data, "utf-8"))
                chatobj = lightmodeTheme1()
                chat_row += 1
                Label(
                    temp,
                    text=data,
                    width=25,
                    wraplength=180,
                    bg=chatobj.snd_chat_bg,
                    fg=chatobj.snd_chat_fg,
                    pady=4,
                ).grid(row=chat_row, column=1, sticky="e", padx=15)
                data = None

        def filesender():
            global filepath
            global data
            filename = filepath.split("/")[-1]
            try:
                if filename != None:
                    file = open(filepath, "r")
                    ffmt = "file_:" + " " + filename
                    self.con.send(bytes(ffmt, "utf-8"))
                    self.con.send(bytes(file.read(), "utf-8"))
                    Label(
                        temp,
                        text=f'File "{filename}" sent.',
                        width=25,
                        wraplength=180,
                        bg=chatobj.snd_chat_bg,
                        fg=chatobj.snd_chat_fg,
                    ).grid(row=chat_row, column=1, sticky="w", padx=15)
                    error.set(f"File {filename} sent successfully")
                    filepath = None
            except:
                pass

        name = current_thread().name
        global reset
        while reset:
            time.sleep(1)
            global chat_row
            global data
            if name == "sender":
                chatsender()
                if filepath != None:
                    filesender()

            elif name == "receiver":
                global filedata_wait

                recvdata = self.con.recv(100000).decode()
                chat_row += 1

                if recvdata.split()[0] == "file_:" or filedata_wait:
                    if filedata_wait == 0:
                        savefile = recvdata.split()[1]
                        filedata_wait = 1
                        Label(
                            temp,
                            text=f'File recieved : "{recvdata.split()[-1]}"',
                            width=25,
                            wraplength=180,
                            pady=4,
                            bg=chatobj.rcv_chat_bg,
                            fg=chatobj.rcv_chat_fg,
                        ).grid(row=chat_row, column=0, sticky="w", padx=15)
                    elif filedata_wait:
                        file = open(savefile, "w")
                        file.write(recvdata)
                        file.close()
                        filedata_wait = 0
                else:
                    Label(
                        temp,
                        text=recvdata,
                        width=25,
                        wraplength=180,
                        bg=chatobj.rcv_chat_bg,
                        fg=chatobj.rcv_chat_fg,
                    ).grid(row=chat_row, column=0, sticky="w", padx=15)


def initiate(target):
    ipadrs = target
    name = socket.gethostname()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        socket.timeout(30)
        server.connect((ipadrs[0], ipadrs[1]))
        socket.timeout(None)
        sender = Message()
        sender.binder(server, name)
        sender.setName("sender")
        receiver = Message()
        receiver.binder(server, name)
        receiver.setName("receiver")
        sender.start()
        receiver.start()
    except Exception as e:
        try:
            server.bind(('127.0.0.1', ipadrs[1]))
            server.listen(5)
            clt, addr = server.accept()
            error.set(f"Connection Stablished {clt}")
            sender = Message()
            sender.binder(clt, name)
            sender.setName("sender")
            receiver = Message()
            receiver.binder(clt, name)
            receiver.setName("receiver")
            sender.start()
            receiver.start()
        except (ConnectionResetError, TypeError) as EE:
            error.set(EE)
            connectionreset()

        except (OSError, PermissionError) as OS:
            error.set(OS)
            messagebox.showerror(
                title="Port Assignment error", message="Cannot assign requested port"
            )


# code portion
def endsession():
    app.destroy()
    exit()


def connectionreset():
    global chat_row
    chat_row += 1
    cleanbox(ip)
    messagebox.showinfo(
        title="Connection reset",
        message="Connection reset, Waiting for new connection...!!!",
    )
    Label(
        temp,
        text="Connection reset........!!",
        bg="#f93822",
        fg="#fdd20e",
        font=(14),
        justify="center",
        padx=10,
        pady=4,
    ).grid(row=chat_row, column=0, columnspan=2, sticky="we")
    global reset
    reset = 0
    raise Exception("Connection reset")


def openfile():
    global filepath
    global defaultopendir
    filepath = filedialog.askopenfilename(
        title="Select File to be sent",
        filetypes=(("text files", "*.txt"), ("python files", "*.py")),
    )
    filepath = str(filepath)


def send(event=None):
    global data
    data = chat_area.get().rstrip(" \n")
    cleanbox(chat_area)


def connection():
    target = getIP()
    global reset
    reset = 1
    if target:
        initiate(target)
    else:
        invalidMachineAddress()


if __name__ == "__main__":
    app = Tk()
    app.title("Connect to peers Indepedently")
    app.geometry("550x900")
    app.maxsize(width=730, height=980)
    icon = PhotoImage(file="PeertopeerTk/p2p.png")
    app.iconphoto(True, icon)

    frame0 = Frame(app)
    frame0.config(bg="#111", width=100)
    frame0.pack()
    app_tab = ttk.Notebook(frame0)
    app_tab.config(padding=15)
    chat_frame = Frame(
        app_tab,
    )
    help_frame = Frame(
        app_tab,
    )
    chat_frame.config(
        bg="light blue",
        padx=14,
        pady=20,
    )
    help_frame.config(
        bd=6,
        bg="#333",
        padx=4,
        pady=4,
    )
    app_tab.add(chat_frame, text="Chat")
    app_tab.add(help_frame, text="Help")
    help = open("connectionHelpModule.txt", "r")
    Label(
        help_frame,
        text=help.read(),
        wraplength=480,
        font=(12),
        bg="#333",
        fg="#fff",
        justify=LEFT,
        padx=3,
        pady=4,
    ).pack()

    labelip = Label(
        chat_frame,
        text="Peer IP/port",
        font=("", 14),
        bg="light green",
        pady=1,
        padx=26,
    )
    btncol = buttonColor()
    labelip.grid(row=0, column=0, sticky=W)
    ip = Entry(chat_frame, font=("", 14))
    ip.grid(row=0, column=1, sticky="e")
    reset = Button(
        chat_frame,
        text="Reset Conn..",
        font=("", 14),
        bg=btncol.bgCol,
        fg=btncol.fgCol,
        activebackground=btncol.actbgCol,
        activeforeground=btncol.actfgCol,
        command=connectionreset,
        bd=6,
        padx=10,
    )
    reset.grid(row=1, column=0, sticky="w")
    connect = Button(
        chat_frame,
        text="Connect..",
        font=("", 14),
        bg=btncol.bgCol,
        fg=btncol.fgCol,
        activebackground=btncol.actbgCol,
        activeforeground=btncol.actfgCol,
        command=connection,
        bd=6,
        padx=20,
        cursor="exchange",
    )
    connect.grid(row=1, column=1, sticky="e")

    colTemp = lightmodeTheme1()
    master = Canvas(chat_frame, height=470, width=480, background=colTemp.beside_bg)
    master.grid(row=2, column=0, columnspan=2)

    scroller = Scrollbar(
        master,
        orient=VERTICAL,
        command=master.yview,
        activebackground="#7da",
    )
    scroller.pack(side="right", fill="both")
    master.configure(yscrollcommand=scroller.set)

    master.bind(
        "<Configure>", lambda e: master.configure(scrollregion=master.bbox("all"))
    )
    temp = Frame(master, bg=colTemp.beside_bg, width=53)
    for i in range(300):
        Label(temp, font=("15"), bg=colTemp.beside_bg, fg=colTemp.beside_fg).grid(
            row=i, column=0
        )
    Label(
        temp, width=25, wraplength=180, bg=colTemp.beside_bg, fg=colTemp.beside_bg
    ).grid(row=chat_row, column=0, sticky="w")
    Label(
        temp, width=25, wraplength=180, bg=colTemp.beside_bg, fg=colTemp.beside_bg
    ).grid(row=chat_row, column=1, sticky="e")

    master.create_window((0, 0), window=temp, anchor="nw")

    attach = Button(
        chat_frame,
        text="Attach",
        font=("", 14),
        bg=btncol.bgCol,
        fg=btncol.fgCol,
        activebackground=btncol.actbgCol,
        activeforeground=btncol.actfgCol,
        command=openfile,
        bd=6,
        padx=40,
    )
    attach.grid(row=3, column=1, sticky="e")

    chat_area = Entry(chat_frame, font=("", 14))
    chat_area.config(bg="white", width=27)
    chat_area.grid(row=4, column=0, sticky="w", columnspan=2) 

    send_button = Button(
        chat_frame,
        text="Send",
        font=("", 14),
        bg=btncol.bgCol,
        fg=btncol.fgCol,
        activebackground=btncol.actbgCol,
        activeforeground=btncol.actfgCol,
        command=send,
        bd=6,
        padx=14,
        relief="raised",
    )
    send_button.grid(row=4, column=1, sticky="e")
    app.bind("<Return>", send)
    quit = Button(
        chat_frame,
        bg=btncol.bgCol,
        fg=btncol.fgCol,
        activebackground=btncol.actbgCol,
        activeforeground=btncol.actfgCol,
        text="Quit Session",
        bd=6,
        font=("", 14),
        command=endsession,
    ).grid(row=5, column=0, columnspan=2, pady=3)
    error = StringVar()
    error_review = Label(
        chat_frame,
        textvariable=error,
        bg="#333",
        bd=3,
        width=48,
        height=5,
        font=("", 12),
        fg="light green",
        justify=LEFT,
        wraplength=490,
    )
    error_review.grid(
        row=6,
        column=0,
        columnspan=2,
    )
    master.pack_propagate(0)
    app_tab.pack()

    app.mainloop()
