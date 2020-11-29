from game import Scene
from war2.footman import Footman

scene = Scene(800, 600, caption='Warcraft 2 Python', icon='./icon.png')

scene.add(Footman())
scene.run()
