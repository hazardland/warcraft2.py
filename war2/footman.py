import pygame
import game

BLUE = ((208, 212), (209, 213), (210, 214), (211, 215))

class Sprite(game.Sprite):
    def __init__(self, scene, replace):
        super().__init__('./assets/sprites/grunt.png',
                         width=72,
                         height=72,
                         vertical=True,
                         replace=replace,
                         pause=60)

        self.add('walk_up', frame=(1, 2), count=4)
        self.add('walk_down', frame=(5, 2), count=4)
        self.add('walk_right', frame=(3, 2), count=4)
        self.add('walk_left', frame=(3, 2), count=4, flip=(True, False))
        self.add('walk_rightup', frame=(2, 2), count=4)
        self.add('walk_rightdown', frame=(4, 2), count=4)
        self.add('walk_leftup', frame=(2, 2), count=4, flip=(True, False))
        self.add('walk_leftdown', frame=(4, 2), count=4, flip=(True, False))

        self.add('stand_up', frame=(1, 1), count=1)
        self.add('stand_down', frame=(5, 1), count=1)
        self.add('stand_right', frame=(3, 1), count=1)
        self.add('stand_left', frame=(3, 1), count=1, flip=(True, False))
        self.add('stand_rightup', frame=(2, 1), count=1)
        self.add('stand_rightdown', frame=(4, 1), count=1)
        self.add('stand_leftup', frame=(2, 1), count=1, flip=(True, False))
        self.add('stand_leftdown', frame=(4, 1), count=1, flip=(True, False))

        self.add('attack_up', frame=(1, 6), count=4)
        self.add('attack_down', frame=(5, 6), count=4)
        self.add('attack_right', frame=(3, 6), count=4)
        self.add('attack_left', frame=(3, 6), count=4, flip=(True, False))
        self.add('attack_rightup', frame=(2, 6), count=4)
        self.add('attack_rightdown', frame=(4, 6), count=4)
        self.add('attack_leftup', frame=(2, 6), count=4, flip=(True, False))
        self.add('attack_leftdown', frame=(4, 6), count=4, flip=(True, False))

        scene.sprites['footman'] = self

class Footman(game.Unit):
    def __init__(self, scene):
        super().__init__(scene)

        self.sprite = self.scene.sprites['footman']

        self.anim = 'stand_down'

        self.x = 0
        self.y = 0
        self.width = 72
        self.height = 72

        self.vertical = 'down'
        self.horizontal = ''
        self.speed = 5

        self.mode = 'stand'

    def update(self, delta):
        self.next(delta)

        x = 0
        y = 0

        if self.key(pygame.K_UP):
            y = -1
            self.vertical = 'up'
        elif self.key(pygame.K_DOWN):
            y = 1
            self.vertical = 'down'
        elif self.key(pygame.K_RIGHT) or self.key(pygame.K_LEFT):
            self.vertical = ''

        if self.key(pygame.K_LEFT):
            x = -1
            self.horizontal = 'left'

        elif self.key(pygame.K_RIGHT):
            x = 1
            self.horizontal = 'right'
        elif self.key(pygame.K_UP) or self.key(pygame.K_DOWN):
            self.horizontal = ''

        if self.vertical == '' and self.horizontal == '':
            self.vertical = 'down'

        if self.key(pygame.K_SPACE):
            self.mode = 'attack'
        elif x != 0 or y != 0:
            self.mode = 'walk'
        else:
            self.mode = 'stand'

        if self.mode == 'walk':
            self.play('walk_'+self.horizontal+self.vertical)
            self.move(x*delta/self.speed, y*delta/self.speed)
        elif self.mode == 'attack':
            self.play('attack_'+self.horizontal+self.vertical)
        else:
            self.play('stand_'+self.horizontal+self.vertical)
