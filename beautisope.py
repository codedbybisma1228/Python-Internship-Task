import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# ✅ Updated GEO News RSS feed
RSS_FEEDS = {
    "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
    "CNN": "http://rss.cnn.com/rss/edition.rss",
    "GEO News": "https://www.geo.tv/rss/1/1"  # ✅ Fixed URL
}

class NewsScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("News Scraper - BBC, CNN, GEO")
        self.root.geometry("950x650")
        self.root.config(bg="#f0f4f8")
        self.headlines = []
        self.filtered_headlines = []

        # 📰 Title
        tk.Label(root, text="📰 Live News Headlines", font=("Segoe UI", 20, "bold"),
                 bg="#1d3557", fg="white", pady=10).pack(fill=tk.X)

        # 🔘 Controls
        controls = tk.Frame(root, bg="#f0f4f8")
        controls.pack(pady=10)

        tk.Label(controls, text="Source:", font=("Segoe UI", 11), bg="#f0f4f8").pack(side=tk.LEFT, padx=5)
        self.source_var = tk.StringVar(value="BBC News")
        self.source_dropdown = ttk.Combobox(controls, textvariable=self.source_var,
                                            values=list(RSS_FEEDS.keys()), state="readonly", width=20)
        self.source_dropdown.pack(side=tk.LEFT, padx=5)

        tk.Button(controls, text="Fetch News", font=("Segoe UI", 11), bg="#457b9d", fg="white",
                  command=self.fetch_news).pack(side=tk.LEFT, padx=10)

        tk.Label(controls, text="Filter:", font=("Segoe UI", 11), bg="#f0f4f8").pack(side=tk.LEFT, padx=5)
        self.filter_var = tk.StringVar()
        self.filter_entry = tk.Entry(controls, textvariable=self.filter_var, font=("Segoe UI", 11), width=30)
        self.filter_entry.pack(side=tk.LEFT, padx=5)
        self.filter_entry.bind("<KeyRelease>", lambda e: self.display_filtered_news())

        tk.Button(controls, text="Export to TXT", font=("Segoe UI", 11), bg="#2a9d8f", fg="white",
                  command=self.export_txt).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Export to CSV", font=("Segoe UI", 11), bg="#e76f51", fg="white",
                  command=self.export_csv).pack(side=tk.LEFT, padx=5)

        # 🖥️ Display Area
        self.text_area = tk.Text(root, font=("Segoe UI", 11), wrap="word", bg="white", fg="#333")
        self.scrollbar = tk.Scrollbar(root, command=self.text_area.yview)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0), pady=(5, 20))
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(5, 20))

        # 🕒 Timestamp
        self.timestamp = tk.Label(root, text="Last updated: --", font=("Segoe UI", 9), bg="#f0f4f8", fg="gray")
        self.timestamp.pack()

        # 👤 Footer
        tk.Label(root, text="© 2025 Bisma Aslam | News Scraper GUI", font=("Segoe UI", 9),
                 bg="#f0f4f8", fg="#888").pack(side=tk.BOTTOM, pady=5)

        self.schedule_auto_refresh()

    def fetch_news(self):
        source = self.source_var.get()
        url = RSS_FEEDS.get(source)
        self.headlines.clear()
        self.filtered_headlines.clear()

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item")

            for item in items:
                title = item.find("title").text.strip() if item.find("title") else "No Title"
                link = item.find("link").text.strip() if item.find("link") else "No Link"
                date_tag = item.find("pubDate")
                date = date_tag.text.strip() if date_tag else "No date available"
                self.headlines.append({"title": title, "link": link, "date": date, "source": source})

            self.display_filtered_news()
            self.update_timestamp()

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Could not fetch news:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def display_filtered_news(self):
        keyword = self.filter_var.get().lower()
        self.filtered_headlines = [h for h in self.headlines if keyword in h["title"].lower()]
        self.text_area.delete(1.0, tk.END)

        if not self.filtered_headlines:
            self.text_area.insert(tk.END, "No matching news found.\n")
            return

        for i, h in enumerate(self.filtered_headlines[:10]):
            self.text_area.insert(tk.END, f"{i+1}. {h['title']}\n🕒 {h['date']}\n🔗 {h['link']}\n\n")

    def export_txt(self):
        if not self.filtered_headlines:
            messagebox.showinfo("No Data", "No headlines to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                for h in self.filtered_headlines:
                    f.write(f"{h['title']}\n{h['date']}\n{h['link']}\n\n")
            messagebox.showinfo("Success", "Headlines exported to TXT.")

    def export_csv(self):
        if not self.filtered_headlines:
            messagebox.showinfo("No Data", "No headlines to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV Files", "*.csv")])
        if file_path:
            df = pd.DataFrame(self.filtered_headlines)
            df.to_csv(file_path, index=False, encoding="utf-8")
            messagebox.showinfo("Success", "Headlines exported to CSV.")

    def update_timestamp(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp.config(text=f"Last updated: {now}")

    def schedule_auto_refresh(self):
        self.fetch_news()
        self.root.after(300000, self.schedule_auto_refresh)  # Refresh every 5 minutes

if __name__ == "__main__":
    root = tk.Tk()
    app = NewsScraperApp(root)
    root.mainloop()
