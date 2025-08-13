import wmi
import GPUtil
import psutil
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# pip install wmi
# pip install gputil
# pip install psutil
# pip install matplotlib
# pip install tk
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
global bg_colour
bg_colour = '#f0f0f0'
task=None
# -- builds tabs
notebook = ttk.Notebook(root)
cpuTab = Frame(notebook)
gpuTab = Frame(notebook)
ramTab = Frame(notebook)
notebook.add(cpuTab, text="CPU")
notebook.add(gpuTab, text="GPU")
notebook.add(ramTab, text="RAM")
notebook.grid(row=0, column=1, rowspan=8)
# -- graph
MAX_POINTS = 32
data = [0] * MAX_POINTS  
# -- info get
def cpuGetInfo():
    i = wmi.WMI()
    for cpu in i.Win32_Processor():
        cpu_make = cpu.Name
        cpu_cores = cpu.NumberOfCores
        cpu_speed = cpu.MaxClockSpeed
        return cpu_make, cpu_cores, cpu_speed
    
def gpuGetInfo():
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        gpu_make = gpu.name
        gpu_mem = gpu.memoryTotal
        return gpu_make, round(gpu_mem)
# -- Usage get
def cpuGetUsage():
    cpu_usage = psutil.cpu_percent(interval=0)
    return round(cpu_usage)
def gpuGetUsage():
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        gpu_usage = gpu.load*100 
        gpu_FMem = gpu.memoryFree
        gpu_UMem = gpu.memoryUsed
        return round(gpu_usage), gpu_FMem, gpu_UMem
# -- build page
def cpu_page():
    global cpu_label0
    cpu_label0 = Label(cpuTab, text="") 
    cpu_label0.grid(row=0, column=0)  
    cpu_label = Label(cpuTab, text="")
    cpu_label.grid(row=2, column=1, padx=20)   
    cpu_label1 = Label(cpuTab, text="")
    cpu_label1.grid(row=2, column=2, padx=20) 
    cpu_label2 = Label(cpuTab, text="")
    cpu_label2.grid(row=3, column=1, padx=20) 
    cpu_label3 = Label(cpuTab, text="")
    cpu_label3.grid(row=3, column=2, padx=20) 
    return cpu_label0, cpu_label, cpu_label1, cpu_label2, cpu_label3

def gpu_page():
    global gpu_label0, gpu_label_fmem, gpu_label_umem
    gpu_label0 = Label(gpuTab, text="")
    gpu_label0.grid(row=0, column=0)  
    gpu_label = Label(gpuTab, text="")
    gpu_label.grid(row=2, column=1, padx=20)   
    gpu_label_mem = Label(gpuTab, text="")
    gpu_label_mem.grid(row=2, column=2, padx=20)   
    gpu_label_fmem = Label(gpuTab, text="")
    gpu_label_fmem.grid(row=3, column=1, padx=20)
    gpu_label_umem = Label(gpuTab, text="")
    gpu_label_umem.grid(row=3, column=2, padx=20)
    return gpu_label0, gpu_label, gpu_label_mem, gpu_label_fmem, gpu_label_umem
def ram_page():
    ram_label0 = Label(ramTab, text="")
    ram_label0.grid(row=0, column=0)
    return ram_label0
# -- sets page
def show_cpu():
    cpu_label0, cpu_label, cpu_label1, cpu_label2, cpu_label3 = cpu_page()
    cpu_make, cpu_cores, cpu_speed = cpuGetInfo() 
    cpu_label0.config(text="CPU")
    cpu_label.config(text=cpu_make)
    cpu_label1.config(text=f"Cores: {cpu_cores}")
    cpu_label2.config(text=f"Max Clock Speed: {cpu_speed} (MHz):")
    cpu_label3.config(text="Temp: ??")
    fig = Figure(figsize=(4, 2), dpi=100)
    plot1 = fig.add_subplot(111)
    plot1.set_ylim(0, 100)
    plot1.set_facecolor('lightgray')
    fig.patch.set_facecolor(bg_colour)
    plot1.set_xticks([])
    canvas = FigureCanvasTkAgg(fig, master=cpuTab)
    canvas.get_tk_widget().grid(row=1, column=0, padx=40,columnspan=8)
    notebook.select(cpuTab)
    GraphUsageUpdate(plot1, canvas, cpuTab)

