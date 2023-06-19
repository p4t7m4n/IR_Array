# This is an example for saving images (txt and png) with the Heimann IR Sensor.
# It is not finished yet and has some errors (running the script multiple times solves this for now)
#
# hterm.exe als Serial Plotter

# Import needed libraries
import serial
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

# For Folder Selection Window
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()


# 1) Select your type of sensor

# ARRAY = (8, 8)    # 8x8 Sensor
# ARRAY = (16, 16)    # 16x16 Sensor
ARRAY = (40, 60)  # 60x40 Sensor

# 2) Select your COM Port and Baudrate (should be fixed for the ESP.ino script)
COMPORT = "COM4"
BAUDRATE = 115200

# 3) Save Options
showFolderSelectionWindow = True


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    d["micro"] = tdelta.microseconds
    return fmt.format(**d)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Prompt to ask how many images should be saved
    nImagesToSave = int(input("How many images to save?\n"))

    # Save Settings
    if showFolderSelectionWindow:
        dir_name = filedialog.askdirectory(initialdir=os.getcwd())  # Folder Selection Dialog
    else:
        dir_name = os.getcwd()  # Current Working Directory
    suffix = '.txt'

    # Initialize Serial Communication
    print("Initializing serial communication ...")
    ser = serial.Serial(COMPORT, BAUDRATE)  # Open port with baud rate
    print("finished.\n")

    # TODO Lösung bei Sensor-Abbruch (evtl. Arduino-seitig)
    while ser.in_waiting:
        print("hier")
        data_out = ser.readline() #.decode("ascii")
        print("ende")
        print(data_out)

    # sleep(0.1)

    # Using current time
    ini_time = datetime.now()

    for x in range(nImagesToSave):

        ser.write("a".encode())
        # ser.write(b'01100001')
        sleep(0.01)

        if ARRAY == (8, 8):
            data_out = ser.read(357)  # 8*302 Bytes + 21 Bytes Header
            # print(data_out.decode())

        if ARRAY == (16, 16):
            data_out = ser.read(1339)  # 16*82 Bytes + 21 Bytes Header
            # print("Ab hier.")
            # print(data_out.decode())
            # print("Bis hier.")

        # Reads one frame for 40,60 Sensor
        if ARRAY == (40, 60):
            data_out = ser.read(12101)  # 40*302 Bytes + 21 Bytes Header
            # print(data_out.decode())

        # Evtl. TODO for other Sensors

        # else:
        #     # Reads one frame
        #     while ser.in_waiting:
        #         data_out = ser.read()  # .decode("ascii")
        #         sleep(0.05)
        #         data_left = ser.inWaiting()  # check for remaining byte
        #         data_out += ser.read(data_left)
        #         # print(data_out.decode())
        #         print("Received Data.\n")

        imageData = data_out.decode()

        if ARRAY == (8,8):
            imageData = imageData[21:-1]    # (ab dem 21. Bit wg. Header)
        elif ARRAY == (16, 16):
            imageData = imageData[27:-1]    #TODO (ab dem 27. Bit wg. Header)
        elif ARRAY == (40, 60):
            imageData = imageData[21:-1]    # (ab dem 21. Bit wg. Header)

        # Write result to file
        fname = '{}_{}_{}.txt'.format(ARRAY, x, strfdelta(datetime.now()-ini_time, "{hours}-{minutes}-{seconds}-{micro}"))
        base_filename = '{}_{}_{}'.format(ARRAY, x, strfdelta(datetime.now()-ini_time, "{hours}-{minutes}-{seconds}-{micro}"))
        savePath = os.path.join(dir_name, base_filename + suffix)
        f = open(savePath, 'w')
        f.write(imageData.strip("\n"))
        print("File written to '{}'.\n".format(fname))

        sleep(0.01)

    # Closing Port
    ser.close()

    # Plots last image and saves it
    test = np.fromstring(imageData, sep='\t')
    test = test.reshape(ARRAY)
    plt.imshow(test, interpolation='none')
    plt.title("Received IR-Data")

    plt.savefig('IR_Array.png')
    plt.show()


