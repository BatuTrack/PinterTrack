import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import re
import os

def get_video_url(pinterest_url):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(pinterest_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    matches = re.findall(r'"contentUrl":"(https://[^"]+\.mp4)"', response.text)
    if matches:
        return matches[0].replace('\\u0026', '&')
    return None

def download_video():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("YOU'RE MISTAKE YOU STUPID!", "Enter your Pinterest video link.")
        return

    status_label.config(text="Searching for video...", bg="#000000", fg="#ff0a0a")
    video_url = get_video_url(url)

    if not video_url:
        status_label.config(text="Video URL not found", bg="#000000", fg="#ff0a0a")
        return

    try:
        status_label.config(text="Downloading...", bg="#000000", fg="#ff0a0a")
        r = requests.get(video_url, stream=True)
        filename = "pinterest_video.mp4"
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
        status_label.config(text=f"Download completed: {filename}", bg="#000000", fg="green")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")

 # Gui part :O
root = tk.Tk()
root.title("discord: batu.track")
root.geometry("400x200")
root.iconbitmap("icon.ico")
root.configure(bg="#7c0000")

tk.Label(root, text="Pinterest Video Link:", bg="#000000", fg="#ff0a0a").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack()

tk.Button(root, text="Download Video", bg="#000000", fg="#ff0a0a", command=download_video).pack(pady=10)
status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
