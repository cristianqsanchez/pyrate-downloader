import tkinter as tk
import requests
from time import sleep
from PIL import ImageTk, Image
from io import BytesIO
from pytube import YouTube


def get_video_info(url):
    try:
        response = requests.get(f"https://www.youtube.com/oembed?url={url}&format=json")
        response.raise_for_status()
        data = response.json()

        title = data["title"]
        thumbnail_url = data["thumbnail_url"]

        thumbnail_response = requests.get(thumbnail_url)
        thumbnail_image = Image.open(BytesIO(thumbnail_response.content))
        thumbnail_tk_image = ImageTk.PhotoImage(thumbnail_image)

        return title, thumbnail_tk_image

    except Exception as e:
        print(f"Error al obtener la información del video: {e}")
        return None


def show_video_info():
    url = url_entry.get()
    video_info = get_video_info(url)

    if video_info is not None:
        title, thumbnail_tk_image = video_info
        title_label.config(text=title)
        thumbnail_label.config(image=thumbnail_tk_image)
        thumbnail_label.image = thumbnail_tk_image


def download_video():
    url = url_entry.get()
    yt = YouTube(url)
    while True:
        try:
            yt.streams.get_by_itag(22).download()
            break
        except Exception as e:
            print(f"Descargando... - {e}")
            sleep(1)
            yt = YouTube(url)
            continue


root = tk.Tk()
root.title("Pyrate downloader")

url_label = tk.Label(root, text="URL del video:")
url_label.pack()
url_entry = tk.Entry(root)
url_entry.pack()

get_info_button = tk.Button(root, text="Preparar video", command=show_video_info)
get_info_button.pack()

download_video = tk.Button(root, text="Descargar video", command=download_video)
download_video.pack()

title_label = tk.Label(root, text="")
title_label.pack()
thumbnail_label = tk.Label(root)
thumbnail_label.pack()

root.mainloop()
