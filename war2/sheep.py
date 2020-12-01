from random import randrange
import pygame
import game

class Sprite(game.Sprite):
    def __init__(self, scene):
        super().__init__('./assets/sprites/critter.png',
                         width=32,
                         height=32)

        self.add('stand_up', frame=(1, 1))
        self.add('stand_down', frame=(5, 1))
        self.add('stand_right', frame=(3, 1))
        self.add('stand_left', frame=(3, 1), flip=(True, False))
        self.add('stand_rightup', frame=(2, 1))
        self.add('stand_rightdown', frame=(4, 1))
        self.add('stand_leftup', frame=(2, 1), flip=(True, False))
        self.add('stand_leftdown', frame=(4, 1), flip=(True, False))

        scene.sprites['sheep'] = self

class Sheep(game.Unit):
    def __init__(self, scene):
        super().__init__(scene)

        self.sprite = self.scene.sprites['sheep']

        self.anim = 'stand_leftdown'

        self.x = 200
        self.y = 200
        self.width = 32
        self.height = 32

        self.x = randrange(0, self.scene.width-self.width)
        self.y = randrange(0, self.scene.height-self.height)

        self.vertical = 'down'
        self.horizontal = ''
        self.speed = 5

        self.actions = []
        self.act()

    def act(self):
        self.actions.append(game.Action(
            self,
            {
                'x': randrange(0, self.scene.width-self.width),
                'y': randrange(0, self.scene.height-self.height)
            },
            speed=10,
            #time=10000,
            pause=2000
            ))


    def update(self, delta):
        x = self.x
        y = self.y

        for action in self.actions:
            if not action.update(delta):
                self.actions.remove(action)
                #print('action end')
                self.act()

        self.next(delta)


        x = self.x - x
        y = self.y - y

        #print(x, y)

        if y < 0:
            self.vertical = 'up'
        elif y > 0:
            self.vertical = 'down'
        elif x != 0:
            self.vertical = ''

        if x < 0:
            self.horizontal = 'left'
        elif x > 0:
            self.horizontal = 'right'
        elif y != 0:
            self.horizontal = ''

        # if self.vertical == '' and self.horizontal == '':
        #     self.vertical = 'down'

        if x != 0 or y != 0:
            self.play('stand_'+self.horizontal+self.vertical)
        # # self.move(x*delta/self.speed, y*delta/self.speed)
