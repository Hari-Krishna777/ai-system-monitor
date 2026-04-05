from flask import Flask, jsonify, render_template
import psutil
import time
import threading
import joblib
import pandas as pd
import os

app = Flask(__name__)

# ✅ Load ML model
model = joblib.load("model.pkl")


# 🛠️ Auto-healing function
def auto_heal():
    print("🛠️ Auto-healing triggered!")

    processes = []

    for p in psutil.process_iter(['pid', 'name']):
        try:
            cpu = p.cpu_percent(interval=0.1)
            processes.append((cpu, p.info['pid'], p.info['name']))
        except:
            pass

    processes.sort(reverse=True)

    if processes:
        cpu, pid, name = processes[0]

        try:
            os.kill(pid, 9)
            print(f"❌ Killed: {name} (PID {pid}) CPU={cpu}")
        except Exception as e:
            print("Error:", e)


# 🧠 Background AI monitoring (runs continuously)
def background_monitor():
    print("🧠 Background AI Monitor Started...\n")

    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        input_data = pd.DataFrame([[cpu, ram, disk]], columns=['cpu', 'ram', 'disk'])
        prediction = model.predict(input_data)

        if prediction[0] == -1 or cpu > 80:
            print(f"⚠️ ANOMALY DETECTED! CPU={cpu}, RAM={ram}, Disk={disk}")
            auto_heal()
        else:
            print(f"Normal: CPU={cpu}, RAM={ram}, Disk={disk}")

        time.sleep(2)


# 📊 Get system stats (for API/dashboard)
def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    timestamp = time.strftime("%H:%M:%S")

    return {
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "timestamp": timestamp
    }


# 🌐 Routes

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/stats')
def stats():
    return jsonify(get_system_stats())


@app.route('/processes')
def processes():
    process_list = []

    for p in psutil.process_iter(['pid', 'name']):
        try:
            cpu = p.cpu_percent(interval=0.1)
            process_list.append({
                "pid": p.info['pid'],
                "name": p.info['name'],
                "cpu": cpu
            })
        except:
            pass

    process_list = sorted(process_list, key=lambda x: x['cpu'], reverse=True)

    return jsonify(process_list[:5])


@app.route('/health')
def health():
    return jsonify({"status": "healthy"})


@app.route('/alerts')
def alerts():
    stats = get_system_stats()
    return jsonify({
        "alert": "⚠️ High CPU usage!" if stats['cpu'] > 80 else "✅ All systems normal"
    })


# 🚀 Start everything
if __name__ == '__main__':
    t = threading.Thread(target=background_monitor)
    t.daemon = True
    t.start()

    app.run(host='0.0.0.0', port=5000)