from pygame import draw
from math import sin, cos, radians
import numpy as np


class LIDARSensor:

    originPointSize = 6
    pointSize = 3
    lineSize = 1
    zoomInCoefficient = 1.05
    zoomOutCoefficient = 0.95
    translationCoefficient = 5
    NAVY = "0xB3A369"
    GOLD = "0x003057"

    def __init__(self):
        self.origin = np.array([0.0, 0.0, 0.0])
        self.topLeft = np.array([-15.745752354, -11.19679625, 41.787012946])
        self.topRight = np.array([15.745752354, -11.19679625, 41.787012946])
        self.bottomLeft = np.array([-15.745752354, 11.19679625, 41.787012946])
        self.bottomRight = np.array([15.745752354, 11.19679625, 41.787012946])
        self.outerTopLeft = np.array([-186.400978110, -132.54963901, 544.681987300])
        self.outerTopRight = np.array([186.400978110, -132.54963901, 544.681987300])
        self.outerBottomLeft = np.array([-186.400978110, 132.54963901, 544.681987300])
        self.outerBottomRight = np.array([186.400978110, 132.54963901, 544.681987300])
    
    def drawPoints(self, window):
        draw.circle(window.window, LIDARSensor.NAVY, (self.topLeft[0] + (window.width // 2), self.topLeft[1] + (window.height // 2)), LIDARSensor.pointSize)
        draw.circle(window.window, LIDARSensor.NAVY, (self.topRight[0] + (window.width // 2), self.topRight[1] + (window.height // 2)), LIDARSensor.pointSize)
        draw.circle(window.window, LIDARSensor.NAVY, (self.bottomLeft[0] + (window.width // 2), self.bottomLeft[1] + (window.height // 2)), LIDARSensor.pointSize)
        draw.circle(window.window, LIDARSensor.NAVY, (self.bottomRight[0] + (window.width // 2), self.bottomRight[1] + (window.height // 2)), LIDARSensor.pointSize)
        draw.circle(window.window, LIDARSensor.GOLD, (self.origin[0] + (window.width // 2), self.origin[1] + (window.height // 2)), LIDARSensor.originPointSize)
    
    def drawLIDARFOV(self, window):
        draw.line(window.window, LIDARSensor.NAVY, (self.origin[0] + (window.width // 2), self.origin[1] + (window.height // 2)), (self.outerTopLeft[0] + (window.width // 2), self.outerTopLeft[1] + (window.height // 2)), LIDARSensor.lineSize)
        draw.line(window.window, LIDARSensor.NAVY, (self.origin[0] + (window.width // 2), self.origin[1] + (window.height // 2)), (self.outerTopRight[0] + (window.width // 2), self.outerTopRight[1] + (window.height // 2)), LIDARSensor.lineSize)
        draw.line(window.window, LIDARSensor.NAVY, (self.origin[0] + (window.width // 2), self.origin[1] + (window.height // 2)), (self.outerBottomLeft[0] + (window.width // 2), self.outerBottomLeft[1] + (window.height // 2)), LIDARSensor.lineSize)
        draw.line(window.window, LIDARSensor.NAVY, (self.origin[0] + (window.width // 2), self.origin[1] + (window.height // 2)), (self.outerBottomRight[0] + (window.width // 2), self.outerBottomRight[1] + (window.height // 2)), LIDARSensor.lineSize)

        draw.polygon(window.window, LIDARSensor.GOLD, [
                (self.origin[0] + (window.width // 2), self.origin[1] + (window.height // 2)),
                (self.bottomRight[0] + (window.width // 2), self.bottomRight[1] + (window.height // 2)),
                (self.bottomLeft[0] + (window.width // 2), self.bottomLeft[1] + (window.height // 2))
            ]
        )
        draw.polygon(window.window, LIDARSensor.NAVY, [
                (self.origin[0] + (window.width // 2), self.origin[1] + (window.height // 2)),
                (self.bottomLeft[0] + (window.width // 2), self.bottomLeft[1] + (window.height // 2)),
                (self.topLeft[0] + (window.width // 2), self.topLeft[1] + (window.height // 2))
            ]
        )
        draw.polygon(window.window, LIDARSensor.NAVY, [
                (self.origin[0] + (window.width // 2), self.origin[1] + (window.height // 2)),
                (self.topRight[0] + (window.width // 2), self.topRight[1] + (window.height // 2)),
                (self.bottomRight[0] + (window.width // 2), self.bottomRight[1] + (window.height // 2))
            ]
        )
        draw.polygon(window.window, LIDARSensor.GOLD, [
                (self.origin[0] + (window.width // 2), self.origin[1] + (window.height // 2)),
                (self.topLeft[0] + (window.width // 2), self.topLeft[1] + (window.height // 2)),
                (self.topRight[0] + (window.width // 2), self.topRight[1] + (window.height // 2))
            ]
        )

    def rotateX(self, angle = 0):
        xRotationMatrix = np.array([
            [cos(radians(angle)), 0, sin(radians(angle))],
            [0, 1, 0],
            [-sin(radians(angle)), 0, cos(radians(angle))]
        ])
        self.origin = xRotationMatrix @ self.origin
        self.topLeft = xRotationMatrix @ self.topLeft
        self.topRight = xRotationMatrix @ self.topRight
        self.bottomLeft = xRotationMatrix @ self.bottomLeft
        self.bottomRight = xRotationMatrix @ self.bottomRight
        self.outerTopLeft = xRotationMatrix @ self.outerTopLeft
        self.outerTopRight = xRotationMatrix @ self.outerTopRight
        self.outerBottomLeft = xRotationMatrix @ self.outerBottomLeft
        self.outerBottomRight = xRotationMatrix @ self.outerBottomRight

    def rotateY(self, angle = 0):
        yRotationMatrix = np.array([
            [1, 0, 0],
            [0, cos(radians(angle)), -sin(radians(angle))],
            [0, sin(radians(angle)), cos(radians(angle))]
        ])
        self.origin = yRotationMatrix @ self.origin
        self.topLeft = yRotationMatrix @ self.topLeft
        self.topRight = yRotationMatrix @ self.topRight
        self.bottomLeft = yRotationMatrix @ self.bottomLeft
        self.bottomRight = yRotationMatrix @ self.bottomRight
        self.outerTopLeft = yRotationMatrix @ self.outerTopLeft
        self.outerTopRight = yRotationMatrix @ self.outerTopRight
        self.outerBottomLeft = yRotationMatrix @ self.outerBottomLeft
        self.outerBottomRight = yRotationMatrix @ self.outerBottomRight
    
    def zoomIn(self):
        zoomInMatrix = np.array([[LIDARSensor.zoomInCoefficient, 0, 0], [0, LIDARSensor.zoomInCoefficient, 0], [0, 0, LIDARSensor.zoomInCoefficient]])
        self.origin = zoomInMatrix @ self.origin
        self.topLeft = zoomInMatrix @ self.topLeft
        self.topRight = zoomInMatrix @ self.topRight
        self.bottomLeft = zoomInMatrix @ self.bottomLeft
        self.bottomRight = zoomInMatrix @ self.bottomRight
        self.outerTopLeft = zoomInMatrix @ self.outerTopLeft
        self.outerTopRight = zoomInMatrix @ self.outerTopRight
        self.outerBottomLeft = zoomInMatrix @ self.outerBottomLeft
        self.outerBottomRight = zoomInMatrix @ self.outerBottomRight
    
    def zoomOut(self):
        zoomOutMatrix = np.array([[LIDARSensor.zoomOutCoefficient, 0, 0], [0, LIDARSensor.zoomOutCoefficient, 0], [0, 0, LIDARSensor.zoomOutCoefficient]])
        self.origin = zoomOutMatrix @ self.origin
        self.topLeft = zoomOutMatrix @ self.topLeft
        self.topRight = zoomOutMatrix @ self.topRight
        self.bottomLeft = zoomOutMatrix @ self.bottomLeft
        self.bottomRight = zoomOutMatrix @ self.bottomRight
        self.outerTopLeft = zoomOutMatrix @ self.outerTopLeft
        self.outerTopRight = zoomOutMatrix @ self.outerTopRight
        self.outerBottomLeft = zoomOutMatrix @ self.outerBottomLeft
        self.outerBottomRight = zoomOutMatrix @ self.outerBottomRight
    
    def translateX(self, translation):
        xTranslationMatrix = np.array([translation, 0, 0])
        self.origin += xTranslationMatrix
        self.topLeft += xTranslationMatrix
        self.topRight += xTranslationMatrix
        self.bottomLeft += xTranslationMatrix
        self.bottomRight += xTranslationMatrix
        self.outerTopLeft += xTranslationMatrix
        self.outerTopRight += xTranslationMatrix
        self.outerBottomLeft += xTranslationMatrix
        self.outerBottomRight += xTranslationMatrix

    def translateY(self, translation):
        yTranslationMatrix = np.array([0, translation, 0])
        self.origin += yTranslationMatrix
        self.topLeft += yTranslationMatrix
        self.topRight += yTranslationMatrix
        self.bottomLeft += yTranslationMatrix
        self.bottomRight += yTranslationMatrix
        self.outerTopLeft += yTranslationMatrix
        self.outerTopRight += yTranslationMatrix
        self.outerBottomLeft += yTranslationMatrix
        self.outerBottomRight += yTranslationMatrix