from tkinter import *
from tkinter import filedialog
import tkinter as TK
import tkinter.messagebox
import os
import time
import threading
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from tkinter import ttk
from pygame import mixer  # mixer is responsible for playing music

root = tk.ThemedTk()
root.get_themes()
root.set_theme('radiance')

# Fonts - Arial (Correspsonds to Helvetica), Courier New, Comic Sans MS Fixedsys, MS Sans Serif, MS Serif, Symbol, System, Times New Roman (Times), Verada
# Styles - normal, bold, roman, italic, underline, overstrike

statusbar = TK.ttk.Label(root, text='Welcome to Melody', relief=SUNKEN, anchor=W, font='Times 15 roman')  # anchor = move text to the area I want
statusbar.pack(side=BOTTOM, fill=X)

menubar = Menu(root)  # create Menubar
root.config(menu=menubar)  # make sure it is on top and ready to receive submenues

playlist = []

# playlist containts the full path + filename
# playlistbox contains just the filename
# fullpath + filename is required to play the music inside play_music load function
def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    print(filename)
    index = 0
    index += 1
    playlistBox.insert(index, filename)
    playlist.insert(index,filename_path)


def about_us():
    TK.messagebox.showinfo('Info about us', 'This is my first music player')

def del_song():
    selected_song = playlistBox.curselection()    # curselection gives me a tuple
    selected_song = int(selected_song[0])         # get the first element of the tuple
    playlistBox.delete(selected_song)             # remove items from playlistBox
    playlist.pop(selected_song)                   # remove the item from playlist by using the index = selected song

# create submenus
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=subMenu)
subMenu.add_command(label='Open', command=browse_file)
subMenu.add_command(label='Exit', command=root.destroy)

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=subMenu)
subMenu.add_command(label='About us', command=about_us)

mixer.init()  # initializing

root.title('Melody')
root.iconbitmap(r'images/melody.ico')

# root Window - Statusbar, LeftFrame, RightFrame
# leftFrame - The listbox,
# rightFrame - Topframe, MiddleFrame and bottomFrame
leftFrame = Frame(root)
leftFrame.pack(side=LEFT, padx=30, pady=30)

playlistBox = Listbox(leftFrame)
playlistBox.pack()

addBtn = TK.ttk.Button(leftFrame, text=' + Add', command=browse_file)
addBtn.pack(side=LEFT)

delBtn = TK.ttk.Button(leftFrame, text=' - Del', command=del_song)
delBtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()

middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack()

lengthlabel = TK.ttk.Label(topframe, text='Total length - --:--')
lengthlabel.pack(pady=10)  # pady = create distance

currenttimelabel = TK.ttk.Label(topframe, text='Current Time : --:-- ', relief=GROOVE)  # making countdown
currenttimelabel.pack()  # pady = create distance


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':  # file_data=list, second element is .mp3
        audio = MP3(play_song)
        total_length = audio.info.length  # length of the music file  - metadata

    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()  # length of another file

    mins, secs = divmod(total_length, 60)  # div - total_length/60, mod - total_length % 60
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = 'Total length' + ' - ' + timeformat

    # threading makes sure that programm could execute different functions at the same time
    t1 = threading.Thread(target=start_count, args=(
        total_length,))  # ruf funktion zwar sofort auf, fehlt aber ein Argument zum bearbeiten - > wenn ich start_count() schreibe dann funktioniert es nicht
    t1.start()


# countdown for music file
def start_count(t):
    global paused  # activate the variable paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():  # mixer.music.get_busy() returns FALSE when we press the stop butten
        if paused:
            continue  # continue = ignores all of the statements below it. We check if music is paused or not
        else:
            mins, secs = divmod(current_time, 60)  # div - total_length/60, mod - total_length % 60
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = 'Current time' + ' - ' + timeformat
            time.sleep(1)  # after every loop, sleeps for 1 sec
            current_time += 1  # time should decrease


def playMusic():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = 'Music resumed'
        paused = FALSE
    else:
        try:
            stopMusic()
            time.sleep(1)
            selected_song = playlistBox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = 'Playing music' + ' ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            TK.messagebox.showerror('File not found', 'Music could not be played. Please check if the file exists!')


def stopMusic():
    mixer.music.stop()
    statusbar['text'] = 'Music stopped'


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)  # set volume of mixer takes value only from 0 to 1


paused = FALSE


def pauseMusic():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = 'Music paused'


def rewindMusic():
    playMusic()
    statusbar['text'] = 'Music rewinded'


muted = FALSE  # music is still playing


def muteMusic():
    global muted
    if muted:  # unmuted the music
        mixer.music.set_volume(0.5)
        volumeBtn.configure(image=volumePhoto)  # change image if i press on button
        scale.set(50)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)  # change image if i press on button
        scale.set(0)
        muted = TRUE


playPhoto = TK.PhotoImage(file='images/music-player.png')
playBtn = TK.ttk.Button(middleframe, image=playPhoto, command=playMusic)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = TK.PhotoImage(file='images/stop.png')
stopBtn = TK.ttk.Button(middleframe, image=stopPhoto, command=stopMusic)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = TK.PhotoImage(file='images/pause.png')
pauseBtn = TK.ttk.Button(middleframe, image=pausePhoto, command=pauseMusic)
pauseBtn.grid(row=0, column=2, padx=10)

rewindPhoto = TK.PhotoImage(file='images/play.png')  # rewind= zurückspulen
rewindBtn = TK.ttk.Button(bottomframe, image=rewindPhoto, command=rewindMusic)
rewindBtn.grid(row=0, column=1, padx=10)

mutePhoto = TK.PhotoImage(file='images/mute.png')  # rewind= zurückspulen
volumePhoto = TK.PhotoImage(file='images/volume.png')
volumeBtn = TK.ttk.Button(bottomframe, image=volumePhoto, command=muteMusic)
volumeBtn.grid(row=0, column=2)

scale = TK.ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(50)  # set scale shows to 50
mixer.music.set_volume(0.5)  # set volume automatically to 50
scale.grid(row=0, column=3, pady=10, padx=30)


# event and binding  - how should the x button behave if i press on it during playing the music
def on_closing():
    stopMusic()
    root.destroy()


root.protocol('WM_DELETE_WINDOW', on_closing)
root.mainloop()  # keep the window appeared
