import os
import psutil
import pandas as pd
import joblib
import time

model = joblib.load("model.pkl")

def auto_heal():
    print("🛠️ Attempting auto-healing...")

    # kill highest CPU process
    processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']),
                       key=lambda p: p.info['cpu_percent'],
                       reverse=True)

    if processes:
        pid = processes[0].info['pid']
        name = processes[0].info['name']

        try:
            os.kill(pid, 9)
            print(f"❌ Killed process: {name} (PID {pid})")
        except Exception as e:
            print("Error:", e)

print("🔍 AI Monitoring Started...\n")

while True:
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    input_data = pd.DataFrame([[cpu, ram, disk]], columns=['cpu', 'ram', 'disk'])

    prediction = model.predict(input_data)

    if prediction[0] == -1 or cpu>80 :
        print(f"⚠️ ANOMALY DETECTED! CPU={cpu}, RAM={ram}, Disk={disk}")
        auto_heal()
    else:
        print(f"Normal: CPU={cpu}, RAM={ram}, Disk={disk}")

    time.sleep(2)

