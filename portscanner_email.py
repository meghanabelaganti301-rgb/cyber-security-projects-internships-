# 18BCE7038

# ========== MODULE IMPORTS ==========
import sys
import os
import socket
import threading
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime
from tkinter import *

# ========== DEFAULTS ==========
log = []
ports = []
target = 'localhost'

# ========== PORT SCANNER FUNCTION ==========
def scanPort(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        c = s.connect_ex((target, port))
        if c == 0:
            m = f"> Port {port} is open!"
            log.append(m)
            ports.append(port)
            listbox.insert("end", m)
            updateResult()
        s.close()
    except:
        pass

def updateResult():
    rtext = f" [ {len(ports)} / {end} ] ports open for {target}"
    L27.configure(text=rtext)

def startScan():
    global ports, log, target, end
    clearScan()
    ports = []
    log = []

    try:
        start = int(L24.get())
        end = int(L25.get())
    except:
        listbox.insert("end", "Invalid port range input.")
        return

    target_input = L22.get()
    try:
        target = socket.gethostbyname(target_input)
    except socket.gaierror:
        m = f"> Target {target_input} not found."
        log.append(m)
        listbox.insert("end", m)
        return

    # Log header
    log.extend([
        "> Port Scanner",
        "=" * 14,
        f" Target:\t{target_input}",
        f" IP:\t{target}",
        f" Time Started:\t{datetime.now()}",
        f" Port Range:\t[ {start} / {end} ]",
        "=" * 14 + "\n"
    ])

    for port in range(start, end + 1):
        thread = threading.Thread(target=scanPort, args=(target, port))
        thread.daemon = True
        thread.start()
        time.sleep(0.01)

def saveScan():
    log.append(f"\nOpen Ports:\t[ {len(ports)} / {end} ]\n")
    filename = f'portscan-{target}.txt'
    with open(filename, mode='wt', encoding='utf-8') as f:
        f.write('\n'.join(log))
    listbox.insert("end", f"> Result saved to {filename}")

def mailScan():
    User = 'your_email@gmail.com'
    Passwd = 'your_password'
    filename = f'portscan-{target}.txt'
    msg = EmailMessage()
    msg['Subject'] = f'Scan Results For {target}'
    msg['From'] = User
    msg['To'] = User
    msg.set_content(f'Scan results for target: {target}\nConducted on: {datetime.now()}')

    try:
        with open(filename, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype='text', subtype='txt', filename=filename)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(User, Passwd)
            smtp.send_message(msg)
        listbox.insert("end", "> Email sent successfully.")
    except Exception as e:
        listbox.insert("end", f"> Error sending email: {e}")

def clearScan():
    listbox.delete(0, 'end')

# ========== GUI DESIGN ==========
gui = Tk()
gui.title('🎯 Port Scanner')
gui.geometry("500x650+100+50")
gui.configure(bg="#1e1e2e")

# Fonts
title_font = ("Helvetica", 18, "bold")
label_font = ("Helvetica", 11)
entry_font = ("Consolas", 11)

# Title
L11 = Label(gui, text="🔍 Port Scanner", font=title_font, fg="#00ffd0", bg="#1e1e2e")
L11.place(x=160, y=20)

# Target
L21 = Label(gui, text="Target Address:", font=label_font, fg="#f4f4f4", bg="#1e1e2e")
L21.place(x=30, y=80)
L22 = Entry(gui, font=entry_font, bg="#2a2a3b", fg="#ffffff", insertbackground='white')
L22.place(x=170, y=80, width=280)
L22.insert(0, "localhost")

# Port Range
L23 = Label(gui, text="Port Range:", font=label_font, fg="#f4f4f4", bg="#1e1e2e")
L23.place(x=30, y=130)
L24 = Entry(gui, font=entry_font, bg="#2a2a3b", fg="#ffffff", insertbackground='white')
L24.place(x=170, y=130, width=120)
L24.insert(0, "1")
L25 = Entry(gui, font=entry_font, bg="#2a2a3b", fg="#ffffff", insertbackground='white')
L25.place(x=310, y=130, width=140)
L25.insert(0, "1024")

# Scan Result
L26 = Label(gui, text="Scan Progress:", font=label_font, fg="#f4f4f4", bg="#1e1e2e")
L26.place(x=30, y=180)
L27 = Label(gui, text="[ ... ]", font=label_font, fg="#00ff88", bg="#1e1e2e")
L27.place(x=170, y=180)

# Listbox Frame
frame = Frame(gui, bg="#2a2a3b", bd=2, relief=GROOVE)
frame.place(x=30, y=230, width=440, height=280)

listbox = Listbox(frame, width=64, height=14, font=("Courier", 10), bg="#111122", fg="#00ffaa", selectbackground="#00cc99")
listbox.pack(side=LEFT, fill=BOTH, padx=2, pady=2)

scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Buttons
button_style = {
    "font": ("Helvetica", 11, "bold"),
    "bg": "#0066cc",
    "fg": "white",
    "activebackground": "#0055aa",
    "activeforeground": "white",
    "bd": 0,
    "relief": GROOVE
}

B11 = Button(gui, text="▶ Start Scan", command=startScan, **button_style)
B11.place(x=30, y=540, width=130, height=40)

B21 = Button(gui, text="💾 Save Result", command=saveScan, **button_style)
B21.place(x=180, y=540, width=130, height=40)

B31 = Button(gui, text="📧 Send Mail", command=mailScan, **button_style)
B31.place(x=330, y=540, width=130, height=40)

# Run GUI
gui.mainloop()
