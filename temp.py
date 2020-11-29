class Chicken(Object):
    def __init__(self, x=None, y=None):
        super().__init__()
        self.sprite = Sprite('chicken.png', 24, 24, 10, 1)
        self.sprite.add('left', 3, 5)
        self.sprite.add('left_eat', 1, 2)
        self.sprite.add('right', 3, 5, flip=(True, False))
        self.sprite.add('right_eat', 1, 2, flip=(True, False))
        self.sprite.add('down', 10, 5)
        self.sprite.add('down_eat', 8, 2)
        self.sprite.add('up', 17, 5)
        self.sprite.add('up_eat', 15, 2)
        self.x = 100
        self.y = 100
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.width = 60
        self.height = 60
        self.speed = 10
    def update(self, delta):
        self.next(delta)
        x = 0
        y = 0
        eating = False
        if self.key(pygame.K_SPACE):
            eating = True
            if self.anim == 'main':
                self.play('down_eat')
            elif '_eat' not in self.anim:
                self.play(self.anim+'_eat')
        else:
            if self.key(pygame.K_UP):
                self.play('up')
                y = -1
            elif self.key(pygame.K_DOWN):
                self.play('down')
                y = 1
            elif self.key(pygame.K_LEFT):
                self.play('left')
                x = -1
            elif self.key(pygame.K_RIGHT):
                self.play('right')
                x = 1

        if x != 0 or y != 0:
            self.move(x*delta/self.speed, y*delta/self.speed)
        elif not eating:
            self.play('main')
