import wmi
import GPUtil
# import psutil
# pip install wmi
# pip install gputil
# pip install psutil

from tkinter import *
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Rheolwr-Proses")
root.geometry("580x640")
root.resizable(width=False, height=False)

style = ttk.Style()
style.layout("TNotebook", [])
style.layout("TNotebook.Tab", [])

notebook = ttk.Notebook(root)
cpuTab = Frame(notebook)
gpuTab = Frame(notebook)
ramTab = Frame(notebook)
notebook.add(cpuTab, text="CPU")
notebook.add(gpuTab, text="GPU")
notebook.add(ramTab, text="RAM")

notebook.grid(row=0, column=1)

def cpuGetInfo():
    i = wmi.WMI()
    for processor in i.Win32_Processor():
        cpu_make = processor.Name
        return cpu_make
    
def gpuGetInfo():
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        gpu_make = gpu.name
        gpu_mem = gpu.memoryTotal
        return gpu_make, gpu_mem

def cpu_page():
    cpu_label = Label(cpuTab, text="")
    cpu_label.grid(row=0, column=0)   
    return cpu_label

def gpu_page():
    gpu_label = Label(gpuTab, text="")
    gpu_label.grid(row=0, column=0)   
    gpu_label_mem = Label(gpuTab, text="")
    gpu_label_mem.grid(row=4, column=0)   
    return gpu_label, gpu_label_mem

def show_cpu():
    cpu_label = cpu_page()
    cpu_make = cpuGetInfo() 
    cpu_label.config(text=cpu_make)
    notebook.select(cpuTab)

def show_gpu():
    gpu_label, gpu_label_mem = gpu_page()
    gpu_make, gpu_mem = gpuGetInfo() 
    print(gpu_make, gpu_mem)
    gpu_label.config(text=gpu_make)
    gpu_label_mem.config(text=f"Total VRAM: {gpu_mem} MB")
    notebook.select(gpuTab)

def show_ram():
    notebook.select(ramTab)

Button(root, text="CPU", command=show_cpu, relief="solid", padx=40, pady=10, activebackground="grey", activeforeground="white").grid(column=0, row=0, padx=10, pady=8)
Button(root, text="GPU", command=show_gpu, relief="solid", padx=40, pady=10, activebackground="grey", activeforeground="white").grid(column=0, row=1, padx=10, pady=8)
Button(root, text="RAM", command=show_ram, relief="solid", padx=40, pady=10, activebackground="grey", activeforeground="white").grid(column=0, row=2, padx=10, pady=8)
Button(root, text="Quit", command=root.destroy, relief="solid", padx=40, pady=10, activebackground="grey", activeforeground="white").grid(column=0, row=3, padx=10, pady=8)

root.mainloop()
