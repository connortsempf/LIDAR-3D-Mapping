import serial
from math import sin, cos, radians
import numpy as np
import os


class DistanceExtraction:
    
    comPort = "COM3"
    baudRate = 9600
    encoding = "utf-8"
    clearCommand = "CLEAR"

    def __init__(self):
        self.serialPort = serial.Serial(DistanceExtraction.comPort, DistanceExtraction.baudRate, timeout = 0)

    def extractDistance(self):
        data = str(self.serialPort.readline().decode(DistanceExtraction.encoding))
        self.serialPort.flush()
        if data.strip() == DistanceExtraction.clearCommand:
            os.system("cls" if os.name == "nt" else "clear")
        else:
            return data

    def getCoordinates(self, horizontalAngle, verticalAngle, distance):
        horizontalRotationMatrix = np.array([
            [cos(radians(horizontalAngle)), 0, sin(radians(horizontalAngle))],
            [0, 1, 0],
            [-sin(radians(horizontalAngle)), 0, cos(radians(horizontalAngle))]
        ])
        verticalRotationMatrix = np.array([
            [1, 0, 0],
            [0, cos(radians(verticalAngle)), -sin(radians(verticalAngle))],
            [0, sin(radians(verticalAngle)), cos(radians(verticalAngle))]
        ])
        posVector = horizontalRotationMatrix @ np.array([0, 0, distance])
        posVector = verticalRotationMatrix @ posVector
        return posVector

    def closePort(self):
        if self.serialPort.is_open:
            self.serialPort.close()