from tkinter import *
import tkinter as TK
from pygame import mixer    # mixer is responsible for playing music

root = Tk()
mixer.init()    # initializing
root.geometry('300x300')
root.title('Melody')
root.iconbitmap(r'melody.ico')

text = TK.Label(root, text='Lets make some noise!')
text.pack()




def playMusic():
    # load the file
    mixer.music.load('journey.wav')
    mixer.music.play()

def stopMusic():
    mixer.music.stop()


playPhoto = TK.PhotoImage(file='music-player.png')
playBtn = TK.Button(root, image=playPhoto, command = playMusic)
playBtn.pack()
stopPhoto = TK.PhotoImage(file='stop.png')
stopBtn =TK.Button(root, image=stopPhoto, command=stopMusic)
stopBtn.pack()




root.mainloop() # keep the window appeared