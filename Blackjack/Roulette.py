from tkinter import *
from tkinter import ttk
import random

root=Tk()

symbols = ['X','?','%','£']

def spin():
	slot1.config(text=symbols[random.randint(0,3)])
	slot2.config(text=symbols[random.randint(0,3)])
	slot3.config(text=symbols[random.randint(0,3)])

slotFrame=LabelFrame(root, text="Slot Machine")
slotFrame.grid(row=0, column=0)

slot1=Label(slotFrame, text="X", font=("arial",36))
slot1.grid(row=0, column=0)
slot2=Label(slotFrame, text="X", font=("arial",36))
slot2.grid(row=0, column=1)
slot3=Label(slotFrame, text="X", font=("arial",36))
slot3.grid(row=0, column=2)

submit=Button(root, text="Spin", command=spin)
submit.grid(row=1, column=0)

root.mainloop()
