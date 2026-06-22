import serial
import os
from datetime import datetime
from openpyxl import Workbook

# Replace with your COM port ,obser it in device manager
SERIAL_PORT = "COM3"

# Replace if your machine uses a different baud rate
BAUD_RATE = 9600

# Output folder
OUTPUT_FOLDER = "Machine_Output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

while True:

    patient_name = input("\nEnter Patient Name (or type 'exit' to quit): ").strip()

    if patient_name.lower() == "exit":
        print("Program Closed.")
        break

    file_type = input(
        "Enter File Type (csv/txt/log/xlsx): "
    ).strip().lower()

    if file_type not in ["csv", "txt", "log", "xlsx"]:
        print("Invalid file type. Defaulting to csv.")
        file_type = "csv"

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

        file_name = f"{patient_name}.{file_type}"
        file_path = os.path.join(OUTPUT_FOLDER, file_name)

        # Avoid overwriting existing files
        if os.path.exists(file_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{patient_name}_{timestamp}.{file_type}"
            file_path = os.path.join(OUTPUT_FOLDER, file_name)

        try:

            # CSV
            if file_type == "csv":
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("Timestamp,Machine_Data\n")
                    for row in patient_data:
                        file.write(f"{row[0]},{row[1]}\n")

            # TXT or LOG
            elif file_type in ["txt", "log"]:
                with open(file_path, "w", encoding="utf-8") as file:
                    for row in patient_data:
                        file.write(f"{row[0]}  {row[1]}\n")

            # XLSX
            elif file_type == "xlsx":
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
        if 'ser' in locals() and ser.is_open:
            ser.close()
#