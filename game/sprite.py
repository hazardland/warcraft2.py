import pygame

class Sprite:
    def __init__(self,
                 file,
                 width=None,
                 height=None,
                 frame=None,
                 count=1,
                 pause=100,
                 replace=None,
                 vertical=False):
        self.image = pygame.image.load(file).convert_alpha()
        self.vertical = vertical
        self.width = width
        self.height = height
        self.cells = self.image.get_width()//self.width
        self.rows = self.image.get_height()//self.height
        self.frames = {}
        self.pauses = {}
        self.pause = pause

        if replace is not None:
            array = pygame.PixelArray(self.image)
            for color in replace:
                array.replace(color[0], color[1])
            array.close()

        if frame is not None:
            self.add('main', frame, count, pause)

    def frame(self, frame):
        """
            Returns frame number based on frame=(cell,row) tuple
            considers sprite.vertical=False/True parameter
            by default sprite is horizontal
        """
        if self.vertical:
            cell = ((frame-1)//self.rows)+1
            row = frame-(cell-1)*self.rows
        else:
            row = ((frame-1)//self.cells)+1
            cell = frame-(row-1)*self.cells

        return cell, row

    def get(self, frame, flip=None):

        if isinstance(frame, tuple):
            cell, row = frame
        else:
            cell, row = self.frame(frame)

        rect = pygame.Rect(((cell-1)*self.width, (row-1)*self.height, self.width, self.height))

        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.image, (0, 0), rect)
        if isinstance(flip, tuple):
            image = pygame.transform.flip(image, flip[0], flip[1])

        return image

    def slice(self, frame=1, count=1, flip=None):

        if isinstance(frame, tuple):
            cell, row = frame
        else:
            cell, row = self.frame(frame)

        rects = []
        for _ in range(count):
            rects.append((cell, row))
            if self.vertical:
                if row+1 > self.rows:
                    row = 1
                    cell += 1
                row += 1
            else:
                if cell+1 > self.cells:
                    cell = 1
                    row += 1
                cell += 1

        return [self.get((rect[0], rect[1]), flip=flip) for rect in rects]

    def add(self, name, frame, count=1, flip=None, pause=None):
        self.frames[name] = self.slice(frame, count, flip=flip)
        self.pauses[name] = pause if pause is not None else self.pause
