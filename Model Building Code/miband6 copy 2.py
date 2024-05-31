import pygatt

# Set the MAC address of your Mi Band 6
address = "EC:8A:ED:F8:0D:E2"

# Create a proxy to the Mi Band 6
proxy = pygatt.BGAPIBackend()

# Connect to the Mi Band 6
try:
    proxy.start(address)
    print("Connected to Mi Band 6")
except Exception as e:
    print("Failed to connect to Mi Band 6: " + str(e))
    exit()

# Get the heart rate service UUID
hr_service_uuid = "0000180d-0000-1000-8000-00805f9b34fb"

# Get the heart rate measurement characteristic UUID
hr_char_uuid = "00002a37-0000-1000-8000-00805f9b34fb"

# Get the list of available services and characteristics
services, characteristics = proxy.get_primary_services_and_characteristics(address)

# Find the heart rate service and characteristic
hr_service = None
hr_char = None
for service in services:
    if service.get_handle() == int(hr_service_uuid.replace("0000", ""), 16):
        hr_service = service
        break
if hr_service is not None:
    for char in hr_service.get_characteristics():
        if char.get_handle() == int(hr_char_uuid.replace("0000", ""), 16):
            hr_char = char
            break

# If the heart rate service and characteristic are found
if hr_service is not None and hr_char is not None:
    # Enable notifications for the heart rate measurement characteristic
    proxy.write_characteristic_value(address, hr_char.get_handle(), "\x01\x00", False)

    # Wait for the heart rate measurement notification
    def on_notification(handle, value):
        if handle == hr_char.get_handle():
            heart_rate = int.from_bytes(value, byteorder="little")
            print("Heart rate: " + str(heart_rate))

    proxy.on_notification(address, hr_char.get_handle(), on_notification)

    # Wait for the heart rate measurement notification
    while True:
        time.sleep(1)

# Close the connection to the Mi Band 6
proxy.stop()