def show_gpu():
    gpu_label0, gpu_label, gpu_label_mem, gpu_label_fmem, gpu_label_umem  = gpu_page()
    gpu_make, gpu_mem = gpuGetInfo() 
    new_value, gpu_FMem, gpu_UMem  = gpuGetUsage()
    gpu_label.config(text=gpu_make)
    gpu_label0.config(text="GPU")
    gpu_label_mem.config(text=f"{gpu_mem}: Megabytes")
    gpu_label_fmem.config(text=f"{gpu_FMem}: Free VRAM")
    gpu_label_umem.config(text=f"{gpu_UMem}: Used VRAM")
    fig = Figure(figsize=(4, 2), dpi=100)
    plot1 = fig.add_subplot(111)
    plot1.set_ylim(0, 100)
    plot1.set_facecolor('lightgray')
    fig.patch.set_facecolor(bg_colour)
    plot1.set_xticks([])
    canvas = FigureCanvasTkAgg(fig, master=gpuTab)
    canvas.get_tk_widget().grid(row=1, column=0, padx=40,columnspan=8)
    notebook.select(gpuTab)
    GraphUsageUpdate(plot1, canvas, gpuTab)

def show_ram():
    ram_label0 = ram_page()
    ram_label0.config(text="r
    fig = Figure(figsize=(4, 2), dpi=100)
    plot1 = fig.add_subplot(111)
    plot1.set_ylim(0, 100)
    plot1.set_facecolor('lightgray')
    fig.patch.set_facecolor(bg_colour)
    plot1.set_xticks([])
    canvas = FigureCanvasTkAgg(fig, master=ramTab)
    canvas.get_tk_widget().grid(row=1, column=0, padx=40,columnspan=8)
    notebook.select(ramTab)
    GraphUsageUpdate(plot1, canvas, ramTab)

def GraphUpdate(new_value, plot1, canvas):
    data.pop(0)
    data.append(new_value)
    plot1.clear()
    plot1.plot(data, marker='o')
    plot1.set_ylim(0, 100)
    plot1.set_xticks([])
    canvas.draw()

def GraphUsageUpdate(plot1, canvas, tab_frame):
    global task
    if notebook.tab(notebook.select(), "text").lower() == "CPU".lower():
        new_value = cpuGetUsage()
        cpu_label0.config(text=f"CPU: {new_value}%")
    elif notebook.tab(notebook.select(), "text").lower() == "GPU".lower():
        new_value, gpu_FMem, gpu_UMem  = gpuGetUsage()
        gpu_label0.config(text=f"GPU: {new_value}%")
        gpu_label_fmem.config(text=f"{gpu_FMem}: Free VRAM")
        gpu_label_umem.config(text=f"{gpu_UMem}: Used VRAM")
    else:
        return
    GraphUpdate(new_value, plot1, canvas)
    if task:
        root.after_cancel(task)

    task = tab_frame.after(1000, GraphUsageUpdate, plot1, canvas, tab_frame)


def on_close():
    os._exit(0) 
root.protocol("WM_DELETE_WINDOW", on_close)


Button(root, text="CPU", command=show_cpu, relief="solid", padx=40, pady=10, activebackground="grey", activeforeground="white").grid(column=0, row=0, sticky="nw", padx=10, pady=8)
Button(root, text="GPU", command=show_gpu, relief="solid", padx=40, pady=10, activebackground="grey", activeforeground="white").grid(column=0, row=1, sticky="nw", padx=10, pady=8)
Button(root, text="RAM", command=show_ram, relief="solid", padx=40, pady=10, activebackground="grey", activeforeground="white").grid(column=0, row=2,  sticky="nw",padx=10, pady=8)
Button(root, text="Quit", command=on_close, relief="solid", padx=40, pady=10, activebackground="grey", activeforeground="white").grid(column=0, row=3, padx=10, pady=8)

root.mainloop()
