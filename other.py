import ppb
from ppb.features.default_sprites import TargetSprite


class Player(TargetSprite):
    target = ppb.Vector(0, 40)


def setup(scene):
    scene.add(Player(pos=(0, -7)))


ppb.run(setup=setup)