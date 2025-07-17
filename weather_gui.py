import tkinter as tk
import requests
is_dark_mode = False
def set_colors():
    global bg_color, entry_bg, text_color, label_color, button_bg, button_fg
    if is_dark_mode:
        bg_color = "#121212"
        entry_bg = "#1F1F1F"
        text_color = "#FFFFFF"
        label_color = "#00FFF7"
        button_bg = "#03DAC6"
        button_fg = "#000000"
    else:
        bg_color = "#F5F5F5"
        entry_bg = "#FFFFFF"
        text_color = "#000000"
        label_color = "#005599"
        button_bg = "#FFD700"
        button_fg = "#000000"
set_colors()
root = tk.Tk()
root.title("Weather App")
root.geometry("460x430")
root.configure(bg=bg_color)
def apply_theme():
    root.configure(bg=bg_color)
    city_label.config(bg=bg_color, fg=label_color)
    city_entry.config(bg=entry_bg, fg=text_color, insertbackground=text_color)
    get_button.config(bg=button_bg, fg=button_fg)
    result_label.config(bg=bg_color, fg=text_color)
    toggle_button.config(bg="#666666" if is_dark_mode else "#CCCCCC",
                         fg="#FFFFFF" if is_dark_mode else "#000000")
def color(text, hex_color="#000000"):
    return f"{text}"
def get_weather():
    city = city_entry.get()
    api_key = "fb01f4eb938f35c9b843806926e1d1d8"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather = data["weather"][0]["description"].title()
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            city_name = data["name"]
            result = (
                f"{color('📍  City:', label_color)} {color(city_name)}\n"
                f"{color('🌤️ Condition:', label_color)} {color(weather)}\n"
                f"{color('🌡️  Temperature:', label_color)} {color(f'{temp} °C')}\n"
                f"{color('🤒 Feels Like:', label_color)} {color(f'{feels_like} °C')}\n"
                f"{color('💧  Humidity:', label_color)} {color(f'{humidity}%')}"
            )
            result_label.config(text=result)
        else:
            result_label.config(text=color("❌ City not found or error in data.", "#FF5555"))
    except requests.exceptions.RequestException:
        result_label.config(text=color("⚠️ Network error occurred.", "#FF5555"))
def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    set_colors()
    apply_theme()
city_label = tk.Label(root, text="Enter city name:", font=("Arial", 12, "bold"))
city_label.pack(pady=(20, 5))
city_entry = tk.Entry(root, font=("Arial", 12), width=30)
city_entry.pack(pady=5)
root.bind('<Return>', lambda event: get_weather())
get_button = tk.Button(root, text="Get Weather", command=get_weather,
                       font=("Arial", 11, "bold"), padx=10, pady=5)
get_button.pack(pady=12)
result_label = tk.Label(root, text="", justify="left", anchor="w",
                        font=("Consolas", 12), width=44, height=7)
result_label.pack(pady=10)

toggle_button = tk.Button(root, text="🌓 Toggle Theme", command=toggle_theme,
                          font=("Arial", 10, "bold"), padx=5, pady=5)
toggle_button.pack(pady=(5, 15))
apply_theme()
root.mainloop()
