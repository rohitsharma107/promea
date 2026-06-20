import serial
from datetime import datetime

# Adjust COM port and baudrate as per your machine's setup
SERIAL_PORT = "COM3" 
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Reading from machine on {SERIAL_PORT}...")
    print("Press Ctrl + C to stop and save.")
    
    # Open file in append mode to log incoming machine records
    with open("machine_output.log", "a") as file:
        while True:
            line = ser.readline().decode(errors="ignore").strip()

            if line:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                saved_line = f"{current_time},{line}"

                print(saved_line)
                file.write(saved_line + "\n")
                file.flush()

except KeyboardInterrupt:
    print("\nStopped. File saved safely as machine_output.log")
except Exception as e:
    print(f"Connection Error: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()