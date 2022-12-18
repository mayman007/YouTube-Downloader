from tkinter import *
from tkinter import filedialog, messagebox
import customtkinter
from pytube import YouTube, Playlist, Search, extract, request
import pytube.request
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
import threading
import json
from PIL import Image
import urllib.request
import os
import io
import reprlib
import getpass
import time
import subprocess
import webbrowser
import ffmpeg
import pathlib


# Get config prefences from JSON
def get_bg_theme():
    with open("theme_config.json", "r") as f:
        theme = json.load(f)
    return theme["bg_theme"]
def get_default_color():
    with open("theme_config.json", "r") as f:
        theme = json.load(f)
    return theme["default_color"]

# Set themes
customtkinter.set_appearance_mode(get_bg_theme())
customtkinter.set_default_color_theme(get_default_color())

# On closing
def onClosing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Create form
root = customtkinter.CTk()
width = 700
height = 460
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")
root.resizable(False, False)
root.iconbitmap("YDICO.ico")
root.title("YouTube Downloader")
root.protocol("WM_DELETE_WINDOW", onClosing)
customtkinter.CTkLabel(root, text = "YouTube Downloader", font = ("arial bold", 35)).pack()

# Paste link here
link_var = StringVar()
customtkinter.CTkLabel(root, text = "Type Link / Keywords Here", font = ("arial bold", 30)).place(x = 240 , y = 85)
link_entry = customtkinter.CTkEntry(root, width = 345, textvariable = link_var)
link_entry.place(x = 265 , y = 140)
root.after(200, lambda: link_entry.focus())

# Format and quality selections
quality_var = IntVar()
customtkinter.CTkLabel(root, text = "Video Download", font = ("arial bold", 20)).place(x = 35 , y = 75)
customtkinter.CTkRadioButton(root, text = "1080p", variable = quality_var, value = 137, font = ("arial", 20)).place(x = 50 , y = 110)
customtkinter.CTkRadioButton(root, text = "720p", variable = quality_var, value = 22, font = ("arial", 20)).place(x = 50 , y = 140)
customtkinter.CTkRadioButton(root, text = "480p", variable = quality_var, value = 135, font = ("arial", 20)).place(x = 50 , y = 170)
customtkinter.CTkRadioButton(root, text = "360p", variable = quality_var, value = 18, font = ("arial", 20)).place(x = 50 , y = 200)
customtkinter.CTkRadioButton(root, text = "240p", variable = quality_var, value = 133, font = ("arial", 20)).place(x = 50 , y = 230)
customtkinter.CTkRadioButton(root, text = "144p", variable = quality_var, value = 160, font = ("arial", 20)).place(x = 50 , y = 260)
customtkinter.CTkLabel(root, text = "Audio Download", font = ("arial bold", 20)).place(x = 35 , y = 290)
customtkinter.CTkRadioButton(root, text = "160kbps", variable = quality_var, value = 251, font = ("arial", 20)).place(x = 50 , y = 325)
customtkinter.CTkRadioButton(root, text = "128kbps", variable = quality_var, value = 140, font = ("arial", 20)).place(x = 50 , y = 355)
customtkinter.CTkRadioButton(root, text = "70kbps", variable = quality_var, value = 250, font = ("arial", 20)).place(x = 50 , y = 385)
customtkinter.CTkRadioButton(root, text = "50kbps", variable = quality_var, value = 249, font = ("arial", 20)).place(x = 50 , y = 415)

# Appearance theme
def changeTheme(bg):
    with open("theme_config.json", "r", encoding="utf8") as f:
        theme = json.load(f)
    with open("theme_config.json", "w", encoding="utf8") as f:
        theme["bg_theme"] = bg
        json.dump(theme, f, sort_keys = True, indent = 4, ensure_ascii = False)
    customtkinter.set_appearance_mode(get_bg_theme())
customtkinter.CTkLabel(root, text = "Appearance Theme", font = ("arial bold", 19)).place(x = 502 , y = 380)
themes_menu = customtkinter.CTkOptionMenu(root, values=["System", "Dark", "Light"], command = changeTheme)
themes_menu.place(x = 520 , y = 415)
themes_menu.set(get_bg_theme())

# Loadings
loading_var = StringVar()
loading_var.set("Download / Search")
ploading_counter_var = StringVar()
customtkinter.CTkLabel(root, textvariable = ploading_counter_var, font = ("arial", 22)).place(x = 412 , y = 250)
def Loading(loading_text):
    loading_var.set(loading_text)
    time.sleep(0.5)
    while True:
        if loading_var.get() == loading_text:
            loading_var.set(f"{loading_text}.")
            time.sleep(0.5)
        else: break
        if loading_var.get() == f"{loading_text}.":
            loading_var.set(f"{loading_text}..")
            time.sleep(0.5)
        else: break
        if loading_var.get() == f"{loading_text}..":
            loading_var.set(f"{loading_text}...")
            time.sleep(0.5)
        else: break
        if loading_var.get() == f"{loading_text}...":
            loading_var.set(loading_text)
            time.sleep(0.5)
        else: break

# On Download Button
def OnDownloadButton(event = None):
    global link
    link = link_var.get()
    if "https://" not in link or "youtu" not in link:
        loading_text = "Searching"
        threading.Thread(target = SearchWindow).start()
    elif "playlist" in link:
        loading_text = "Loading"
        threading.Thread(target = PlaylistWindow).start()
    else:
        loading_text = "Loading"
        threading.Thread(target = DownlaodWindow).start()
    threading.Thread(target = Loading, args = (loading_text,)).start()
link_entry.bind("<Return>", OnDownloadButton)

# Integer -> time format
def to_hms(s):
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "{}:{:0>2}:{:0>2}".format(h, m, s)

# Clean file names
def clean_filename(name):
    forbidden_chars = "*\\/\"'.|?:<>"
    filename = ("".join([x if x not in forbidden_chars else " " for x in name])).replace("  ", " ").strip()
    if len(filename) >= 176:
        filename = filename[:170] + "..."
    return filename

# When error happens return everything to normal in root
def whenError():
        video_button = customtkinter.CTkButton(root, textvariable = loading_var, width = 235, font = ("arial bold", 25), command = OnDownloadButton)
        video_button.place(x = 305 , y = 205)
        themes_menu.configure(state = "normal")
        loading_var.set("Download / Search")
        ploading_counter_var.set("")

