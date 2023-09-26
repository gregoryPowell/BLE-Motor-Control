import asyncio
import uuid

from bleak import BleakClient, BleakScanner
from bleak.backends.bluezdbus.client import BleakClientBlueZDBus

# device_name1 = "Nunchuk"
device_name2 = "Nunchuk"
z_button_uuid = '9ea41596-18ec-45a9-a194-49597368e655'
# switch_status_char_uuid = "8158b2fe-94e4-4ff5-a99d-9a7980e998d7"


def notification_handler(sender, data):
    print("Z button is active: {}".format(bool(data[0])))


async def run():
    client = None
    external_heartbeat_received = False
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: d.name and d.name.lower() == device_name2.lower()
    )

    if device is None:
        print("{} not found".format(device_name2))
    else:
        print("{} found".format(device))

    # client = BleakClientBlueZDBus(device)
    client = BleakClient(device)

    try:
        timer = 30  # seconds

        while timer != 0 or external_heartbeat_received:
            if not client.is_connected:
                if await client.connect():
                    print("Connected to {}".format(device_name2))
                    print("Attempting to notify")
                    await client.start_notify(z_button_uuid, notification_handler)
                    print("Notify on...")
            await asyncio.sleep(1)
            timer -= 1

            # If timer expired and we received a heartbeat, restart timer and carry on.
            if timer == 0:
                if external_heartbeat_received:
                    timer = 60
                    external_heartbeat_received = False
    except Exception as error:
        print('ERROR: ',error)
        print("Connected to {} failed".format(device_name2))
        

    if client is not None and client.is_connected:
        await client.disconnect()
        print("Disconnected from {}".format(device_name2))

loop = asyncio.get_event_loop()
loop.run_until_complete(run())