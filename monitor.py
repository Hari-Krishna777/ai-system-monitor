import psutil
import time
import os

while True:
    os.system('clear')

    print("=== AI SYSTEM MONITOR ===\n")

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    disk = psutil.disk_usage('/').percent
    
    with open('data.csv', 'a') as file:
        file.write("timestamp,cpu,ram,disk\n") if os.stat('data.csv').st_size == 0 else None
        file.write(f"{timestamp} | CPU: {cpu}% | RAM: {ram}% | Disk: {disk}%\n")

    print(f"CPU Usage: {cpu}%")
    print(f"RAM Usage: {ram}%")
    print(f"Disk Usage: {disk}%")
    print(f"Timestamp: {timestamp}\n")

    print("Top Processes:\n")

    if cpu > 80:
        print("⚠️ High CPU usage!")

    if ram > 80:
        print("⚠️ High RAM usage!")

    if disk > 80:
        print("⚠️ High Disk usage!")


    processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']),
                       key=lambda p: p.info['cpu_percent'],
                       reverse=True)

    for p in processes[:5]:
        print(f"PID: {p.info['pid']} | Name: {p.info['name']} | CPU: {p.info['cpu_percent']}%")

    time.sleep(2)