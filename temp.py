class Sprite:
    def __init__(self):
        self.cells = 3
        self.rows = 5
        self.vertical = True
    def frame(self, frame):
        if self.vertical:
            cell = ((frame-1)//self.rows)+1
            row = frame-(cell-1)*self.rows
        else:
            row = ((frame-1)//self.cells)+1
            cell = frame-(row-1)*self.cells
        print(frame, '-->', (cell, row))

s = Sprite()
print(1)
s.frame(1)
s.frame(2)
s.frame(3)
print(2)
s.frame(4)
s.frame(5)
s.frame(6)
print(3)
s.frame(7)
s.frame(8)
s.frame(9)
print(4)
s.frame(10)
