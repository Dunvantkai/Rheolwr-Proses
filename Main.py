import platform
from tkinter import Tk, Label, Button, ttk

def callSpecs():
    cpu_make = platform.processor()
    return cpu_make

root = Tk()
root.title("Rheolwr-Proses")
root.geometry("480x640")


frame = ttk.Frame(root)
frame.grid(row=0, column=0)

Label(frame, text=callSpecs()).grid(column=0, row=0)  # label inside frame
Button(frame, text="Quit", command=root.destroy).grid(column=0, row=1)  # different row

root.mainloop()
