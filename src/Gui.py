from PIL import ImageTk
import PIL.Image
from tkinter import * 
from tkinter import ttk
import tkinter as tk
import pafy
import io
from urllib.request import urlopen
import os

# Frond End
# Tkinter window
window = Tk()
window.configure(background='white')
window.title("YouTube Video Downloader")

window.geometry('1220x520')
window.iconbitmap(r'./meta/top.png')
window.resizable(0, 0)

def get_info():
    global video, lc, img5
    link_vid = url_box.get() # url_box i
    try:
        video = pafy.new(link_vid)
    except Exception as e:
        error = tk.Label(window, text="Please check URL!!", 
                        width=35, height=2,fg="white", bg='#218F76', font=('times', 18, 'bold'))
        error.place(x=274, y=370)
        window.after(5000, destroy_widget, error)
        print(e)

    # Set Video Title
    v_name = video.title
    video_title.config(text="Name: "+v_name, width=80)
    video_title.place(x=50, y=300)

    # Set Video Duration
    dura = video.duration
    video_dur.config(text="Time: "+dura, width=17)
    video_dur.place(x=50, y=330)

    # Get the Thumbnail of Video
    thumb = video.bigthumb # returns the url of the video thumbsnail
    u = urlopen(thumb)
    raw_data = u.read() # read from url it is in bytes formate
    img5 = PIL.Image.open(io.BytesIO(raw_data))
    img5_resized = img5.resize((240, 150), PIL.Image.ANTIALIAS)

    # image in url
    image = ImageTk.PhotoImage(img5_resized)
    panel50 = Label(window, image=image, borderwidth=0)
    panel50.image = image
    panel50.pack()
    panel50.place(x=881, y=90)
    
    # Download button of Thumbnail
    img7 = PIL.Image.open(r'./meta/tumb.png')
    img7 = img7.resize((40, 40), PIL.Image.ANTIALIAS)
    img7 = ImageTk.PhotoImage(img7)
    panel8 = Button(window, borderwidth=0, command=download_video_thumbnail, image=img7, bg="white")
    panel8.image = img7
    panel8.pack()
    panel8.place(x=985, y=245)

    # Download options
    dow_list = ["Choose Format", "Video with Sound", "Video(No Sound)", "Audio Only"]
    lc = ttk.Combobox(window, width=16, state="readonly")
    lc['values'] = dow_list
    lc.current(0)
    lc.place(x=280, y=234)

    lc.bind("<<ComboboxSelected>>", quality_choose)

def destroy_widget(widget):
    widget.destroy()

def chdir(path):
    os.chdir(path)

def download_video_thumbnail():
    try:
        vid_id = video.videoid
        chdir(r'./Downloads/Tumbnail/')
        img5.save(vid_id+'.jpg')
        msg = tk.Label(window, text='Thumbnail Downloaded', width=25, height=20, bg="white", font=('times', 18, 'bold'))
        msg.place(x=274, y=370)
        window.after(5000, destroy_widget, msg)
    except Exception as e:
        print(e)

def quality_choose(event):
    global lc1, best, down_qual
    cho = lc.get()
    if cho == "Video with Sound":
        down_qual = video.streams
        best = list(video.streams)
        best.insert(0, '--Select Quality--')
        
        for i, s in enumerate(best):
            best[i] = str(s).replace('normal:', '')
        lc1 = ttk.Combobox(window, width=18, state='readonly')
        lc1.pack()
        lc1['values'] = best
        lc1.current(0)
        lc1.place(x=430, y=234)
    if cho == "Video(No Sound)":
        down_qual = video.videostreams
        best = list(video.videostreams)
        best.insert(0, 'Select Video Quality')
        for i, s in enumerate(best):
            best[i] = str(s).replace('video:', '')
        
        lc1 = ttk.Combobox(window, width=18, state='readonly')
        lc1.pack()
        lc1['values'] = best
        lc1.current(0)
        lc1.place(x=430, y=234)
    if cho == 'Audio Only':
        down_qual = video.audiostreams
        best = list(video.audiostreams)
        best.insert(0, 'Select Audio Quality')
        for i, s in enumerate(best):
            best[i] = str(s).replace('audio:', '')
        lc1 = ttk.Combobox(window, width=18, state="readonly")
        lc1.pack()
        lc1['values'] = best
        lc1.current(0)
        lc1.place(x=430, y=234)

    lc1.bind("<<ComboboxSelected>>", download_button)
