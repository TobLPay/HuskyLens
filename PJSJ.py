import serial
from app import choolseokcheck

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendance.db")
print(os.path.abspath(DB_PATH))

ser = serial.Serial("COM9", 115200)

while True:
    line = ser.readline().decode().strip()
    if line == "NO":
        continue
    if line.startswith("ID"):
        insik = int(line.split("=")[1].strip())
        print(f"Detected ID: {insik}")
        choolseokcheck(insik)