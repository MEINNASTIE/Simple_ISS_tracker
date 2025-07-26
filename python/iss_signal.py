import requests
import serial
import time
import math

# only for testing Jenny simulation
USE_SIMULATED_LOCATION = False  # Set to False to use real Frankfurt position

# Frankfurt am Main 
REAL_LAT = 50.1109
REAL_LON = 8.6821

# Simulated location near current ISS coordinates (e.g., from today)
SIM_LAT = 4.85
SIM_LON = 144.82

MY_LAT = SIM_LAT if USE_SIMULATED_LOCATION else REAL_LAT
MY_LON = SIM_LON if USE_SIMULATED_LOCATION else REAL_LON

# Serial port 
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

def is_iss_close(lat1, lon1, lat2, lon2, threshold_km=500):
    R = 6371  
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance < threshold_km

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)  

try:
    while True:
        res = requests.get("http://api.open-notify.org/iss-now.json")
        data = res.json()
        iss_lat = float(data['iss_position']['latitude'])
        iss_lon = float(data['iss_position']['longitude'])

        print(f"ISS Position: lat={iss_lat}, lon={iss_lon}")
        print(f"Your Location: lat={MY_LAT}, lon={MY_LON}")

        if is_iss_close(MY_LAT, MY_LON, iss_lat, iss_lon):
            print("→ ISS is close. Sending: 1")
            arduino.write(b'1')  
        else:
            print("→ ISS is far. Sending: 0")
            arduino.write(b'0')

        time.sleep(10)


except KeyboardInterrupt:
    print("Exiting and closing serial connection.")
    arduino.close()
