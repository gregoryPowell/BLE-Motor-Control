import asyncio
import uuid

from bleak import BleakClient, BleakScanner
from bleak.backends.bluezdbus.client import BleakClientBlueZDBus

DEVICE_NAME = "Nunchuk"
Z_BUTTON_UUID = '9ea41596-18ec-45a9-a194-49597368e655'
C_BUTTON_UUID = '9ea41596-18ed-45a9-a194-49597368e655'
JOYSTICK_X_UUID = '9ea41596-18ee-45a9-a194-49597368e655'
JOYSTICK_Y_UUID = '9ea41596-18ef-45a9-a194-49597368e655'
ACC_X_UUID = '9ea41596-18f0-45a9-a194-49597368e655'
ACC_Y_UUID = '9ea41596-18f1-45a9-a194-49597368e655'
ACC_Z_UUID = '9ea41596-18f2-45a9-a194-49597368e655'
PITCH_UUID = '9ea41596-18f3-45a9-a194-49597368e655'
ROLL_UUID = '9ea41596-18f4-45a9-a194-49597368e655'


def notification_handler(sender, data):
    if (sender.uuid == Z_BUTTON_UUID):
        print("Z button is active: {}".format(bool(data[0])))
    elif (sender.uuid == C_BUTTON_UUID):
        print("C button is active: {}".format(data[0]))
    elif (sender.uuid == JOYSTICK_X_UUID):
        print("Joystick X is active: {}".format(data[0]))
    elif (sender.uuid == JOYSTICK_Y_UUID):
        print("Joystick Y is active: {}".format(data[0]))
    elif (sender.uuid == ACC_X_UUID):
        print("ACC X is active: {}".format(data[0]))
    elif (sender.uuid == ACC_Y_UUID):
        print("ACC Y is active: {}".format(data[0]))
    elif (sender.uuid == ACC_Z_UUID):
        print("ACC Z is active: {}".format(data[0]))
    elif (sender.uuid == PITCH_UUID):
        print("Pitch is active: {.2f}".format(data[0]))
    elif (sender.uuid == ROLL_UUID):
        print("Roll is active: {.2f}".format(data[0]))


async def run():
    client = None
    external_heartbeat_received = False
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: d.name and d.name.lower() == DEVICE_NAME.lower()
    )

    if device is None:
        print("{} not found".format(DEVICE_NAME))
    else:
        print("{} found".format(device))

    # client = BleakClientBlueZDBus(device)
    client = BleakClient(device)

    try:
        timer = 30  # seconds

        while timer != 0 or external_heartbeat_received:
            if not client.is_connected:
                if await client.connect():
                    print("Connected to {}".format(DEVICE_NAME))
                    print("Attempting to notify")
                    await client.start_notify(Z_BUTTON_UUID, notification_handler)
                    await client.start_notify(C_BUTTON_UUID, notification_handler)
                    await client.start_notify(JOYSTICK_X_UUID, notification_handler)
                    await client.start_notify(JOYSTICK_Y_UUID, notification_handler)
                    await client.start_notify(ACC_X_UUID, notification_handler)
                    await client.start_notify(ACC_Y_UUID, notification_handler)
                    await client.start_notify(ACC_Z_UUID, notification_handler)
                    await client.start_notify(PITCH_UUID, notification_handler)
                    await client.start_notify(ROLL_UUID, notification_handler)
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
        print("Connected to {} failed".format(DEVICE_NAME))
        

    if client is not None and client.is_connected:
        await client.disconnect()
        print("Disconnected from {}".format(DEVICE_NAME))

loop = asyncio.get_event_loop()
loop.run_until_complete(run())