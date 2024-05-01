from pygame import draw
from math import sin, cos, radians
import numpy as np


class CoordinateReference:

    originPointSize = 10
    pointSize = 6
    lineSize = 3
    OWHITE = "0xFFFFFF"
    XBLUE = "0x3F48CC"
    YRED = "0xCC3F3F"
    ZGREEN = "0x41CC3F"

    def __init__(self):
        self.drawPoint = np.array([100, 700,   0])
        self.xVector = np.array([ 75,   0,   0])
        self.yVector = np.array([  0, -75,   0])
        self.zVector = np.array([  0,   0, -75])
    
    def draw(self, window):
        draw.line(window.window, CoordinateReference.XBLUE, (self.drawPoint[0], self.drawPoint[1]), (self.xVector[0] + self.drawPoint[0], self.xVector[1] + self.drawPoint[1]), CoordinateReference.lineSize)
        draw.line(window.window, CoordinateReference.YRED, (self.drawPoint[0], self.drawPoint[1]), (self.yVector[0] + self.drawPoint[0], self.yVector[1] + self.drawPoint[1]), CoordinateReference.lineSize)
        draw.line(window.window, CoordinateReference.ZGREEN, (self.drawPoint[0], self.drawPoint[1]), (self.zVector[0] + self.drawPoint[0], self.zVector[1] + self.drawPoint[1]), CoordinateReference.lineSize)
        draw.circle(window.window, CoordinateReference.XBLUE, (self.xVector[0] + self.drawPoint[0], self.xVector[1] + self.drawPoint[1]), CoordinateReference.pointSize)
        draw.circle(window.window, CoordinateReference.YRED, (self.yVector[0] + self.drawPoint[0], self.yVector[1] + self.drawPoint[1]), CoordinateReference.pointSize)
        draw.circle(window.window, CoordinateReference.ZGREEN, (self.zVector[0] + self.drawPoint[0], self.zVector[1] + self.drawPoint[1]), CoordinateReference.pointSize)
        draw.circle(window.window, CoordinateReference.OWHITE, (self.drawPoint[0], self.drawPoint[1]), CoordinateReference.originPointSize)

    def rotateX(self, angle = 0):
        xRotationMatrix = np.array([
            [cos(radians(angle)), 0, sin(radians(angle))],
            [0, 1, 0],
            [-sin(radians(angle)), 0, cos(radians(angle))]
        ])
        self.xVector = xRotationMatrix @ self.xVector
        self.yVector = xRotationMatrix @ self.yVector
        self.zVector = xRotationMatrix @ self.zVector

    def rotateY(self, angle = 0):
        yRotationMatrix = np.array([
            [1, 0, 0],
            [0, cos(radians(angle)), -sin(radians(angle))],
            [0, sin(radians(angle)), cos(radians(angle))]
        ])
        self.xVector = yRotationMatrix @ self.xVector
        self.yVector = yRotationMatrix @ self.yVector
        self.zVector = yRotationMatrix @ self.zVector