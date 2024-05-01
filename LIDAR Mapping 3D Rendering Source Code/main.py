from pygame import init, quit, event, mouse, key, display, time, QUIT, VIDEORESIZE, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN, K_ESCAPE, K_SPACE, MOUSEMOTION, MOUSEWHEEL
from random import randrange
import Window
import System
import Point
import LIDARSensor
import CoordinateReference
import DistanceExtraction

## Vertical and Horizontal Servo Arm to LIDAR Sensor Radius Offset: 1.8125" ##

WHITE  = "0xFFFFFF"
xRange = (-205, 205)
yRange = (-145, 145)
zRange = ( 392, 544)
lidarSensor = LIDARSensor.LIDARSensor()
window = Window.Window()
system = System.System()
coordinateReference = CoordinateReference.CoordinateReference()
distanceExtractor   = DistanceExtraction.DistanceExtraction()
points = []
distanceDataBuffer = []




def main():
    global distanceDataBuffer

    while system.running:
        system.clock.tick(system.fps)
        for pyEvent in event.get():
            if pyEvent.type == QUIT:
                distanceExtractor.closePort()
                system.quit()
            if pyEvent.type == KEYDOWN:
                if pyEvent.key == K_ESCAPE:
                    system.quit()
            ## Clear Points ##
            if pyEvent.type == KEYDOWN:
                if pyEvent.key == K_SPACE:
                    points.clear()
                    system.extractedDataCount = 0
            if pyEvent.type == MOUSEBUTTONDOWN:
                if pyEvent.button == 1:
                    system.mouseLeftDragging = True
                    system.mousePos = mouse.get_pos()
                elif pyEvent.button == 3:
                    system.mouseRightDragging = True
                    system.mousePos = mouse.get_pos()
            if pyEvent.type == MOUSEBUTTONUP:
                if pyEvent.button == 1:
                    system.mouseLeftDragging = False
                elif pyEvent.button == 3:
                    system.mouseRightDragging = False
            ## Zooming Transformations ##
            if pyEvent.type == MOUSEWHEEL:
                scrollAmount = pyEvent.y
                if scrollAmount > 0:
                    lidarSensor.zoomIn()
                    for point in points:
                        point.zoomIn()
                elif scrollAmount < 0:
                    lidarSensor.zoomOut()
                    for point in points:
                        point.zoomOut()
            if pyEvent.type == MOUSEMOTION:
                ## Rotating Transformations ##
                if system.mouseLeftDragging:
                    system.xRotation = system.mousePos[0] - pyEvent.pos[0]
                    system.yRotation = pyEvent.pos[1] - system.mousePos[1]
                    coordinateReference.rotateX(system.xRotation * system.xRotOffset)
                    coordinateReference.rotateY(system.yRotation * system.yRotOffset)
                    lidarSensor.rotateX(system.xRotation * system.xRotOffset)
                    lidarSensor.rotateY(system.yRotation * system.yRotOffset)
                    for point in points:
                        point.rotateX(system.xRotation * system.xRotOffset)
                        point.rotateY(system.yRotation * system.yRotOffset)
                    system.mousePos = pyEvent.pos
                ## Translating Transformations ##
                elif system.mouseRightDragging:
                    system.xTranslation = pyEvent.pos[0] - system.mousePos[0]
                    system.yTranslation = pyEvent.pos[1] - system.mousePos[1]
                    lidarSensor.translateX(system.xTranslation)
                    lidarSensor.translateY(system.yTranslation)
                    for point in points:
                        point.translateX(system.xTranslation)
                        point.translateY(system.yTranslation)
                    system.mousePos = pyEvent.pos

        ## mBed Coordinates Extraction ##
        distanceData = distanceExtractor.extractDistance()
        if distanceData:
            try:
                if distanceData[0] == "C":
                    distanceDataBuffer.append(int(distanceData[2:].strip()))
                    if distanceDataBuffer[2] != 0:
                        coordinates = distanceExtractor.getCoordinates(distanceDataBuffer[0], distanceDataBuffer[1], distanceDataBuffer[2])
                        points.append(Point.Point(coordinates[0], coordinates[1], coordinates[2], WHITE))
                        print(distanceDataBuffer)
                        distanceDataBuffer.clear()
                        system.extractedDataCount += 1
                    else:
                        print(distanceDataBuffer, "CLEARING")
                        distanceData.clear()
                elif distanceData[0] == "A" or distanceData[0] == "B":
                    distanceDataBuffer.append(float(distanceData[2:].strip()))
            except:
                pass

        ## Screen Rendering Drawing ##
        coordinateReference.draw(window)
        for point in points:
            point.draw(window)
        lidarSensor.drawPoints(window)
        lidarSensor.drawLIDARFOV(window)
        window.draw()

    quit()




if __name__ == "__main__":
    init()
    main()