# Download window
def DownlaodWindow():
    # Starting
    def VideoStart():
        threading.Thread(target = Downloading).start()
        threading.Thread(target = VideoDownloader).start()

    # Back home
    def backHome():
        download = downloading_var.get()
        non_downloading_list = ["", "Finished", "Canceled"]
        if download in non_downloading_list:
            pass
        else:
            msg_box = messagebox.askquestion(title = "Cancel Download",
            message = "Going back to home will cancel the current download.\n\nDo you wish to continue?",
            icon = "warning")
            if msg_box == "yes": pass
            else: return
        newWindow.destroy()
        root.deiconify()

    # Set path
    user = getpass.getuser()
    path = f"C:/Users\{user}\Downloads"
    global directory
    directory = os.path.realpath(path) # Deafult path in case the user didn't choose
    def BrowseDir(): # Path function
        global directory2
        directory2 = filedialog.askdirectory()
        path_var.set(directory2)

    # Captions download
    def CaptionsDownload():
        lang = lang_choose.get()
        if lang.lower() == "none":
            return
        elif lang.lower() == "arabic":
            lang = "ar"
        elif lang.lower() == "english":
            for transcript in transcript_list:
                if transcript.language_code == "en-US":
                    lang = "en-US"
                    break
                elif transcript.language_code == "en-UK":
                    lang = "en-UK"
                    break
                else:
                    lang = "en"
        else:
            progressbar.stop()
            toggle_button = customtkinter.CTkButton(newWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
            toggle_button.place(x = 550 , y = 347)
            cancel_button = customtkinter.CTkButton(newWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled")
            cancel_button.place(x = 595 , y = 347)
            download_button = customtkinter.CTkButton(newWindow, text = "Download", font = ("arial bold", 25), command = VideoStart)
            download_button.place(x = 540 , y = 306)
            path_button = customtkinter.CTkButton(newWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", hover_color = "gray25", width = 5, command = BrowseDir)
            path_button.place(x = 430 , y = 347)
            lang_choose.configure(state = "normal")
            downloading_var.set("")
            messagebox.showerror(title = "Subtitle Not Supported", message = "Please choose a supported language.")
            return False
        try: # Get the subtitle directly if it's there
            final = YouTubeTranscriptApi.get_transcript(video_id = video_id, languages = [lang])
            print("got one already there")
            sub = "subtitle"
        except: # If not then translate it
            translated = "no"
            en_list = ["en", "en-US","en-UK"]
            for transcript in transcript_list:
                if transcript.language_code in en_list: # Translate from English if it's there
                    final = transcript.translate(lang).fetch()
                    print(f"translated from {transcript.language_code}")
                    sub = "translated_subtitle"
                    translated = "yes"
                if translated == "no": # Avoid translating twice
                    final = transcript.translate(lang).fetch()
                    print(f"translated {transcript.language_code}")
                    sub = "translated_subtitle"
                    translated = "yes"
                else:
                    pass
        formatter = SRTFormatter()
        srt_formatted = formatter.format_transcript(final)
        try:
            with open(f"{directory2}/{clean_filename(url.title)}_{sub}_{lang}.srt", "w", encoding = "utf-8") as srt_file:
                srt_file.write(srt_formatted)
        except NameError:
            with open(f"{directory}/{clean_filename(url.title)}_{sub}_{lang}.srt", "w", encoding = "utf-8") as srt_file:
                srt_file.write(srt_formatted)

    # Pause/Resume function
    def toggle_download():
        global is_paused
        is_paused = not is_paused
        if is_paused:
            progressbar.stop()
            toggle_button = customtkinter.CTkButton(newWindow, text = "▶️", font = ("arial", 15), fg_color = "grey14", hover_color = "gray10", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
            toggle_button.place(x = 550 , y = 347)
            downloading_var.set("Paused")
        else:
            progressbar.start()
            toggle_button = customtkinter.CTkButton(newWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", hover_color = "gray10", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
            toggle_button.place(x = 550 , y = 347)
            downloading_var.set("Downloading")

    # Cancel function
    def cancel_download():
        global is_cancelled
        is_cancelled = True

    # Open folder in file explorer when download is finished
    def openFile():
        try:
            dir2 = os.path.normpath(directory2)
            subprocess.Popen(f'explorer "{dir2}"')
        except NameError:
            subprocess.Popen(f'explorer "{directory}"')

    # Downloading label function
    def Downloading():
        if downloading_var.get() == "Merging":
            while True:
                if downloading_var.get() == "Merging":
                    downloading_var.set("Merging.")
                    time.sleep(0.5)
                else: break
                if downloading_var.get() == "Merging.":
                    downloading_var.set("Merging..")
                    time.sleep(0.5)
                else: break
                if downloading_var.get() == "Merging..":
                    downloading_var.set("Merging...")
                    time.sleep(0.5)
                else: break
                if downloading_var.get() == "Merging...":
                    downloading_var.set("Merging")
                    time.sleep(0.5)
                else: break
        elif downloading_var.get() == "Downloading audio":
            while True:
                if downloading_var.get() == "Downloading audio":
                    downloading_var.set("Downloading audio.")
                    time.sleep(0.5)
                else: break
                if downloading_var.get() == "Downloading audio.":
                    downloading_var.set("Downloading audio..")
                    time.sleep(0.5)
                else: break
                if downloading_var.get() == "Downloading audio..":
                    downloading_var.set("Downloading audio...")
                    time.sleep(0.5)
                else: break
                if downloading_var.get() == "Downloading audio...":
                    downloading_var.set("Downloading audio")
                    time.sleep(0.5)
                else: break
        else:
            downloading_var.set("Downloading")
            time.sleep(0.5)
            while True:
                if downloading_var.get() == "Downloading":
                    downloading_var.set("Downloading.")
                    time.sleep(0.5)
                else: break
                if downloading_var.get() == "Downloading.":
                    downloading_var.set("Downloading..")
                    time.sleep(0.5)
                else: break
                if downloading_var.get() == "Downloading..":
                    downloading_var.set("Downloading...")
                    time.sleep(0.5)
                else: break
                if downloading_var.get() == "Downloading...":
                    downloading_var.set("Downloading")
                    time.sleep(0.5)
                else: break
        dont_change = ["Canceled", "Paused", "Finished"]
        while True:
            time.sleep(1)
            if downloading_var.get() in dont_change: continue
            else: Downloading()

    # One Video Downloader
    def VideoDownloader():
        # Preperations
        global is_paused, is_cancelled
        toggle_button = customtkinter.CTkButton(newWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", hover_color = "gray10", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
        toggle_button.place(x = 550 , y = 347)
        cancel_button = customtkinter.CTkButton(newWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", hover_color = "red4", width = 80, height = 26, command = cancel_download)
        cancel_button.place(x = 595 , y = 347)
        download_button = customtkinter.CTkButton(newWindow, text = "Download", font = ("arial bold", 25), state = "disabled")
        download_button.place(x = 540 , y = 306)
        path_button = customtkinter.CTkButton(newWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", width = 5, state = "disabled")
        path_button.place(x = 430 , y = 347)
        lang_choose.configure(state = "disabled")
        audio_tags_list = ["251" , "140" , "250" , "249"]
        non_progressive_list = ["137" , "135" , "133", "160"]
        if quality == "135": video = url.streams.filter(res = "480p").first()
        elif quality == "133": video = url.streams.filter(res = "240p").first()
        elif quality == "160": video = url.streams.filter(res = "144p").first()
        else: video = url.streams.get_by_itag(quality)
        # Download subtitles if selected
        if caps == "yes":
            if CaptionsDownload() == False: return
        else: pass
        # Progress stuff
        pytube.request.default_range_size = 2097152  # 2MB chunk size (update progress every 2MB)
        progressbar.start()
        progress_label.configure(text_color = "green")
        progress_size_label.configure(text_color = "LightBlue")

        # If the quality is non progressive video (1080p, 480p, 240p and 144p)
        if quality in non_progressive_list:
            try:
                vname = f"{directory2}/{clean_filename(url.title)}_video.mp4"
                aname = f"{directory2}/{clean_filename(url.title)}_audio.mp3"
            except NameError:
                vname = f"{directory}/{clean_filename(url.title)}_video.mp4"
                aname = f"{directory}/{clean_filename(url.title)}_audio.mp3"
            # Downlaod video
            with open(vname, "wb") as f:
                is_paused = is_cancelled = False
                video = request.stream(video.url) # Get an iterable stream
                downloaded = 0
                while True:
                    if is_cancelled:
                        downloading_var.set("Canceled")
                        break
                    if is_paused:
                        time.sleep(0.1)
                        continue
                    try: chunk = next(video, None) # Get next chunk of video
                    except Exception as e:
                        print(e)
                        return messagebox.showerror(title = "Something Went Wrong", message = "Something went wrong, please try again.")
                    if chunk:
                        f.write(chunk)
                        # Update progress
                        downloaded += len(chunk)
                        remaining = size - downloaded
                        bytes_downloaded = size - remaining
                        percentage_of_completion = bytes_downloaded / size * 100
                        percentage_var.set(f"{round(percentage_of_completion, 2)}%  ")
                        sizeprogress_var.set(f"{int(bytes_downloaded / 1024 / 1024)} MB  ")
                    else:
                        # When finished
                        break
            progressbar.stop()
            toggle_button = customtkinter.CTkButton(newWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
            toggle_button.place(x = 550 , y = 347)
            cancel_button = customtkinter.CTkButton(newWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled")
            cancel_button.place(x = 595 , y = 347)
            if is_cancelled:
                pass
            else: # Download audio
                downloading_var.set("Downloading audio")
                with open(aname, "wb") as f:
                    is_paused = is_cancelled = False
                    audio = url.streams.get_by_itag(251)
                    video = request.stream(audio.url) # Get an iterable stream
                    downloaded = 0
                    while True:
                        if is_paused:
                            time.sleep(0.1)
                            continue
                        try: chunk = next(video, None) # Get next chunk of video
                        except Exception as e:
                            print(e)
                            return messagebox.showerror(title = "Something Went Wrong", message = "Something went wrong, please try again.")
                        if chunk:
                            f.write(chunk) # Download the chunk into the file
                        else:
                            # When finished
                            break
                # Merge video and audio
                downloading_var.set("Merging")
                final_name = vname.replace("_video", f"_({quality_string})")
                cmd = f'ffmpeg -y -i "{aname}"  -r 30 -i "{vname}"  -filter:a aresample=async=1 -c:a flac -c:v copy "{final_name}"'
                subprocess.call(cmd, shell=True)
                # Finished
                newWindow.bell()
                downloading_var.set("Finished")
                converting_var.set("")
                customtkinter.CTkButton(newWindow, text = "Open File in Explorer", font = ("arial bold", 20), command = openFile).place(x = 470 , y = 420)
                global convert_count
                convert_count = 0

        # If the quality is 720p or 360p or audio
        else:
            if quality in audio_tags_list: ext = "mp3"
            else: ext = "mp4"
            try: vname = f"{directory2}/{clean_filename(url.title)}_({quality_string}).{ext}"
            except NameError: vname = f"{directory}/{clean_filename(url.title)}_({quality_string}).{ext}"
            with open(vname, "wb") as f:
                is_paused = is_cancelled = False
                video = request.stream(video.url) # get an iterable stream
                downloaded = 0
                while True:
                    if is_cancelled:
                        progressbar.stop()
                        toggle_button = customtkinter.CTkButton(newWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
                        toggle_button.place(x = 550 , y = 347)
                        cancel_button = customtkinter.CTkButton(newWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled")
                        cancel_button.place(x = 595 , y = 347)
                        downloading_var.set("Canceled")
                        break
                    if is_paused:
                        time.sleep(0.5)
                        continue
                    try: chunk = next(video, None) # Get next chunk of video
                    except: return messagebox.showerror(title = "Something Went Wrong", message = "Something went wrong, please try again.")
                    if chunk:
                        f.write(chunk) # Downlaod the chunk into the file
                        # Update progress
                        downloaded += len(chunk)
                        remaining = size - downloaded
                        bytes_downloaded = size - remaining
                        percentage_of_completion = bytes_downloaded / size * 100
                        percentage_var.set(f"{round(percentage_of_completion, 2)}%  ")
                        sizeprogress_var.set(f"{int(bytes_downloaded / 1024 / 1024)} MB  ")
                    else:
                        # When finished
                        progressbar.stop()
                        toggle_button = customtkinter.CTkButton(newWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
                        toggle_button.place(x = 550 , y = 347)
                        cancel_button = customtkinter.CTkButton(newWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled")
                        cancel_button.place(x = 595 , y = 347)
                        newWindow.bell()
                        downloading_var.set("Finished")
                        customtkinter.CTkButton(newWindow, text = "Open File in Explorer", font = ("arial bold", 20), command = openFile).place(x = 470 , y = 420)
                        break
        if is_cancelled:
            msg_box = messagebox.askquestion(title = "Delete Canceled File", message = f"Do you want to delete '{vname}'?")
            if msg_box == "yes": os.remove(vname)


    # Get video info, get link and check errors
    video_button = customtkinter.CTkButton(root, textvariable = loading_var, width = 235, font = ("arial bold", 25), state = "disabled")
    video_button.place(x = 305 , y = 205)
    themes_menu.configure(state = "disabled")
    try:
        global url
        url = YouTube(link)
        quality = str(quality_var.get())
        if not "youtu" in link or "playlist" in link:
            raise pytube.exceptions.RegexMatchError()
    except:
        whenError()
        return messagebox.showerror(title = "Link Not Valid", message = "Please enter a valid video link.")
    global video
    global size
    try:
        if quality == "0":
            whenError()
            return messagebox.showerror(title = "Format Not Selected", message = "Please select a format to download.")
        elif quality == "135": video = url.streams.filter(res = "480p").first()
        elif quality == "133": video = url.streams.filter(res = "240p").first()
        elif quality == "160": video = url.streams.filter(res = "144p").first()
        else: video = url.streams.get_by_itag(quality) # 1080p, 720, 360p, *audio
        size = video.filesize
        size_string = f"{round(size/1024/1024, 2)} MB"
    except urllib.error.URLError as e:
        print(e)
        whenError()
        return messagebox.showerror(title = "Not Connected", message = "Please check your internet connection.")
    except KeyError as e:
        print(e)
        whenError()
        return messagebox.showerror(title = "Something Went Wrong", message = "Something went wrong, please try again.")
    except AttributeError as e:
        print(e)
        whenError()
        return messagebox.showerror(title = "Format Not Available", message = "This video is not available in the format that you chose.")
    except pytube.exceptions.LiveStreamError as e:
        print(e)
        whenError()
        return messagebox.showerror(title = "Video is Live", message = "Can't download a live video.")

    # Get transcripts
    try:
        video_id = extract.video_id(link)
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        lang_choose_state = "normal"
        caps = "yes"
    except:
        lang_choose_state = "disabled"
        caps = "no"

    # Getting video thumbnail
    raw_data = urllib.request.urlopen(url.thumbnail_url).read()
    photo = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (270 , 150))

    # Video labels info
    r = reprlib.Repr()
    r.maxlist = 5       # max elements displayed for lists
    r.maxstring = 50    # max characters displayed for strings
    date_format = "%d/%m/%Y"
    if quality == "160":
        quality_string = "144p"
    elif quality == "133":
        quality_string = "240p"
    elif quality == "18":
        quality_string = "360p"
    elif quality == "135":
        quality_string = "480p"
    elif quality == "22":
        quality_string = "720p"
    elif quality == "137":
        quality_string = "1080p"
    elif quality == "249":
        quality_string = "50kbps"
    elif quality == "250":
        quality_string = "70kbps"
    elif quality == "140":
        quality_string = "128kbps"
    elif quality == "251":
        quality_string = "160kbps"

    # Return to normal state in root
    whenError()

    # Video form creating
    newWindow = customtkinter.CTkToplevel() # Toplevel object which will be treated as a new window
    newWindow.title("Video Downloader")
    width = 700
    height = 460
    x = (newWindow.winfo_screenwidth() // 2) - (width // 2)
    y = (newWindow.winfo_screenheight() // 2) - (height // 2)
    newWindow.geometry(f"{width}x{height}+{x}+{y}")
    newWindow.maxsize(700, 460)
    newWindow.minsize(700, 460)
    newWindow.iconbitmap("YDICO.ico")
    newWindow.protocol("WM_DELETE_WINDOW", onClosing)
    root.withdraw()

    # Downloading label
    downloading_var = StringVar()
    customtkinter.CTkLabel(newWindow, textvariable = downloading_var, font = ("arial", 25)).place(x = 265 , y = 418)
    global converting_var
    converting_var = StringVar()
    customtkinter.CTkLabel(newWindow, textvariable = converting_var, font = ("arial", 25)).place(x = 415 , y = 420)

    # Video labels
    customtkinter.CTkLabel(newWindow, text = "", image = photo).pack()
    customtkinter.CTkLabel(newWindow, text = "Video Title:", font = ("arial bold", 20)).place(x = 20 , y = 165)
    customtkinter.CTkLabel(newWindow, text = r.repr(url.title), font = ("arial", 20)).place(x = 132 , y = 165)
    customtkinter.CTkLabel(newWindow, text = "Channel:", font = ("arial bold", 20)).place(x = 20 , y = 195)
    customtkinter.CTkLabel(newWindow, text = r.repr(url.author), font = ("arial", 20)).place(x = 108 , y = 195)
    customtkinter.CTkLabel(newWindow, text = "Publish Date:", font = ("arial bold", 20)).place(x = 20 , y = 225)
    customtkinter.CTkLabel(newWindow, text = url.publish_date.strftime(date_format), font = ("arial", 20)).place(x = 152 , y = 225)
    customtkinter.CTkLabel(newWindow, text = "Length:", font = ("arial bold", 20)).place(x = 20 , y = 255)
    customtkinter.CTkLabel(newWindow, text = to_hms(url.length), font = ("arial", 20)).place(x = 97 , y = 255)
    customtkinter.CTkLabel(newWindow, text = "Quality:", font = ("arial bold", 20)).place(x = 20 , y = 285)
    customtkinter.CTkLabel(newWindow, text = quality_string, font = ("arial", 20)).place(x = 97 , y = 285)
    customtkinter.CTkLabel(newWindow, text = "File Size:", font = ("arial bold", 20)).place(x = 20 , y = 315)
    customtkinter.CTkLabel(newWindow, text = size_string, font = ("arial", 20)).place(x = 112 , y = 315)

    # Path change
    customtkinter.CTkLabel(newWindow, text = "Download Path:", font = ("arial bold", 20)).place(x = 20 , y = 345)
    path_var = StringVar()
    customtkinter.CTkEntry(newWindow, width = 245, textvariable = path_var, state = "disabled", height = 26).place(x = 175 , y = 347)
    try:
        path_var.set(directory2)
    except NameError:
        path_var.set(directory)
    path_button = customtkinter.CTkButton(newWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", hover_color = "gray25", width = 5, height = 26, command = BrowseDir)
    path_button.place(x = 430 , y = 347)

    # Subtitle Combobox
    customtkinter.CTkLabel(newWindow, text = "Subtitle:", font = ("arial bold", 20)).place(x = 340 , y = 315)
    lang_choose = customtkinter.CTkComboBox(newWindow, width = 100, height = 26, values = ["None", "Arabic", "English"], state = lang_choose_state)
    lang_choose.set("None")
    lang_choose.place(x = 425 , y = 315)

    # Progress bar/labels
    percentage_var = StringVar()
    sizeprogress_var = StringVar()
    progress_label = customtkinter.CTkLabel(newWindow, textvariable = percentage_var, font = ("arial", 22))
    progress_label.place(x = 540 , y = 384)
    progress_size_label = customtkinter.CTkLabel(newWindow, textvariable = sizeprogress_var, font = ("arial", 22))
    progress_size_label.place(x = 624 , y = 384)
    percentage_var.set("0.00%")
    sizeprogress_var.set("0 MB")
    progressbar = customtkinter.CTkProgressBar(newWindow, width = 505, mode = "indeterminate")
    progressbar.place(x = 20 , y = 393)

    # Pause/Resume & Cancel buttons
    toggle_button = customtkinter.CTkButton(newWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
    toggle_button.place(x = 550 , y = 347)
    cancel_button = customtkinter.CTkButton(newWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled")
    cancel_button.place(x = 595 , y = 347)

    # Back to home button
    back_button = customtkinter.CTkButton(newWindow, text = "Back To Home", font = ("arial bold", 20), command = backHome)
    back_button.place(x = 20 , y = 420)

    # Download button
    download_button = customtkinter.CTkButton(newWindow, text = "Download", font = ("arial bold", 25), command = VideoStart)
    download_button.place(x = 540 , y = 306)


# Playlist window
def PlaylistWindow():
    # Starting
    def pVideoStart():
        threading.Thread(target = Downloading).start()
        threading.Thread(target = PlaylistDownloader).start()

    # Back home
    def backHome():
        download = downloading_var.get()
        non_downloading_list = ["", "Finished", "Canceled"]
        if download in non_downloading_list:
            pass
        else:
            msg_box = messagebox.askquestion(title = "Cancel Download",
            message = "Going back to home will cancel the current download.\n\nDo you wish to continue?",
            icon = "warning")
            if msg_box == "yes": pass
            else: return
        pWindow.destroy()
        root.deiconify()

    # Set path
    user = getpass.getuser()
    path = f"C:/Users\{user}\Downloads"
    global directory
    directory = os.path.realpath(path) # Deafult path in case the user didn't choose
    def pBrowseDir(): # Path function
        global directory2
        directory2 = filedialog.askdirectory()
        ppath_var.set(directory2)

    # Captions download
    def pCaptionsDownload():
        for vid_link in vids_subs:
            url = YouTube(vid_link)
            video = url.streams.get_by_itag(quality)
            if f"✔️ {p.repr(clean_filename(url.title))} | {to_hms(url.length)} | {round(video.filesize/1024/1024, 2)} MB" in vids_list:
                lang = lang_choose.get()
                video_id = extract.video_id(vid_link)
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                if lang.lower() == "none":
                    return
                elif lang.lower() == "arabic":
                    lang = "ar"
                elif lang.lower() == "english":
                    for transcript in transcript_list:
                        if transcript.language_code == "en-US":
                            lang = "en-US"
                            break
                        elif transcript.language_code == "en-UK":
                            lang = "en-UK"
                            break
                        else:
                            lang = "en"
                else:
                    progressbar.stop()
                    toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
                    toggle_button.place(x = 550 , y = 347)
                    cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled")
                    cancel_button.place(x = 595 , y = 347)
                    download_button = customtkinter.CTkButton(pWindow, text = "Download", font = ("arial bold", 25), command = pVideoStart)
                    download_button.place(x = 540 , y = 306)
                    path_button = customtkinter.CTkButton(pWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", hover_color = "gray25", width = 5, command = pBrowseDir)
                    path_button.place(x = 430 , y = 347)
                    lang_choose.configure(state = "normal")
                    menubutton.configure(state = "normal")
                    downloadcounter_var.set("")
                    downloading_var.set("")
                    messagebox.showerror(title = "Subtitle Not Supported", message = "Please choose a supported language.")
                    return False
                downloadcounter_var.set("Subtitle Download")
                try: # Get the subtitle directly if it's there
                    final = YouTubeTranscriptApi.get_transcript(video_id = video_id, languages = [lang])
                    print("got one already there")
                    sub = "subtitle"
                except: # If not then translate it
                    translated = "no"
                    en_list = ["en", "en-US","en-UK"]
                    for transcript in transcript_list:
                        if transcript.language_code in en_list: # Translate from English if it's there
                            final = transcript.translate(lang).fetch()
                            print(f"translated from {transcript.language_code}")
                            sub = "translated_subtitle"
                            translated = "yes"
                        if translated == "no": # Avoid translating twice
                            final = transcript.translate(lang).fetch()
                            print(f"translated {transcript.language_code}")
                            sub = "translated_subtitle"
                            translated = "yes"
                        else:
                            pass
                formatter = SRTFormatter()
                srt_formatted = formatter.format_transcript(final)
                try:
                    with open(f"{directory2}/{clean_filename(url.title)}_{sub}_{lang}.srt", "w", encoding = "utf-8") as srt_file:
                        srt_file.write(srt_formatted)
                except NameError:
                    with open(f"{directory}/{clean_filename(url.title)}_{sub}_{lang}.srt", "w", encoding = "utf-8") as srt_file:
                        srt_file.write(srt_formatted)
            else:
                print(f"{url.title} not in list")

    # Add/Remove videos from download list
    def videoSelector(choice):
        global vids_counter, psize, plength
        if choice.startswith("✔️ "): # Remove from list
            vids_list.remove(choice)
            choice = choice.replace("✔️ ","")
            vids_list.append(choice)
            vids_counter = vids_counter - 1

            choice_list = choice.split(" | ")
            time = choice_list[1].split(":")
            h = int(time[0]) * 60 * 60
            m = int(time[1]) * 60
            s = int(time[2])
            seconds = h + m + s
            plength = plength - seconds
            size_float = choice_list[2]
            size_float = size_float.replace(" MB", "")
            size_float = round(float(size_float)*1024*1024, 2)
            psize = psize - size_float

        else: # Add to list
            vids_list.remove(choice)
            choice = "✔️ " + choice
            vids_list.append(choice)
            vids_counter = vids_counter + 1

            choice_list = choice.split(" | ")
            time = choice_list[1].split(":")
            h = int(time[0]) * 60 * 60
            m = int(time[1]) * 60
            s = int(time[2])
            seconds = h + m + s
            plength = plength + seconds
            size_float = choice_list[2]
            size_float = size_float.replace(" MB", "")
            size_float = round(float(size_float)*1024*1024, 2)
            psize = psize + size_float

        print("==================")
        print(vids_list)
        print(vids_counter)
        menubutton.configure(values = vids_list)
        menubutton.set("Open Videos Menu")
        length_var.set(to_hms(plength))
        size_var.set(f"{round(psize/1024/1024, 2)} MB")
        videos_var.set(vids_counter)

    # Pause/Resume function
    def toggle_download():
        global is_paused
        is_paused = not is_paused
        if is_paused:
            progressbar.stop()
            toggle_button = customtkinter.CTkButton(pWindow, text = "▶️", font = ("arial", 15), fg_color = "grey14", hover_color = "gray10", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
            toggle_button.place(x = 550 , y = 347)
            downloading_var.set("Paused")
        else:
            progressbar.start()
            toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
            toggle_button.place(x = 550 , y = 347)
            downloading_var.set("Downloading")

    # Cancel function
    def cancel_download():
        global is_cancelled
        is_cancelled = True

    # Open folder in file explorer when download is finished
    def openFile():
        try:
            dir2 = os.path.normpath(directory2)
            subprocess.Popen(f'explorer "{dir2}"')
        except NameError:
            subprocess.Popen(f'explorer "{directory}"')

    # Downloading label function
    def Downloading():
        downloading_var.set("Downloading")
        time.sleep(0.5)
        while True:
            if downloading_var.get() == "Downloading":
                downloading_var.set("Downloading.")
                time.sleep(0.5)
            else: break
            if downloading_var.get() == "Downloading.":
                downloading_var.set("Downloading..")
                time.sleep(0.5)
            else: break
            if downloading_var.get() == "Downloading..":
                downloading_var.set("Downloading...")
                time.sleep(0.5)
            else: break
            if downloading_var.get() == "Downloading...":
                downloading_var.set("Downloading")
                time.sleep(0.5)
            else: break
        dont_change = ["Canceled", "Paused", "Finished"]
        while True:
            time.sleep(1)
            if downloading_var.get() in dont_change:
                continue
            else:
                Downloading()

    # Download playlist
    def PlaylistDownloader():
        # Preperations
        global is_paused, is_cancelled
        is_paused = is_cancelled = False
        toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
        toggle_button.place(x = 550 , y = 347)
        cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, command = cancel_download)
        cancel_button.place(x = 595 , y = 347)
        download_button = customtkinter.CTkButton(pWindow, text = "Download", font = ("arial bold", 25), state = "disabled")
        download_button.place(x = 540 , y = 306)
        path_button = customtkinter.CTkButton(pWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", width = 5, state = "disabled")
        path_button.place(x = 430 , y = 347)
        lang_choose.configure(state = "disabled")
        menubutton.configure(state = "disabled")
        audio_tags_list = ["251" , "140" , "250" , "249"]
        # Download subtitles if selected
        if caps == "yes":
            if pCaptionsDownload() == False: return
        else: pass
        # Progress stuff
        pytube.request.default_range_size = 2097152  # 2MB chunk size (update progress every 2MB)
        progressbar.start()
        progress_label.configure(text_color = "green")
        progress_size_label.configure(text_color = "LightBlue")

        # Download playlist
        if vids_counter == 0:
            progressbar.stop()
            toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
            toggle_button.place(x = 550 , y = 347)
            cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled")
            cancel_button.place(x = 595 , y = 347)
            download_button = customtkinter.CTkButton(pWindow, text = "Download", font = ("arial bold", 25), command = pVideoStart)
            download_button.place(x = 540 , y = 306)
            path_button = customtkinter.CTkButton(pWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", hover_color = "gray25", width = 5, command = pBrowseDir)
            path_button.place(x = 430 , y = 347)
            lang_choose.configure(state = "normal")
            menubutton.configure(state = "normal")
            downloading_var.set("")
            return messagebox.showerror(title = "No Selected Video", message = "Please select at least one video.")
        downloaded_counter = 0
        downloadcounter_var.set(f"{downloaded_counter}/{vids_counter} Downloaded")
        for url in urls.videos:
            if is_cancelled: break
            video = url.streams.get_by_itag(quality)
            if f"✔️ {p.repr(clean_filename(url.title))} | {to_hms(url.length)} | {round(video.filesize/1024/1024, 2)} MB" in vids_list: pass
            else: continue
            if quality in audio_tags_list: ext = "mp3"
            else: ext = "mp4"
            video = url.streams.get_by_itag(quality)
            size = video.filesize
            try: vname = f"{directory2}/{clean_filename(url.title)}_({quality_string}).{ext}"
            except NameError: vname = f"{directory}/{clean_filename(url.title)}_({quality_string}).{ext}"
            raw_data = urllib.request.urlopen(url.thumbnail_url).read()
            photo = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (270 , 150))
            customtkinter.CTkLabel(pWindow, text = "", image = photo).place(x = 220 , y = 0)
            with open(vname, "wb") as f:
                video = request.stream(video.url) # Get an iterable stream
                downloaded = 0
                while True:
                    if is_cancelled:
                        downloading_var.set("Canceled")
                        progressbar.stop()
                        toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
                        toggle_button.place(x = 550 , y = 347)
                        cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled")
                        cancel_button.place(x = 595 , y = 347)
                        break
                    if is_paused:
                        time.sleep(0.5)
                        continue
                    try: chunk = next(video, None) # Get next chunk of video
                    except: return messagebox.showerror(title = "Something Went Wrong", message = "Something went wrong, please try again.")
                    if chunk:
                        f.write(chunk) # Download the chunk into the file
                        # Update Progress
                        downloaded += len(chunk)
                        remaining = size - downloaded
                        bytes_downloaded = size - remaining
                        percentage_of_completion = bytes_downloaded / size * 100
                        percentage_var.set(f"{round(percentage_of_completion, 2)}%  ")
                        sizeprogress_var.set(f"{int(bytes_downloaded / 1024 / 1024)} MB  ")
                    else:
                        downloaded_counter = downloaded_counter + 1
                        downloadcounter_var.set(f"{downloaded_counter}/{vids_counter} Downloaded")
                        break # No more data = Finished

        # When finished
        progressbar.stop()
        toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
        toggle_button.place(x = 550 , y = 347)
        cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled")
        cancel_button.place(x = 595 , y = 347)
        if is_cancelled:
            msg_box = messagebox.askquestion(title = "Delete Canceled File", message = f"Do you want to delete '{vname}'?")
            if msg_box == "yes": os.remove(vname)
        else:
            downloadcounter_var.set("")
            pWindow.bell()
            downloading_var.set("Finished")
            customtkinter.CTkButton(pWindow, text = "Open File in Explorer", font = ("arial bold", 20), command = openFile).place(x = 470 , y = 420)


    # Get playlist info, get link and check errors
    video_button = customtkinter.CTkButton(root, textvariable = loading_var, width = 235, font = ("arial bold", 25), state = "disabled")
    video_button.place(x = 305 , y = 205)
    themes_menu.configure(state = "disabled")
    try:
        urls = Playlist(link)
        quality = str(quality_var.get())
        if not "youtu" in link or not "playlist" in link: raise KeyError()
    except KeyError:
        whenError()
        return messagebox.showerror(title = "Link Not Valid", message = "Please enter a valid playlist link.")
    if quality != "0":
        not_supported_list = ["137" , "135" , "250" , "249" , "133" , "160"]
        if quality in not_supported_list:
            whenError()
            return messagebox.showerror(title = "Not Supported", message = "Currently, we support downloading playlists in 720p, 360p, 160kbps and 128kbps only.")
        else:
            global vids_counter, psize, plength
            vids_list = []
            plength = 0
            psize = 0
            vids_counter = 0
            vids_subs = []
            pl_tst_counter = 0
            for url in urls.videos:
                pl_tst_counter = pl_tst_counter + 1
                print(f"================================")
                print(f"({pl_tst_counter}) loop started")
                try:
                    video = url.streams.get_by_itag(quality)
                    print(f"({pl_tst_counter}) got video item")
                except urllib.error.URLError:
                    print(e)
                    whenError()
                    return messagebox.showerror(title = "Not Connected", message = "Please check your internet connection.")
                except pytube.exceptions.LiveStreamError as e:
                    print(e)
                    whenError()
                    return messagebox.showerror(title = "Video is Live", message = "Can't download a live video.")
                try:
                    video_id = extract.video_id(url.watch_url)
                    YouTubeTranscriptApi.list_transcripts(video_id)
                    vids_subs.append(url.watch_url)
                    print(f"({pl_tst_counter}) found subtitle")
                except:
                    print(f"({pl_tst_counter}) no subtitle")
                    pass
                try:
                    size = video.filesize
                except KeyError:
                    whenError()
                    return messagebox.showerror(title = "Something Went Wrong", message = "Something went wrong, please try again.")
                p = reprlib.Repr()
                p.maxstring = 40    # max characters displayed for strings
                psize = psize + size
                print(f"({pl_tst_counter}) got size")
                size_string = round(psize/1024/1024, 2)
                print(f"({pl_tst_counter}) got size string")
                plength = plength + url.length
                print(f"({pl_tst_counter}) got length")
                vid_option = f"✔️ {p.repr(clean_filename(url.title))} | {to_hms(url.length)} | {round(video.filesize/1024/1024, 2)} MB"
                print(f"({pl_tst_counter}) got vid_option")
                vids_list.append(vid_option)
                print(f"({pl_tst_counter}) added vid_option to list")
                vids_counter = vids_counter + 1
                ploading_counter_var.set(f"({vids_counter})")
    else:
        whenError()
        return messagebox.showerror(title = "Link Not Valid", message = "Please select a format to download.")

    # Getting playlist thumbnail
    raw_data = urllib.request.urlopen(url.thumbnail_url).read()
    photo = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (270 , 150))

    # Playlist labels info
    r = reprlib.Repr()
    r.maxstring = 60    # max characters displayed for strings
    date_format = "%d/%m/%Y"
    if quality == "144":
        quality_string = "144p"
    elif quality == "240":
        quality_string = "240p"
    elif quality == "18":
        quality_string = "360p"
    elif quality == "135":
        quality_string = "480p"
    elif quality == "22":
        quality_string = "720p"
    elif quality == "137":
        quality_string = "1080p"
    elif quality == "249":
        quality_string = "50kbps"
    elif quality == "250":
        quality_string = "70kbps"
    elif quality == "140":
        quality_string = "128kbps"
    elif quality == "251":
        quality_string = "160kbps"

    # Return to normal state in root
    whenError()

    # Playlist form creating
    pWindow = customtkinter.CTkToplevel() # Toplevel object which will be treated as a new window
    pWindow.title("Playlist Downloader")
    width = 700
    height = 460
    x = (pWindow.winfo_screenwidth() // 2) - (width // 2)
    y = (pWindow.winfo_screenheight() // 2) - (height // 2)
    pWindow.geometry(f"{width}x{height}+{x}+{y}")
    pWindow.maxsize(700, 460)
    pWindow.minsize(700, 460)
    pWindow.iconbitmap("YDICO.ico")
    pWindow.protocol("WM_DELETE_WINDOW", onClosing)
    root.withdraw()

    # Downloading label
    downloading_var = StringVar()
    customtkinter.CTkLabel(pWindow, textvariable = downloading_var, font = ("arial", 25)).place(x = 265 , y = 418)
    downloadcounter_var = StringVar()
    customtkinter.CTkLabel(pWindow, textvariable = downloadcounter_var, font = ("arial", 25)).place(x = 460 , y = 418)

    # Playlist labels
    length_var = StringVar()
    length_var.set(to_hms(plength))
    size_var = StringVar()
    size_var.set(f"{size_string} MB")
    videos_var = IntVar()
    videos_var.set(vids_counter)
    customtkinter.CTkLabel(pWindow, text = "", image = photo).place(x = 220 , y = 0)
    customtkinter.CTkLabel(pWindow, text = "Playlist Title:", font = ("arial bold", 20)).place(x = 20 , y = 165)
    customtkinter.CTkLabel(pWindow, text = r.repr(urls.title), font = ("arial", 20)).place(x = 148 , y = 165)
    customtkinter.CTkLabel(pWindow, text = "Channel:", font = ("arial bold", 20)).place(x = 20 , y = 195)
    customtkinter.CTkLabel(pWindow, text = r.repr(url.author), font = ("arial", 20)).place(x = 108 , y = 195)
    customtkinter.CTkLabel(pWindow, text = "Publish Date:", font = ("arial bold", 20)).place(x = 20 , y = 225)
    customtkinter.CTkLabel(pWindow, text = url.publish_date.strftime(date_format), font = ("arial", 20)).place(x = 152 , y = 225)
    customtkinter.CTkLabel(pWindow, text = "Total Length:", font = ("arial bold", 20)).place(x = 20 , y = 255)
    customtkinter.CTkLabel(pWindow, textvariable = length_var, font = ("arial", 20)).place(x = 149 , y = 255)
    customtkinter.CTkLabel(pWindow, text = "Quality:", font = ("arial bold", 20)).place(x = 20 , y = 285)
    customtkinter.CTkLabel(pWindow, text = quality_string, font = ("arial", 20)).place(x = 97 , y = 285)
    customtkinter.CTkLabel(pWindow, text = "Total Size:", font = ("arial bold", 20)).place(x = 20 , y = 315)
    customtkinter.CTkLabel(pWindow, textvariable = size_var, font = ("arial", 20)).place(x = 126 , y = 315)
    customtkinter.CTkLabel(pWindow, text = "Total Videos:", font = ("arial bold", 20)).place(x = 340 , y = 285)
    customtkinter.CTkLabel(pWindow, textvariable = videos_var, font = ("arial", 20)).place(x = 470 , y = 285)

    # Path change
    customtkinter.CTkLabel(pWindow, text = "Download Path:", font = ("arial bold", 20)).place(x = 20 , y = 345)
    ppath_var = StringVar()
    customtkinter.CTkEntry(pWindow, width = 245, height = 26, textvariable = ppath_var, state = "disabled").place(x = 175 , y = 347)
    try:
        ppath_var.set(directory2)
    except NameError:
        ppath_var.set(directory)
    path_button = customtkinter.CTkButton(pWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", hover_color = "gray25", width = 5, height = 26, command = pBrowseDir)
    path_button.place(x = 430 , y = 347)

    # Subtitle Combobox
    if vids_subs == []:
        lang_choose_state = "disabled"
        caps = "no"
    else:
        lang_choose_state = "normal"
        caps = "yes"
    print(vids_subs)
    customtkinter.CTkLabel(pWindow, text = "Subtitle:", font = ("arial bold", 20)).place(x = 340 , y = 315)
    lang_choose = customtkinter.CTkComboBox(pWindow, width = 100, height = 26, values = ["None", "Arabic", "English"], state = lang_choose_state)
    lang_choose.set("None")
    lang_choose.place(x = 425 , y = 315)

    # Video selector
    menubutton = customtkinter.CTkOptionMenu(pWindow, font = ("arial", 14), values = vids_list, command = videoSelector)
    menubutton.set("Open Videos Menu")
    menubutton.place(x = 531 , y = 270)

    # Progress bar/labels
    percentage_var = StringVar()
    sizeprogress_var = StringVar()
    progress_label = customtkinter.CTkLabel(pWindow, textvariable = percentage_var, font = ("arial", 22))
    progress_label.place(x = 540 , y = 384)
    progress_size_label = customtkinter.CTkLabel(pWindow, textvariable = sizeprogress_var, font = ("arial", 22))
    progress_size_label.place(x = 624 , y = 384)
    percentage_var.set("0.00%")
    sizeprogress_var.set("0 MB")
    progressbar = customtkinter.CTkProgressBar(pWindow, width = 505, mode = "indeterminate")
    progressbar.place(x = 20 , y = 395)

    # Pause/Resume & Cancel buttons
    toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
    toggle_button.place(x = 550 , y = 347)
    cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled")
    cancel_button.place(x = 595 , y = 347)

    # Download button
    download_button = customtkinter.CTkButton(pWindow, text = "Download", font = ("arial bold", 25), command = pVideoStart)
    download_button.place(x = 540 , y = 306)

    # Back to home button
    back_button = customtkinter.CTkButton(pWindow, text = "Back To Home", font = ("arial bold", 20), command = backHome)
    back_button.place(x = 20 , y = 420)

# Search window
def SearchWindow():
    # For length format
    def to_hms(s):
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return "{}:{:0>2}:{:0>2}".format(h, m, s)
    # Disable root
    video_button = customtkinter.CTkButton(root, textvariable = loading_var, width = 235, font = ("arial bold", 25), state = "disabled")
    video_button.place(x = 305 , y = 205)
    themes_menu.configure(state = "disabled")
    # Window creating
    search_text = link
    if search_text == "":
        whenError()
        return messagebox.showerror(title = "Entry is Empty", message = "Please type something.")
    elif len(search_text) < 3:
        whenError()
        return messagebox.showerror(title = "Characters Not Enough", message = "Please type at least 3 characters.")
    quality = str(quality_var.get())
    if quality == "0":
        whenError()
        return messagebox.showerror(title = "Format Not Selected", message = "Please select a format.")
    not_supported_list = ["137" , "135" , "250" , "249" , "133" , "160"]
    if quality in not_supported_list:
        whenError()
        return messagebox.showerror(title = "Not Supported", message = "Currently, we support searching youtube in 720p, 360p, 160kbps and 128kbps only.")
    sWindow = customtkinter.CTkToplevel()
    sWindow.title(f'Search Results For "{search_text}"')
    sWindow.withdraw()
    # On closing
    def onClosing():
        msg_box = messagebox.askquestion(title = "Back To Home",
        message = "You will return back to home. This will delete all your selections.\n\n Do you wish to continue?",
        icon = "warning")
        if msg_box == "yes":
            sWindow.destroy()
            root.deiconify()
    width = 700
    height = 460
    x = (sWindow.winfo_screenwidth() // 2) - (width // 2)
    y = (sWindow.winfo_screenheight() // 2) - (height // 2)
    sWindow.geometry(f"{width}x{height}+{x}+{y}")
    sWindow.maxsize(700, 460)
    sWindow.minsize(700, 460)
    sWindow.iconbitmap("YDICO.ico")
    sWindow.withdraw()
    sWindow.protocol("WM_DELETE_WINDOW", onClosing)
    global to_download
    to_download = []
    def checkboxes():
        global to_download
        if cb_var1.get() == 1:
            if search.results[0] not in to_download:
                to_download.append(search.results[0])
        else:
            if search.results[0] in to_download:
                to_download.remove(search.results[0])
        if cb_var2.get() == 1:
            if search.results[1] not in to_download:
                to_download.append(search.results[1])
        else:
            if search.results[1] in to_download:
                to_download.remove(search.results[1])
        if cb_var3.get() == 1:
            if search.results[2] not in to_download:
                to_download.append(search.results[2])
        else:
            if search.results[2] in to_download:
                to_download.remove(search.results[2])
        if cb_var4.get() == 1:
            if search.results[3] not in to_download:
                to_download.append(search.results[3])
        else:
            if search.results[3] in to_download:
                to_download.remove(search.results[3])

        if cb_var5.get() == 1:
            if search.results[4] not in to_download:
                to_download.append(search.results[4])
        else:
            if search.results[4] in to_download:
                to_download.remove(search.results[4])
        if cb_var6.get() == 1:
            if search.results[5] not in to_download:
                to_download.append(search.results[5])
        else:
            if search.results[5] in to_download:
                to_download.remove(search.results[5])
        if cb_var7.get() == 1:
            if search.results[6] not in to_download:
                to_download.append(search.results[6])
        else:
            if search.results[6] in to_download:
                to_download.remove(search.results[6])
        if cb_var8.get() == 1:
            if search.results[7] not in to_download:
                to_download.append(search.results[7])
        else:
            if search.results[7] in to_download:
                to_download.remove(search.results[7])

        if cb_var9.get() == 1:
            if search.results[8] not in to_download:
                to_download.append(search.results[8])
        else:
            if search.results[8] in to_download:
                to_download.remove(search.results[8])
        if cb_var10.get() == 1:
            if search.results[9] not in to_download:
                to_download.append(search.results[9])
        else:
            if search.results[9] in to_download:
                to_download.remove(search.results[9])
        if cb_var11.get() == 1:
            if search.results[10] not in to_download:
                to_download.append(search.results[10])
        else:
            if search.results[10] in to_download:
                to_download.remove(search.results[10])
        if cb_var12.get() == 1:
            if search.results[11] not in to_download:
                to_download.append(search.results[11])
        else:
            if search.results[11] in to_download:
                to_download.remove(search.results[11])

        if cb_var13.get() == 1:
            if search.results[12] not in to_download:
                to_download.append(search.results[12])
        else:
            if search.results[12] in to_download:
                to_download.remove(search.results[12])
        if cb_var14.get() == 1:
            if search.results[13] not in to_download:
                to_download.append(search.results[13])
        else:
            if search.results[13] in to_download:
                to_download.remove(search.results[13])
        if cb_var15.get() == 1:
            if search.results[14] not in to_download:
                to_download.append(search.results[14])
        else:
            if search.results[14] in to_download:
                to_download.remove(search.results[14])
        if cb_var16.get() == 1:
            if search.results[15] not in to_download:
                to_download.append(search.results[15])
        else:
            if search.results[15] in to_download:
                to_download.remove(search.results[15])

        selected_counter.set(f"{len(to_download)} Selected")
        print("==========")
        print(to_download)
        print(len(to_download))

    #Checkboxes variables
    cb_var1 = IntVar()
    cb_var2 = IntVar()
    cb_var3 = IntVar()
    cb_var4 = IntVar()
    cb_var5 = IntVar()
    cb_var6 = IntVar()
    cb_var7 = IntVar()
    cb_var8 = IntVar()
    cb_var9 = IntVar()
    cb_var10 = IntVar()
    cb_var11 = IntVar()
    cb_var12 = IntVar()
    cb_var13 = IntVar()
    cb_var14 = IntVar()
    cb_var15 = IntVar()
    cb_var16 = IntVar()

    # Open in Youtube buttons
    def openYouTube1():
        if results_counter == 4: webbrowser.open(search.results[0].watch_url, new=1)
        if results_counter == 8: webbrowser.open(search.results[4].watch_url, new=1)
        if results_counter == 12: webbrowser.open(search.results[8].watch_url, new=1)
        if results_counter == 16: webbrowser.open(search.results[12].watch_url, new=1)
    def openYouTube2():
        if results_counter == 4: webbrowser.open(search.results[1].watch_url, new=1)
        if results_counter == 8: webbrowser.open(search.results[5].watch_url, new=1)
        if results_counter == 12: webbrowser.open(search.results[9].watch_url, new=1)
        if results_counter == 16: webbrowser.open(search.results[13].watch_url, new=1)
    def openYouTube3():
        if results_counter == 4: webbrowser.open(search.results[2].watch_url, new=1)
        if results_counter == 8: webbrowser.open(search.results[6].watch_url, new=1)
        if results_counter == 12: webbrowser.open(search.results[10].watch_url, new=1)
        if results_counter == 16: webbrowser.open(search.results[14].watch_url, new=1)
    def openYouTube4():
        if results_counter == 4: webbrowser.open(search.results[3].watch_url, new=1)
        if results_counter == 8: webbrowser.open(search.results[7].watch_url, new=1)
        if results_counter == 12: webbrowser.open(search.results[11].watch_url, new=1)
        if results_counter == 16: webbrowser.open(search.results[15].watch_url, new=1)

    # First video
    cb1 = customtkinter.CTkCheckBox(sWindow, text = "", variable = cb_var1, command = checkboxes)
    cb1.place(x = 30, y = 40)
    t1 = customtkinter.CTkLabel(sWindow, text = "Not Available", font = ("arial bold", 20))
    t1.place(x = 250, y = 15)
    a1 = customtkinter.CTkLabel(sWindow, text = "Not Available", font = ("arial", 15))
    a1.place(x = 255, y = 40)
    s1 = customtkinter.CTkLabel(sWindow, text = "0.00 MB", font = ("arial", 12))
    s1.place(x = 260, y = 65)
    l1 = customtkinter.CTkLabel(sWindow, text = "0:00:00", font = ("arial", 12))
    l1.place(x = 320, y = 65)
    b1 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube1)
    b1.place(x = 375, y = 63)

    # Second video
    cb2 = customtkinter.CTkCheckBox(sWindow, text = "", variable = cb_var2, command = checkboxes)
    cb2.place(x = 30, y = 140)
    t2 = customtkinter.CTkLabel(sWindow, text = "Not Available", font = ("arial bold", 20))
    t2.place(x = 250, y = 115)
    a2 = customtkinter.CTkLabel(sWindow, text = "Not Available", font = ("arial", 15))
    a2.place(x = 255, y = 140)
    s2 = customtkinter.CTkLabel(sWindow, text = "0.00 MB", font = ("arial", 12))
    s2.place(x = 260, y = 165)
    l2 = customtkinter.CTkLabel(sWindow, text = "0:00:00", font = ("arial", 12))
    l2.place(x = 320, y = 165)
    b2 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube2)
    b2.place(x = 375, y = 163)

    # Third video
    cb3 = customtkinter.CTkCheckBox(sWindow, text = "", variable = cb_var3, command = checkboxes)
    cb3.place(x = 30, y = 240)
    t3 = customtkinter.CTkLabel(sWindow, text = "Not Available", font = ("arial bold", 20))
    t3.place(x = 250, y = 215)
    a3 = customtkinter.CTkLabel(sWindow, text = "Not Available", font = ("arial", 15))
    a3.place(x = 255, y = 240)
    s3 = customtkinter.CTkLabel(sWindow, text = "0.00 MB", font = ("arial", 12))
    s3.place(x = 260, y = 265)
    l3 = customtkinter.CTkLabel(sWindow, text = "0:00:00", font = ("arial", 12))
    l3.place(x = 320, y = 265)
    b3 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube3)
    b3.place(x = 375, y = 263)

    # Fourth video
    cb4 = customtkinter.CTkCheckBox(sWindow, text = "", variable = cb_var4, command = checkboxes)
    cb4.place(x = 30, y = 340)
    t4 = customtkinter.CTkLabel(sWindow, text = "Not Available", font = ("arial bold", 20))
    t4.place(x = 250, y = 315)
    a4 = customtkinter.CTkLabel(sWindow, text = "Not Available", font = ("arial", 15))
    a4.place(x = 255, y = 340)
    s4 = customtkinter.CTkLabel(sWindow, text = "0.00 MB", font = ("arial", 12))
    s4.place(x = 260, y = 365)
    l4 = customtkinter.CTkLabel(sWindow, text = "0:00:00", font = ("arial", 12))
    l4.place(x = 320, y = 365)
    b4 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube4)
    b4.place(x = 375, y = 363)

    # Loading
    def Loading(button_var):
        # Disabled widgets
        cb1.configure(state = "disabled")
        cb2.configure(state = "disabled")
        cb3.configure(state = "disabled")
        cb4.configure(state = "disabled")
        b1 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", width = 0, state = "disabled")
        b1.place(x = 375, y = 63)
        b2 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", width = 0, state = "disabled")
        b2.place(x = 375, y = 163)
        b3 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", width = 0, state = "disabled")
        b3.place(x = 375, y = 263)
        b4 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", width = 0, state = "disabled")
        b4.place(x = 375, y = 363)
        pr_button.configure(state = "disabled")
        dn_button.configure(state = "disabled")
        nr_button.configure(state = "disabled")
        # Loading label
        button_var.set("Loading")
        time.sleep(0.5)
        while True:
            if button_var.get() == "Loading":
                button_var.set("Loading.")
                time.sleep(0.5)
            else: break
            if button_var.get() == "Loading.":
                button_var.set("Loading..")
                time.sleep(0.5)
            else: break
            if button_var.get() == "Loading..":
                button_var.set("Loading...")
                time.sleep(0.5)
            else: break
            if button_var.get() == "Loading...":
                button_var.set("Loading")
                time.sleep(0.5)
            else: break

    # Return to normal
    def normalWidgets(results_counter, error):
        cb1.configure(state = "normal")
        cb2.configure(state = "normal")
        cb3.configure(state = "normal")
        cb4.configure(state = "normal")
        b1 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube1)
        b1.place(x = 375, y = 63)
        b2 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube2)
        b2.place(x = 375, y = 163)
        b3 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube3)
        b3.place(x = 375, y = 263)
        b4 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube4)
        b4.place(x = 375, y = 363)
        dn_button.configure(state = "normal")
        pr_button_var.set("Previous Results")
        nr_button_var.set("Next Results")
        if results_counter == 4:
            pr_button.configure(state = "disabled")
            nr_button.configure(state = "normal")
            page_counter.set("Page 1/4")
        elif results_counter == 8:
            pr_button.configure(state = "normal")
            nr_button.configure(state = "normal")
            page_counter.set("Page 2/4")
        elif results_counter == 12:
            pr_button.configure(state = "normal")
            nr_button.configure(state = "normal")
            page_counter.set("Page 3/4")
        elif results_counter == 16:
            pr_button.configure(state = "normal")
            nr_button.configure(state = "disabled")
            page_counter.set("Page 4/4")
        if error == "yes":
            nr_button.configure(state = "disabled")

    # When error happen while on a page
    def whenSearchError(counter):
        global results_counter
        results_counter = counter
        if results_counter == 4:
            whenError()
            sWindow.destroy()
        else:
            if results_counter == 8: results_counter = 4
            elif results_counter == 12: results_counter = 8
            elif results_counter == 16: results_counter = 12
            error = "yes"
            normalWidgets(results_counter, error)

    # On buttons click
    def onPrClick():
        button_var = pr_button_var
        threading.Thread(target=Loading, args = (button_var,)).start()
        threading.Thread(target=deresults).start()
    def onNrClick():
        button_var = nr_button_var
        threading.Thread(target=Loading, args = (button_var,)).start()
        threading.Thread(target=results).start()

    # Previous results
    def deresults():
        global results_counter
        if results_counter == 16: results_counter = 8
        elif results_counter == 12: results_counter = 4
        elif results_counter == 8: results_counter = 0
        results()

    # Search
    search = Search(search_text)
    try:
        print(len(search.results))
    except urllib.error.URLError:
        whenError()
        return messagebox.showerror(title = "Not Connected", message = "Please check your internet connection.")
    global results_counter
    results_counter = 0
    r = reprlib.Repr()
    r.maxstring = 40
    def results():
        global results_counter
        if results_counter == 0:
            limit = 4
            results_list = search.results[0:4]
        elif results_counter == 4:
            limit = 8
            results_list = search.results[4:8]
        elif results_counter == 8:
            limit = 12
            results_list = search.results[8:12]
        elif results_counter == 12:
            limit = 16
            results_list = search.results[12:16]
        print("====================================")
        print("====================================")
        for url in results_list:
            first = [0, 4, 8, 12]
            second = [1, 5, 9, 13]
            third = [2, 6, 10, 14]
            fourth = [3, 7, 11, 15]
            if results_counter == limit: break
            elif results_counter in first: url1 = url
            elif results_counter in second: url2 = url
            elif results_counter in third: url3 = url
            elif results_counter in fourth: url4 = url
            results_counter = results_counter + 1
            print(f"results_counter {results_counter}")

        print("====================")
        try:
            video1 = url1.streams.get_by_itag(quality)
            size1 = f"{round(video1.filesize/1024/1024, 2)} MB"
            ploading_counter_var.set("(1)")
            print("first done")
            video2 = url2.streams.get_by_itag(quality)
            size2 = f"{round(video2.filesize/1024/1024, 2)} MB"
            ploading_counter_var.set("(2)")
            print("second done")
            video3 = url3.streams.get_by_itag(quality)
            size3 = f"{round(video3.filesize/1024/1024, 2)} MB"
            ploading_counter_var.set("(3)")
            print("third done")
            video4 = url4.streams.get_by_itag(quality)
            size4 = f"{round(video4.filesize/1024/1024, 2)} MB"
            ploading_counter_var.set("(4)")
            print("fourth done")
        except urllib.error.URLError as e:
            whenSearchError(results_counter)
            return messagebox.showerror(title = "Not Connected", message = "Please check your internet connection.")
        except KeyError as e:
            print(f"KeyError: {e}")
            whenSearchError(results_counter)
            return messagebox.showerror(title = "Something Went Wrong", message = f"I can't retrieve results for '{search_text}' at the moment.")
        except AttributeError as e:
            print(f"AttributeError: {e}")
            whenSearchError(results_counter)
            return messagebox.showerror(title = "Something Went Wrong", message = f"I can't retrieve results for '{search_text}' at the moment.")
        except pytube.exceptions.LiveStreamError as e:
            print(f"LiveStreamError: {e}")
            whenSearchError(results_counter)
            return messagebox.showerror(title = "Video is Live", message = "Can't retrive a live video.")
        print("Done videos and sizes")

        # Configure checkboxes
        if results_counter == 4:
            cb1.configure(variable = cb_var1)
            cb2.configure(variable = cb_var2)
            cb3.configure(variable = cb_var3)
            cb4.configure(variable = cb_var4)
        elif results_counter == 8:
            cb1.configure(variable = cb_var5)
            cb2.configure(variable = cb_var6)
            cb3.configure(variable = cb_var7)
            cb4.configure(variable = cb_var8)
        elif results_counter == 12:
            cb1.configure(variable = cb_var9)
            cb2.configure(variable = cb_var10)
            cb3.configure(variable = cb_var11)
            cb4.configure(variable = cb_var12)
        elif results_counter == 16:
            cb1.configure(variable = cb_var13)
            cb2.configure(variable = cb_var14)
            cb3.configure(variable = cb_var15)
            cb4.configure(variable = cb_var16)

        # Configure first video in page
        t1.configure(text = r.repr(url1.title))
        a1.configure(text = r.repr(url1.author))
        l1.configure(text = to_hms(url1.length))
        s1.configure(text = size1)
        raw_data = urllib.request.urlopen(url1.thumbnail_url).read()
        photo = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (160 , 90))
        customtkinter.CTkLabel(sWindow, text = "", image = photo).place(x = 80, y = 10)

        # Configure second video in page
        t2.configure(text = r.repr(url2.title))
        a2.configure(text = r.repr(url2.author))
        l2.configure(text = to_hms(url2.length))
        s2.configure(text = size2)
        raw_data = urllib.request.urlopen(url2.thumbnail_url).read()
        photo = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (160 , 90))
        customtkinter.CTkLabel(sWindow, text = "", image = photo).place(x = 80, y = 110)

        # Configure third video in page
        t3.configure(text = r.repr(url3.title))
        a3.configure(text = r.repr(url3.author))
        l3.configure(text = to_hms(url3.length))
        s3.configure(text = size3)
        raw_data = urllib.request.urlopen(url3.thumbnail_url).read()
        photo = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (160 , 90))
        customtkinter.CTkLabel(sWindow, text = "", image = photo).place(x = 80, y = 210)

        # Configure fourth video in page
        t4.configure(text = r.repr(url4.title))
        a4.configure(text = r.repr(url4.author))
        l4.configure(text = to_hms(url4.length))
        s4.configure(text = size4)
        raw_data = urllib.request.urlopen(url4.thumbnail_url).read()
        photo = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (160 , 90))
        customtkinter.CTkLabel(sWindow, text = "", image = photo).place(x = 80, y = 310)

        # Returns widgets to right state
        error = "no"
        normalWidgets(results_counter, error)

    # Proceed to downlaod page
    def onDnClick():
        if to_download == []:
            return messagebox.showerror(title = "No Selected Video", message = "Please select at least one video to download.")
        msg_box = messagebox.askquestion(title = "Proceed To Download", message = f"Are you sure that you want to download {len(to_download)} video(s)")
        if msg_box == "yes":
            button_var = dn_button_var
            threading.Thread(target = ResultsWindow, args = (to_download,)).start()
            threading.Thread(target = Loading, args = (button_var,)).start()
        else: return

    # Search download
    def ResultsWindow(to_download):
        # Starting
        def pVideoStart():
            threading.Thread(target = Downloading).start()
            threading.Thread(target = SearchDownloader).start()

        # Back home
        def backHome():
            download = downloading_var.get()
            non_downloading_list = ["", "Finished", "Canceled"]
            if download in non_downloading_list:
                pass
            else:
                msg_box = messagebox.askquestion(title = "Cancel Download",
                message = "Going back to home will cancel the current download.\n\nDo you wish to continue?",
                icon = "warning")
                if msg_box == "yes": pass
                else: return
            sDWindow.destroy()
            root.deiconify()

        # Set path
        user = getpass.getuser()
        path = f"C:/Users\{user}\Downloads"
        global directory
        directory = os.path.realpath(path) # Deafult path in case the user didn't choose
        def pBrowseDir(): # Path function
            global directory2
            directory2 = filedialog.askdirectory()
            ppath_var.set(directory2)

        # Captions download
        def sCaptionsDownload():
            for vid_link in vids_subs:
                url = YouTube(vid_link)
                if url in to_download:
                    lang = lang_choose.get()
                    video_id = extract.video_id(vid_link)
                    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                    if lang.lower() == "none":
                        return
                    elif lang.lower() == "arabic":
                        lang = "ar"
                    elif lang.lower() == "english":
                        for transcript in transcript_list:
                            if transcript.language_code == "en-US":
                                lang = "en-US"
                                break
                            elif transcript.language_code == "en-UK":
                                lang = "en-UK"
                                break
                            else:
                                lang = "en"
                    else:
                        progressbar.stop()
                        toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
                        toggle_button.place(x = 550 , y = 347)
                        cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled")
                        cancel_button.place(x = 595 , y = 347)
                        download_button = customtkinter.CTkButton(sDWindow, text = "Download", font = ("arial bold", 25), command = pVideoStart)
                        download_button.place(x = 540 , y = 306)
                        path_button = customtkinter.CTkButton(sDWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", hover_color = "gray25", width = 5, command = pBrowseDir)
                        path_button.place(x = 430 , y = 347)
                        lang_choose.configure(state = "normal")
                        downloadcounter_var.set("")
                        downloading_var.set("")
                        messagebox.showerror(title = "Subtitle Not Supported", message = "Please choose a supported language.")
                        return False
                    downloadcounter_var.set("Subtitle Download")
                    try: # Get the subtitle directly if it's there
                        final = YouTubeTranscriptApi.get_transcript(video_id = video_id, languages = [lang])
                        print("got one already there")
                        sub = "subtitle"
                    except: # If not then translate it
                        translated = "no"
                        en_list = ["en", "en-US","en-UK"]
                        for transcript in transcript_list:
                            if transcript.language_code in en_list: # Translate from English if it's there
                                final = transcript.translate(lang).fetch()
                                print(f"translated from {transcript.language_code}")
                                sub = "translated_subtitle"
                                translated = "yes"
                            if translated == "no": # Avoid translating twice
                                final = transcript.translate(lang).fetch()
                                print(f"translated {transcript.language_code}")
                                sub = "translated_subtitle"
                                translated = "yes"
                            else:
                                pass
                    formatter = SRTFormatter()
                    srt_formatted = formatter.format_transcript(final)
                    try:
                        with open(f"{directory2}/{clean_filename(url.title)}_{sub}_{lang}.srt", "w", encoding = "utf-8") as srt_file:
                            srt_file.write(srt_formatted)
                    except NameError:
                        with open(f"{directory}/{clean_filename(url.title)}_{sub}_{lang}.srt", "w", encoding = "utf-8") as srt_file:
                            srt_file.write(srt_formatted)
                else:
                    print(f"{url.title} not in list")

        # Open folder in file explorer when download is finished
        def openFile():
            try:
                dir2 = os.path.normpath(directory2)
                subprocess.Popen(f'explorer "{dir2}"')
            except NameError:
                subprocess.Popen(f'explorer "{directory}"')

        # Downloading label function
        def Downloading():
            downloading_var.set("Downloading")
            time.sleep(0.5)
            while True:
                if downloading_var.get() == "Downloading":
                    downloading_var.set("Downloading.")
                    time.sleep(0.5)
                else: break
                if downloading_var.get() == "Downloading.":
                    downloading_var.set("Downloading..")
                    time.sleep(0.5)
                else: break
                if downloading_var.get() == "Downloading..":
                    downloading_var.set("Downloading...")
                    time.sleep(0.5)
                else: break
                if downloading_var.get() == "Downloading...":
                    downloading_var.set("Downloading")
                    time.sleep(0.5)
                else: break
            dont_change = ["Canceled", "Paused", "Finished"]
            while True:
                time.sleep(1)
                if downloading_var.get() in dont_change:
                    continue
                else:
                    Downloading()

        # Pause/Resume function
        def toggle_download():
            global is_paused
            is_paused = not is_paused
            if is_paused:
                progressbar.stop()
                toggle_button = customtkinter.CTkButton(sDWindow, text = "▶️", font = ("arial", 15), fg_color = "grey14", hover_color = "gray10", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
                toggle_button.place(x = 550 , y = 347)
                downloading_var.set("Paused")
            else:
                progressbar.start()
                toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
                toggle_button.place(x = 550 , y = 347)
                downloading_var.set("Downloading")

        # Cancel function
        def cancel_download():
            global is_cancelled
            is_cancelled = True

        # Download search
        def SearchDownloader():
            # Preperations
            global is_paused, is_cancelled
            is_paused = is_cancelled = False
            toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
            toggle_button.place(x = 550 , y = 347)
            cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, command = cancel_download)
            cancel_button.place(x = 595 , y = 347)
            download_button = customtkinter.CTkButton(sDWindow, text = "Download", font = ("arial bold", 25), state = "disabled")
            download_button.place(x = 540 , y = 306)
            path_button = customtkinter.CTkButton(sDWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", width = 5, state = "disabled")
            path_button.place(x = 430 , y = 347)
            audio_tags_list = ["251" , "140" , "250" , "249"]
            # Progress stuff
            pytube.request.default_range_size = 2097152  # 2MB chunk size (update progress every 2MB)
            progressbar.start()
            progress_label.configure(text_color = "green")
            progress_size_label.configure(text_color = "LightBlue")
            lang_choose.configure(state = "disabled")
            # Download subtitles if selected
            if caps == "yes":
                if sCaptionsDownload() == False: return
            else: pass

            # Download to_download
            downloaded_counter = 0
            downloadcounter_var.set(f"{downloaded_counter}/{len(to_download)} Downloaded")
            r = reprlib.Repr()
            r.maxstring = 27
            for url in to_download:
                if is_cancelled: break
                video = url.streams.get_by_itag(quality)
                title_var.set(r.repr(url.title))
                length_var.set(to_hms(url.length))
                size_var.set(f"{round(video.filesize/1024/1024, 2)} MB")
                if quality in audio_tags_list: ext = "mp3"
                else: ext = "mp4"
                video = url.streams.get_by_itag(quality)
                size = video.filesize
                try: vname = f"{directory2}/{clean_filename(url.title)}_({quality_string}).{ext}"
                except NameError: vname = f"{directory}/{clean_filename(url.title)}_({quality_string}).{ext}"
                raw_data = urllib.request.urlopen(url.thumbnail_url).read()
                photo = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (270 , 150))
                thumb = customtkinter.CTkLabel(sDWindow, text = "", image = photo)
                thumb.place(x = 415 , y = 15)
                with open(vname, "wb") as f:
                    video = request.stream(video.url) # Get an iterable stream
                    downloaded = 0
                    while True:
                        if is_cancelled:
                            downloading_var.set("Canceled")
                            progressbar.stop()
                            toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
                            toggle_button.place(x = 550 , y = 347)
                            cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled")
                            cancel_button.place(x = 595 , y = 347)
                            break
                        if is_paused:
                            time.sleep(0.5)
                            continue
                        try: chunk = next(video, None) # Get next chunk of video
                        except: return messagebox.showerror(title = "Something Went Wrong", message = "Something went wrong, please try again.")
                        if chunk:
                            f.write(chunk) # Download the chunk into the file
                            # Update Progress
                            downloaded += len(chunk)
                            remaining = size - downloaded
                            bytes_downloaded = size - remaining
                            percentage_of_completion = bytes_downloaded / size * 100
                            percentage_var.set(f"{round(percentage_of_completion, 2)}%  ")
                            sizeprogress_var.set(f"{int(bytes_downloaded / 1024 / 1024)} MB  ")
                        else:
                            downloaded_counter = downloaded_counter + 1
                            downloadcounter_var.set(f"{downloaded_counter}/{len(to_download)} Downloaded")
                            break # No more data = Finished

            # When finished
            progressbar.stop()
            toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
            toggle_button.place(x = 550 , y = 347)
            cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled")
            cancel_button.place(x = 595 , y = 347)
            if is_cancelled:
                msg_box = messagebox.askquestion(title = "Delete Canceled File", message = f"Do you want to delete '{vname}'?")
                if msg_box == "yes": os.remove(vname)
            else:
                downloadcounter_var.set("")
                sDWindow.bell()
                thumb.configure(image = "")
                title_var.set("Finished")
                length_var.set("Finished")
                size_var.set("Finished")
                downloading_var.set("Finished")
                customtkinter.CTkButton(sDWindow, text = "Open File in Explorer", font = ("arial bold", 20), command = openFile).place(x = 470 , y = 420)

        # Get to_download list info, get link and check errors
        total_size = 0
        total_length = 0
        vids_subs = []
        for url in to_download:
            video = url.streams.get_by_itag(quality)
            total_size = total_size + video.filesize
            total_length = total_length + url.length
            try:
                video_id = extract.video_id(url.watch_url)
                YouTubeTranscriptApi.list_transcripts(video_id)
                vids_subs.append(url.watch_url)
                print(f"({url.title}) found subtitle")
            except:
                print(f"({url.title}) no subtitle")
                pass

        # Selected labels prepare
        if quality == "144":
            quality_string = "144p"
        elif quality == "240":
            quality_string = "240p"
        elif quality == "18":
            quality_string = "360p"
        elif quality == "135":
            quality_string = "480p"
        elif quality == "22":
            quality_string = "720p"
        elif quality == "137":
            quality_string = "1080p"
        elif quality == "249":
            quality_string = "50kbps"
        elif quality == "250":
            quality_string = "70kbps"
        elif quality == "140":
            quality_string = "128kbps"
        elif quality == "251":
            quality_string = "160kbps"

        # Form creating
        sWindow.destroy()
        sDWindow = customtkinter.CTkToplevel()
        sDWindow.title("Results Downloader")
        width = 700
        height = 460
        x = (sDWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (sDWindow.winfo_screenheight() // 2) - (height // 2)
        sDWindow.geometry(f"{width}x{height}+{x}+{y}")
        sDWindow.maxsize(700, 460)
        sDWindow.minsize(700, 460)
        sDWindow.protocol("WM_DELETE_WINDOW", onClosing)
        sDWindow.iconbitmap("YDICO.ico")

        # Downloading label
        downloading_var = StringVar()
        customtkinter.CTkLabel(sDWindow, textvariable = downloading_var, font = ("arial", 25)).place(x = 265 , y = 418)
        downloadcounter_var = StringVar()
        customtkinter.CTkLabel(sDWindow, textvariable = downloadcounter_var, font = ("arial", 25)).place(x = 500 , y = 418)

        # Search download labels
        title_var = StringVar()
        title_var.set("...")
        length_var = StringVar()
        length_var.set("...")
        size_var = StringVar()
        size_var.set("...")
        customtkinter.CTkLabel(sDWindow, text = "Current Video Info", font = ("arial bold italic", 30)).place(x = 10 , y = 15)
        customtkinter.CTkLabel(sDWindow, text = "Video Title:", font = ("arial bold", 20)).place(x = 20 , y = 55)
        customtkinter.CTkLabel(sDWindow, textvariable = title_var, font = ("arial", 20)).place(x = 132 , y = 55)
        customtkinter.CTkLabel(sDWindow, text = "Length:", font = ("arial bold", 20)).place(x = 20 , y = 90)
        customtkinter.CTkLabel(sDWindow, textvariable = length_var, font = ("arial", 20)).place(x = 97 , y = 90)
        customtkinter.CTkLabel(sDWindow, text = "File size:", font = ("arial bold", 20)).place(x = 20 , y = 125)
        customtkinter.CTkLabel(sDWindow, textvariable = size_var, font = ("arial", 20)).place(x = 111 , y = 125)

        customtkinter.CTkLabel(sDWindow, text = "Total Videos Info", font = ("arial bold italic", 30)).place(x = 10 , y = 165)
        customtkinter.CTkLabel(sDWindow, text = "Total Videos:", font = ("arial bold", 20)).place(x = 20 , y = 205)
        customtkinter.CTkLabel(sDWindow, text = len(to_download), font = ("arial", 20)).place(x = 151 , y = 205)
        customtkinter.CTkLabel(sDWindow, text = "Total Length:", font = ("arial bold", 20)).place(x = 20 , y = 240)
        customtkinter.CTkLabel(sDWindow, text = f"{to_hms(total_length)}", font = ("arial", 20)).place(x = 150 , y = 240)
        customtkinter.CTkLabel(sDWindow, text = "Quality:", font = ("arial bold", 20)).place(x = 20 , y = 275)
        customtkinter.CTkLabel(sDWindow, text = quality_string, font = ("arial", 20)).place(x = 96 , y = 275)
        customtkinter.CTkLabel(sDWindow, text = "Total Size:", font = ("arial bold", 20)).place(x = 20 , y = 310)
        customtkinter.CTkLabel(sDWindow, text = f"{round(total_size/1024/1024, 2)} MB", font = ("arial", 20)).place(x = 123 , y = 310)

        # Path change
        customtkinter.CTkLabel(sDWindow, text = "Download Path:", font = ("arial bold", 20)).place(x = 20 , y = 345)
        ppath_var = StringVar()
        customtkinter.CTkEntry(sDWindow, width = 245, height = 26, textvariable = ppath_var, state = "disabled").place(x = 175 , y = 347)
        try:
            ppath_var.set(directory2)
        except NameError:
            ppath_var.set(directory)
        path_button = customtkinter.CTkButton(sDWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", hover_color = "gray25", width = 5, height = 26, command = pBrowseDir)
        path_button.place(x = 430 , y = 347)

        # Subtitle Combobox
        if vids_subs == []:
            lang_choose_state = "disabled"
            caps = "no"
        else:
            lang_choose_state = "normal"
            caps = "yes"
        print(vids_subs)
        customtkinter.CTkLabel(sDWindow, text = "Subtitle:", font = ("arial bold", 20)).place(x = 340 , y = 315)
        lang_choose = customtkinter.CTkComboBox(sDWindow, width = 100, height = 26, values = ["None", "Arabic", "English"], state = lang_choose_state)
        lang_choose.set("None")
        lang_choose.place(x = 425 , y = 315)

        # Progress bar/labels
        percentage_var = StringVar()
        sizeprogress_var = StringVar()
        progress_label = customtkinter.CTkLabel(sDWindow, textvariable = percentage_var, font = ("arial", 22))
        progress_label.place(x = 540 , y = 384)
        progress_size_label = customtkinter.CTkLabel(sDWindow, textvariable = sizeprogress_var, font = ("arial", 22))
        progress_size_label.place(x = 624 , y = 384)
        percentage_var.set("0.00%")
        sizeprogress_var.set("0 MB")
        progressbar = customtkinter.CTkProgressBar(sDWindow, width = 505, mode = "indeterminate")
        progressbar.place(x = 20 , y = 395)

        # Pause/Resume & Cancel buttons
        toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
        toggle_button.place(x = 550 , y = 347)
        cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled")
        cancel_button.place(x = 595 , y = 347)

        # Download button
        download_button = customtkinter.CTkButton(sDWindow, text = "Download", font = ("arial bold", 25), command = pVideoStart)
        download_button.place(x = 540 , y = 306)

        # Back to home button
        back_button = customtkinter.CTkButton(sDWindow, text = "Back To Home", font = ("arial bold", 20), command = backHome)
        back_button.place(x = 20 , y = 420)


    # Buttons&label
    page_counter = StringVar()
    page_counter.set("Page 1/4")
    selected_counter = StringVar()
    selected_counter.set("0 Selected")
    pr_button_var = StringVar()
    pr_button_var.set("Previous Results")
    nr_button_var = StringVar()
    nr_button_var.set("Next Results")
    pr_button = customtkinter.CTkButton(sWindow, textvariable = pr_button_var, font = ("arial bold", 15), command = onPrClick)
    pr_button.place(x = 20, y = 420)
    customtkinter.CTkLabel(sWindow, textvariable = selected_counter, font = ("arial bold", 15)).place(x = 185, y = 420)
    dn_button_var = StringVar()
    dn_button_var.set("Download")
    dn_button = customtkinter.CTkButton(sWindow, textvariable = dn_button_var, font = ("arial bold", 15), command = onDnClick)
    dn_button.place(x = 290, y = 420)
    customtkinter.CTkLabel(sWindow, textvariable = page_counter, font = ("arial bold", 15)).place(x = 450, y = 420)
    nr_button = customtkinter.CTkButton(sWindow, textvariable = nr_button_var, font = ("arial bold", 15), command = onNrClick)
    nr_button.place(x = 540, y = 420)

    results()
    whenError()
    sWindow.deiconify()
    root.withdraw()

# Download buttons
video_button = customtkinter.CTkButton(root, textvariable = loading_var, width = 235, font = ("arial bold", 25), command = OnDownloadButton)
video_button.place(x = 305 , y = 205)

# Run the app
root.mainloop()
