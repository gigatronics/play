# python

import imutils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,360)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

cap1 = cv2.VideoCapture(1)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH,360)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

def read_frame():
    webCameShow(cap.read(),display1)
    webCameShow(cap1.read(),display2)
    window.after(10, read_frame)

def webCameShow(N,Display):
    _, frameXX = N
    cv2imageXX = cv2.cvtColor(frameXX, cv2.COLOR_BGR2RGBA)
    imgXX = Image.fromarray(cv2imageXX)
    #imgtkXX = ImageTk.PhotoImage(image=imgXX)
    Display.imgtk = imgtkXX
    Display.configure(image=imgtkXX)
