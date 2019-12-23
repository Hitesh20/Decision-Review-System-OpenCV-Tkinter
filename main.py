import tkinter as tk
import PIL.Image, PIL.ImageTk
import cv2
from functools import partial
import threading
import imutils
import time

# width and height of main screen
SET_WIDTH = 650
SET_HEIGHT = 368

stream = cv2.VideoCapture("clip.mp4")
flag=True
def play(speed):
    global flag
    count=0
    print(f'Playing Video at speed = {speed}')

    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    # frame1 = cv2.resize(frame1, (SET_HEIGHT ,SET_HEIGHT))
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1+speed)
    grabbed, frame = stream.read()

    """
    while grabbed:
        grabbed,frame = stream.read()
        height , width , layers =  frame.shape
        new_h=SET_HEIGHT
        new_w=SET_WIDTH
        resize = cv2.resize(frame, (new_w, new_h)) 
        cv2.imwrite("%03d.jpg" % count, resize)
    """
    if not grabbed:
        exit()
    frame =  cv2.resize(frame, (SET_WIDTH ,SET_HEIGHT))
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tk.NW)
    if flag:
        canvas.create_text(140, 25, fill="black", font="Times 26 bold", text="Decision Pending")
    flag = not flag




def pending(decision):
    #1. Display decision pending image
    frame = cv2.cvtColor(cv2.imread("pending.jpg"), cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (SET_WIDTH ,SET_HEIGHT))
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tk.NW)
    #2. wait for 1 sec
    time.sleep(1)
    #3. display sponsor if any
    #4. wait for 1 sec
    #5. display out/not out image
    if decision=='out':
        decision_image = 'out.jpg'
    else:
        decision_image = 'notOut.jpg'
    frame = cv2.cvtColor(cv2.imread(decision_image), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tk.NW)



def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")

def notOut():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")





#Tkinter GUI starts here
window = tk.Tk()
window.title("Decision Review System")
cv_image = cv2.cvtColor(cv2.imread("welcome.jpg"), cv2.COLOR_BGR2RGB)
canvas = tk.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_image))
image_onCanvas = canvas.create_image(0, 0, anchor=tk.NW, image = photo)
canvas.pack()




#buttons to control playback
btn = tk.Button(window, text="<< Previous(Fast)", width=50, command=partial(play, -25))
btn.pack()

btn = tk.Button(window, text="<< Previous(Slow)", width=50, command=partial(play, -2))
btn.pack()

btn = tk.Button(window, text="Next(Slow) >>", width=50, command=partial(play, 2))
btn.pack()

btn = tk.Button(window, text="Next(Fast) >>", width=50, command=partial(play, 25))
btn.pack()

btn = tk.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tk.Button(window, text="Give Not Out", width=50, command=notOut)
btn.pack()
window.mainloop()
