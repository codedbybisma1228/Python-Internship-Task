import tkinter as tk
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("300x420")  # Compact starting size
root.configure(bg="#f0f0f0")
root.resizable(True, True)  # ✅ Enable maximize/resizing
expression = ""
text_input = tk.StringVar()
entry = tk.Entry(root, font=('Arial', 20), textvariable=text_input,
                 bd=8, relief="sunken", justify='right', bg="white")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=15, ipadx=5, ipady=10, sticky="we")
def press(num):
    global expression
    expression += str(num)
    text_input.set(expression)

def equal():
    global expression
    try:
        result = str(eval(expression))
        text_input.set(result)
        expression = result
    except:
        text_input.set("Error")
        expression = ""

def clear_all():
    global expression
    expression = ""
    text_input.set("")

def clear_entry():
    global expression
    expression = expression[:-1]
    text_input.set(expression)
button_style = {
    "font": ('Arial', 14),
    "padx": 15,
    "pady": 15,
    "bd": 1,
    "relief": "ridge"
}
buttons = [
    ('7', 1, 0, "#ffffff"), ('8', 1, 1, "#ffffff"), ('9', 1, 2, "#ffffff"), ('/', 1, 3, "#d9edf7"),
    ('4', 2, 0, "#ffffff"), ('5', 2, 1, "#ffffff"), ('6', 2, 2, "#ffffff"), ('*', 2, 3, "#d9edf7"),
    ('1', 3, 0, "#ffffff"), ('2', 3, 1, "#ffffff"), ('3', 3, 2, "#ffffff"), ('-', 3, 3, "#d9edf7"),
    ('0', 4, 0, "#ffffff"), ('.', 4, 1, "#ffffff"), ('=', 4, 2, "#d4edda"), ('+', 4, 3, "#d9edf7"),
]

for (text, row, col, color) in buttons:
    action = lambda x=text: press(x) if x != '=' else equal()
    tk.Button(root, text=text, command=action, bg=color, **button_style).grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

tk.Button(root, text='C', command=clear_all, bg="#f8d7da", **button_style).grid(row=5, column=0, columnspan=2, sticky="we", padx=3, pady=10)
tk.Button(root, text='CE', command=clear_entry, bg="#fff3cd", **button_style).grid(row=5, column=2, columnspan=2, sticky="we", padx=3, pady=10)
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
for j in range(4):
    root.grid_columnconfigure(j, weight=1)
root.mainloop()




