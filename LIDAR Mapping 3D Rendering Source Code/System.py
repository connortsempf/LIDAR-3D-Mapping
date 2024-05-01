from pygame import time


class System:

    def __init__(self):
        self.fps = 120
        self.clock = time.Clock()
        self.running = True
        self.mouseLeftDragging = False
        self.mouseRightDragging = False
        self.mousePos = (0, 0)
        self.xRotation = 0
        self.yRotation = 0
        self.xRotOffset = 0.035
        self.yRotOffset = 0.035
        self.xTranslation = 0
        self.yTranslation = 0
        self.extractedDataCount = 0
    
    def quit(self):
        self.running = False