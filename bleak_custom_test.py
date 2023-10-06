import asyncio
import RPi.GPIO as GPIO

from bleak import BleakClient, BleakScanner
from RpiMotorLib import RpiMotorLib


################################
# BLE Defines
################################
DEVICE_NAME = "Nunchuk"
Z_BUTTON_UUID = "9ea41596-18ec-45a9-a194-49597368e655"
C_BUTTON_UUID = "9ea41596-18ed-45a9-a194-49597368e655"
JOYSTICK_X_UUID = "9ea41596-18ee-45a9-a194-49597368e655"
JOYSTICK_Y_UUID = "9ea41596-18ef-45a9-a194-49597368e655"
ACC_X_UUID = "9ea41596-18f0-45a9-a194-49597368e655"
ACC_Y_UUID = "9ea41596-18f1-45a9-a194-49597368e655"
ACC_Z_UUID = "9ea41596-18f2-45a9-a194-49597368e655"
PITCH_UUID = "9ea41596-18f3-45a9-a194-49597368e655"
ROLL_UUID = "9ea41596-18f4-45a9-a194-49597368e655"


################################
# GPIO Defines
################################
# define GPIO pins
GPIO_pins = (14, 15, 18)  # Microstep Resolution
direction = 20  # DIR GPIO pin
step = 21  # Step GPIO pin


################################
# Classes
################################
class Nunchuk:
    def __init__(self):
        self.z_button = 0
        self.c_button = 0
        self.joystick = [0, 0]
        self.acc = [0, 0, 0]
        self.pitch = 0
        self.roll = 0

    def __str__(self):
        # joy_values = [f"{value}" for value in self.joystick]
        # acc_values = [f"{value}" for value in self.acc]
        return f"||  {self.z_button}  |  {self.c_button}  |  {self.joystick}  |  {self.acc}  |  {self.pitch}  |  {self.roll}  ||"


################################
# Named Class Instances
################################
nunchuk = Nunchuk()
motor1 = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "DRV8825")


################################
# BLE Notiy Call-Back
################################
def notification_handler(sender, data):
    external_heartbeat_received = True
    if sender.uuid == Z_BUTTON_UUID:
        nunchuk.z_button = int.from_bytes(data, "little")
    elif sender.uuid == C_BUTTON_UUID:
        nunchuk.c_button = int.from_bytes(data, "little")
    elif sender.uuid == JOYSTICK_X_UUID:
        nunchuk.joystick[0] = int.from_bytes(data, "little")
    elif sender.uuid == JOYSTICK_Y_UUID:
        nunchuk.joystick[1] = int.from_bytes(data, "little")
    elif sender.uuid == ACC_X_UUID:
        nunchuk.acc[0] = int.from_bytes(data, "little")
    elif sender.uuid == ACC_Y_UUID:
        nunchuk.acc[1] = int.from_bytes(data, "little")
    elif sender.uuid == ACC_Z_UUID:
        nunchuk.acc[2] = int.from_bytes(data, "little")
    elif sender.uuid == PITCH_UUID:
        nunchuk.pitch = int.from_bytes(data, "little")
    elif sender.uuid == ROLL_UUID:
        nunchuk.roll = int.from_bytes(data, "little")


################################
# Motor Controller Function
################################
def motor_controller():
    if (nunchuk.joystick[0] > 128):
        direction = False
    elif (nunchuk.joystick[0] < 128):
        direction = True
    else:
        return

    motor1.motor_go(direction, "1/4", 1, 0.01, False, 0)


################################
# Main Program Loop
################################
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
        timer = 60  # seconds
        print("attempting to connect")
        while timer != 0:
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
                    break

            await asyncio.sleep(1)
            timer -= 1

    except Exception as error:
        print("ERROR: ", error)
        print("Connected to {} failed".format(DEVICE_NAME))

    
    while(client.is_connected):
        
        print(str(nunchuk))

        motor_controller()
        await asyncio.sleep(0)

        # force disconnect
        if (nunchuk.z_button == 255) and (nunchuk.c_button == 255):
            await client.disconnect()
            print("Disconnected from {}".format(DEVICE_NAME))






if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

    GPIO.cleanup()
    print("Program Ended and GPIOs cleaned!")
