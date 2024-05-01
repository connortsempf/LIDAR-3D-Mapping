from pygame import display, RESIZABLE, image, transform


class Window:

    def __init__(self):
        self.window = display.set_mode((1200, 800))
        self.width = self.window.get_size()[0]
        self.height = self.window.get_size()[1]
        self.backgroundColor = "0x232323"
        display.set_caption("LIDAR Mapping")

    def draw(self):
        display.update()
        self.window.fill(self.backgroundColor)