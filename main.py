from tkinter import *
from tkinter import filedialog, messagebox
import customtkinter
from pytube import YouTube, Playlist, Search, extract, request
import pytube.request
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
import threading
from threading import Thread
import json
from PIL import Image
import urllib.request
import os
import io
import reprlib
import time
import subprocess
import webbrowser
import shlex
from sys import platform
import requests


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
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    root.destroy()

# Create form
root = customtkinter.CTk()
width = 700
height = 460
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}") # Centers the window
root.resizable(False, False)
if platform == "linux" or platform == "linux2": pass # Linux
else: root.iconbitmap("YDICO.ico") # Windows
root.title("YouTube Downloader")
customtkinter.CTkLabel(root, text = "YouTube Downloader", font = ("arial bold", 45)).place(x = 140 , y = 20)

# Link Entry Copy
def linkCopy():
    start = link_entry.index("sel.first")
    end = link_entry.index("sel.last")
    to_copy = link_entry.get()[start:end]
    root.clipboard_append(to_copy)

# Link Entry Cut
def linkCut():
    start = link_entry.index("sel.first")
    end = link_entry.index("sel.last")
    to_copy = link_entry.get()[start:end]
    root.clipboard_append(to_copy) # Get text from clipboard
    try: # Delete the selected text
        start = link_entry.index("sel.first")
        end = link_entry.index("sel.last")
        link_entry.delete(start, end)
    except TclError:
        pass # Nothing was selected, so paste won't delete

# Link Entry Paste
def linkPaste():
    clipboard = root.clipboard_get() # Get text from clipboard
    clipboard = clipboard.replace("\n", "\\n")
    try: # delete the selected text, if any
        start = link_entry.index("sel.first")
        end = link_entry.index("sel.last")
        link_entry.delete(start, end)
    except TclError:
        pass # Nothing was selected, so paste won't delete
    link_entry.insert("insert", clipboard) # Insert the modified clipboard contents

# Right-Click menu
m = Menu(root, tearoff = 0)
m.add_command(label ="Cut", font = ("arial", 11), command = linkCut)
m.add_command(label ="Copy", font = ("arial", 11), command = linkCopy)
m.add_command(label ="Paste", font = ("arial", 11), command = linkPaste)
def linkRightClickMenu(event):
    try: m.tk_popup(event.x_root, event.y_root)
    finally: m.grab_release()

# Search Entry Copy
def searchCopy():
    start = link_entry.index("sel.first")
    end = link_entry.index("sel.last")
    to_copy = link_entry.get()[start:end]
    root.clipboard_append(to_copy)

# Search Entry Cut
def searchCut():
    start = search_entry.index("sel.first")
    end = search_entry.index("sel.last")
    to_copy = search_entry.get()[start:end]
    root.clipboard_append(to_copy) # Get text from clipboard
    try: # Delete the selected text
        start = search_entry.index("sel.first")
        end = search_entry.index("sel.last")
        search_entry.delete(start, end)
    except TclError:
        pass # Nothing was selected, so paste won't delete

# Search Entry Paste
def searchPaste():
    clipboard = root.clipboard_get() # Get text from clipboard
    clipboard = clipboard.replace("\n", "\\n")
    try: # Delete the selected text, if any
        start = search_entry.index("sel.first")
        end = search_entry.index("sel.last")
        search_entry.delete(start, end)
    except TclError:
        pass # Nothing was selected, so paste won't delete
    search_entry.insert("insert", clipboard) # Insert the modified clipboard contents

# Right-Click menu
m2 = Menu(root, tearoff = 0)
m2.add_command(label ="Cut", font = ("arial", 11), command = searchCut)
m2.add_command(label ="Copy", font = ("arial", 11), command = searchCopy)
m2.add_command(label ="Paste", font = ("arial", 11), command = searchPaste)
def searchRightClickMenu(event):
    try: m2.tk_popup(event.x_root, event.y_root)
    finally: m2.grab_release()

# Paste link widgets
link_var = StringVar()
customtkinter.CTkLabel(root, text = "Paste Your URL Here", font = ("arial bold", 25)).place(x = 105 , y = 120)
link_entry = customtkinter.CTkEntry(root, width = 345, textvariable = link_var, corner_radius = 20)
link_entry.place(x = 100 , y = 160)
link_entry.bind("<Button-3>", linkRightClickMenu)

# Type keywords widgets
search_var = StringVar()
customtkinter.CTkLabel(root, text = "Type Your Keywords Here", font = ("arial bold", 25)).place(x = 105 , y = 220)
search_entry = customtkinter.CTkEntry(root, width = 345, textvariable = search_var, corner_radius = 20)
search_entry.place(x = 100 , y = 260)
search_entry.bind("<Button-3>", searchRightClickMenu)

# Quality selections for downloads
quality_var = IntVar()
def downloadQualitySelect(quality):
    if quality == "Video: 1080p": quality_var.set(137)
    elif quality == "Video: 720p": quality_var.set(22)
    elif quality == "Video: 480p": quality_var.set(135)
    elif quality == "Video: 360p": quality_var.set(18)
    elif quality == "Video: 240p": quality_var.set(133)
    elif quality == "Video: 144p": quality_var.set(160)
    elif quality == "Audio: 160kbps": quality_var.set(251)
    elif quality == "Audio: 128kbps": quality_var.set(140)
    elif quality == "Audio: 70kbps": quality_var.set(250)
    elif quality == "Audio: 50kbps": quality_var.set(249)
    else: quality_var.set(0)
    global link
    link = link_var.get()
    if "playlist" in link: threading.Thread(target = PlaylistWindow).start()
    else: threading.Thread(target = DownlaodWindow).start()
    loading_optionmenu = download_optionmenu
    threading.Thread(target = Loading, args = (loading_optionmenu,)).start()
download_quality_list = ["Video: 1080p", "Video: 720p", "Video: 480p", "Video: 360p", "Video: 240p", "Video: 144p", "Audio: 160kbps", "Audio: 128kbps", "Audio: 70kbps", "Audio: 50kbps"]
download_optionmenu = customtkinter.CTkOptionMenu(root, width = 175, height = 35, font = ("arial bold", 25), values = download_quality_list, command = downloadQualitySelect, corner_radius = 15)
download_optionmenu.place(x = 460 , y = 155)
download_optionmenu.set("Download")

# Quality selections for search
quality_var = IntVar()
def searchQualitySelect(quality):
    if quality == "Video: 1080p": quality_var.set(137)
    elif quality == "Video: 720p": quality_var.set(22)
    elif quality == "Video: 480p": quality_var.set(135)
    elif quality == "Video: 360p": quality_var.set(18)
    elif quality == "Video: 240p": quality_var.set(133)
    elif quality == "Video: 144p": quality_var.set(160)
    elif quality == "Audio: 160kbps": quality_var.set(251)
    elif quality == "Audio: 128kbps": quality_var.set(140)
    elif quality == "Audio: 70kbps": quality_var.set(250)
    elif quality == "Audio: 50kbps": quality_var.set(249)
    else: quality_var.set(0)
    global search
    search = search_var.get()
    loading_optionmenu = search_optionmenu
    search_optionmenu.configure(corner_radius = 15)
    threading.Thread(target = SearchWindow).start()
    threading.Thread(target = Loading, args = (loading_optionmenu,)).start()
search_quality_list = ["Video: 1080p", "Video: 720p", "Video: 480p", "Video: 360p", "Video: 240p", "Video: 144p", "Audio: 160kbps", "Audio: 128kbps", "Audio: 70kbps", "Audio: 50kbps"]
search_optionmenu = customtkinter.CTkOptionMenu(root, width = 175, height = 35, font = ("arial bold", 25), values = search_quality_list, command = searchQualitySelect, corner_radius = 35)
search_optionmenu.place(x = 460 , y = 255)
search_optionmenu.set("Search")

# Appearance theme
def changeTheme(color):
    color = color.lower()
    themes_list = ["system", "dark", "light"]
    if color in themes_list:
        customtkinter.set_appearance_mode(color)
        to_change = "bg_theme"
    else:
        customtkinter.set_default_color_theme(color)
        customtkinter.CTkLabel(root, text = "(Restart to take full effect)", font = ("arial", 12)).place(x = 242 , y = 415)
        to_change = "default_color"
    with open("theme_config.json", "r", encoding="utf8") as f:
        theme = json.load(f)
    with open("theme_config.json", "w", encoding="utf8") as f:
        theme[to_change] = color
        json.dump(theme, f, sort_keys = True, indent = 4, ensure_ascii = False)
customtkinter.CTkLabel(root, text = "Appearance Settings", font = ("arial bold", 19)).place(x = 34 , y = 340)
customtkinter.CTkLabel(root, text = "Theme Mode: ", font = ("arial", 15)).place(x = 27 , y = 375)
themes_menu = customtkinter.CTkOptionMenu(root, values = ["System", "Dark", "Light"], width = 110, command = changeTheme, corner_radius = 15)
themes_menu.place(x = 127 , y = 375)
themes_menu.set(get_bg_theme().title())
customtkinter.CTkLabel(root, text = "Default Color: ", font = ("arial", 15)).place(x = 27 , y = 415)
defaultcolor_menu = customtkinter.CTkOptionMenu(root, values = ["Blue", "Dark-blue", "Green"], width = 110, command = changeTheme, corner_radius = 15)
defaultcolor_menu.place(x = 127 , y = 415)
defaultcolor_menu.set(get_default_color().title())

# Loading labels dots loop
ploading_counter_var = StringVar()
customtkinter.CTkLabel(root, textvariable = ploading_counter_var, font = ("arial", 22)).place(x = 530 , y = 208)
def Loading(loading_optionmenu):
    loading_optionmenu.set("Loading")
    time.sleep(0.5)
    while True:
        if loading_optionmenu.get() == "Loading":
            loading_optionmenu.set("Loading.")
            time.sleep(0.5)
        else: break
        if loading_optionmenu.get() == "Loading.":
            loading_optionmenu.set("Loading..")
            time.sleep(0.5)
        else: break
        if loading_optionmenu.get() == "Loading..":
            loading_optionmenu.set("Loading...")
            time.sleep(0.5)
        else: break
        if loading_optionmenu.get() == "Loading...":
            loading_optionmenu.set("Loading")
            time.sleep(0.5)
        else: break

# Downloading labels dots loop
def Downloading(downloading_var):
    if downloading_var.get() == "Converting":
        while True:
            if downloading_var.get() == "Converting":
                downloading_var.set("Converting.")
                time.sleep(0.5)
            else: break
            if downloading_var.get() == "Converting.":
                downloading_var.set("Converting..")
                time.sleep(0.5)
            else: break
            if downloading_var.get() == "Converting..":
                downloading_var.set("Converting...")
                time.sleep(0.5)
            else: break
            if downloading_var.get() == "Converting...":
                downloading_var.set("Converting")
                time.sleep(0.5)
            else: break
    elif downloading_var.get() == "Merging":
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
        dont_change = ["Canceled", "Paused", "Finished", " "]
        while True:
            time.sleep(1)
            if downloading_var.get() in dont_change: continue
            else: Downloading(downloading_var)

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
        download_optionmenu.configure(state = "normal")
        search_optionmenu.configure(state = "normal")
        themes_menu.configure(state = "normal")
        defaultcolor_menu.configure(state = "normal")
        download_optionmenu.set("Download")
        search_optionmenu.set("Search")
        search_optionmenu.configure(corner_radius = 35)
        ploading_counter_var.set("")
        adv_quailty_button = customtkinter.CTkButton(root, text = "Advanced Quality Settings", width = 175, font = ("arial bold", 15), command = AdvancedWindow, corner_radius = 20)
        adv_quailty_button.place(x = 460 , y = 415)
        link_entry.configure(state = "normal")
        search_entry.configure(state = "normal")

# When opens a new window from home page
def whenOpening():
    download_optionmenu.configure(state = "disabled")
    search_optionmenu.configure(state = "disabled")
    themes_menu.configure(state = "disabled")
    defaultcolor_menu.configure(state = "disabled")
    ploading_counter_var.set("")
    adv_quailty_button = customtkinter.CTkButton(root, text = "Advanced Quality Settings", width = 175, font = ("arial bold", 15), state = "disabled", corner_radius = 20)
    adv_quailty_button.place(x = 460 , y = 415)
    link_entry.configure(state = "disabled")
    search_entry.configure(state = "disabled")


