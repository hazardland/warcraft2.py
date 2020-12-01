import pygame

class Unit:
    def __init__(self, scene):
        self.scene = scene
        self.sprite = None
        self.x = 0
        self.y = 0
        self.width = None
        self.height = None
        self.anim = 'main'
        self.frame = 1
        self.timer = 0
        self.speed = 100
        scene.add(self)

    def update(self, delta):
        self.next(delta)

    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.image(), (self.width, self.height)),
                    (self.x, self.y))

    def next(self, delta):
        if len(self.sprite.frames[self.anim]) == 1:
            return
        self.timer += delta
        if self.timer < self.sprite.pauses[self.anim]:
            return
        self.timer = 0
        self.frame += 1
        if self.frame > len(self.sprite.frames[self.anim]):
            self.frame = 1

    def image(self):
        if self.sprite is None:
            return None
        return self.sprite.frames[self.anim][self.frame-1]

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
