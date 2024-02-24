from tkinter import *


def print_hello():
    return print('hello')

root = Tk() #root is window
root.geometry('300x300') #size of the window
l = Label(root, text="Start or stop the microphone")
l.pack()
b1 = Button(root, text= 'start recording', command=print_hello)
b1.pack()
b2 = Button(root, text= 'stop recording')
b2.pack()
root.mainloop()