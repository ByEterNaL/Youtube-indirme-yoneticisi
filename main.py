from pytube import YouTube
from pytube.cli import on_progress
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename
from colorama import init, Fore

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def choose_save_path():
    while True:
        Tk().withdraw()
        save_path = askdirectory()
        if save_path:
            print(Fore.GREEN + f"İndirme yolu seçildi:" + Fore.YELLOW + f"{save_path}")
            return save_path
        else:
            print(Fore.Red + "Dosya yolu seçilmedi veya seçilen klasör silindi, lütfen tekrar seçiniz.")

def choose_file():
    Tk().withdraw()
    return askopenfilename()

def download_video(url, save_path, format_choice, resolution=None):
    yt = YouTube(url, on_progress_callback=on_progress)
    if format_choice == 'mp4':
        if resolution:
            yt_stream = yt.streams.filter(file_extension='mp4', resolution=resolution).first()
        else:
            yt_stream = yt.streams.filter(file_extension='mp4').first()
        yt_stream.download(output_path=save_path)
    elif format_choice == 'mp3':
        yt_stream = yt.streams.filter(only_audio=True).first()
        output_file = yt_stream.download(output_path=save_path)
        base, ext = os.path.splitext(output_file)
        new_file = base + '.mp3'
        os.rename(output_file, new_file)
    print(Fore.GREEN + "Video indirildi: " + Fore.YELLOW + f"{yt.title}")

def download_videos_from_file(file_path, save_path, format_choice, resolution=None):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    for url in urls:
        download_video(url.strip(), save_path, format_choice, resolution)

def main():
    save_path = choose_save_path()
    while True:
        clear_screen()
        print(Fore.GREEN + f"İndirme yolu seçildi:" + Fore.YELLOW + f"{save_path}")
        choice = input("Seçim yapın: (1) Tekli İndirme (2) Çoklu İndirme: ")
        if choice == '1':
            video_url = input("Video URL'sini girin: ")
            format_choice = input("Format seçin (mp3/mp4): ")
            resolution = None
            if format_choice == 'mp4':
                resolution = input("Çözünürlük seçin (örn., 720p): ")
            download_video(video_url, save_path, format_choice, resolution)
        elif choice == '2':
            file_path = choose_file()
            format_choice = input("Format seçin (mp3/mp4): ")
            resolution = None
            if format_choice == 'mp4':
                resolution = input("Çözünürlük seçin (örn., 720p): ")
            download_videos_from_file(file_path, save_path, format_choice, resolution)
        
        repeat = input("İndirme işlemini tekrarlamak ister misiniz? (y/n): ")
        if repeat.lower() != 'y':
            break

if __name__ == "__main__":
    main()
