# EC:8A:ED:F8:0D:E2
import asyncio
from bleak import BleakClient, BleakError

MAC_ADDRESS = "EC:8A:ED:F8:0D:E2"  # Replace with your Mi Band's MAC address

HEART_RATE_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HEART_RATE_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

heart_rate_values = []

async def heart_rate_callback(sender, data):
    heart_rate = data[1]
    print(f"Heart rate: {heart_rate} bpm")
    heart_rate_values.append(heart_rate)

async def run():
    retry_count = 0
    max_retries = 3

    while retry_count < max_retries:
        try:
            async with BleakClient(MAC_ADDRESS) as client:
                services = await client.get_services()
                for service in services:
                    print(f"Service: {service.uuid}")
                    for char in service.characteristics:
                        print(f"  Characteristic: {char.uuid}, Handle: {char.handle}, Properties: {char.properties}")

                heart_rate_service = None
                for service in services:
                    if service.uuid == HEART_RATE_SERVICE_UUID:
                        heart_rate_service = service
                        break

                if heart_rate_service is not None:
                    heart_rate_measurement_char = heart_rate_service.get_characteristic(HEART_RATE_MEASUREMENT_UUID)
                    if heart_rate_measurement_char is not None:
                        # Enable notifications for the characteristic
                        await client.start_notify(HEART_RATE_MEASUREMENT_UUID, heart_rate_callback)
                        await asyncio.sleep(30)  # Collect data for 30 seconds
                        await client.stop_notify(HEART_RATE_MEASUREMENT_UUID)
                        average_heart_rate = sum(heart_rate_values) / len(heart_rate_values)
                        print(f"Average Heart Rate: {average_heart_rate} bpm")
                        if average_heart_rate < 60:
                            print("Low heart rate")
                        elif 60 <= average_heart_rate <= 100:
                            print("Normal heart rate")
                        else:
                            print("High heart rate")
                    else:
                        print("Heart Rate Measurement Characteristic not found")
                else:
                    print("Heart Rate Service not found")

                break  # Exit loop if successful
        except BleakError as e:
            retry_count += 1
            print(f"Attempt {retry_count} failed: {e}")
            if retry_count == max_retries:
                print("Max retries reached. Could not connect to the device.")
            else:
                print("Retrying...")

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
