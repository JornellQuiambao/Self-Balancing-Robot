import state_machines
import event_checker
import string
import time

# Two inputs:
#   sensor
#   sensor value

# Initial value: Top level state, sub level state

# "PowerOn -> FIND_TARGET -> STANDARD_FOLLOW"
# input(sensor, sensor value)
# "PowerOn -> FIND_TARGET -> BEYOND_LEFT"

# Sensors:
#   ping x3
#       0-1023
#   switch x1
#       0 (off)
#       1 (on)
#   cpvision x1
#       left
#       right
#       center
#       lost


def Run_Test_Bench(event_arr=None):
    HSM = state_machines.HSM_TopLevel(True)
    if event_arr is not None:
        user_in_value_arr = []
        i = 0
        while event_arr[i] is not None:
            pass

    print(HSM.get_state())

    # Get user input
    while True:
        user_in_sensor = input('Sensor: ')
        if user_in_sensor == "STOP":
            return
        user_in_value= input("Value: ")
        if user_in_sensor != 'cp vision':
            user_in_value = int(user_in_value)

        HSM.Event_Checker.Alter_Sensor(user_in_sensor, user_in_value)
        time.sleep(0.5)
        HSM.run_HSM()
        print(HSM.get_state())


if __name__ == "__main__":
    event_arr = None
    Run_Test_Bench(event_arr)