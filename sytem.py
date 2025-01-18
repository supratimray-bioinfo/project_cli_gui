import os
import psutil
import platform
import distro  

def cpu_name():
    try:
        
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if "model name" in line:
                    return line.split(":")[1].strip()
    except FileNotFoundError:
        return "CPU info not available"

def system_details():
    if platform.system() == "Linux":
        os_info = f"{distro.name()} {distro.version()} ({distro.codename()})"
    else:
        os_info = platform.system() + " " + platform.release()
    
    system_info = {
        "Operating System": os_info,
        "Processor": _cpu_name(),
        "CPU Cores": os.cpu_count(),
        "RAM (GB)": {
            "Total": round(psutil.virtual_memory().total / (1024 ** 3), 2),
            "Used": round(psutil.virtual_memory().used / (1024 ** 3), 2),
            "Available": round(psutil.virtual_memory().available / (1024 ** 3), 2),
        },
        "Storage (GB)": {
            "Total": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
            "Used": round(psutil.disk_usage('/').used / (1024 ** 3), 2),
            "Free": round(psutil.disk_usage('/').free / (1024 ** 3), 2),
        },
    }
    return system_info

def display_system_details(details):
    print("System Details:")
    for key, value in details.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for sub_key, sub_value in value.items():
                print(f"    {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")

if __name__ == "__main__":
    details = system_details()
    display_system_details(details)

