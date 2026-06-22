import os
from datetime import datetime
from openpyxl import Workbook
import serial

# Replace according to the machine  COM port ,obser it in device manager
SERIAL_PORT = "COM6"

# Replace if machine uses a different baud rate
BAUD_RATE = 9600

# Output folder
OUTPUT_FOLDER = "Machine_Output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Default file type so we don't have to choose every time
# Options: "csv", "xlsx", "txt", "log"
DEFAULT_FILE_TYPE = "csv"

while True:
    patient_name = (
        input("\nEnter Patient Name (or type 'exit' to quit): ").strip()
    )

    if patient_name.lower() == "exit":
        print("Program Closed.")
        break

    patient_data = []

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

        print(f"\nCollecting data for {patient_name}...")
        print("Press Ctrl+C when report is complete.\n")

        while True:
            line = ser.readline().decode(errors="ignore").strip()

            if line:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                saved_line = f"{current_time},{line}"

                print(saved_line)
                patient_data.append([current_time, line])

    except KeyboardInterrupt:
        print("\nSaving report...")

        file_name = f"{patient_name}.{DEFAULT_FILE_TYPE}"
        file_path = os.path.join(OUTPUT_FOLDER, file_name)

        # Avoid overwriting existing files
        if os.path.exists(file_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{patient_name}_{timestamp}.{DEFAULT_FILE_TYPE}"
            file_path = os.path.join(OUTPUT_FOLDER, file_name)

        try:
            # CSV
            if DEFAULT_FILE_TYPE == "csv":
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("Timestamp,Machine_Data\n")
                    for row in patient_data:
                        file.write(f"{row[0]},{row[1]}\n")

            # TXT or LOG
            elif DEFAULT_FILE_TYPE in ["txt", "log"]:
                with open(file_path, "w", encoding="utf-8") as file:
                    for row in patient_data:
                        file.write(f"{row[0]}  {row[1]}\n")

            # XLSX
            elif DEFAULT_FILE_TYPE == "xlsx":
                wb = Workbook()
                ws = wb.active
                ws.title = "Patient Report"
                ws.append(["Timestamp", "Machine_Data"])
                for row in patient_data:
                    ws.append(row)
                wb.save(file_path)

            print(f"Report saved successfully:")
            print(file_path)

        except Exception as save_error:
            print(f"Error saving file: {save_error}")

    except Exception as e:
        print(f"Connection Error: {e}")

    finally:
        if "ser" in locals() and ser.is_open:
            ser.close()