import sqlite3

config_conn = sqlite3.connect('config.db')
config_c = config_conn.cursor()

config_c.execute('''
    CREATE TABLE IF NOT EXISTS config (
        id INTEGER PRIMARY KEY,
        threshold INTEGER,
        interval INTEGER
    )
''')
config_conn.commit()

config_c.execute("INSERT INTO config (threshold, interval) VALUES (?, ?)", (10, 5))

config_conn.commit()
config_conn.close()

conn = sqlite3.connect('alarms.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS alarms (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME,
        action TEXT
    )
''')
conn.commit()
conn.close()

con = sqlite3.connect('entries.db')
cc = con.cursor()

cc.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME,
        cpu_utilization REAL
    )
''')

con.commit()
con.close()