def download_button(event):
    img7 = PIL.Image.open(r'./meta/video_down.webp')
    img7 = img7.resize((40, 40), PIL.Image.ANTIALIAS)
    img7 = ImageTk.PhotoImage(img7)
    panel8 = Button(window, command = download_vid, borderwidth=0, image=img7, bg='#7CEC9F', fg='white')
    panel8.image = img7
    panel8.pack()
    panel8.place(x=580, y=223)

def download_vid():
    try:
        choice_qual = lc1.get()
        ind = int(best.index(choice_qual))
        new_ind = ind-1
        selected_qual = down_qual[new_ind]
        if ind == 3:
            chdir(r'./Downloads/Music')
        else:
            chdir(r'./Downloads/Videos')
        selected_qual.download()
        msg = tk.Label(window, text='Stream Downloaded', width=25, height=5, 
                        font=('times', 1, 'bold')) # Todo
        msg.place(x=274, y=370)
        window.after(4000, destroy_widget, msg)
    except Exception as e:
        error = tk.Label(window, text="Please Check your Internet !!", width=27, height=2, fg="white", bg="#A3CB37",
                        font=('times', 18, 'bold')) # Todo
        error.place(x=274, y=370)
        window.after(5000, destroy_widget, error)
        print(e)
def clear():
    url_box.delete(first=0, last=100)
    
# logo setup
logo_img = PIL.Image.open(r'./meta/yt.ico') # Todo
logo_img = logo_img.resize((200, 200), PIL.Image.ANTIALIAS)
logo_img = ImageTk.PhotoImage(logo_img)
panel4 = tk.Label(window, image=logo_img, bg='white')
panel4.pack()
panel4.place(x=50, y=70)

# search png setup
search_img = PIL.Image.open(r'./meta/search.png')
search_img = search_img.resize((40, 40), PIL.Image.ANTIALIAS)
search_img = ImageTk.PhotoImage(search_img)
panel5 = Button(window, borderwidth=0, command=get_info, imag=search_img, bg='white') # Todo 
panel5.pack()
panel5.place(x=775, y=175)

# clear png setup
clear_img = PIL.Image.open(r'./meta/clear.png')
clear_img = clear_img.resize((40, 40), PIL.Image.ANTIALIAS)
clear_img = ImageTk.PhotoImage(clear_img)
panel6 = Button(window, borderwidth=0, command=clear, image=clear_img, bg='white')
panel6.pack()
panel6.place(x=830, y=175)

# tkinter window setup
pred = tk.Label(window, text="YouTube Video Downloder!", width=30, height=2, fg="#2B2B52", bg="white", font=('times', 25, 'bold'))
pred.place(x=274, y=10)

# For url input field
input_label = tk.Label(window, text="Enter your URL", width =18, height=1, fg="white", bg="#2F363F", font=('times', 16, 'bold'))
input_label.place(x=394, y=120)

# input url box setup
url_box = tk.Entry(window, borderwidth=7, width=43, bg='white', fg='black', font=('times', 16, 'bold'))
url_box.place(x=280, y=170)

# Video Title setup
video_title = tk.Label(window, width=10, height =1, fg="#74B9FF", bg="white",
                        font=("times", 18, 'bold'))
# Video Duration
video_dur = tk.Label(window, width=10, height=1, fg="white", bg='#30336B', 
                        font=("times", 18, 'bold')) 
                        
# window.mainloop()
window.mainloop()