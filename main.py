from game import Scene
import war2.footman as footman
import war2.sheep as sheep
import war2.map as map
scene = Scene(1024, 768, caption='Warcraft 2 Python', icon='./icon.png')


map.Map(scene)

sheep.Sprite(scene)
for _ in range(30):
    sheep.Sheep(scene)

footman.Sprite(scene, footman.BLUE)
footman.Footman(scene)

scene.run()
