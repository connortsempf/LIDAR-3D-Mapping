from pygame import draw
from math import sin, cos, radians
import numpy as np


class Point:

    zoomInCoefficient = 1.05
    zoomOutCoefficient = 0.95
    translationCoefficient = 5 

    def __init__(self, xPos, yPos, zPos, color, size = 2):
        self.posVector = np.array([xPos, yPos, zPos])
        self.size = size
        self.color = color

    def draw(self, window):
        draw.circle(window.window, self.color, \
        (self.posVector[0] + (window.width // 2), self.posVector[1] + (window.height // 2)), self.size)

    def rotateX(self, angle = 0):
        xRotationMatrix = np.array([
            [cos(radians(angle)), 0, sin(radians(angle))],
            [0, 1, 0],
            [-sin(radians(angle)), 0, cos(radians(angle))]
        ])
        self.posVector = xRotationMatrix @ self.posVector

    def rotateY(self, angle = 0):
        yRotationMatrix = np.array([
            [1, 0, 0],
            [0, cos(radians(angle)), -sin(radians(angle))],
            [0, sin(radians(angle)), cos(radians(angle))]
        ])
        self.posVector = yRotationMatrix @ self.posVector
    
    def zoomIn(self):
        zoomInMatrix = np.array([[Point.zoomInCoefficient, 0, 0], [0, Point.zoomInCoefficient, 0], [0, 0, Point.zoomInCoefficient]])
        self.posVector = zoomInMatrix @ self.posVector

    def zoomOut(self):
        zoomOutMatrix = np.array([[Point.zoomOutCoefficient, 0, 0], [0, Point.zoomOutCoefficient, 0], [0, 0, Point.zoomOutCoefficient]])
        self.posVector = zoomOutMatrix @ self.posVector

    def translateX(self, translation):
        xTranslationMatrix = np.array([translation, 0, 0])
        self.posVector += xTranslationMatrix

    def translateY(self, translation):
        yTranslationMatrix = np.array([0, translation, 0])
        self.posVector += yTranslationMatrix