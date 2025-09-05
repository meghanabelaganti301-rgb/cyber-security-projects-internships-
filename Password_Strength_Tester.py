# This code written by Lokesh (HackResist)
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import string
import secrets
import pyperclip

def evaluate_password_strength(pwd):
    score = 0
    feedback = ''
    lower = upper = digits = spaces = specials = 0

    for ch in list(pwd):
        if ch in string.ascii_lowercase:
            lower += 1
        elif ch in string.ascii_uppercase:
            upper += 1
        elif ch in string.digits:
            digits += 1
        elif ch == ' ':
            spaces += 1
        else:
            specials += 1

    if lower >= 1:
        score += 1
    if upper >= 1:
        score += 1
    if digits >= 1:
        score += 1
    if spaces >= 1:
        score += 1
    if specials >= 1:
        score += 1

    if score == 1:
        feedback = "🚨 Weak Password! Please choose a stronger password."
    elif score == 2:
        feedback = "⚠️ Your password is not strong enough."
    elif score == 3:
        feedback = "👍 Your password is decent but could be stronger."
    elif score == 4:
        feedback = "✅ Good password! Consider adding more complexity."
    elif score == 5:
        feedback = "💪 Excellent password! You're all set."

    return f'Your password has:\n{lower} lowercase letters\n{upper} uppercase letters\n{digits} digits\n{spaces} spaces\n{specials} special characters\nPassword Score: {score}/5\nRemarks: {feedback}', score

def verify_password():
    pwd = entry_pwd.get()
    result, score = evaluate_password_strength(pwd)
    text_output.config(state='normal')
    text_output.delete('1.0', 'end')
    text_output.insert('end', result)
    text_output.config(state='disabled')
    if score < 3:
        progress_meter["style"] = "Red.Horizontal.TProgressbar"
    elif score < 5:
        progress_meter["style"] = "Orange.Horizontal.TProgressbar"
    else:
        progress_meter["style"] = "Green.Horizontal.TProgressbar"
    animate_progress(progress_meter, score * 20, 0)

def create_password():
    characters = string.ascii_letters + string.digits + string.punctuation + " "
    pwd = ''.join(secrets.choice(characters) for _ in range(20))
    entry_pwd.delete(0, 'end')
    entry_pwd.insert('end', pwd)

def copy_to_clipboard():
    pwd = entry_pwd.get()
    if pwd:
        pyperclip.copy(pwd)
        
        # Create a custom dialog window for confirmation
        copy_dialog = tk.Toplevel(root)
        copy_dialog.title("Password Copied")
        copy_dialog.geometry("400x150")
        copy_dialog.configure(bg="#e0f7fa")  # Light cyan background

        # Add an icon or emoji
        icon_label = tk.Label(copy_dialog, text="✅", font=("Helvetica", 32), bg="#e0f7fa", fg="#1ee31d")
        icon_label.pack(pady=10)

        # Add a message
        msg_label = tk.Label(copy_dialog, text="Password copied to clipboard successfully!", 
                             font=("Helvetica", 12, "bold"), bg="#e0f7fa", fg="#00796b")
        msg_label.pack(pady=5)

        # Add an "OK" button to close the dialog
        ok_button = tk.Button(copy_dialog, text="OK", command=copy_dialog.destroy, 
                              bg="#14dc6b", fg="white", font=("Helvetica", 10, "bold"))
        ok_button.pack(pady=10)

    else:
        messagebox.showwarning("No Password", "⚠️ Please enter a password to copy!")

def clear_entry():
    entry_pwd.delete(0, 'end')

def toggle_password_visibility():
    if entry_pwd.cget('show') == '':
        entry_pwd.config(show='*')
        toggle_btn.config(text="👀 Show")
    else:
        entry_pwd.config(show='')
        toggle_btn.config(text="🙈 Hide ")

def on_close():
    exit_dialog = tk.Toplevel(root)
    exit_dialog.title("Exit Confirmation")
    exit_dialog.geometry("300x150")
    exit_dialog.configure(bg="#f0f8ff")

    msg_label = tk.Label(exit_dialog, text="Are you sure you want to exit?", bg="#f0f8ff", fg="#333333", font=("Helvetica", 12, "bold"))
    msg_label.pack(pady=20)

    btn_frame = tk.Frame(exit_dialog, bg="#f0f8ff")
    btn_frame.pack(pady=10)

    def confirm_exit():
        root.destroy()

    yes_button = tk.Button(btn_frame, text="Yes, Exit", command=confirm_exit, bg="#ff6347", fg="white", font=("Helvetica", 10, "bold"))
    yes_button.pack(side=tk.LEFT, padx=10)

    no_button = tk.Button(btn_frame, text="No, Stay", command=exit_dialog.destroy, bg="#32cd32", fg="white", font=("Helvetica", 10, "bold"))
    no_button.pack(side=tk.RIGHT, padx=10)