# Advanced Settings Window
def AdvancedWindow():
    global advWindow
    try:
        advWindow.deiconify()
        root.withdraw()
    except:
        # Form creating
        def onClosing():
            advWindow.destroy()
            root.deiconify()
        advWindow = customtkinter.CTkToplevel() # Toplevel object which will be treated as a new window
        advWindow.withdraw()
        advWindow.title("Advanced Quality Settings")
        width = 700
        height = 460
        x = (advWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (advWindow.winfo_screenheight() // 2) - (height // 2)
        advWindow.geometry(f"{width}x{height}+{x}+{y}")
        advWindow.maxsize(700, 460)
        advWindow.minsize(700, 460)
        if platform == "linux" or platform == "linux2": pass
        else: advWindow.iconbitmap("YDICO.ico")
        advWindow.protocol("WM_DELETE_WINDOW", onClosing)

        # CRF slider function
        def crfSlider(num):
            if num == 23: crf_var.set(f"{int(num)} (Default)")
            elif num == 0: crf_var.set(f"{int(num)} (Loseless Quality)")
            elif num == 51: crf_var.set(f"{int(num)} (Lowest Quality)")
            else: crf_var.set(int(num))

        # Radiobuttons function
        def radioDisableNormal():
            if video_crf_or_bitrate.get() == "crf":
                crf_slider.configure(state = "normal")
                bitrate_entry.configure(state = "disabled")
                bitrate_entry.configure(border_color = "#565B5E")
            else:
                bitrate_entry.configure(state = "normal")
                crf_slider.configure(state = "disabled")
            if audio_quality_or_bitrate.get() == "bitrate":
                abitrate_combobox.configure(state = "readonly")
                aquality_combobox.configure(state = "disabled")
            else:
                aquality_combobox.configure(state = "readonly")
                abitrate_combobox.configure(state = "disabled")

        # Widgets vars
        video_crf_or_bitrate = StringVar()
        video_crf_or_bitrate.set("crf")
        crf_var = StringVar()
        crf_var.set("23 (Default)")
        audio_quality_or_bitrate = StringVar()
        audio_quality_or_bitrate.set("bitrate")
        bitrate_entry_var = StringVar()
        # Widgets lists
        profile_combobox_list = ["High", "Main (Default)", "Baseline"] # -profile [selected option]
        tune_combobox_list = ["Film", "Animation", "Grain", "Still Image", "Fast Decode", "Zero Latency", "None (Default)"] # -tune [selected option]
        preset_combobox_list = ["Ultrafast", "Superfast", "Veryfast", "Faster", "Fast", "Medium (Default)", "Slow"] # -preset [prselected optioneset]
        format_combobox_list = ["MP4 (Default)", "M4A", "MKV"]
        codec_combobox_list = ["H.264 (Default)", "H.265", "AV1", "MPEG-4"]
        fps_combobox_list = ["5", "10", "15", "20", "23.976", "24", "30 (Default)", "40", "45", "50", "60"]
        aformat_combobox_list = ["MP3 (Default)", "WAV", "AAC", "OPUS", "FLAC"]
        abitrate_combobox_list = ["320", "192", "160", "128", "96", "70", "50"]
        aquality_combobox_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        # Widgets placing
        customtkinter.CTkLabel(advWindow, text = "Video Settings", font = ("arial bold italic", 30)).place(x = 8 , y = 13)
        customtkinter.CTkLabel(advWindow, text = "Format:", font = ("arial bold", 20)).place(x = 20 , y = 55)
        format_combobox = customtkinter.CTkComboBox(advWindow, width = 133, height = 26, values = format_combobox_list, corner_radius = 15, state = "readonly")
        format_combobox._entry.configure(readonlybackground = format_combobox._apply_appearance_mode(format_combobox._fg_color))
        format_combobox.set("MP4 (Default)")
        format_combobox.place(x = 97 , y = 55)
        customtkinter.CTkLabel(advWindow, text = "Encoder Tune:", font = ("arial bold", 20)).place(x = 360 , y = 125)
        tune_combobox = customtkinter.CTkComboBox(advWindow, width = 137, height = 26, values = tune_combobox_list, corner_radius = 15, state = "readonly")
        tune_combobox._entry.configure(readonlybackground = tune_combobox._apply_appearance_mode(tune_combobox._fg_color))
        tune_combobox.set("None (Default)")
        tune_combobox.place(x = 505 , y =125)
        customtkinter.CTkLabel(advWindow, text = "Encoder Profile:", font = ("arial bold", 20)).place(x = 360 , y = 90)
        profile_combobox = customtkinter.CTkComboBox(advWindow, width = 137, height = 26, values = profile_combobox_list, corner_radius = 15, state = "readonly")
        profile_combobox._entry.configure(readonlybackground = profile_combobox._apply_appearance_mode(profile_combobox._fg_color))
        profile_combobox.set("Main (Default)")
        profile_combobox.place(x = 518 , y = 90)
        customtkinter.CTkLabel(advWindow, text = "Encoder Preset:", font = ("arial bold", 20)).place(x = 360 , y = 55)
        preset_combobox = customtkinter.CTkComboBox(advWindow, width = 150, height = 26, values = preset_combobox_list, corner_radius = 15, state = "readonly")
        preset_combobox._entry.configure(readonlybackground = preset_combobox._apply_appearance_mode(preset_combobox._fg_color))
        preset_combobox.set("Medium (Default)")
        preset_combobox.place(x = 519 , y = 55)
        customtkinter.CTkLabel(advWindow, text = "Codec:", font = ("arial bold", 20)).place(x = 20 , y = 90)
        codec_combobox = customtkinter.CTkComboBox(advWindow, width = 138, height = 26, values = codec_combobox_list, corner_radius = 15, state = "readonly")
        codec_combobox.place(x = 93 , y = 90)
        codec_combobox._entry.configure(readonlybackground = codec_combobox._apply_appearance_mode(codec_combobox._fg_color))
        codec_combobox.set("H.264 (Default)")
        customtkinter.CTkLabel(advWindow, text = "Framerate (FPS):", font = ("arial bold", 20)).place(x = 20 , y = 125)
        fps_combobox = customtkinter.CTkComboBox(advWindow, width = 120, height = 26, values = fps_combobox_list, corner_radius = 15, state = "readonly")
        fps_combobox.place(x = 185 , y = 125)
        fps_combobox._entry.configure(readonlybackground = fps_combobox._apply_appearance_mode(fps_combobox._fg_color))
        fps_combobox.set("30 (Default)")
        crf_radiobutton = customtkinter.CTkRadioButton(advWindow, text = "Constant Quality:", font = ("arial bold", 20), variable = video_crf_or_bitrate, value = "crf", command = radioDisableNormal)
        crf_radiobutton.place(x = 20 , y = 163)
        customtkinter.CTkLabel(advWindow, textvariable = crf_var, font = ("arial", 17)).place(x = 520 , y = 161)
        crf_slider = customtkinter.CTkSlider(advWindow, corner_radius = 15, width = 300, from_ = 0, to = 51, number_of_steps = 51, command = crfSlider)
        crf_slider.place(x = 212 , y = 167)
        crf_slider.set(23)
        bitrate_radiobutton = customtkinter.CTkRadioButton(advWindow, text = "Total Bitrate (kbps):", font = ("arial bold", 20), variable = video_crf_or_bitrate, value = "bitrate", command = radioDisableNormal)
        bitrate_radiobutton.place(x = 20 , y = 198)
        bitrate_entry = customtkinter.CTkEntry(advWindow, textvariable = bitrate_entry_var, width = 100, height = 26, corner_radius = 15, state = "disabled")
        bitrate_entry.place(x = 238 , y = 198)
        customtkinter.CTkLabel(advWindow, text = "Audio Settings", font = ("arial bold italic", 30)).place(x = 8 , y = 238)
        customtkinter.CTkLabel(advWindow, text = "Format:", font = ("arial bold", 20)).place(x = 20 , y = 280)
        aformat_combobox = customtkinter.CTkComboBox(advWindow, width = 133, height = 26, values = aformat_combobox_list, corner_radius = 15, state = "readonly")
        aformat_combobox._entry.configure(readonlybackground = aformat_combobox._apply_appearance_mode(aformat_combobox._fg_color))
        aformat_combobox.set("MP3 (Default)")
        aformat_combobox.place(x = 96 , y = 280)
        abitrate_radiobutton = customtkinter.CTkRadioButton(advWindow, text = "Bitrate:", font = ("arial bold", 20), variable = audio_quality_or_bitrate, value = "bitrate", command = radioDisableNormal)
        abitrate_radiobutton.place(x = 20 , y = 318)
        abitrate_combobox = customtkinter.CTkComboBox(advWindow, width = 80, height = 26, values = abitrate_combobox_list, corner_radius = 15, state = "readonly")
        abitrate_combobox._entry.configure(readonlybackground = abitrate_combobox._apply_appearance_mode(abitrate_combobox._fg_color))
        abitrate_combobox.set("320")
        abitrate_combobox.place(x = 121 , y = 316)
        aquality_radiobutton = customtkinter.CTkRadioButton(advWindow, text = "Quality:", font = ("arial bold", 20), variable = audio_quality_or_bitrate, value = "quality", command = radioDisableNormal)
        aquality_radiobutton.place(x = 20 , y = 353)
        aquality_combobox = customtkinter.CTkComboBox(advWindow, width = 90, height = 26, values = aquality_combobox_list, corner_radius = 15, state = "disabled")
        aquality_combobox._entry.configure(readonlybackground = aquality_combobox._apply_appearance_mode(aquality_combobox._fg_color))
        aquality_combobox.place(x = 125 , y = 351)

        # Switch stuff
        global switch_value
        switch_value = "video and audio"
        def switchFunction():
            global switch_value
            if switch_value == "video and audio":
                switch_value = "audio only"
                format_combobox.configure(state = "disabled")
                codec_combobox.configure(state = "disabled")
                fps_combobox.configure(state = "disabled")
                crf_slider.configure(state = "disabled")
                bitrate_entry.configure(state = "disabled")
                crf_radiobutton.configure(state = "disabled")
                bitrate_radiobutton.configure(state = "disabled")
                preset_combobox.configure(state = "disabled")
                tune_combobox.configure(state = "disabled")
                profile_combobox.configure(state = "disabled")
            elif switch_value == "audio only":
                switch_value = "video and audio"
                format_combobox.configure(state = "readonly")
                codec_combobox.configure(state = "readonly")
                fps_combobox.configure(state = "readonly")
                if video_crf_or_bitrate.get() == "crf": crf_slider.configure(state = "normal")
                else: bitrate_entry.configure(state = "normal")
                crf_radiobutton.configure(state = "normal")
                bitrate_radiobutton.configure(state = "normal")
                preset_combobox.configure(state = "normal")
                tune_combobox.configure(state = "normal")
                profile_combobox.configure(state = "normal")

        # Placing the switch and labels
        customtkinter.CTkLabel(advWindow, text = "Audio Only", font = ("arial", 15)).place(x = 27 , y = 417)
        switch = customtkinter.CTkSwitch(advWindow, text = "", command = switchFunction)
        switch.place(x = 110 , y = 420)
        switch.select()
        customtkinter.CTkLabel(advWindow, text = "Video & Audio", font = ("arial", 15)).place(x = 154 , y = 417)

        # Cancel
        def cancelButton():
            advWindow.destroy()
            root.deiconify()

        # Reset everything
        def resetButton():
            switch.select()
            if switch_value == "audio only": switchFunction()
            crf_slider.configure(state = "normal")
            bitrate_entry.configure(state = "disabled")
            abitrate_combobox.configure(state = "normal")
            aquality_combobox.configure(state = "disabled")
            format_combobox.set("MP4 (Default)")
            codec_combobox.set("H.264 (Default)")
            fps_combobox.set("30 (Default)")
            preset_combobox.set("Medium (Default)")
            tune_combobox.set("None (Default)")
            profile_combobox.set("Main (Default)")
            video_crf_or_bitrate.set("crf")
            crfSlider(23)
            bitrate_entry_var.set("")
            aformat_combobox.set("MP3 (Default)")
            audio_quality_or_bitrate.set("bitrate")
            abitrate_combobox.set("320")
            aquality_combobox.set("")

        # Save the ffmpeg command
        def okButton():
            global ffmpeg_command, advanced_quality_settings, advanced_extention, fps
            fps = "30"
            ffmpeg_command = 'ffmpeg -i "input"'
            format_combobox.configure(border_color = "#565B5E")
            bitrate_entry.configure(border_color = "#565B5E")
            aformat_combobox.configure(border_color = "#565B5E")
            if switch_value == "video and audio":
                if format_combobox.get() == "MP4 (Default)": advanced_extention = "mp4"
                else: advanced_extention = format_combobox.get().lower()
                if codec_combobox.get() == "H.264 (Default)": codec = "libx264"
                elif codec_combobox.get() == "H.265": codec = "libx265"
                elif codec_combobox.get() == "AV1": codec = "libaom-av1"
                elif codec_combobox.get() == "MPEG-4": codec = "mpeg4"
                ffmpeg_command = ffmpeg_command + f' -c:v {codec}'
                if fps_combobox.get() == "30 (Default)": fps = "30"
                else: fps = fps_combobox.get()
                ffmpeg_command = ffmpeg_command + f' -filter:v fps=fps={fps}'
                if aformat_combobox.get() == "MP3 (Default)": format_codec = "libmp3lame"
                elif aformat_combobox.get() == "AAC": format_codec = "aac"
                elif aformat_combobox.get() == "OPUS": format_codec = "libopus"
                elif aformat_combobox.get() == "FLAC": format_codec = "flac"
                if format_combobox.get() == "M4A" and aformat_combobox.get() == "FLAC":
                    format_combobox.configure(border_color = "red")
                    aformat_combobox.configure(border_color = "red")
                    return messagebox.showerror(title = "Formats Not Compatible", message = "M4A Container doesn't support FLAC format.")
                if profile_combobox.get() == "Main (Default)": profile = "main"
                else: profile = profile_combobox.get().lower()
                ffmpeg_command = ffmpeg_command + f' -profile {profile}'
                if preset_combobox.get() == "Medium (Default)": preset = "medium"
                else: preset = preset_combobox.get().lower()
                ffmpeg_command = ffmpeg_command + f' -preset {preset}'
                if tune_combobox.get() == "None (Default)":
                    pass
                else:
                    tune = tune_combobox.get().lower().replace(" ", "")
                    ffmpeg_command = ffmpeg_command + f' -tune {tune}'
                if video_crf_or_bitrate.get() == "crf":
                    if crf_slider.get() == "23 (Default)": crf = "23"
                    elif crf_slider.get() == "0 (Loseless Quality)": crf = "0"
                    elif crf_slider.get() == "51 (Highest Quality)": crf = "51"
                    else: crf = crf_slider.get()
                    ffmpeg_command = ffmpeg_command + f' -crf {crf}'
                else:
                    try:
                        if int(bitrate_entry.get()) not in range(100, 50001):
                            bitrate_entry.configure(border_color = "red")
                            return messagebox.showerror(title = "Wrong Video Bitrate", message = "Please select a valid video bitrate (from 100 to 50000).")
                    except ValueError:
                        bitrate_entry.configure(border_color = "red")
                        return messagebox.showerror(title = "Wrong Video Bitrate", message = "Please select a valid video bitrate (from 100 to 50000).")
                    else: fps = fps_combobox.get()
                    bitrate = bitrate_entry.get() + "K"
                    ffmpeg_command = ffmpeg_command + f' -b:v {bitrate}'
                advanced_quality_settings = "video"
            else:
                advanced_quality_settings = "audio"
                if aformat_combobox.get() == "MP3 (Default)":
                    format_codec = "libmp3lame"
                    advanced_extention = "mp3"
                elif aformat_combobox.get() == "WAV":
                    format_codec = "pcm_s32le"
                    advanced_extention = "wav"
                elif aformat_combobox.get() == "AAC":
                    format_codec = "aac"
                    advanced_extention = "aac"
                elif aformat_combobox.get() == "OPUS":
                    format_codec = "libopus"
                    advanced_extention = "opus"
                elif aformat_combobox.get() == "FLAC":
                    format_codec = "flac"
                    advanced_extention = "flac"
                ffmpeg_command = ffmpeg_command + f' -c:a {format_codec}'
            if audio_quality_or_bitrate.get() == "bitrate":
                abitrate = abitrate_combobox.get() + "K"
                ffmpeg_command = ffmpeg_command + f' -b:a {abitrate}'
            else:
                ffmpeg_command = ffmpeg_command + f' -q:a {aquality_combobox.get()}'
            ffmpeg_command = ffmpeg_command + ' -progress pipe:1 "output"'
            print(ffmpeg_command)
            print(advanced_quality_settings)
            print(advanced_extention)
            advWindow.withdraw()
            root.deiconify()
            customtkinter.CTkLabel(root, text = "(Advanced Quality Settings will apply on your next downloads)", font = ("arial", 12)).place(x = 375 , y = 385)

        # Placing the buttons
        customtkinter.CTkButton(advWindow, text = "OK", font = ("arial bold", 20), width = 120, corner_radius = 20, command = okButton).place(x = 565 , y = 415)
        customtkinter.CTkButton(advWindow, text = "Reset", font = ("arial bold", 20), width = 120, corner_radius = 20, command = resetButton).place(x = 435 , y = 415)
        customtkinter.CTkButton(advWindow, text = "Cancel", font = ("arial bold", 20), width = 120, corner_radius = 20, command = cancelButton).place(x = 305 , y = 415)
        root.withdraw()
        advWindow.deiconify()


# Advanced settings button
advanced_quality_settings = "no"
adv_quailty_button = customtkinter.CTkButton(root, text = "Advanced Quality Settings", width = 175, font = ("arial bold", 15), command = AdvancedWindow, corner_radius = 20)
adv_quailty_button.place(x = 460 , y = 415)


# Conversion function
def Conversion(input, ext, seconds):
    global ffmpeg_command
    output = input.replace(f").{ext}", f"_advanced_settings_applied).{advanced_extention}")
    ffmpeg_command = ffmpeg_command.replace("input", input)
    ffmpeg_command = ffmpeg_command.replace("output", output)
    # Progress reader function
    def progress_reader(procs, q):
        while True:
            if procs.poll() is not None: break  # Break if FFmpeg sun-process is closed
            progress_text = procs.stdout.readline()  # Read line from the pipe
            # Break the loop if progress_text is None (when pipe is closed).
            if progress_text is None: break
            progress_text = progress_text.decode("utf-8")  # Convert bytes array to strings
            # Look for "frame=xx"
            if progress_text.startswith("frame="):
                frame = int(progress_text.partition('=')[-1])  # Get the frame number
                q[0] = frame  # Store the last sample
    # Count number of frames
    tot_n_frames = seconds * float(fps)
    # Execute FFmpeg as sub-process with stdout as a pipe
    # Redirect progress to stdout using -progress pipe:1 arguments
    process = subprocess.Popen(shlex.split(ffmpeg_command), stdout=subprocess.PIPE)
    q = [0]  # We don't really need to use a Queue - use a list of size 1
    progress_reader_thread = Thread(target=progress_reader, args=(process, q))  # Initialize progress reader thread
    progress_reader_thread.start()  # Start the thread
    while True:
        if process.poll() is not None: break  # Break if FFmpeg sun-process is closed
        time.sleep(1)  # Sleep 1 second (do some work...)
        n_frame = q[0]  # Read last element from progress_reader - current encoded frame
        progress_percent = (n_frame/tot_n_frames)*100   # Convert to percentage.
        print(f'Progress [%]: {progress_percent:.2f} ')  # Print the progress
        if ext == "mp4": converting_percentage_var.set(f'{progress_percent:.2f}%')  # Show the progress
        else: pass # For some reson, progress doesn't get printed when it's an audio
    process.stdout.close()          # Close stdin pipe.
    progress_reader_thread.join()   # Join thread
    process.wait()                  # Wait for FFmpeg sub-process to finish
    ffmpeg_command = ffmpeg_command.replace(input, "input")
    ffmpeg_command = ffmpeg_command.replace(output, "output")


# Download window
def DownlaodWindow():
    # Starting
    def VideoStart():
        threading.Thread(target = Downloading, args = (downloading_var,)).start()
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
    if platform == "linux" or platform == "linux2": path = f"/home/{os.getlogin()}/Downloads"
    else: path = f"C:/Users\{os.getlogin()}\Downloads"
    global directory
    directory = os.path.realpath(path) # Deafult path in case the user didn't choose
    def BrowseDir(): # Path function
        global directory2
        directory2 = filedialog.askdirectory()
        path_var.set(directory2)

    # When an error happens
    def whenVideoError():
        toggle_button = customtkinter.CTkButton(newWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
        toggle_button.place(x = 550 , y = 347)
        cancel_button = customtkinter.CTkButton(newWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
        cancel_button.place(x = 595 , y = 347)
        download_button = customtkinter.CTkButton(newWindow, text = "Download", font = ("arial bold", 25), command = VideoStart)
        download_button.place(x = 540 , y = 306)
        path_button = customtkinter.CTkButton(newWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", hover_color = "gray25", width = 5, command = BrowseDir, corner_radius = 20)
        path_button.place(x = 430 , y = 347)
        lang_choose.configure(state = "normal")
        try: adv_checkbox.configure(state = "normal")
        except: pass
        downloading_var.set(" ")
        progress_label.configure(text_color = "#DCE4EE")
        progress_size_label.configure(text_color = "#DCE4EE")

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

    # Advanced checker
    def advancedChecker():
        global advanced_quality_settings
        if advanced_quality_settings == "no": advanced_quality_settings = "yes"
        elif advanced_quality_settings == "yes": advanced_quality_settings = "no"

    # Pause/Resume function
    def toggle_download():
        global is_paused
        is_paused = not is_paused
        if is_paused:
            toggle_button = customtkinter.CTkButton(newWindow, text = "▶️", font = ("arial", 15), fg_color = "grey14", hover_color = "gray10", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
            toggle_button.place(x = 550 , y = 347)
            downloading_var.set("Paused")
        else:
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
            try:
                dir2 = os.path.normpath(directory2)
                if platform == "linux" or platform == "linux2": subprocess.Popen(dir2)
                else: subprocess.Popen(f'explorer "{dir2}"')
            except NameError:
                if platform == "linux" or platform == "linux2": subprocess.Popen(directory)
                else: subprocess.Popen(f'explorer "{directory}"')
        except PermissionError:
            try: messagebox.showerror(title = "Permission Denied", message = f"I do not have permission to open '{dir2}'")
            except NameError: messagebox.showerror(title = "Permission Denied", message = f"I do not have permission to open '{directory}'")

    # One Video Downloader
    def VideoDownloader(event = None):
        # Preperations
        global is_paused, is_cancelled
        toggle_button = customtkinter.CTkButton(newWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", hover_color = "gray10", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
        toggle_button.place(x = 550 , y = 347)
        cancel_button = customtkinter.CTkButton(newWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", hover_color = "red4", width = 80, height = 26, command = cancel_download, corner_radius = 20)
        cancel_button.place(x = 595 , y = 347)
        download_button = customtkinter.CTkButton(newWindow, text = "Download", font = ("arial bold", 25), state = "disabled", corner_radius = 20)
        download_button.place(x = 540 , y = 306)
        path_button = customtkinter.CTkButton(newWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", width = 5, state = "disabled", corner_radius = 20)
        path_button.place(x = 430 , y = 347)
        lang_choose.configure(state = "disabled")
        try: adv_checkbox.configure(state = "disabled")
        except: pass
        audio_tags_list = ["251" , "140" , "250" , "249"]
        non_progressive_list = ["137" , "135" , "133", "160"]
        # Download subtitles if selected
        if caps == "yes": CaptionsDownload()
        else: pass
        # Progress stuff
        pytube.request.default_range_size = 2097152  # 2MB chunk size (update progress every 2MB)
        progress_label.configure(text_color = "green")
        progress_size_label.configure(text_color = "LightBlue")

        # If the quality is non progressive video (1080p, 480p, 240p and 144p)
        if quality in non_progressive_list:
            if quality == "137": video = url.streams.filter(res = "1080p").first()
            elif quality == "135": video = url.streams.filter(res = "480p").first()
            elif quality == "133": video = url.streams.filter(res = "240p").first()
            elif quality == "160": video = url.streams.filter(res = "144p").first()
            audio = url.streams.get_by_itag(251)
            size = video.filesize + audio.filesize
            try:
                vname = f"{directory2}/{clean_filename(url.title)}_video.mp4"
                aname = f"{directory2}/{clean_filename(url.title)}_audio.mp3"
            except NameError:
                vname = f"{directory}/{clean_filename(url.title)}_video.mp4"
                aname = f"{directory}/{clean_filename(url.title)}_audio.mp3"
            # Downlaod video
            try:
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
                            progressbar.set(percentage_of_completion/100)
                        else:
                            # When finished
                            break
            except PermissionError:
                whenVideoError()
                path = vname.replace(f"/{clean_filename(url.title)}_video.mp4", "")
                return messagebox.showerror(title = "Permission Error", message = f"I don't have permission to access '{path}'. Change the path or run me as administrator.")
            except FileNotFoundError:
                whenVideoError()
                path = vname.replace(f"/{clean_filename(url.title)}_video.mp4", "")
                return messagebox.showerror(title = "Folder Not Found", message = f"'{path}' is not found. Change the path to an existing folder.")
            toggle_button = customtkinter.CTkButton(newWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
            toggle_button.place(x = 550 , y = 347)
            cancel_button = customtkinter.CTkButton(newWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
            cancel_button.place(x = 595 , y = 347)
            if is_cancelled:
                pass
            else: # Download audio
                downloading_var.set("Downloading audio")
                with open(aname, "wb") as f:
                    is_paused = is_cancelled = False
                    video = request.stream(audio.url) # Get an iterable stream
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
                            # Update progress
                            downloaded += len(chunk)
                            remaining = size - downloaded
                            bytes_downloaded = size - remaining
                            percentage_of_completion = bytes_downloaded / size * 100
                            percentage_var.set(f"{round(percentage_of_completion, 2)}%  ")
                            sizeprogress_var.set(f"{int(bytes_downloaded / 1024 / 1024)} MB  ")
                            progressbar.set(percentage_of_completion/100)
                        else:
                            # When finished
                            break
                # Merge video and audio
                downloading_var.set("Merging")
                final_name = vname.replace("_video", f"_({quality_string})")
                cmd = f'ffmpeg -y -i "{aname}" -i "{vname}" -c copy "{final_name}"'
                subprocess.call(cmd, shell=True)
                os.remove(vname)
                os.remove(aname)
                # Convert if there is a conversion
                if advanced_checker == "yes":
                    downloading_var.set("Converting")
                    Conversion(final_name, "mp4", url.length)
                # Finished
                newWindow.bell()
                downloading_var.set("Finished")
                converting_percentage_var.set("")
                customtkinter.CTkButton(newWindow, text = "Open in File Explorer", font = ("arial bold", 20), command = openFile, corner_radius = 20).place(x = 460 , y = 420)
                global convert_count
                convert_count = 0

        # If the quality is 720p or 360p or audio
        else:
            video = url.streams.get_by_itag(quality)
            size = video.filesize
            if quality in audio_tags_list: ext = "mp3"
            else: ext = "mp4"
            try: vname = f"{directory2}/{clean_filename(url.title)}_({quality_string}).{ext}"
            except NameError: vname = f"{directory}/{clean_filename(url.title)}_({quality_string}).{ext}"
            try:
                with open(vname, "wb") as f:
                    is_paused = is_cancelled = False
                    video = request.stream(video.url) # get an iterable stream
                    downloaded = 0
                    while True:
                        if is_cancelled:
                            toggle_button = customtkinter.CTkButton(newWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
                            toggle_button.place(x = 550 , y = 347)
                            cancel_button = customtkinter.CTkButton(newWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
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
                            progressbar.set(percentage_of_completion/100)
                        else:
                            # When finished
                            toggle_button = customtkinter.CTkButton(newWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
                            toggle_button.place(x = 550 , y = 347)
                            cancel_button = customtkinter.CTkButton(newWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
                            cancel_button.place(x = 595 , y = 347)
                            # Convert if there is a conversion
                            if advanced_checker == "yes":
                                downloading_var.set("Converting")
                                Conversion(vname, ext, url.length)
                            newWindow.bell()
                            downloading_var.set("Finished")
                            converting_percentage_var.set("")
                            customtkinter.CTkButton(newWindow, text = "Open in File Explorer", font = ("arial bold", 20), command = openFile, corner_radius = 20).place(x = 460 , y = 420)
                            break
            except PermissionError:
                whenVideoError()
                path = vname.replace(f"/{clean_filename(url.title)}_({quality_string}).{ext}", "")
                return messagebox.showerror(title = "Permission Error", message = f"I don't have permission to access '{path}'. Change the path or run me as administrator.")
            except FileNotFoundError:
                whenVideoError()
                path = vname.replace(f"/{clean_filename(url.title)}_({quality_string}).{ext}", "")
                return messagebox.showerror(title = "Folder Not Found", message = f"'{path}' is not found. Change the path to an existing folder.")
        if is_cancelled:
            msg_box = messagebox.askquestion(title = "Delete Canceled File", message = f"Do you want to delete '{vname}'?")
            if msg_box == "yes": os.remove(vname)


    whenOpening() # Disable widgets in root to load
    try: # Get url object
        global url
        url = YouTube(link)
        quality = str(quality_var.get())
        if not "youtu" in link:
            raise pytube.exceptions.RegexMatchError
    except pytube.exceptions.RegexMatchError:
        whenError()
        return messagebox.showerror(title = "Link Not Valid", message = "Please enter a valid video link.")
    global video
    global size
    try: # Get video and size
        if quality == "0":
            whenError()
            return messagebox.showerror(title = "Format Not Selected", message = "Please select a format to download.")
        elif quality == "137":
            video = url.streams.filter(res = "1080p").first()
            audio = url.streams.get_by_itag(251)
            size = video.filesize + audio.filesize
        elif quality == "135":
            video = url.streams.filter(res = "480p").first()
            audio = url.streams.get_by_itag(251)
            size = video.filesize + audio.filesize
        elif quality == "133":
            video = url.streams.filter(res = "240p").first()
            audio = url.streams.get_by_itag(251)
            size = video.filesize + audio.filesize
        elif quality == "160":
            video = url.streams.filter(res = "144p").first()
            audio = url.streams.get_by_itag(251)
            size = video.filesize + audio.filesize
        else:
            video = url.streams.get_by_itag(quality) # 1080p, 720, 360p, *audio
            size = video.filesize
        size_string = f"{round(size/1024/1024, 2)} MB"
    except urllib.error.URLError as e:
        print(e)
        whenError()
        return messagebox.showerror(title = "Not Connected", message = "Please check your internet connection.")
    except KeyError as e:
        print(f"KeyError: {e}")
        whenError()
        return messagebox.showerror(title = "Something Went Wrong", message = f"I can't retrieve '{url.title}' at the moment. Change the selected quality or try again later.")
    except AttributeError as e:
        print(f"AttributeError: {e}")
        whenError()
        return messagebox.showerror(title = "Quality Not Available",
        message = f"I can't retrieve '{url.title}' in the quality that you chose. Change the selected quality or try again later.")
    except pytube.exceptions.LiveStreamError as e:
        print(e)
        whenError()
        return messagebox.showerror(title = "Video is Live", message = "Can't download a live video.")
    except pytube.exceptions.AgeRestrictedError as e:
        print(e)
        whenError()
        return messagebox.showerror(title = "Age Restricted", message = "This video is age restricted.")
    except pytube.exceptions.MembersOnly as e:
        print(e)
        whenError()
        return messagebox.showerror(title = "Members Only", message = "This video is members only.")
    except pytube.exceptions.VideoPrivate as e:
        print(e)
        whenError()
        return messagebox.showerror(title = "Private Video", message = "This video is private.")
    except pytube.exceptions.VideoRegionBlocked as e:
        print(e)
        whenError()
        return messagebox.showerror(title = "Region Blocked", message = "This video is region blocked.")
    except pytube.exceptions.VideoUnavailable as e:
        print(e)
        whenError()
        return messagebox.showerror(title = "Video Unavailable", message = "This video is unavailable.")

    # Get transcripts
    try:
        video_id = extract.video_id(link)
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        lang_choose_state = "readonly"
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
    if quality == "160": quality_string = "144p"
    elif quality == "133": quality_string = "240p"
    elif quality == "18": quality_string = "360p"
    elif quality == "135": quality_string = "480p"
    elif quality == "22": quality_string = "720p"
    elif quality == "137": quality_string = "1080p"
    elif quality == "249": quality_string = "50kbps"
    elif quality == "250": quality_string = "70kbps"
    elif quality == "140": quality_string = "128kbps"
    elif quality == "251": quality_string = "160kbps"

    # Video form creating
    newWindow = customtkinter.CTkToplevel() # Toplevel object which will be treated as a new window
    newWindow.withdraw()
    newWindow.title("Video Downloader")
    width = 700
    height = 460
    x = (newWindow.winfo_screenwidth() // 2) - (width // 2)
    y = (newWindow.winfo_screenheight() // 2) - (height // 2)
    newWindow.geometry(f"{width}x{height}+{x}+{y}")
    newWindow.maxsize(700, 460)
    newWindow.minsize(700, 460)
    if platform == "linux" or platform == "linux2": pass
    else: newWindow.iconbitmap("YDICO.ico")
    newWindow.protocol("WM_DELETE_WINDOW", onClosing)
    # newWindow.bind("<Return>", VideoDownloader)

    # Downloading label
    downloading_var = StringVar()
    customtkinter.CTkLabel(newWindow, textvariable = downloading_var, font = ("arial", 25)).place(x = 265 , y = 418)
    global converting_percentage_var
    converting_percentage_var = StringVar()
    customtkinter.CTkLabel(newWindow, textvariable = converting_percentage_var, font = ("arial", 22)).place(x = 410 , y = 418)

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

    # Get thumbnail
    def download_thumbnail():
        try:
            response = requests.get(url.thumbnail_url)
            response.raise_for_status()  # Raise an exception if there's an error
        except requests.exceptions.ConnectionError:
            return messagebox.showinfo(title = "Connection Error", message = f"Check your internet connection and try again.")
        thumb_dir = filedialog.askdirectory()
        thumb_path = f"{thumb_dir}/{url.title}_thumbnail.png"
        with open(thumb_path, 'wb') as file:
            file.write(response.content)
        messagebox.showinfo(title = "Thumbnail Downloaded", message = f"Thumbnail has been downloaded successfully in '{thumb_dir}'")
    thumbnail_button = customtkinter.CTkButton(newWindow, text = "Download Thumbnail", font = ("arial bold", 18), command = Thread(target = download_thumbnail).start, corner_radius = 20)
    thumbnail_button.place(x = 480 , y = 260)

    # Path change
    customtkinter.CTkLabel(newWindow, text = "Download Path:", font = ("arial bold", 20)).place(x = 20 , y = 345)
    path_var = StringVar()
    customtkinter.CTkEntry(newWindow, width = 245, textvariable = path_var, state = "disabled", height = 26, corner_radius = 20).place(x = 175 , y = 347)
    try:
        path_var.set(directory2)
    except NameError:
        path_var.set(directory)
    path_button = customtkinter.CTkButton(newWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", hover_color = "gray25", width = 5, height = 26, command = BrowseDir, corner_radius = 20)
    path_button.place(x = 430 , y = 347)

    # Subtitle Combobox
    customtkinter.CTkLabel(newWindow, text = "Subtitle:", font = ("arial bold", 20), corner_radius = 20).place(x = 325 , y = 315)
    lang_choose = customtkinter.CTkComboBox(newWindow, width = 100, height = 26, values = ["None", "Arabic", "English"], state = lang_choose_state, corner_radius = 15)
    lang_choose._entry.configure(readonlybackground = lang_choose._apply_appearance_mode(lang_choose._fg_color))
    lang_choose.set("None")
    lang_choose.place(x = 430 , y = 315)

    # Progress bar/labels
    percentage_var = StringVar()
    sizeprogress_var = StringVar()
    progress_label = customtkinter.CTkLabel(newWindow, textvariable = percentage_var, font = ("arial", 22))
    progress_label.place(x = 540 , y = 384)
    progress_size_label = customtkinter.CTkLabel(newWindow, textvariable = sizeprogress_var, font = ("arial", 22))
    progress_size_label.place(x = 624 , y = 384)
    percentage_var.set("0.00%")
    sizeprogress_var.set("0 MB")
    progressbar = customtkinter.CTkProgressBar(newWindow, width = 505)
    progressbar.place(x = 20 , y = 393)
    progressbar.set(0)

    # Pause/Resume & Cancel buttons
    toggle_button = customtkinter.CTkButton(newWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
    toggle_button.place(x = 550 , y = 347)
    cancel_button = customtkinter.CTkButton(newWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
    cancel_button.place(x = 595 , y = 347)

    # Advanced quality settings check
    global advanced_checker
    advanced_checker = "no"
    if not advanced_quality_settings == "no":
        audio_quality_list = ["160kbps" , "128kbps" , "70kbps" , "50kbps"]
        if advanced_quality_settings == "audio":
            if quality_string in audio_quality_list:
                adv_checkbox = customtkinter.CTkCheckBox(newWindow, text = "Apply Advanced Quality Settings", font = ("arial bold", 15), command = advancedChecker)
                adv_checkbox.place(x = 410 , y = 225)
                adv_checkbox.select()
                advanced_checker = "yes"
        else:
            if not quality_string in audio_quality_list:
                adv_checkbox = customtkinter.CTkCheckBox(newWindow, text = "Apply Advanced Quality Settings", font = ("arial bold", 15), command = advancedChecker)
                adv_checkbox.place(x = 410 , y = 225)
                adv_checkbox.select()
                advanced_checker = "yes"

    # Download button
    download_button = customtkinter.CTkButton(newWindow, text = "Download", font = ("arial bold", 25), command = VideoStart, corner_radius = 20)
    download_button.place(x = 540 , y = 306)

    # Back to home button
    back_button = customtkinter.CTkButton(newWindow, text = "Back To Home", font = ("arial bold", 20), command = backHome, corner_radius = 20)
    back_button.place(x = 20 , y = 420)

    # Return to normal state in root
    whenError()
    root.withdraw()
    newWindow.deiconify()


# Playlist window
def PlaylistWindow():
    # Starting
    def pVideoStart():
        threading.Thread(target = Downloading, args = (downloading_var,)).start()
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
    if platform == "linux" or platform == "linux2": path = f"/home/{os.getlogin()}/Downloads"
    else: path = f"C:/Users\{os.getlogin()}\Downloads"
    global directory
    directory = os.path.realpath(path) # Deafult path in case the user didn't choose
    def pBrowseDir(): # Path function
        global directory2
        directory2 = filedialog.askdirectory()
        ppath_var.set(directory2)

    # When an error happens
    def whenPlaylistError():
        toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
        toggle_button.place(x = 550 , y = 347)
        cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
        cancel_button.place(x = 595 , y = 347)
        download_button = customtkinter.CTkButton(pWindow, text = "Download", font = ("arial bold", 25), command = pVideoStart)
        download_button.place(x = 540 , y = 306)
        path_button = customtkinter.CTkButton(pWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", hover_color = "gray25", width = 5, command = pBrowseDir, corner_radius = 20)
        path_button.place(x = 430 , y = 347)
        lang_choose.configure(state = "normal")
        menubutton.configure(state = "normal")
        try: adv_checkbox.configure(state = "normal")
        except: pass
        downloading_var.set(" ")
        downloadcounter_var.set("")
        progress_label.configure(text_color = "#DCE4EE")
        progress_size_label.configure(text_color = "#DCE4EE")

    # Captions download
    def pCaptionsDownload(vid_link, title):
        if vid_link in vids_subs:
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
                with open(f"{directory2}/{clean_filename(title)}_{sub}_{lang}.srt", "w", encoding = "utf-8") as srt_file:
                    srt_file.write(srt_formatted)
            except NameError:
                with open(f"{directory}/{clean_filename(title)}_{sub}_{lang}.srt", "w", encoding = "utf-8") as srt_file:
                    srt_file.write(srt_formatted)
        else:
            print(f"{title} not in caption list")

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

    # Advanced checker
    def advancedChecker():
        global advanced_quality_settings
        if advanced_quality_settings == "no": advanced_quality_settings = "yes"
        elif advanced_quality_settings == "yes": advanced_quality_settings = "no"

    # Pause/Resume function
    def toggle_download():
        global is_paused
        is_paused = not is_paused
        if is_paused:
            toggle_button = customtkinter.CTkButton(pWindow, text = "▶️", font = ("arial", 15), fg_color = "grey14", hover_color = "gray10", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
            toggle_button.place(x = 550 , y = 347)
            downloading_var.set("Paused")
        else:
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
            try:
                dir2 = os.path.normpath(directory2)
                if platform == "linux" or platform == "linux2": subprocess.Popen(dir2)
                else: subprocess.Popen(f'explorer "{dir2}"')
            except NameError:
                if platform == "linux" or platform == "linux2": subprocess.Popen(directory)
                else: subprocess.Popen(f'explorer "{directory}"')
        except PermissionError:
            try: messagebox.showerror(title = "Permission Denied", message = f"I do not have permission to open '{dir2}'")
            except NameError: messagebox.showerror(title = "Permission Denied", message = f"I do not have permission to open '{directory}'")

    # Download playlist
    def PlaylistDownloader(event = None):
        # Preperations
        global is_paused, is_cancelled
        is_paused = is_cancelled = False
        toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
        toggle_button.place(x = 550 , y = 347)
        cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, command = cancel_download, corner_radius = 20)
        cancel_button.place(x = 595 , y = 347)
        download_button = customtkinter.CTkButton(pWindow, text = "Download", font = ("arial bold", 25), state = "disabled", corner_radius = 20)
        download_button.place(x = 540 , y = 306)
        path_button = customtkinter.CTkButton(pWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", width = 5, state = "disabled", corner_radius = 20)
        path_button.place(x = 430 , y = 347)
        lang_choose.configure(state = "disabled")
        menubutton.configure(state = "disabled")
        try: adv_checkbox.configure(state = "disabled")
        except: pass
        audio_tags_list = ["251" , "140" , "250" , "249"]
        non_progressive_list = ["137" , "135" , "133", "160"]
        # Progress stuff
        pytube.request.default_range_size = 2097152  # 2MB chunk size (update progress every 2MB)
        progress_label.configure(text_color = "green")
        progress_size_label.configure(text_color = "LightBlue")

        # Download playlist
        if vids_counter == 0:
            toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
            toggle_button.place(x = 550 , y = 347)
            cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
            cancel_button.place(x = 595 , y = 347)
            download_button = customtkinter.CTkButton(pWindow, text = "Download", font = ("arial bold", 25), command = pVideoStart, corner_radius = 20)
            download_button.place(x = 540 , y = 306)
            path_button = customtkinter.CTkButton(pWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", hover_color = "gray25", width = 5, command = pBrowseDir, corner_radius = 20)
            path_button.place(x = 430 , y = 347)
            lang_choose.configure(state = "normal")
            menubutton.configure(state = "normal")
            downloading_var.set(" ")
            return messagebox.showerror(title = "No Selected Video", message = "Please select at least one video.")
        downloaded_counter = 0

        # If the quality is non progressive video (1080p, 480p, 240p and 144p)
        if quality in non_progressive_list:
            for url in urls_list:
                if is_cancelled: break
                toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
                toggle_button.place(x = 550 , y = 347)
                cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, command = cancel_download, corner_radius = 20)
                cancel_button.place(x = 595 , y = 347)
                raw_data = urllib.request.urlopen(url.thumbnail_url).read()
                photo = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (270 , 150))
                if quality == "137": video = url.streams.filter(res = "1080p").first()
                elif quality == "135": video = url.streams.filter(res = "480p").first()
                elif quality == "133": video = url.streams.filter(res = "240p").first()
                elif quality == "160": video = url.streams.filter(res = "144p").first()
                audio = url.streams.get_by_itag(251)
                size = video.filesize + audio.filesize
                if f"✔️ {p.repr(clean_filename(url.title))} | {to_hms(url.length)} | {round(size/1024/1024, 2)} MB" in vids_list: pass
                else: continue
                # Download subtitles if selected
                if caps == "yes": pCaptionsDownload(url.watch_url, url.title)
                else: pass
                ext = "mp4"
                try:
                    vname = f"{directory2}/{clean_filename(url.title)}_video.mp4"
                    aname = f"{directory2}/{clean_filename(url.title)}_audio.mp3"
                except NameError:
                    vname = f"{directory}/{clean_filename(url.title)}_video.mp4"
                    aname = f"{directory}/{clean_filename(url.title)}_audio.mp3"
                # Downlaod video
                try:
                    with open(vname, "wb") as f:
                        percentage_var.set(f"0.00%  ")
                        sizeprogress_var.set(f"0 MB  ")
                        downloading_var.set("Downloading")
                        converting_percentage_var.set("")
                        progressbar.set(0)
                        downloaded_counter = downloaded_counter + 1
                        downloadcounter_var.set(f"{downloaded_counter}/{vids_counter}")
                        thumbnail.configure(image = photo)
                        downloaded = 0
                        is_paused = is_cancelled = False
                        video = request.stream(video.url) # Get an iterable stream
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
                                progressbar.set(percentage_of_completion/100)
                            else:
                                # When finished
                                break
                except PermissionError:
                    whenPlaylistError()
                    path = vname.replace(f"/{clean_filename(url.title)}_video.mp4", "")
                    return messagebox.showerror(title = "Permission Error", message = f"I don't have permission to access '{path}'. Change the path or run me as administrator.")
                except FileNotFoundError:
                    whenPlaylistError()
                    path = vname.replace(f"/{clean_filename(url.title)}_video.mp4", "")
                    return messagebox.showerror(title = "Folder Not Found", message = f"'{path}' is not found. Change the path to an existing folder.")
                toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
                toggle_button.place(x = 550 , y = 347)
                cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
                cancel_button.place(x = 595 , y = 347)
                if is_cancelled:
                    pass
                else: # Download audio
                    downloading_var.set("Downloading audio")
                    with open(aname, "wb") as f:
                        is_paused = is_cancelled = False
                        video = request.stream(audio.url) # Get an iterable stream
                        # downloaded = 0
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
                                downloaded += len(chunk)
                                remaining = size - downloaded
                                bytes_downloaded = size - remaining
                                percentage_of_completion = bytes_downloaded / size * 100
                                percentage_var.set(f"{round(percentage_of_completion, 2)}%  ")
                                sizeprogress_var.set(f"{int(bytes_downloaded / 1024 / 1024)} MB  ")
                                progressbar.set(percentage_of_completion/100)
                            else:
                                # When finished
                                break
                    # Merge video and audio
                    downloading_var.set("Merging")
                    final_name = vname.replace("_video", f"_({quality_string})")
                    cmd = f'ffmpeg -y -i "{aname}"  -r 30 -i "{vname}"  -filter:a aresample=async=1 -c:a flac -c:v copy "{final_name}"'
                    subprocess.call(cmd, shell=True)
                    os.remove(vname)
                    os.remove(aname)
                    # Convert if there is a conversion
                    if advanced_checker == "yes":
                        downloading_var.set("Converting")
                        Conversion(final_name, "mp4", url.length)

        # If playlist is 720p, 360p, *audio
        else:
            for url in urls_list:
                if is_cancelled: break
                toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
                toggle_button.place(x = 550 , y = 347)
                cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, command = cancel_download, corner_radius = 20)
                cancel_button.place(x = 595 , y = 347)
                raw_data = urllib.request.urlopen(url.thumbnail_url).read()
                photo = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (270 , 150))
                video = url.streams.get_by_itag(quality)
                size = video.filesize
                if f"✔️ {p.repr(clean_filename(url.title))} | {to_hms(url.length)} | {round(size/1024/1024, 2)} MB" in vids_list: pass
                else: continue
                # Download subtitles if selected
                if caps == "yes": pCaptionsDownload(url.watch_url, url.title)
                else: pass
                if quality in audio_tags_list: ext = "mp3"
                else: ext = "mp4"
                try: vname = f"{directory2}/{clean_filename(url.title)}_({quality_string}).{ext}"
                except NameError: vname = f"{directory}/{clean_filename(url.title)}_({quality_string}).{ext}"
                try:
                    with open(vname, "wb") as f:
                        percentage_var.set(f"0.00%  ")
                        sizeprogress_var.set(f"0 MB  ")
                        downloading_var.set("Downloading")
                        converting_percentage_var.set("")
                        progressbar.set(0)
                        downloaded_counter = downloaded_counter + 1
                        downloadcounter_var.set(f"{downloaded_counter}/{vids_counter}")
                        thumbnail.configure(image = photo)
                        downloaded = 0
                        video = request.stream(video.url) # Get an iterable stream
                        while True:
                            if is_cancelled:
                                downloading_var.set("Canceled")
                                toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
                                toggle_button.place(x = 550 , y = 347)
                                cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
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
                                progressbar.set(percentage_of_completion/100)
                            else:
                                # Convert if there is a conversion
                                if advanced_checker == "yes":
                                    toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
                                    toggle_button.place(x = 550 , y = 347)
                                    cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
                                    cancel_button.place(x = 595 , y = 347)
                                    downloading_var.set("Converting")
                                    Conversion(vname, ext, url.length)
                                break # No more data = Finished
                except PermissionError:
                    whenPlaylistError()
                    path = vname.replace(f"/{clean_filename(url.title)}_({quality_string}).{ext}", "")
                    return messagebox.showerror(title = "Permission Error", message = f"I don't have permission to access '{path}'. Change the path or run me as administrator.")
                except FileNotFoundError:
                    whenPlaylistError()
                    path = vname.replace(f"/{clean_filename(url.title)}_({quality_string}).{ext}", "")
                    return messagebox.showerror(title = "Folder Not Found", message = f"'{path}' is not found. Change the path to an existing folder.")

        # When finished
        toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
        toggle_button.place(x = 550 , y = 347)
        cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
        cancel_button.place(x = 595 , y = 347)
        if is_cancelled:
            msg_box = messagebox.askquestion(title = "Delete Canceled File", message = f"Do you want to delete '{vname}'?")
            if msg_box == "yes": os.remove(vname)
        else:
            downloadcounter_var.set("")
            pWindow.bell()
            downloading_var.set("Finished")
            converting_percentage_var.set("")
            customtkinter.CTkButton(pWindow, text = "Open in File Explorer", font = ("arial bold", 20), command = openFile, corner_radius = 20).place(x = 460 , y = 420)


    # Get playlist info, get link and check errors
    whenOpening()
    try:
        urls = Playlist(link)
        quality = str(quality_var.get())
        if not "youtu" in link or not "playlist" in link: raise KeyError()
    except KeyError:
        whenError()
        return messagebox.showerror(title = "Link Not Valid", message = "Please enter a valid link.")
    except pytube.exceptions.RegexMatchError:
        whenError()
        return messagebox.showerror(title = "Link Not Valid", message = "Please enter a valid link.")
    if quality == "0":
        whenError()
        return messagebox.showerror(title = "Format Not Selected", message = "Please select a format to download.")
    else:
        not_supported_list = ["250" , "249"]
        if quality in not_supported_list:
            whenError()
            return messagebox.showerror(title = "Not Supported", message = "Currently, we don't support downloading playlists in 50kbps or 70kbps.")
        else:
            global vids_counter, psize, plength
            vids_list = []
            urls_list = []
            plength = 0
            psize = 0
            vids_counter = 0
            vids_subs = []
            pl_tst_counter = 0
            p = reprlib.Repr()
            p.maxstring = 40
            for url in urls.videos:
                pl_tst_counter = pl_tst_counter + 1
                print(f"================================")
                print(f"({pl_tst_counter}) loop started")
                try:
                    if quality == "137":
                        video = url.streams.filter(res = "1080p").first()
                        audio = url.streams.get_by_itag(251)
                        size = video.filesize + audio.filesize
                    elif quality == "135":
                        video = url.streams.filter(res = "480p").first()
                        audio = url.streams.get_by_itag(251)
                        size = video.filesize + audio.filesize
                    elif quality == "133":
                        video = url.streams.filter(res = "240p").first()
                        audio = url.streams.get_by_itag(251)
                        size = video.filesize + audio.filesize
                    elif quality == "160":
                        video = url.streams.filter(res = "144p").first()
                        audio = url.streams.get_by_itag(251)
                        size = video.filesize + audio.filesize
                    else:
                        video = url.streams.get_by_itag(quality) # 1080p, 720, 360p, *audio
                        size = video.filesize
                    print(f"({pl_tst_counter}) got video item")
                except urllib.error.URLError as e:
                    print(e)
                    whenError()
                    return messagebox.showerror(title = "Not Connected", message = "Please check your internet connection.")
                except pytube.exceptions.LiveStreamError as e:
                    print(e)
                    messagebox.showwarning(title = "Video is Live", message = f"I couldn't retrieve '{url.title}' because it's live.\nThe load of the playlist will continue.")
                    continue
                except KeyError as e:
                    print(f"KeyError: {e}")
                    messagebox.showwarning(title = "Something Went Wrong", message = f"I can't retrieve '{url.title}' at the moment. Change the selected quality or try again later.\nThe load of the playlist will continue.")
                    continue
                except AttributeError as e:
                    print(f"AttributeError: {e}")
                    messagebox.showwarning(title = "Quality Not Available", message = f"I can't retrieve '{url.title}' in the quality that you chose. Change the selected quality or try again later.\nThe load of the playlist will continue.")
                    continue
                try:
                    video_id = extract.video_id(url.watch_url)
                    YouTubeTranscriptApi.list_transcripts(video_id)
                    vids_subs.append(url.watch_url)
                    print(f"({pl_tst_counter}) found subtitle")
                except:
                    print(f"({pl_tst_counter}) no subtitle")
                psize = psize + size
                size_string = round(psize/1024/1024, 2)
                plength = plength + url.length
                vids_list.append(f"✔️ {p.repr(clean_filename(url.title))} | {to_hms(url.length)} | {round(size/1024/1024, 2)} MB")
                urls_list.append(url)
                vids_counter = vids_counter + 1
                ploading_counter_var.set(f"({vids_counter})")
                print(f"({pl_tst_counter}) got size + length + added vid_option to list")
    if vids_list == []: # If an exception occured on every video...
        whenError()
        return messagebox.showerror(title = "Something Went Wrong", message = f"I can't retrieve this playlist at the moment. Change the selected quality or try again later.")

    # Getting playlist thumbnail
    try:
        raw_data = urllib.request.urlopen(url.thumbnail_url).read()
        photo = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (270 , 150))
    except UnboundLocalError:
        whenError()
        return messagebox.showerror(title = "Playlist is Unavailable",
                                    message = "The cause for this may be one of the following:\n- Playlist is private\n- Playlist is age-restricted\n- Playlist is region blocked\n- Playlist is members only")

    # Playlist labels info
    r = reprlib.Repr()
    r.maxstring = 60    # max characters displayed for strings
    date_format = "%d/%m/%Y"
    if quality == "160": quality_string = "144p"
    elif quality == "133": quality_string = "240p"
    elif quality == "18": quality_string = "360p"
    elif quality == "135": quality_string = "480p"
    elif quality == "22": quality_string = "720p"
    elif quality == "137": quality_string = "1080p"
    elif quality == "249": quality_string = "50kbps"
    elif quality == "250": quality_string = "70kbps"
    elif quality == "140": quality_string = "128kbps"
    elif quality == "251": quality_string = "160kbps"

    # Playlist form creating
    pWindow = customtkinter.CTkToplevel()
    pWindow.withdraw()
    pWindow.title("Playlist Downloader")
    width = 700
    height = 460
    x = (pWindow.winfo_screenwidth() // 2) - (width // 2)
    y = (pWindow.winfo_screenheight() // 2) - (height // 2)
    pWindow.geometry(f"{width}x{height}+{x}+{y}")
    pWindow.maxsize(700, 460)
    pWindow.minsize(700, 460)
    if platform == "linux" or platform == "linux2": pass
    else: pWindow.iconbitmap("YDICO.ico")
    pWindow.protocol("WM_DELETE_WINDOW", onClosing)
    # pWindow.bind("<Return>", PlaylistDownloader)

    # Downloading label
    downloading_var = StringVar()
    customtkinter.CTkLabel(pWindow, textvariable = downloading_var, font = ("arial", 25)).place(x = 305 , y = 418)
    downloadcounter_var = StringVar()
    customtkinter.CTkLabel(pWindow, textvariable = downloadcounter_var, font = ("arial", 25), text_color = "LightBlue").place(rely = 1.0, relx = 1.0, x = -405, y = -13, anchor = SE)
    global converting_percentage_var
    converting_percentage_var = StringVar()
    customtkinter.CTkLabel(pWindow, textvariable = converting_percentage_var, font = ("arial", 25)).place(x = 450 , y = 418)

    # Playlist labels
    length_var = StringVar()
    length_var.set(to_hms(plength))
    size_var = StringVar()
    size_var.set(f"{size_string} MB")
    videos_var = IntVar()
    videos_var.set(vids_counter)
    thumbnail = customtkinter.CTkLabel(pWindow, text = "", image = photo)
    thumbnail.place(x = 220 , y = 0)
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

    # Get thumbnail
    def download_thumbnail():
        if messagebox.askokcancel(title = "Download Thumbnails", message = f"Do you want to download the thumbnails of all the videos?"):
            thumb_dir = filedialog.askdirectory()
            try:
                for url in urls_list:
                    # Below line doesn't work properly for some reason
                    # if f"✔️ {p.repr(clean_filename(url.title))} | {to_hms(url.length)} | {round(size/1024/1024, 2)} MB" in vids_list:
                    response = requests.get(url.thumbnail_url)
                    response.raise_for_status()
                    thumb_path = f"{thumb_dir}/{url.title}_thumbnail.png"
                    with open(thumb_path, 'wb') as file:
                        file.write(response.content)
            except requests.exceptions.ConnectionError:
                return messagebox.showinfo(title = "Connection Error", message = f"Check your internet connection and try again.")
            messagebox.showinfo(title = "Thumbnails Downloaded", message = f"Thumbnails has been downloaded successfully in '{thumb_dir}'")
    thumbnail_button = customtkinter.CTkButton(pWindow, text = "Download Thumbnail", font = ("arial bold", 18), command = Thread(target = download_thumbnail).start, corner_radius = 20)
    thumbnail_button.place(x = 480 , y = 230)

    # Path change
    customtkinter.CTkLabel(pWindow, text = "Download Path:", font = ("arial bold", 20)).place(x = 20 , y = 345)
    ppath_var = StringVar()
    customtkinter.CTkEntry(pWindow, width = 245, height = 26, textvariable = ppath_var, state = "disabled", corner_radius = 20).place(x = 175 , y = 347)
    try:
        ppath_var.set(directory2)
    except NameError:
        ppath_var.set(directory)
    path_button = customtkinter.CTkButton(pWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", hover_color = "gray25", width = 5, height = 26, command = pBrowseDir, corner_radius = 20)
    path_button.place(x = 430 , y = 347)

    # Subtitle Combobox
    if vids_subs == []:
        lang_choose_state = "disabled"
        caps = "no"
    else:
        lang_choose_state = "readonly"
        caps = "yes"
    print(vids_subs)
    customtkinter.CTkLabel(pWindow, text = "Subtitle:", font = ("arial bold", 20)).place(x = 340 , y = 315)
    lang_choose = customtkinter.CTkComboBox(pWindow, width = 100, height = 26, values = ["None", "Arabic", "English"], state = lang_choose_state, corner_radius = 15)
    lang_choose._entry.configure(readonlybackground = lang_choose._apply_appearance_mode(lang_choose._fg_color))
    lang_choose.set("None")
    lang_choose.place(x = 430 , y = 315)

    # Video selector
    menubutton = customtkinter.CTkOptionMenu(pWindow, font = ("arial", 14), values = vids_list, command = videoSelector, corner_radius = 13)
    menubutton.set("Open Videos Menu")
    menubutton.place(x = 525 , y = 270)

    # Progress bar/labels
    percentage_var = StringVar()
    sizeprogress_var = StringVar()
    progress_label = customtkinter.CTkLabel(pWindow, textvariable = percentage_var, font = ("arial", 22))
    progress_label.place(x = 540 , y = 384)
    progress_size_label = customtkinter.CTkLabel(pWindow, textvariable = sizeprogress_var, font = ("arial", 22))
    progress_size_label.place(x = 624 , y = 384)
    percentage_var.set("0.00%")
    sizeprogress_var.set("0 MB")
    progressbar = customtkinter.CTkProgressBar(pWindow, width = 505)
    progressbar.place(x = 20 , y = 395)
    progressbar.set(0)

    # Pause/Resume & Cancel buttons
    toggle_button = customtkinter.CTkButton(pWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
    toggle_button.place(x = 550 , y = 347)
    cancel_button = customtkinter.CTkButton(pWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
    cancel_button.place(x = 595 , y = 347)

    # Advanced quality settings check
    global advanced_checker
    advanced_checker = "no"
    if not advanced_quality_settings == "no":
        audio_quality_list = ["160kbps" , "128kbps" , "70kbps" , "50kbps"]
        if advanced_quality_settings == "audio":
            if quality_string in audio_quality_list:
                adv_checkbox = customtkinter.CTkCheckBox(pWindow, text = "Apply Advanced Quality Settings", font = ("arial bold", 15), command = advancedChecker)
                adv_checkbox.place(x = 410 , y = 195)
                adv_checkbox.select()
                advanced_checker = "yes"
        else:
            if not quality_string in audio_quality_list:
                adv_checkbox = customtkinter.CTkCheckBox(pWindow, text = "Apply Advanced Quality Settings", font = ("arial bold", 15), command = advancedChecker)
                adv_checkbox.place(x = 410 , y = 195)
                adv_checkbox.select()
                advanced_checker = "yes"

    # Download button
    download_button = customtkinter.CTkButton(pWindow, text = "Download", font = ("arial bold", 25), command = pVideoStart, corner_radius = 20)
    download_button.place(x = 540 , y = 306)

    # Back to home button
    back_button = customtkinter.CTkButton(pWindow, text = "Back To Home", font = ("arial bold", 20), command = backHome, corner_radius = 20)
    back_button.place(x = 20 , y = 420)

    # Return to normal state in root
    whenError()
    root.withdraw()
    pWindow.deiconify()

# Search window
def SearchWindow():
    # For length format
    def to_hms(s):
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return "{}:{:0>2}:{:0>2}".format(h, m, s)
    # Disable root
    whenOpening()
    # Window creating
    search_text = search_var.get()
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
    sWindow = customtkinter.CTkToplevel()
    sWindow.title(f'Search Results For "{search_text}"')
    sWindow.withdraw()
    # On closing
    def onClosing():
        sWindow.destroy()
        root.deiconify()
    width = 700
    height = 460
    x = (sWindow.winfo_screenwidth() // 2) - (width // 2)
    y = (sWindow.winfo_screenheight() // 2) - (height // 2)
    sWindow.geometry(f"{width}x{height}+{x}+{y}")
    sWindow.maxsize(700, 460)
    sWindow.minsize(700, 460)
    if platform == "linux" or platform == "linux2": pass
    else: sWindow.iconbitmap("YDICO.ico")
    sWindow.withdraw()
    sWindow.protocol("WM_DELETE_WINDOW", onClosing)
    global to_download
    to_download = []
    def checkboxes():
        global to_download
        if cb_var1.get() == 1:
            if search.results[0] not in to_download: to_download.append(search.results[0])
        else:
            if search.results[0] in to_download: to_download.remove(search.results[0])
        if cb_var2.get() == 1:
            if search.results[1] not in to_download: to_download.append(search.results[1])
        else:
            if search.results[1] in to_download: to_download.remove(search.results[1])
        if cb_var3.get() == 1:
            if search.results[2] not in to_download: to_download.append(search.results[2])
        else:
            if search.results[2] in to_download: to_download.remove(search.results[2])
        if cb_var4.get() == 1:
            if search.results[3] not in to_download: to_download.append(search.results[3])
        else:
            if search.results[3] in to_download: to_download.remove(search.results[3])

        if cb_var5.get() == 1:
            if search.results[4] not in to_download: to_download.append(search.results[4])
        else:
            if search.results[4] in to_download: to_download.remove(search.results[4])
        if cb_var6.get() == 1:
            if search.results[5] not in to_download: to_download.append(search.results[5])
        else:
            if search.results[5] in to_download: to_download.remove(search.results[5])
        if cb_var7.get() == 1:
            if search.results[6] not in to_download: to_download.append(search.results[6])
        else:
            if search.results[6] in to_download: to_download.remove(search.results[6])
        if cb_var8.get() == 1:
            if search.results[7] not in to_download: to_download.append(search.results[7])
        else:
            if search.results[7] in to_download: to_download.remove(search.results[7])

        if cb_var9.get() == 1:
            if search.results[8] not in to_download: to_download.append(search.results[8])
        else:
            if search.results[8] in to_download: to_download.remove(search.results[8])
        if cb_var10.get() == 1:
            if search.results[9] not in to_download: to_download.append(search.results[9])
        else:
            if search.results[9] in to_download: to_download.remove(search.results[9])
        if cb_var11.get() == 1:
            if search.results[10] not in to_download: to_download.append(search.results[10])
        else:
            if search.results[10] in to_download: to_download.remove(search.results[10])
        if cb_var12.get() == 1:
            if search.results[11] not in to_download: to_download.append(search.results[11])
        else:
            if search.results[11] in to_download: to_download.remove(search.results[11])

        if cb_var13.get() == 1:
            if search.results[12] not in to_download: to_download.append(search.results[12])
        else:
            if search.results[12] in to_download: to_download.remove(search.results[12])
        if cb_var14.get() == 1:
            if search.results[13] not in to_download: to_download.append(search.results[13])
        else:
            if search.results[13] in to_download: to_download.remove(search.results[13])
        if cb_var15.get() == 1:
            if search.results[14] not in to_download: to_download.append(search.results[14])
        else:
            if search.results[14] in to_download: to_download.remove(search.results[14])
        if cb_var16.get() == 1:
            if search.results[15] not in to_download: to_download.append(search.results[15])
        else:
            if search.results[15] in to_download: to_download.remove(search.results[15])

        selected_counter.set(f"{len(to_download)} Selected")
        print("==========")
        print(to_download)
        print(len(to_download))

    # Checkboxes variables
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

    # Titles variables
    t_var1 = StringVar()
    t_var2 = StringVar()
    t_var3 = StringVar()
    t_var4 = StringVar()

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
    img1 = customtkinter.CTkLabel(sWindow, text = "", image = "")
    img1.place(x = 80, y = 10)
    t1 = customtkinter.CTkLabel(sWindow, textvariable = t_var1, font = ("arial bold", 20))
    t1.place(x = 250, y = 15)
    a1 = customtkinter.CTkLabel(sWindow, text = "", font = ("arial", 15))
    a1.place(x = 255, y = 40)
    l1 = customtkinter.CTkLabel(sWindow, text = "", font = ("arial", 14))
    l1.place(x = 260, y = 65)
    v1 = customtkinter.CTkLabel(sWindow, text = "", font = ("arial", 14))
    v1.place(x = 320, y = 65)
    b1 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube1, corner_radius = 20)
    b1.place(x = 405, y = 63)
    # s1 = customtkinter.CTkLabel(sWindow, text = "", font = ("arial", 12))
    # s1.place(x = 260, y = 65)

    # Second video
    cb2 = customtkinter.CTkCheckBox(sWindow, text = "", variable = cb_var2, command = checkboxes)
    cb2.place(x = 30, y = 140)
    img2 = customtkinter.CTkLabel(sWindow, text = "", image = "")
    img2.place(x = 80, y = 110)
    t2 = customtkinter.CTkLabel(sWindow, textvariable = t_var2, font = ("arial bold", 20))
    t2.place(x = 250, y = 115)
    a2 = customtkinter.CTkLabel(sWindow, text = "Not Available", font = ("arial", 15))
    a2.place(x = 255, y = 140)
    l2 = customtkinter.CTkLabel(sWindow, text = "", font = ("arial", 14))
    l2.place(x = 260, y = 165)
    v2 = customtkinter.CTkLabel(sWindow, text = "", font = ("arial", 14))
    v2.place(x = 320, y = 165)
    b2 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube2, corner_radius = 20)
    b2.place(x = 405, y = 163)
    # s2 = customtkinter.CTkLabel(sWindow, text = "", font = ("arial", 12))
    # s2.place(x = 260, y = 165)

    # Third video
    cb3 = customtkinter.CTkCheckBox(sWindow, text = "", variable = cb_var3, command = checkboxes)
    cb3.place(x = 30, y = 240)
    img3 = customtkinter.CTkLabel(sWindow, text = "", image = "")
    img3.place(x = 80, y = 210)
    t3 = customtkinter.CTkLabel(sWindow, textvariable = t_var3, font = ("arial bold", 20))
    t3.place(x = 250, y = 215)
    a3 = customtkinter.CTkLabel(sWindow, text = "Not Available", font = ("arial", 15))
    a3.place(x = 255, y = 240)
    l3 = customtkinter.CTkLabel(sWindow, text = "", font = ("arial", 14))
    l3.place(x = 260, y = 265)
    v3 = customtkinter.CTkLabel(sWindow, text = "", font = ("arial", 14))
    v3.place(x = 320, y = 265)
    b3 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube3, corner_radius = 20)
    b3.place(x = 405, y = 263)
    # s3 = customtkinter.CTkLabel(sWindow, text = "", font = ("arial", 12))
    # s3.place(x = 260, y = 265)

    # Fourth video
    cb4 = customtkinter.CTkCheckBox(sWindow, text = "", variable = cb_var4, command = checkboxes)
    cb4.place(x = 30, y = 340)
    img4 = customtkinter.CTkLabel(sWindow, text = "", image = "")
    img4.place(x = 80, y = 310)
    t4 = customtkinter.CTkLabel(sWindow, textvariable = t_var4, font = ("arial bold", 20))
    t4.place(x = 250, y = 315)
    a4 = customtkinter.CTkLabel(sWindow, text = "", font = ("arial", 15))
    a4.place(x = 255, y = 340)
    l4 = customtkinter.CTkLabel(sWindow, text = "", font = ("arial", 14))
    l4.place(x = 260, y = 365)
    v4 = customtkinter.CTkLabel(sWindow, text = "", font = ("arial", 14))
    v4.place(x = 320, y = 365)
    b4 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube4, corner_radius = 20)
    b4.place(x = 405, y = 363)
    # s4 = customtkinter.CTkLabel(sWindow, text = "", font = ("arial", 12))
    # s4.place(x = 260, y = 365)

    # Loading
    def Loading(button_var):
        # Disabled widgets
        cb1.configure(state = "disabled")
        cb2.configure(state = "disabled")
        cb3.configure(state = "disabled")
        cb4.configure(state = "disabled")
        b1 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", width = 0, state = "disabled", corner_radius = 20)
        b1.place(x = 405, y = 63)
        b2 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", width = 0, state = "disabled", corner_radius = 20)
        b2.place(x = 405, y = 163)
        b3 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", width = 0, state = "disabled", corner_radius = 20)
        b3.place(x = 405, y = 263)
        b4 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", width = 0, state = "disabled", corner_radius = 20)
        b4.place(x = 405, y = 363)
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
    def normalWidgets():
        global results_counter
        if t_var1.get() != "Video is Not Available": cb1.configure(state = "normal")
        if t_var2.get() != "Video is Not Available": cb2.configure(state = "normal")
        if t_var3.get() != "Video is Not Available": cb3.configure(state = "normal")
        if t_var4.get() != "Video is Not Available": cb4.configure(state = "normal")
        b1 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube1, corner_radius = 20)
        b1.place(x = 405, y = 63)
        b2 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube2, corner_radius = 20)
        b2.place(x = 405, y = 163)
        b3 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube3, corner_radius = 20)
        b3.place(x = 405, y = 263)
        b4 = customtkinter.CTkButton(sWindow, text = "Open in YouTube", font = ("arial bold", 12), fg_color = "red", hover_color = "red3", width = 0, command = openYouTube4, corner_radius = 20)
        b4.place(x = 405, y = 363)
        dn_button.configure(state = "normal")
        dn_button_var.set("Download")
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
        print(f"got {results_counter} results")

        # Get thumbnails
        try:
            raw_data = urllib.request.urlopen(url1.thumbnail_url).read()
            thumb1 = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (160 , 90))
            raw_data = urllib.request.urlopen(url2.thumbnail_url).read()
            thumb2 = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (160 , 90))
            raw_data = urllib.request.urlopen(url3.thumbnail_url).read()
            thumb3 = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (160 , 90))
            raw_data = urllib.request.urlopen(url4.thumbnail_url).read()
            thumb4 = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (160 , 90))
        except UnboundLocalError:
            whenError()
            sWindow.destroy()
            root.deiconify()
            return messagebox.showerror(title = "Something Went Wrong", message = "Try again later.")
        except urllib.error.URLError:
            normalWidgets()
            return messagebox.showerror(title = "Internet Error", message = "Please check your internet connection.")

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
        if url1.views > 1000000: views = f"{int(url1.views/1000000)}M"
        elif url1.views > 1000: views = f"{int(url1.views/1000)}K"
        else: views = int(url1.views/1000000)
        t_var1.set(r.repr(url1.title))
        a1.configure(text = r.repr(url1.author))
        l1.configure(text = to_hms(url1.length))
        v1.configure(text = f"{views} Views")
        img1.configure(image = thumb1)

        # Configure second video in page
        if url2.views > 1000000: views = f"{int(url2.views/1000000)}M"
        elif url2.views > 1000: views = f"{int(url2.views/1000)}K"
        else: views = int(url2.views/1000000)
        t_var2.set(r.repr(url2.title))
        a2.configure(text = r.repr(url2.author))
        l2.configure(text = to_hms(url2.length))
        v2.configure(text = f"{views} Views")
        img2.configure(image = thumb2)

        # Configure third video in page
        if url3.views > 1000000: views = f"{int(url3.views/1000000)}M"
        elif url3.views > 1000: views = f"{int(url3.views/1000)}K"
        else: views = int(url3.views/1000000)
        t_var3.set(r.repr(url3.title))
        a3.configure(text = r.repr(url3.author))
        l3.configure(text = to_hms(url3.length))
        v3.configure(text = f"{views} Views")
        img3.configure(image = thumb3)

        # Configure fourth video in page
        if url4.views > 1000000: views = f"{int(url4.views/1000000)}M"
        elif url4.views > 1000: views = f"{int(url4.views/1000)}K"
        else: views = int(url4.views/1000000)
        t_var4.set(r.repr(url4.title))
        a4.configure(text = r.repr(url4.author))
        l4.configure(text = to_hms(url4.length))
        v4.configure(text = f"{views} Views")
        img4.configure(image = thumb4)

        # Returns widgets to right state
        normalWidgets()

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
            threading.Thread(target = Downloading, args = (downloading_var,)).start()
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
        if platform == "linux" or platform == "linux2": path = f"/home/{os.getlogin()}/Downloads"
        else: path = f"C:/Users\{os.getlogin()}\Downloads"
        global directory
        directory = os.path.realpath(path) # Deafult path in case the user didn't choose
        def pBrowseDir(): # Path function
            global directory2
            directory2 = filedialog.askdirectory()
            ppath_var.set(directory2)

        # When an error happens
        def whenResultsError():
            toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
            toggle_button.place(x = 550 , y = 347)
            cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
            cancel_button.place(x = 595 , y = 347)
            download_button = customtkinter.CTkButton(sDWindow, text = "Download", font = ("arial bold", 25), command = pVideoStart, corner_radius = 20)
            download_button.place(x = 540 , y = 306)
            path_button = customtkinter.CTkButton(sDWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", hover_color = "gray25", width = 5, command = pBrowseDir, corner_radius = 20)
            path_button.place(x = 430 , y = 347)
            lang_choose.configure(state = "normal")
            try: adv_checkbox.configure(state = "normal")
            except: pass
            downloadcounter_var.set("")
            downloading_var.set(" ")
            progress_label.configure(text_color = "#DCE4EE")
            progress_size_label.configure(text_color = "#DCE4EE")

        # Captions download
        def sCaptionsDownload(vid_link, title):
            if vid_link in vids_subs:
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
                    with open(f"{directory2}/{clean_filename(title)}_{sub}_{lang}.srt", "w", encoding = "utf-8") as srt_file:
                        srt_file.write(srt_formatted)
                except NameError:
                    with open(f"{directory}/{clean_filename(title)}_{sub}_{lang}.srt", "w", encoding = "utf-8") as srt_file:
                        srt_file.write(srt_formatted)
            else:
                print(f"{title} not in list")

        # Advanced checker
        def advancedChecker():
            global advanced_quality_settings
            if advanced_quality_settings == "no": advanced_quality_settings = "yes"
            elif advanced_quality_settings == "yes": advanced_quality_settings = "no"

        # Open folder in file explorer when download is finished
        def openFile():
            try:
                try:
                    dir2 = os.path.normpath(directory2)
                    if platform == "linux" or platform == "linux2": subprocess.Popen(dir2)
                    else: subprocess.Popen(f'explorer "{dir2}"')
                except NameError:
                    if platform == "linux" or platform == "linux2": subprocess.Popen(directory)
                    else: subprocess.Popen(f'explorer "{directory}"')
            except PermissionError:
                try: messagebox.showerror(title = "Permission Denied", message = f"I do not have permission to open '{dir2}'")
                except NameError: messagebox.showerror(title = "Permission Denied", message = f"I do not have permission to open '{directory}'")

        # Pause/Resume function
        def toggle_download():
            global is_paused
            is_paused = not is_paused
            if is_paused:
                toggle_button = customtkinter.CTkButton(sDWindow, text = "▶️", font = ("arial", 15), fg_color = "grey14", hover_color = "gray10", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
                toggle_button.place(x = 550 , y = 347)
                downloading_var.set("Paused")
            else:
                toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
                toggle_button.place(x = 550 , y = 347)
                downloading_var.set("Downloading")

        # Cancel function
        def cancel_download():
            global is_cancelled
            is_cancelled = True

        # Download search
        def SearchDownloader(event = None):
            # Preperations
            global is_paused, is_cancelled
            is_paused = is_cancelled = False
            toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
            toggle_button.place(x = 550 , y = 347)
            cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, command = cancel_download, corner_radius = 20)
            cancel_button.place(x = 595 , y = 347)
            download_button = customtkinter.CTkButton(sDWindow, text = "Download", font = ("arial bold", 25), state = "disabled", corner_radius = 20)
            download_button.place(x = 540 , y = 306)
            path_button = customtkinter.CTkButton(sDWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", width = 5, state = "disabled", corner_radius = 20)
            path_button.place(x = 430 , y = 347)
            audio_tags_list = ["251" , "140" , "250" , "249"]
            non_progressive_list = ["137" , "135" , "133", "160"]
            downloaded_counter = 0
            vids_counter = len(to_download)
            r = reprlib.Repr()
            r.maxstring = 27
            # Progress stuff
            pytube.request.default_range_size = 2097152  # 2MB chunk size (update progress every 2MB)
            progress_label.configure(text_color = "green")
            progress_size_label.configure(text_color = "LightBlue")
            lang_choose.configure(state = "disabled")
            try: adv_checkbox.configure(state = "disabled")
            except: pass

            # If the quality is non progressive video (1080p, 480p, 240p and 144p)
            if quality in non_progressive_list:
                for url in to_download:
                    if is_cancelled: break
                    toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
                    toggle_button.place(x = 550 , y = 347)
                    cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, command = cancel_download, corner_radius = 20)
                    cancel_button.place(x = 595 , y = 347)
                    raw_data = urllib.request.urlopen(url.thumbnail_url).read()
                    photo = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (270 , 150))
                    if quality == "137": video = url.streams.filter(res = "1080p").first()
                    elif quality == "135": video = url.streams.filter(res = "480p").first()
                    elif quality == "133": video = url.streams.filter(res = "240p").first()
                    elif quality == "160": video = url.streams.filter(res = "144p").first()
                    audio = url.streams.get_by_itag(251)
                    size = video.filesize + audio.filesize
                    title_var.set(r.repr(url.title))
                    length_var.set(to_hms(url.length))
                    size_var.set(f"{round(size/1024/1024, 2)} MB")
                    # Download subtitles if selected
                    if caps == "yes": sCaptionsDownload(url.watch_url, url.title)
                    else: pass
                    if quality in audio_tags_list: ext = "mp3"
                    else: ext = "mp4"
                    try:
                        vname = f"{directory2}/{clean_filename(url.title)}_video.mp4"
                        aname = f"{directory2}/{clean_filename(url.title)}_audio.mp3"
                    except NameError:
                        vname = f"{directory}/{clean_filename(url.title)}_video.mp4"
                        aname = f"{directory}/{clean_filename(url.title)}_audio.mp3"
                    # Downlaod video
                    try:
                        with open(vname, "wb") as f:
                            percentage_var.set(f"0.00%  ")
                            sizeprogress_var.set(f"0 MB  ")
                            downloading_var.set("Downloading")
                            converting_percentage_var.set("")
                            progressbar.set(0)
                            downloaded_counter = downloaded_counter + 1
                            downloadcounter_var.set(f"{downloaded_counter}/{vids_counter}")
                            thumbnail.configure(image = photo)
                            video = request.stream(video.url) # Get an iterable stream
                            downloaded = 0
                            while True:
                                if is_cancelled:
                                    downloading_var.set("Canceled")
                                    toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
                                    toggle_button.place(x = 550 , y = 347)
                                    cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
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
                                    progressbar.set(percentage_of_completion/100)
                                else:
                                    break # No more data = Finished
                    except PermissionError:
                        whenResultsError()
                        path = vname.replace(f"/{clean_filename(url.title)}_video.mp4", "")
                        return messagebox.showerror(title = "Permission Error", message = f"I don't have permission to access '{path}'. Change the path or run me as administrator.")
                    except FileNotFoundError:
                        whenResultsError()
                        path = vname.replace(f"/{clean_filename(url.title)}_video.mp4", "")
                        return messagebox.showerror(title = "Folder Not Found", message = f"'{path}' is not found. Change the path to an existing folder.")
                    toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
                    toggle_button.place(x = 550 , y = 347)
                    cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
                    cancel_button.place(x = 595 , y = 347)
                    if is_cancelled:
                        pass
                    else: # Download audio
                        downloading_var.set("Downloading audio")
                        with open(aname, "wb") as f:
                            is_paused = is_cancelled = False
                            video = request.stream(audio.url) # Get an iterable stream
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
                                    # Update progress
                                    downloaded += len(chunk)
                                    remaining = size - downloaded
                                    bytes_downloaded = size - remaining
                                    percentage_of_completion = bytes_downloaded / size * 100
                                    percentage_var.set(f"{round(percentage_of_completion, 2)}%  ")
                                    sizeprogress_var.set(f"{int(bytes_downloaded / 1024 / 1024)} MB  ")
                                    progressbar.set(percentage_of_completion/100)
                                else:
                                    # When finished
                                    break
                        # Merge video and audio
                        downloading_var.set("Merging")
                        final_name = vname.replace("_video", f"_({quality_string})")
                        cmd = f'ffmpeg -y -i "{aname}"  -r 30 -i "{vname}"  -filter:a aresample=async=1 -c:a flac -c:v copy "{final_name}"'
                        subprocess.call(cmd, shell=True)
                        os.remove(vname)
                        os.remove(aname)
                        # Convert if there is a conversion
                        if advanced_checker == "yes":
                            downloading_var.set("Converting")
                            Conversion(final_name, "mp4", url.length)

            # Download to_download
            else:
                for url in to_download:
                    if is_cancelled: break
                    toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
                    toggle_button.place(x = 550 , y = 347)
                    cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, command = cancel_download, corner_radius = 20)
                    cancel_button.place(x = 595 , y = 347)
                    raw_data = urllib.request.urlopen(url.thumbnail_url).read()
                    photo = customtkinter.CTkImage(light_image = Image.open(io.BytesIO(raw_data)), dark_image = Image.open(io.BytesIO(raw_data)), size = (270 , 150))
                    video = url.streams.get_by_itag(quality)
                    title_var.set(r.repr(url.title))
                    length_var.set(to_hms(url.length))
                    size_var.set(f"{round(video.filesize/1024/1024, 2)} MB")
                    # Download subtitles if selected
                    if caps == "yes": sCaptionsDownload(url.watch_url, url.title)
                    else: pass
                    if quality in audio_tags_list: ext = "mp3"
                    else: ext = "mp4"
                    size = video.filesize
                    try: vname = f"{directory2}/{clean_filename(url.title)}_({quality_string}).{ext}"
                    except NameError: vname = f"{directory}/{clean_filename(url.title)}_({quality_string}).{ext}"
                    try:
                        with open(vname, "wb") as f:
                            percentage_var.set(f"0.00%  ")
                            sizeprogress_var.set(f"0 MB  ")
                            downloading_var.set("Downloading")
                            converting_percentage_var.set("")
                            progressbar.set(0)
                            downloaded_counter = downloaded_counter + 1
                            downloadcounter_var.set(f"{downloaded_counter}/{vids_counter}")
                            thumbnail.configure(image = photo)
                            video = request.stream(video.url) # Get an iterable stream
                            downloaded = 0
                            while True:
                                if is_cancelled:
                                    downloading_var.set("Canceled")
                                    toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
                                    toggle_button.place(x = 550 , y = 347)
                                    cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
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
                                    progressbar.set(percentage_of_completion/100)
                                else:
                                    # Convert if there is a conversion
                                    if advanced_checker == "yes":
                                        toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, command = toggle_download)
                                        toggle_button.place(x = 550 , y = 347)
                                        cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, command = cancel_download, corner_radius = 20)
                                        cancel_button.place(x = 595 , y = 347)
                                        downloading_var.set("Converting")
                                        Conversion(vname, ext, url.length)
                                    break # No more data = Finished
                    except PermissionError:
                        whenResultsError()
                        path = vname.replace(f"/{clean_filename(url.title)}_({quality_string}).{ext}", "")
                        return messagebox.showerror(title = "Permission Error", message = f"I don't have permission to access '{path}'. Change the path or run me as administrator.")
                    except FileNotFoundError:
                        whenResultsError()
                        path = vname.replace(f"/{clean_filename(url.title)}_({quality_string}).{ext}", "")
                        return messagebox.showerror(title = "Folder Not Found", message = f"'{path}' is not found. Change the path to an existing folder.")

            # When finished
            toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
            toggle_button.place(x = 550 , y = 347)
            cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
            cancel_button.place(x = 595 , y = 347)
            if is_cancelled:
                msg_box = messagebox.askquestion(title = "Delete Canceled File", message = f"Do you want to delete '{vname}'?")
                if msg_box == "yes": os.remove(vname)
            else:
                downloadcounter_var.set("")
                converting_percentage_var.set("")
                thumbnail.configure(image = "")
                title_var.set("Finished")
                length_var.set("Finished")
                size_var.set("Finished")
                downloading_var.set("Finished")
                customtkinter.CTkButton(sDWindow, text = "Open in File Explorer", font = ("arial bold", 20), command = openFile, corner_radius = 20).place(x = 460 , y = 420)
                sDWindow.bell()

        # Get to_download list info, get link and check errors
        loaded_count = 0
        total_size = 0
        total_length = 0
        vids_subs = []
        for url in to_download:
            try:
                if quality == "137":
                    video = url.streams.filter(res = "1080p").first()
                    audio = url.streams.get_by_itag(251)
                    size = video.filesize + audio.filesize
                elif quality == "135":
                    video = url.streams.filter(res = "480p").first()
                    audio = url.streams.get_by_itag(251)
                    size = video.filesize + audio.filesize
                elif quality == "133":
                    video = url.streams.filter(res = "240p").first()
                    audio = url.streams.get_by_itag(251)
                    size = video.filesize + audio.filesize
                elif quality == "160":
                    video = url.streams.filter(res = "144p").first()
                    audio = url.streams.get_by_itag(251)
                    size = video.filesize + audio.filesize
                else:
                    video = url.streams.get_by_itag(quality) # 1080p, 720, 360p, *audio
                    size = video.filesize
                total_size = total_size + size
                total_length = total_length + url.length
                loaded_count += 1
                loaded_counter.set(f"({loaded_count})")
            except urllib.error.URLError as e:
                normalWidgets()
                return messagebox.showerror(title = "Not Connected", message = "Please check your internet connection.")
            except KeyError as e:
                print(f"KeyError: {e}")
                normalWidgets()
                return messagebox.showerror(title = "Something Went Wrong", message = f"I can't fetch '{url.title}' at the moment. Change the selected quality or try again later.")
            except AttributeError as e:
                print(f"AttributeError: {e}")
                normalWidgets()
                return messagebox.showerror(title = "Quality Not Available",
                message = f"I can't fetch '{url.title}' in the quality that you chose. Change the selected quality or try again later.")
            except pytube.exceptions.LiveStreamError as e:
                print(e)
                normalWidgets()
                return messagebox.showerror(title = "Video is Live", message = f"I Can't fetch '{url.title}' because it's a live video.")
            except pytube.exceptions.AgeRestrictedError as e:
                print(e)
                normalWidgets()
                return messagebox.showerror(title = "Age Restricted", message = f"'{url.title}' is age restricted.")
            except pytube.exceptions.MembersOnly as e:
                print(e)
                normalWidgets()
                return messagebox.showerror(title = "Members Only", message = f"'{url.title}' is members only.")
            except pytube.exceptions.VideoPrivate as e:
                print(e)
                normalWidgets()
                return messagebox.showerror(title = "Private Video", message = f"'{url.title}' is private.")
            except pytube.exceptions.VideoRegionBlocked as e:
                print(e)
                normalWidgets()
                return messagebox.showerror(title = "Region Blocked", message = f"'{url.title}' is region blocked.")
            except pytube.exceptions.VideoUnavailable as e:
                print(e)
                normalWidgets()
                return messagebox.showerror(title = "Video Unavailable", message = f"'{url.title}' is unavailable.")
            try:
                video_id = extract.video_id(url.watch_url)
                YouTubeTranscriptApi.list_transcripts(video_id)
                vids_subs.append(url.watch_url)
                print(f"({url.title}) found subtitle")
            except:
                print(f"({url.title}) no subtitle")
                pass

        # Selected labels prepare
        if quality == "160": quality_string = "144p"
        elif quality == "133": quality_string = "240p"
        elif quality == "18": quality_string = "360p"
        elif quality == "135": quality_string = "480p"
        elif quality == "22": quality_string = "720p"
        elif quality == "137": quality_string = "1080p"
        elif quality == "249": quality_string = "50kbps"
        elif quality == "250": quality_string = "70kbps"
        elif quality == "140": quality_string = "128kbps"
        elif quality == "251": quality_string = "160kbps"

        # Form creating
        sDWindow = customtkinter.CTkToplevel()
        sDWindow.withdraw()
        sDWindow.title("Results Downloader")
        width = 700
        height = 460
        x = (sDWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (sDWindow.winfo_screenheight() // 2) - (height // 2)
        sDWindow.geometry(f"{width}x{height}+{x}+{y}")
        sDWindow.maxsize(700, 460)
        sDWindow.minsize(700, 460)
        def onClosing():
            # if messagebox.askokcancel("Quit", "Do you want to quit?"):
            sDWindow.destroy()
            root.destroy()
        sDWindow.protocol("WM_DELETE_WINDOW", onClosing)
        if platform == "linux" or platform == "linux2": pass
        else: sDWindow.iconbitmap("YDICO.ico")
        # sDWindow.bind("<Return>", SearchDownloader)

        # Downloading label
        downloading_var = StringVar()
        customtkinter.CTkLabel(sDWindow, textvariable = downloading_var, font = ("arial", 25)).place(x = 305 , y = 418)
        downloadcounter_var = StringVar()
        customtkinter.CTkLabel(sDWindow, textvariable = downloadcounter_var, font = ("arial", 25), text_color = "LightBlue").place(rely = 1.0, relx = 1.0, x = -405, y = -13, anchor = SE)
        global converting_percentage_var
        converting_percentage_var = StringVar()
        customtkinter.CTkLabel(sDWindow, textvariable = converting_percentage_var, font = ("arial", 25)).place(x = 450 , y = 418)

        # Search download labels
        title_var = StringVar()
        title_var.set("...")
        length_var = StringVar()
        length_var.set("...")
        size_var = StringVar()
        size_var.set("...")
        thumbnail = customtkinter.CTkLabel(sDWindow, text = "", image = "")
        thumbnail.place(x = 415 , y = 15)
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

        # Get thumbnail
        def download_thumbnail():
            if messagebox.askokcancel(title = "Download Thumbnails", message = f"Do you want to download the thumbnails of all the selected videos?"):
                thumb_dir = filedialog.askdirectory()
                try:
                    for url in to_download:
                        response = requests.get(url.thumbnail_url)
                        response.raise_for_status()
                        thumb_path = f"{thumb_dir}/{url.title}_thumbnail.png"
                        with open(thumb_path, 'wb') as file:
                            file.write(response.content)
                except requests.exceptions.ConnectionError:
                    return messagebox.showinfo(title = "Connection Error", message = f"Check your internet connection and try again.")
                messagebox.showinfo(title = "Thumbnails Downloaded", message = f"Thumbnails has been downloaded successfully in '{thumb_dir}'")
        thumbnail_button = customtkinter.CTkButton(sDWindow, text = "Download Thumbnail", font = ("arial bold", 18), command = Thread(target = download_thumbnail).start, corner_radius = 20)
        thumbnail_button.place(x = 480 , y = 260)

        # Path change
        customtkinter.CTkLabel(sDWindow, text = "Download Path:", font = ("arial bold", 20)).place(x = 20 , y = 345)
        ppath_var = StringVar()
        customtkinter.CTkEntry(sDWindow, width = 245, height = 26, textvariable = ppath_var, state = "disabled", corner_radius = 20).place(x = 175 , y = 347)
        try:
            ppath_var.set(directory2)
        except NameError:
            ppath_var.set(directory)
        path_button = customtkinter.CTkButton(sDWindow, text = "Change Path", font = ("arial bold", 12), fg_color = "dim grey", hover_color = "gray25", width = 5, height = 26, command = pBrowseDir, corner_radius = 20)
        path_button.place(x = 430 , y = 347)

        # Subtitle Combobox
        if vids_subs == []:
            lang_choose_state = "disabled"
            caps = "no"
        else:
            lang_choose_state = "readonly"
            caps = "yes"
        print(vids_subs)
        customtkinter.CTkLabel(sDWindow, text = "Subtitle:", font = ("arial bold", 20)).place(x = 340 , y = 315)
        lang_choose = customtkinter.CTkComboBox(sDWindow, width = 100, height = 26, values = ["None", "Arabic", "English"], state = lang_choose_state, corner_radius = 15)
        lang_choose._entry.configure(readonlybackground = lang_choose._apply_appearance_mode(lang_choose._fg_color))
        lang_choose.set("None")
        lang_choose.place(x = 430 , y = 315)

        # Progress bar/labels
        percentage_var = StringVar()
        sizeprogress_var = StringVar()
        progress_label = customtkinter.CTkLabel(sDWindow, textvariable = percentage_var, font = ("arial", 22))
        progress_label.place(x = 540 , y = 384)
        progress_size_label = customtkinter.CTkLabel(sDWindow, textvariable = sizeprogress_var, font = ("arial", 22))
        progress_size_label.place(x = 624 , y = 384)
        percentage_var.set("0.00%")
        sizeprogress_var.set("0 MB")
        progressbar = customtkinter.CTkProgressBar(sDWindow, width = 505)
        progressbar.place(x = 20 , y = 395)
        progressbar.set(0)

        # Pause/Resume & Cancel buttons
        toggle_button = customtkinter.CTkButton(sDWindow, text = "⏸️", font = ("arial", 15), fg_color = "grey14", text_color = "CadetBlue1", width = 5, height = 26, state = "disabled")
        toggle_button.place(x = 550 , y = 347)
        cancel_button = customtkinter.CTkButton(sDWindow, text = "Cancel", font = ("arial bold", 12), fg_color = "red2", width = 80, height = 26, state = "disabled", corner_radius = 20)
        cancel_button.place(x = 595 , y = 347)

        # Advanced quality settings check
        global advanced_checker
        advanced_checker = "no"
        if not advanced_quality_settings == "no":
            audio_quality_list = ["160kbps" , "128kbps" , "70kbps" , "50kbps"]
            if advanced_quality_settings == "audio":
                if quality_string in audio_quality_list:
                    adv_checkbox = customtkinter.CTkCheckBox(sDWindow, text = "Apply Advanced Quality Settings", font = ("arial bold", 15), command = advancedChecker)
                    adv_checkbox.place(x = 410 , y = 225)
                    adv_checkbox.select()
                    advanced_checker = "yes"
            else:
                if not quality_string in audio_quality_list:
                    adv_checkbox = customtkinter.CTkCheckBox(sDWindow, text = "Apply Advanced Quality Settings", font = ("arial bold", 15), command = advancedChecker)
                    adv_checkbox.place(x = 410 , y = 225)
                    adv_checkbox.select()
                    advanced_checker = "yes"

        # Download button
        download_button = customtkinter.CTkButton(sDWindow, text = "Download", font = ("arial bold", 25), command = pVideoStart, corner_radius = 20)
        download_button.place(x = 540 , y = 306)

        # Back to home button
        back_button = customtkinter.CTkButton(sDWindow, text = "Back To Home", font = ("arial bold", 20), command = backHome, corner_radius = 20)
        back_button.place(x = 20 , y = 420)

        # Return to normal state in root
        whenError()
        sWindow.destroy()
        sDWindow.deiconify()

    # Footer Buttons & label
    page_counter = StringVar()
    page_counter.set("Page 1/4")
    selected_counter = StringVar()
    selected_counter.set("0 Selected")
    loaded_counter = StringVar()
    loaded_counter.set("")
    pr_button_var = StringVar()
    pr_button_var.set("Previous Results")
    nr_button_var = StringVar()
    nr_button_var.set("Next Results")
    pr_button = customtkinter.CTkButton(sWindow, textvariable = pr_button_var, font = ("arial bold", 15), command = onPrClick, corner_radius = 20)
    pr_button.place(x = 20, y = 420)
    customtkinter.CTkLabel(sWindow, textvariable = selected_counter, font = ("arial bold", 15)).place(x = 193, y = 420)
    dn_button_var = StringVar()
    dn_button_var.set("Download")
    dn_button = customtkinter.CTkButton(sWindow, textvariable = dn_button_var, font = ("arial bold", 15), command = onDnClick, corner_radius = 20)
    dn_button.place(x = 290, y = 420)
    customtkinter.CTkLabel(sWindow, textvariable = loaded_counter, font = ("arial bold", 13)).place(x = 350, y = 390)
    customtkinter.CTkLabel(sWindow, textvariable = page_counter, font = ("arial bold", 15)).place(x = 450, y = 420)
    nr_button = customtkinter.CTkButton(sWindow, textvariable = nr_button_var, font = ("arial bold", 15), command = onNrClick, corner_radius = 20)
    nr_button.place(x = 540, y = 420)

    results()
    whenError()
    sWindow.deiconify()
    root.withdraw()

# Run the app
root.mainloop()
