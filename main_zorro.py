#Ahmad Ahmed
#This is the music player project..
#Start Date: 28th December 2019
#Completion Date: 5th January 2020


#importing the ttk theme we want
from ttkthemes import themed_tk as tk

#importing time to help with the timing of the audio files
import time
#importing threading to assist me with threading the startCount function
import threading
#importing mutagen, to help us get the time of MP3 songs
from mutagen.mp3 import MP3
#import OS
import os
#Import the tkinter library
from tkinter import *
#import the pygame library to help me with sound
#importing ttk from tkinter to help us with theming the labels and buttons..
from tkinter import ttk
#importing the function that will help me with creating my message box...eg, error message, info message, e.t.c...
from tkinter import messagebox
#importing the file dialog function from tkinter to help us to load mp3 files..
from  tkinter import filedialog
#importing pygame to help us with the sound
import pygame
#initializing the mixer
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()


#Creating the window...
root = tk.ThemedTk()
root.set_theme("scidgrey")
status_bar = ttk.Label(root, text="Created by Ahmad Umar, 2019", relief=SUNKEN, anchor=W)
status_bar.pack(side=BOTTOM, fill=X)
root.title("Zorro")

lengthLabel = ttk.Label(root,text = "Total Length: --:--")
lengthLabel.pack(pady=5)

currentLabel = ttk.Label(root,text = "Current time: --:--", relief=GROOVE)
currentLabel.pack()
# root.geometry('300x300')
root.iconbitmap(r"C:\Users\Zcapt\PycharmProjects\Melody\Images\zorro.ico")

#creating the menu bar...
Main_menu = Menu(root)
root.config(menu=Main_menu)

#dividing the window into frames

leftframe = Frame(root)
leftframe.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()

#creating the playlist list
playlist = []

#creating the function that helps us open files...
def file_opener():
    global filename_path
    filename_path = filedialog.askopenfilename()
    addtoque(filename_path)

def addtoque(filename):
    # creating a listbox for music list..
    filename = os.path.basename(filename)
    index = 0
    listbox1.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1

def del_song():
    selected_audio = listbox1.curselection()
    selected_audio = int(selected_audio[0])
    listbox1.delete(selected_audio)
    playlist.pop(selected_audio)



# creating a listbox for music list..
listbox1 = Listbox(leftframe)
listbox1.pack(padx=10)

addBtn = ttk.Button(leftframe, text="+ Add", command=file_opener)
addBtn.pack(side=LEFT, padx=10)
delBtn = ttk.Button(leftframe, text="- Delete", command = del_song)
delBtn.pack()

#creating the sub menu in the menu bar...
submenu = Menu(Main_menu, tearoff = 0)
Main_menu.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=file_opener)
submenu.add_command(label="Exit", command=root.destroy)

#creating the function that will show the message box for "About Zorro"
def about():
    messagebox.showinfo("About Zorro", "This is the Zorro Music Player, created by Engr Ahmad Umar using Python Tkinter. \n"
                                       "For more info: \n"
                                       "Email: a.ahmad@alustudent.com \n"
                                       "Instagram: _ahmaadumar "
                                       "\n"
                                       "\n"
                                       "\nAlways remember: No one is the wiser")

submenu2 = Menu(Main_menu, tearoff = 0)
Main_menu.add_cascade(label="Help", menu=submenu2)
submenu2.add_command(label="About Zorro", command=about)


#Creating the button images
play_image = PhotoImage(file=r'C:\Users\Zcapt\PycharmProjects\Melody\Images\play.png')
stop_image = PhotoImage(file=r'C:\Users\Zcapt\PycharmProjects\Melody\Images\stop.png')
pause_image = PhotoImage(file=r'C:\Users\Zcapt\PycharmProjects\Melody\Images\pause.png')
rewind_image = PhotoImage(file=r'C:\Users\Zcapt\PycharmProjects\Melody\Images\rewind.png')
mute_image = PhotoImage(file=r'C:\Users\Zcapt\PycharmProjects\Melody\Images\mute.png')
unmute_image = PhotoImage(file=r'C:\Users\Zcapt\PycharmProjects\Melody\Images\unmute.png')

