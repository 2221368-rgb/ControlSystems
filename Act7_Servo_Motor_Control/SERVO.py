import serial
import serial.tools.list_ports
import time

class ServoController:
    def __init__(self):
        self.connection = None

    def connect(self, port, baud_rate=9600):
        try:
            self.connection = serial.Serial(port, baud_rate, timeout=1)
            time.sleep(2) # Wait for Arduino reset
            return True
        except serial.SerialException as e:
            print(f"Connection Error: {e}")
            return False

    def send_degrees(self, degrees):
        # Client-side validation
        if 0 <= degrees <= 180:
            cmd = f"{degrees}\n"
            self.connection.write(cmd.encode('utf-8'))
            response = self.connection.readline().decode().strip()
            return response
        return "Invalid degree input"

def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if 'arduino' in p.description.lower() or p.vid in [0x2341, 0x1A86]:
            return p.device
    return None
