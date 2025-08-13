# Install with: pip install WinTmp
import WinTmp

def get_cpu_temp_windows():
    try:
        temp = WinTmp.CPU_Temp()
        return temp
    except Exception as e:
        return f"Error getting CPU temperature on Windows: {e}. Ensure script is run as administrator."

    # Example usage
cpu_temperature = get_cpu_temp_windows()
print(f"CPU Temperature: {cpu_temperature}°C")