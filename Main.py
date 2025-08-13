import platform
import tkinter as tk
 tkinter import ttk
from tkinter import Tk, Label, Button, ttk
from tkinter import font
root = Tk()
root.title("Rheolwr-Proses")
root.geometry("580x640")


def callSpecs():
    cpu_make = platform.processor()
    return cpu_make


Button(text="CPU").grid(column=1, row=4, padx=20, pady=10)

# Label(frame, text=callSpecs()).grid(column=0, row=0)
Button(text="Quit", command=root.destroy).grid(column=10, row=10)

root.mainloop()
