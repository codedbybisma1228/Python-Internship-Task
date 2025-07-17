import tkinter as tk
from tkinter import messagebox
FILENAME = "products.txt"
def load_products():
    try:
        with open(FILENAME, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []
def save_products(products):
    with open(FILENAME, "w") as file:
        for product in products:
            file.write(product + "\n")
def add_product():
    product = entry.get().strip()
    if product:
        listbox.insert(tk.END, product)
        entry.delete(0, tk.END)
        save_products(listbox.get(0, tk.END))
    else:
        messagebox.showwarning("Empty", "Please enter a product name.")
def delete_product():
    selected = listbox.curselection()
    if selected:
        listbox.delete(selected)
        save_products(listbox.get(0, tk.END))
        selected_label.config(text="Selected Product: None")
    else:
        messagebox.showwarning("Select", "Please select a product to delete.")
def show_selected(event):
    selected = listbox.curselection()
    if selected:
        selected_item = listbox.get(selected)
        selected_label.config(text=f"Selected Product: {selected_item}")
    else:
        selected_label.config(text="Selected Product: None")
bg_color = "#eaf6ff"        # Soft blue background
entry_bg = "#ffffff"        # White input box
fg_color = "#222222"        # Dark text
button_add = "#4CAF50"      # Green
button_del = "#f44336"      # Red
select_bg = "#d0ebff"       # Light blue selected item
root = tk.Tk()
root.title("🛍 Product List Manager")
root.geometry("420x460")
root.configure(bg=bg_color)
tk.Label(root, text="🛒 Product List Manager", font=("Segoe UI", 16, "bold"),
         bg=bg_color, fg=fg_color).pack(pady=12)
entry_frame = tk.Frame(root, bg=bg_color)
entry_frame.pack(pady=5)

entry = tk.Entry(entry_frame, font=("Segoe UI", 12), width=28, bg=entry_bg, fg=fg_color,
                 insertbackground=fg_color, relief="solid", bd=1)
entry.grid(row=0, column=0, padx=6)

add_btn = tk.Button(entry_frame, text="Add", command=add_product,
                    bg=button_add, fg="white", font=("Segoe UI", 10, "bold"), width=10, relief="flat")
add_btn.grid(row=0, column=1)
listbox_frame = tk.Frame(root, bg=bg_color)
listbox_frame.pack(pady=10)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(
    listbox_frame,
    width=45,
    height=12,
    font=("Segoe UI", 11),
    bg=entry_bg,
    fg=fg_color,
    yscrollcommand=scrollbar.set,
    selectbackground=select_bg,
    relief="solid",
    bd=1
)
listbox.pack()
listbox.bind("<<ListboxSelect>>", show_selected)

scrollbar.config(command=listbox.yview)
selected_label = tk.Label(root, text="Selected Product: None", font=("Segoe UI", 10, "italic"),
                          bg=bg_color, fg=fg_color)
selected_label.pack(pady=5)
delete_btn = tk.Button(root, text="Delete Selected", command=delete_product,
                       bg=button_del, fg="white", font=("Segoe UI", 10, "bold"),
                       relief="flat", width=20)
delete_btn.pack(pady=10)
for item in load_products():
    listbox.insert(tk.END, item)
root.mainloop()

