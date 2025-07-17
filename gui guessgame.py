import tkinter as tk
from tkinter import messagebox
import random
secret_number = 0
attempts = 0
current_range = (1, 100)
def start_game(min_val, max_val):
    global secret_number, attempts, current_range
    current_range = (min_val, max_val)
    secret_number = random.randint(min_val, max_val)
    attempts = 0
    entry.delete(0, tk.END)
    result_label.config(text="")
    attempt_label.config(text=f"Attempts: {attempts}")
    range_label.config(text=f"🎯 Guess a number between {min_val} and {max_val}")
def check_guess():
    global attempts
    guess = entry.get()
    if not guess.isdigit():
        messagebox.showwarning("Invalid Input", "Please enter a valid number.")
        return
    guess = int(guess)
    min_val, max_val = current_range
    if guess < min_val or guess > max_val:
        messagebox.showwarning("Out of Range", f"Enter number between {min_val} and {max_val}.")
        return
    attempts += 1
    attempt_label.config(text=f"Attempts: {attempts}")
    if guess < secret_number:
        result_label.config(text="Too low! Try again.", fg="#f39c12")
    elif guess > secret_number:
        result_label.config(text="Too high! Try again.", fg="#e74c3c")
    else:
        result_label.config(text=f"🎉 Correct! You guessed it in {attempts} tries!", fg="#2ecc71")
bg_color = "#1e1e2f"
fg_color = "#ffffff"
input_bg = "#2c2c3c"
btn_color = "#3498db"
restart_color = "#e67e22"
root = tk.Tk()
root.title("🎮 Number Guessing Game")
root.geometry("450x400")
root.configure(bg=bg_color)
tk.Label(root, text="Number Guessing Game", font=("Segoe UI", 16, "bold"),
         bg=bg_color, fg=fg_color).pack(pady=10)
diff_frame = tk.Frame(root, bg=bg_color)
diff_frame.pack(pady=5)
tk.Label(diff_frame, text="Select Difficulty:", font=("Segoe UI", 10, "bold"),
         bg=bg_color, fg=fg_color).pack(side=tk.LEFT, padx=5)
tk.Button(diff_frame, text="Easy (1–50)", command=lambda: start_game(1, 50),
          bg=btn_color, fg="white", font=("Segoe UI", 9), relief="flat").pack(side=tk.LEFT, padx=5)
tk.Button(diff_frame, text="Medium (1–100)", command=lambda: start_game(1, 100),
          bg=btn_color, fg="white", font=("Segoe UI", 9), relief="flat").pack(side=tk.LEFT, padx=5)
tk.Button(diff_frame, text="Hard (1–200)", command=lambda: start_game(1, 200),
          bg=btn_color, fg="white", font=("Segoe UI", 9), relief="flat").pack(side=tk.LEFT, padx=5)
range_label = tk.Label(root, text="", font=("Segoe UI", 12), bg=bg_color, fg=fg_color)
range_label.pack(pady=5)
entry = tk.Entry(root, font=("Segoe UI", 14), width=10, justify='center',
                 bg=input_bg, fg=fg_color, insertbackground=fg_color, relief="solid", bd=1)
entry.pack(pady=10)
tk.Button(root, text="Guess", command=check_guess, font=("Segoe UI", 11, "bold"),
          bg=btn_color, fg="white", relief="flat", width=15).pack(pady=8)
result_label = tk.Label(root, text="", font=("Segoe UI", 12), bg=bg_color, fg=fg_color)
result_label.pack(pady=5)
attempt_label = tk.Label(root, text="Attempts: 0", font=("Segoe UI", 10, "bold"),
                         bg=bg_color, fg=fg_color)
attempt_label.pack(pady=5)
tk.Button(root, text="Restart Game", command=lambda: start_game(*current_range),
          bg=restart_color, fg="white", font=("Segoe UI", 10), relief="flat", width=15).pack(pady=15)
start_game(1, 100)
root.mainloop()
