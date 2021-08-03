from tkinter import Tk,Button,Label,Listbox,Scale,StringVar
from tkinter.filedialog import askdirectory
import pygame
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
import os

root=Tk()
root.title("My Music Player")

listOfSongs=[]
realnames=[]
var=StringVar()
index=0
choice=1
def playPos(data):
        pygame.mixer.music.set_pos(float(data)*60)
def playSelected(event):
        global index
        data=slist.curselection()
        pygame.mixer.music.load(listOfSongs[data[0]])
        pygame.mixer.music.play()
        index=data[0]
        var.set(realnames[data[0]])
        length.set(0.0)
        audio=MP3(listOfSongs[data[0]])
        slength=float(audio.info.length)/60
        length.config(to=slength)
def setVolume(data):
        pygame.mixer.music.set_volume(float(data))
def previous():
        global index
        if(index==0):
                index=len(realnames)-1
        else:
                index=index-1
        
        pygame.mixer.music.load(listOfSongs[index])
        pygame.mixer.music.play()
        var.set(realnames[index])
        length.set(0.0)
        audio=MP3(listOfSongs[index])
        slength=float(audio.info.length)/60
        length.config(to=slength)
def play():
        global choice
        if(choice==0):
                pygame.mixer.music.unpause()
                choice=1
        else:
                pygame.mixer.music.pause()
                choice=0
def nextSong():
        global index
        if(index==len(realnames)-1):
                index=0
        else:
                index=index+1
        
        pygame.mixer.music.load(listOfSongs[index])
        pygame.mixer.music.play()
        var.set(realnames[index])
        length.set(0.0)
        audio=MP3(listOfSongs[index])
        slength=float(audio.info.length-5)/60
        length.config(to=slength)
length=Scale(root,from_=0.0,to=3.0,orient='horizontal',length=1000,
             resolution=0.1,command=playPos)
def selectSongs():
        directory=askdirectory()
        os.chdir(directory)
        for files in os.listdir(directory):
                if(files.endswith(".mp3")):
                        realpath=os.path.realpath(files)
                        audio=ID3(realpath)
                        realnames.append(audio["TIT2"].text[0])
                        listOfSongs.append(files)
        pygame.mixer.init()
        pygame.mixer.music.load(listOfSongs[0])
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)
        var.set(realnames[0])
        audio=MP3(listOfSongs[0])
        slength=float(audio.info.length)/60
        length.config(to=slength)
selectSongs()

songName=Label(root,textvariable=var,font=('Impact',25))
slist=Listbox(root,font=('Impact',15))
for i in realnames:
        slist.insert('end',i)
prevButton=Button(root,text="Prev",font=('Impact',15),width=20,height=2,
                                            command=previous)
playButton=Button(root,text="Play/Pause",font=('Impact',15),width=20,height=2,
                                                command=play)
nextButton=Button(root,text="Next",font=('Impact',15),width=20,height=2,
                                                command=nextSong)
volume=Scale(root,from_=0.0,to=1.0,resolution=0.2,command=setVolume)
volume.set(0.5)

songName.grid(row=0,column=1,columnspan=5)
slist.grid(row=1,column=0)
prevButton.grid(row=1,column=1)
playButton.grid(row=1,column=2)
nextButton.grid(row=1,column=3)
volume.grid(row=1,column=4)
length.grid(row=2,column=0,columnspan=5)

root.bind('<Double-Button-1>',playSelected)
root.mainloop()
