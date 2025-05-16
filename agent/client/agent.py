import psutil
import socket
import platform
import requests
import json
import shutil

BACKEND_URL = "http://127.0.0.1:8000/api/receive/"
TIMEOUT = 5

def get_system_info():
    hostname = socket.gethostname()
    os_name = platform.system() + " " + platform.release()
    cpu_name = platform.processor() or "Unknown CPU"
    cpu_threads = psutil.cpu_count(logical=True)
    cpu_cores = psutil.cpu_count(logical=False)

    virtual_mem = psutil.virtual_memory()
    ram_total = round(psutil.virtual_memory().total / (1024**2), 2)
    ram_available = round(psutil.virtual_memory().available / (1024**2), 2)
    ram_used = round(psutil.virtual_memory().used / (1024**2), 2)
    ram_free = round(psutil.virtual_memory().free / (1024**2), 2)


    total, used, free = shutil.disk_usage("/")
    storage_total = round(total / (1024**2), 2)  # MB
    storage_free = round(free / (1024**2), 2)    # MB
    # node = my_system.node
    # release = my_system.release
    # version = my_system.version
    # machine = my_system.machine
    # processor = my_system.processor

    my_system = platform.uname()

    print(f"System: {my_system.system}")
    print(f"Node Name: {my_system.node}")
    print(f"Release: {my_system.release}")
    print(f"Version: {my_system.version}")
    print(f"Machine: {my_system.machine}")
    print(f"Processor: {my_system.processor}")

    return {
        "hostname": hostname,
        "system": my_system,
        "os": os_name,
        "cpu": cpu_name,
        "cpu_threads": cpu_threads,
        "cpu_cores": cpu_cores,
        "ram_total": ram_total,
        "ram_available": ram_available,
        "ram_used": ram_used,
        "ram_free": ram_free,
        "storage_total": storage_total,
        "storage_free": storage_free,
        # "node": node,
        # "release": release,
        # "version": version,
        # "machine": machine,
        # "processor": processor
    }

import time

def collect_process_data():
    processes = []
    proc_list = list(psutil.process_iter(['pid', 'ppid', 'name']))
    
    # Initialize CPU measurement
    for p in proc_list:
        try:
            p.cpu_percent(interval=None)
        except Exception:
            continue

    time.sleep(0.1)  # short wait for accurate cpu % calculation

    for proc in proc_list:
        try:
            info = proc.as_dict(attrs=['pid', 'ppid', 'name', 'memory_percent'])
            cpu = proc.cpu_percent(interval=None)
            if not info['name']:
                continue
            processes.append({
                "pid": info['pid'],
                "ppid": info['ppid'],
                "process_name": info['name'],
                "cpu_usage": cpu,
                "memory_usage": info['memory_percent']
            })
        except Exception:
            continue
    return processes


def send_data():
    payload = {
        "system": get_system_info(),
        "processes": collect_process_data()
    }
    try:
        response = requests.post(BACKEND_URL, json=payload, timeout=TIMEOUT)
        print("Status:", response.status_code)
        print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Failed to send data:", e)

if __name__ == "__main__":
    send_data()
