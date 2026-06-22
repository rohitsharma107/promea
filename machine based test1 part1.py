import serial
from datetime import datetime

ser = serial.Serial("COM3", 9600, timeout=1)

file = open("machine_output.log", "a")

print("Reading from machine on COM3...")
print("Press Ctrl + C to stop and save")

try:
    while True:
        line = ser.readline().decode(errors="ignore").strip()

        if line:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            saved_line = current_time + " " + line

            print(saved_line)
            file.write(saved_line + "\n")
            file.flush()

except KeyboardInterrupt:
    print("Stopped. File saved as machine_output.log")

finally:
    file.close()
    ser.close()
#    
