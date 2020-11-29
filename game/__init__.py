import pygame

class Sprite:
    def __init__(self,
                 file,
                 width=None,
                 height=None,
                 cell=None,
                 row=None,
                 count=1,
                 speed=100, # Do not like speed
                 replace=None,
                 vertical=False):
        self.sheet = pygame.image.load(file)
        self.vertical = vertical
        self.width = width
        self.height = height
        self.cells = self.sheet.get_width()//self.width
        self.rows = self.sheet.get_height()//self.height
        self.items = {}
        self.speeds = {}

        if replace is not None:
            array = pygame.PixelArray(self.sheet)
            for color in replace:
                array.replace(color[0], color[1])
            array.close()

        if cell is not None and row is not None:
            self.add('main', cell, row, count, speed)

    # GOOD
    def image(self, cell, row, flip=None):
        rect = pygame.Rect(((cell-1)*self.width, (row-1)*self.height, self.width, self.height))
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        if isinstance(flip, tuple):
            image = pygame.transform.flip(image, flip[0], flip[1])

        return image

    def slice(self, cell=1, row=1, count=1, flip=None):
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

        return [self.image(rect[0], rect[1], flip=flip) for rect in rects]

    def add(self, name, cell=1, row=1, count=1, flip=None, speed=100):
        self.items[name] = self.slice(cell, row, count, flip=flip)
        self.speeds[name] = speed


class Scene:
    def __init__(self, width, height, background=(0, 0, 0), caption=None, icon=None, fps=60):
        self.width = width
        self.height = height
        self.fps = fps
        self.items = []
        self.keyboard = []
        self.background = background

        pygame.init()

        if caption is not None:
            pygame.display.set_caption(caption)
        if icon is not None:
            pygame.display.set_icon(pygame.image.load(icon))

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = None

    def add(self, object):
        object.scene = self
        self.items.append(object)

    def update(self, delta):
        for item in self.items:
            item.update(delta)

    def draw(self, screen):
        for item in self.items:
            item.draw(screen)

    def run(self):
        delta = 0
        running = True
        self.clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
                    running = False

            self.keyboard = pygame.key.get_pressed()
            scene.update(delta)

            self.screen.fill(self.background)

            scene.draw(self.screen)

            pygame.display.update()
            delta = self.clock.tick(self.fps)


class Object:
    def __init__(self):
        self.scene = None
        self.sprite = None
        self.x = 0
        self.y = 0
        self.width = None
        self.height = None
        self.anim = 'main'
        self.frame = 1
        self.timer = 0
        self.speed = 100

    def update(self, delta):
        self.next(delta)

    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.image(), (self.width, self.height)), (self.x, self.y))

    def next(self, delta):
        if len(self.sprite.items[self.anim]) == 1:
            return
        self.timer += delta
        if self.timer < self.sprite.speeds[self.anim]:
            return
        self.timer = 0
        self.frame += 1
        if self.frame > len(self.sprite.items[self.anim]):
            self.frame = 1

    def image(self):
        if self.sprite is None:
            return
        try:
            return self.sprite.items[self.anim][self.frame-1]
        except Exception as e:
            print('Frame', self.frame, 'not found of', self.anim)
            raise(e)

    def move(self, x, y):
        self.x += x
        self.y += y
        if self.y < 0:
            self.y = 0
        elif self.y+self.height > self.scene.height:
            self.y = self.scene.height-self.height
        if self.x < 0:
            self.x = 0
        elif self.x+self.width > self.scene.width:
            self.x = self.scene.width-self.width
    def key(self, key):
        if self.scene.keyboard[key]:
            return True
        return False
    def play(self, anim):
        if self.anim != anim:
            self.timer = 0
            self.frame = 1
            self.anim = anim
