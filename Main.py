import wmi
import GPUtil
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import psutil
# pip install wmi
# pip install gputil
# pip install psutil
# pip install matplotlib
from tkinter import *
import tkinter as tk
from tkinter import ttk
#  -- Builds Window
root = tk.Tk()
root.title("Rheolwr-Proses")
root.geometry("640x400")
root.resizable(width=False, height=False)
# -- removes tabs
style = ttk.Style()
style.layout("TNotebook", [])
style.layout("TNotebook.Tab", [])
# -- builds tabs
notebook = ttk.Notebook(root)
cpuTab = Frame(notebook)
gpuTab = Frame(notebook)
ramTab = Frame(notebook)
notebook.add(cpuTab, text="CPU")
notebook.add(gpuTab, text="GPU")
notebook.add(ramTab, text="RAM")
notebook.grid(row=0, column=1)
# -- graph
MAX_POINTS = 32
data = [0] * MAX_POINTS  
# -- info get
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
# -- build page
def cpu_page():
    cpu_label = Label(cpuTab, text="")
    cpu_label.grid(row=0, column=1)   
    return cpu_label

def gpu_page():
    gpu_label = Label(gpuTab, text="")
    gpu_label.grid(row=0, column=1)   
    gpu_label_mem = Label(gpuTab, text="")
    gpu_label_mem.grid(row=1, column=1)   
    return gpu_label, gpu_label_mem
# -- sets page
def show_cpu():
    fig = Figure(figsize=(4, 2), dpi=100)
    plot1 = fig.add_subplot(111)
    plot1.set_ylim(0, 100)
    plot1.set_xticks([])
    canvas = FigureCanvasTkAgg(fig, master=cpuTab)
    canvas.get_tk_widget().grid(row=1, column=1, padx=40, sticky="nsew")

    cpu_label = cpu_page()
    cpu_make = cpuGetInfo() 
    cpu_label.config(text=cpu_make)
    notebook.select(cpuTab)

def show_gpu():
    gpu_label, gpu_label_mem = gpu_page()
    gpu_make, gpu_mem = gpuGetInfo() 
    gpu_label.config(text=gpu_make)
    gpu_label_mem.config(text=f"Total VRAM: {gpu_mem} MB")
    notebook.select(gpuTab)

def show_ram():
    notebook.select(ramTab)

# -- graph

# def update_graph(new_value):
#     data.pop(0)
#     data.append(new_value)
#     plot1.clear()
#     plot1.plot(data, marker='o')
#     plot1.set_ylim(0, 100)
#     canvas.draw()
#     fig = Figure(figsize=(2, 1), dpi=100)
#     plot1 = fig.add_subplot(111)
#     plot1.set_ylim(0, 100)
#     canvas = FigureCanvasTkAgg(fig, master=root)
#     canvas.get_tk_widget().grid(column=1, row=4)

Button(root, text="CPU", command=show_cpu, relief="solid", padx=40, pady=10, activebackground="grey", activeforeground="white").grid(column=0, row=0, sticky="nw", padx=10, pady=8)
Button(root, text="GPU", command=show_gpu, relief="solid", padx=40, pady=10, activebackground="grey", activeforeground="white").grid(column=0, row=1, sticky="nw", padx=10, pady=8)
Button(root, text="RAM", command=show_ram, relief="solid", padx=40, pady=10, activebackground="grey", activeforeground="white").grid(column=0, row=2,  sticky="nw",padx=10, pady=8)
Button(root, text="Quit", command=root.destroy, relief="solid", padx=40, pady=10, activebackground="grey", activeforeground="white").grid(column=0, row=3, padx=10, pady=8)

root.mainloop()
