import pygame


class Scene:
    def __init__(self, width, height, background=(0, 0, 0), caption=None, icon=None, fps=60):
        self.width = width
        self.height = height
        self.fps = fps
        self.items = []
        self.sprites = {}
        self.keyboard = []
        self.background = background


        pygame.init()

        if caption is not None:
            pygame.display.set_caption(caption)
        if icon is not None:
            pygame.display.set_icon(pygame.image.load(icon))

        self.screen = pygame.display.set_mode((self.width, self.height), vsync=True)
        self.clock = None
        self.font = pygame.font.SysFont("Monaco", 30)

    def add(self, unit):
        self.items.append(unit)

    def update(self, delta):
        for item in self.items:
            item.update(delta)

    def draw(self, screen):
        for item in self.items:
            item.draw(screen)

    def debug(self, delta):
        string = ("FPS "+str(int(self.clock.get_fps()))).rjust(8)+' DELTA '+str(delta)
        pygame.display.set_caption(string)
        self.screen.blit(self.font.render(string, 1, pygame.Color("pink")), (10,10))


    def run(self):
        delta = 0
        running = True
        self.clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
                    running = False

            self.keyboard = pygame.key.get_pressed()
            self.update(delta)

            self.screen.fill(self.background)

            self.draw(self.screen)
            self.debug(delta)

            pygame.display.update()
            delta = self.clock.tick(self.fps)
            #delta = self.clock.tick()
