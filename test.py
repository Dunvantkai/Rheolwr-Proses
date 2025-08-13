import GPUtil

gpus = GPUtil.getGPUs()
for gpu in gpus:
    gpu_usage = gpu.load*100 
    gpu_FMem = gpu.memoryFree
    gpu_UMem = gpu.memoryUsed

print (round(gpu_usage))