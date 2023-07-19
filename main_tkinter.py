import tkinter as tk
from tkinter import messagebox
from pytube import YouTube, Playlist
from PIL import Image, ImageTk


def download_content(url, content_type):
    try:
        if "playlist" in url.lower():
            playlist = Playlist(url)
            for video_url in playlist.video_urls:
                if content_type == "audio":
                    download_single_audio(video_url)
                else:
                    download_single_video(video_url)
        else:
            if content_type == "audio":
                download_single_audio(url)
            else:
                download_single_video(url)

        return True
    except Exception as e:
        return False


def download_single_audio(url):
    try:
        # Get the YouTube video
        yt = YouTube(url)

        # Extract the audio stream (highest quality available, in this case)
        audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()

        # Set the output file path and download the audio
        audio_stream.download(output_path="./downloads")

        return True
    except Exception as e:
        return False


def download_single_video(url):
    try:
        # Get the YouTube video
        yt = YouTube(url)

        # Set the output file path and download the video
        yt.streams.get_highest_resolution().download(output_path="./downloads")

        return True
    except Exception as e:
        return False


def on_download_audio():
    url = url_entry.get()
    if url:
        success = download_content(url, "audio")
        if success:
            messagebox.showinfo("Success", "Audio downloaded successfully!")
    else:
        messagebox.showwarning("Error", "Please enter a valid YouTube video or playlist URL.")

def on_download_video():
    url = url_entry.get()
    if url:
        success = download_content(url, "video")
        if success:
            messagebox.showinfo("Success", "Video downloaded successfully!")
    else:
        messagebox.showwarning("Error", "Please enter a valid YouTube video URL.")

# Create the main Tkinter window
root = tk.Tk()
root.title("YouTube Downloader")

# Load and display the logo image
logo_image = Image.open("logo.png")  # Replace with the path to your logo image
logo_image = logo_image.resize((150, 150))  # Resize the image to fit
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=logo_photo)
logo_label.pack(pady=10)

# Create and pack the URL input field
url_label = tk.Label(root, text="Enter the YouTube video or playlist URL:")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Create and pack the Download buttons
download_frame = tk.Frame(root)
download_frame.pack(pady=10)

download_audio_button = tk.Button(download_frame, text="Download Audio", command=on_download_audio, bg="#f63366", fg="white")
download_audio_button.pack(side=tk.LEFT, padx=10)

download_video_button = tk.Button(download_frame, text="Download Video", command=on_download_video, bg="#f63366", fg="white")
download_video_button.pack(side=tk.LEFT, padx=10)

# Run the Tkinter event loop
root.mainloop()