# labelphoto = Label(root,image = photo)
# labelphoto.pack()

#All the variables defined
def show_details(play_song):
    fileData = os.path.splitext(play_song)
    if fileData[1] == ".mp3":
        audio = MP3(play_song)
        file_length = audio.info.length
    else:
        a = pygame.mixer.Sound(play_song)
        file_length = a.get_length()

    # The lines below divide the total length of the wav file by 60 and saves it in the "mins" variable
    # and saves the remainder in the "sec" variable
    mins, secs = divmod(file_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeFormat = "{:02d}:{:02d}".format(mins, secs)
    lengthLabel["text"] = "Total length - " + timeFormat

    thread1 = threading.Thread(target=startCount, args=(file_length,))
    thread1.start()
def startCount(t):
    # pygame.mixer.music.get_busy() this returns false when the music is paused.
    global pause
    while t and pygame.mixer.music.get_busy():
        if pause:
            continue
        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeFormat = "{:02d}:{:02d}".format(mins, secs)
            currentLabel["text"] = "Current time - " + timeFormat
            time.sleep(1)
            t -= 1


pause = FALSE
def playMusic_btn():
    global pause

    if pause:
        pygame.mixer.music.unpause()
        pause = FALSE
        status_bar["text"] = "Music playing: " + os.path.basename(filename_path)
    else:

        try:
            pygame.mixer.music.stop()
            time.sleep(1)
            selected_audio=listbox1.curselection()
            selected_audio = int(selected_audio[0])
            play_it = playlist[selected_audio]
            pygame.mixer.music.load(play_it)
            pygame.mixer.music.play()
            status_bar["text"] = "Playing Music:" + " " + os.path.basename(play_it)
            show_details(play_it)
        except:
            messagebox.showerror("No MP3 File loaded!!", "Please load an MP3 file before pressing play.")
            pause = TRUE

def rewindMusic_btn():
    playMusic_btn()
    status_bar["text"] = "Music has been restarted: " + os.path.basename(filename_path)
def stopMusic_btn():
    pygame.mixer.music.stop()
    status_bar["text"] = "Music stopped"

def pauseMusic_btn():
    global pause
    pause = TRUE
    pygame.mixer.music.pause()
    status_bar["text"] = "Music paused:" + " " + os.path.basename(filename_path)


def set_vol(value):
    volume = float(value)/100 #divide by 100 because the volume takes number's between 0-1
    pygame.mixer.music.set_volume(volume)

muted=FALSE
def unmute():
    global muted
    if muted:
        pygame.mixer.music.set_volume(0.7)
        unmuteBtn.config(image=unmute_image)
        scale.set(70)
        muted = FALSE
    else:
        pygame.mixer.music.set_volume(0)
        unmuteBtn.config(image=mute_image)
        scale.set(0)
        muted=TRUE

middleframe = Frame(rightframe)
middleframe.pack(pady=10)
#setting the buttons...
playBtn = ttk.Button(middleframe,image = play_image, command=playMusic_btn)
playBtn.grid(row =0, column=0, padx=10)

stopBtn = ttk.Button(middleframe, image = stop_image, command=stopMusic_btn)
stopBtn.grid(row =0, column=1, padx= 10)

pauseBtn = ttk.Button(middleframe, image = pause_image, command = pauseMusic_btn)
pauseBtn.grid(row =0, column=2, padx= 10)

bottomframe = Frame(rightframe)
bottomframe.pack(pady=30, padx=30)
rewindBtn = ttk.Button(bottomframe, image = rewind_image, command = rewindMusic_btn)
rewindBtn.grid(row=0, column=0, padx=30)

muteBtn = ttk.Button(rightframe, image = mute_image, command = unmute)
# muteBtn.pack()
unmuteBtn = ttk.Button(bottomframe, image = unmute_image, command = unmute)
unmuteBtn.grid(row=0, column=1, padx=30)



#creating the volume scale
scale = ttk.Scale(bottomframe, from_=0, to_=100, orient=HORIZONTAL, command=set_vol)
#setting a default value for the volume scale...
scale.set(40)
pygame.mixer.music.set_volume(0.4)
scale.grid(row=0, column=2,pady=30)

def on_closing():
    stopMusic_btn()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
