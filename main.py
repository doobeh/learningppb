import ppb
from ppb import keycodes
from ppb.events import KeyPressed, KeyReleased
from ppb import Image, Scene


class Tile(ppb.Sprite):
    layer = 0
    def on_update(self, update_event, signal):
        for p in update_event.scene.get(kind=Player):
            if (p.position - self.position).length <= self.size:
                self.image = Image('ceramic_tile.png')


class Player(ppb.Sprite):
    layer = 1
    image = Image('player.png')
    height = 1
    width = 1
    position = ppb.Vector(0, 0)
    direction = ppb.Vector(0, 0)
    speed = 4
    left = keycodes.Left
    right = keycodes.Right
    up = keycodes.Up
    down = keycodes.Down

    def on_update(self, update_event, signal):
        self.position += self.direction * self.speed * update_event.time_delta
        #print(self.position)

    def on_key_pressed(self, key_event: KeyPressed, signal):
        if key_event.key == self.left:
            self.direction += ppb.Vector(-1, 0)
        elif key_event.key == self.right:
            self.direction += ppb.Vector(1, 0)
        if key_event.key == self.up:
            self.direction += ppb.Vector(0, 1)
        elif key_event.key == self.down:
            self.direction += ppb.Vector(0, -1)

    def on_key_released(self, key_event: KeyReleased, signal):
        if key_event.key == self.left:
            self.direction += ppb.Vector(1, 0)
        elif key_event.key == self.right:
            self.direction += ppb.Vector(-1, 0)
        if key_event.key == self.up:
            self.direction += ppb.Vector(0, -1)
        elif key_event.key == self.down:
            self.direction += ppb.Vector(0, 1)


def setup(scene):
    print(scene)
    scene.add(Player())
    # Build a lil' map with tile options, and a matrix to reference the tiles:
    tiles = [
        'flat_tile.png',  # 0
        'small_tile.png',  # 1
        'ceramic_tile.png',  # 2
        'flat_tile_tr.png',  # 3
        'flat_tile_t.png',  # 4
        'flat_tile_tl.png',  # 5
    ]
    matrix = [
        [3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 1, 1, 1, 1, 0, 0, 2, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],

    ]
    matrix.reverse()
    # Create sprites for tiles:
    y = 0
    center_y = len(matrix) / 2.0
    for row in matrix:
        center_x = len(row) / 2.0
        y += 1
        x = 0
        for column in row:
            x += 1
            scene.add(
                Tile(
                    position=(x-center_x, y-center_y),
                    image=Image(tiles[column])
                )
            )

ppb.run(
    setup=setup,
    resolution=(1024, 768)
)
