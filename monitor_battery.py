import psutil
from datetime import datetime
import time
import sqlite3
import os


config_conn = sqlite3.connect('config.db')
config_c = config_conn.cursor()

def get_config():
    config_c.execute("SELECT * FROM config")
    config = config_c.fetchone()
    return config[1], config[2]

def update_config(new_threshold, new_interval):
    config_c.execute("UPDATE config SET threshold = ?, interval = ?", (new_threshold, new_interval))
    config_conn.commit()

conn = sqlite3.connect('alarms.db')
c = conn.cursor()

con = sqlite3.connect('entries.db')
cc = con.cursor()

def monitor_cpu_utilization():
    previous_utilization = None 
    while True:
        try:
            threshold, interval = get_config()

            cpu_utilization = psutil.cpu_percent()

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cc.execute("INSERT INTO entries (timestamp, cpu_utilization) VALUES (?, ?)", (current_time, cpu_utilization))
            con.commit()

            if previous_utilization != None :
                print(f"CPU Utilization is {cpu_utilization}% at {current_time}")

            if previous_utilization is not None:
                if cpu_utilization > threshold and previous_utilization <= threshold:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    action = f"Above {threshold}%"
                    c.execute("INSERT INTO alarms (timestamp, action) VALUES (?, ?)", (current_time, action))
                    conn.commit()
                    print(f"Alert: CPU Utilization is now above {threshold}% at {current_time}")

                    os.system(f"osascript -e 'display notification \"CPU Utilization is above {threshold}%\" with title \"Threshold Alert\"'")

                elif cpu_utilization < threshold and previous_utilization >= threshold:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    action = f"Below {threshold}%"
                    c.execute("INSERT INTO alarms (timestamp, action) VALUES (?, ?)", (current_time, action))
                    conn.commit()
                    print(f"Alert: CPU Utilization is now below {threshold}% at {current_time}")

                    os.system(f"osascript -e 'display notification \"CPU Utilization is below {threshold}%\" with title \"Threshold Alert\"'")
            else:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Initial Alert: CPU Utilization is {cpu_utilization}% at {current_time}")

                os.system(f"osascript -e 'display notification \"Initial Alert: CPU Utilization is {cpu_utilization}%\" with title \"Threshold Alert\"'")


            previous_utilization = cpu_utilization

            time.sleep(interval)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    monitor_cpu_utilization()