def animate_progress(progressbar, target, current):
    if current < target:
        progressbar["value"] = current
        root.after(10, animate_progress, progressbar, target, current + 1)

# Hover effect functions
def on_enter(btn, color):
    btn['background'] = color

def on_leave(btn, color):
    btn['background'] = color

root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("650x400")

main_frame = tk.Frame(root, bg="#f0f0f0")  # Changed background color
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

label_pwd = tk.Label(main_frame, text="Enter the password:", bg="#f0f0f0", fg="#333333", font=("Helvetica", 14))
label_pwd.grid(row=0, column=0, padx=5, pady=5, sticky="we")

entry_pwd = tk.Entry(main_frame, show="*", font=("Helvetica", 12))
entry_pwd.grid(row=0, column=1, padx=5, pady=5, sticky="we", columnspan=2)

toggle_btn = tk.Button(main_frame, text="👀 Show", command=toggle_password_visibility, bg="#8A2BE2", fg="white", font=("Helvetica", 12))
toggle_btn.grid(row=0, column=3, padx=5, pady=5, sticky="we")



btn_check = tk.Button(main_frame, text="Check", command=verify_password, 
                      bg="#4caf50", fg="white", font=("Helvetica", 12),
                      highlightthickness=0, bd=0, padx=10, pady=5, 
                      relief=tk.GROOVE, borderwidth=5)
btn_check.grid(row=1, column=0, pady=10, padx=5, sticky="we")


btn_generate = tk.Button(main_frame, text="Generate Password", command=create_password, 
                         bg="#2196f3", fg="white", font=("Helvetica", 12),
                         highlightthickness=0, bd=0, padx=10, pady=5, 
                         relief=tk.GROOVE, borderwidth=5)
btn_generate.grid(row=1, column=1, pady=10, padx=5, sticky="we")

btn_copy = tk.Button(main_frame, text="Copy Password", command=copy_to_clipboard,
                      bg="#ff9800", fg="white",font=("Helvetica", 12),highlightthickness=0, bd=0, padx=10, pady=5, 
                         relief=tk.GROOVE, borderwidth=5)
btn_copy.grid(row=1, column=2, pady=10, padx=5, sticky="we")

btn_clear = tk.Button(main_frame, text="Clear", command=clear_entry, bg="#f44336", fg="white", font=("Helvetica", 12),highlightthickness=0, bd=0, padx=10, pady=5, 
                         relief=tk.GROOVE, borderwidth=5)
btn_clear.grid(row=1, column=3, pady=10, padx=5, sticky="we")

text_output = tk.Text(main_frame, height=10, width=60, state='disabled', font=("Helvetica", 10),highlightthickness=0, bd=0, padx=10, pady=5, 
                         relief=tk.GROOVE, borderwidth=5)
text_output.grid(row=2, column=0, columnspan=4, pady=10)

progress_meter = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=450, mode='determinate', value=0,
                                 style="Blue.Horizontal.TProgressbar")
progress_meter.grid(row=3, column=0, columnspan=4, pady=12)

entry_pwd.bind("<KeyRelease>", lambda event: verify_password())

root.protocol("WM_DELETE_WINDOW", on_close)

# Add hover effects
buttons = [
    (btn_check, "#4caf50", "#388e3c"),
    (btn_generate, "#2196f3", "#1976d2"),
    (btn_copy, "#ff9800", "#f57c00"),
    (btn_clear, "#f44336", "#d32f2f"),
    (toggle_btn, "#8A2BE2", "#7B68EE")
]

for btn, normal_color, hover_color in buttons:
    btn.bind("<Enter>", lambda e, b=btn, c=hover_color: on_enter(b, c))
    btn.bind("<Leave>", lambda e, b=btn, c=normal_color: on_leave(b, c))

# Center all widgets in the frame
for widget in main_frame.winfo_children():
    widget.grid_configure(sticky="nsew")

root.mainloop()