import copy

import ppb
from ppb import keycodes
from ppb.events import KeyPressed, KeyReleased
from ppb.events import ButtonReleased
from ppb import Image, Scene
from shapely.geometry import Point, Polygon, LinearRing, LineString, JOIN_STYLE
from shapely.ops import nearest_points
import numpy as np


class Tile(ppb.Sprite):
    layer = 0
    movement_speed = 4

    @classmethod
    def pos(cls, tile, position):
        new_tile = Tile()
        new_tile.position = position
        new_tile.image = tile.image
        return new_tile


class Wall(ppb.Sprite):
    layer = 0
    height = 1
    width = 1

    @property
    def extents(self):
        # self.position # Centre of geometry.
        return [
            (self.position.x - self.width/2, self.position.y + self.height/2),
            (self.position.x + self.width/2, self.position.y + self.height/2),
            (self.position.x + self.width/2, self.position.y - self.height/2),
            (self.position.x - self.width/2, self.position.y - self.height/2),
            (self.position.x - self.width/2, self.position.y + self.height/2),
        ]

    def extend(self, p1, p2, distance=1.4):
        v = [p2.x - p1.x, p2.y - p1.y]
        px = (p1.x + v[0] * distance, p1.y + v[1] * distance)
        return px


    def collision(self, point):
        print(f"Extents of tile player collided with: {self.extents}")
        poly = LinearRing(self.extents).parallel_offset(distance=-0.1, join_style=JOIN_STYLE.mitre)

        #this is where the player currently is:
        point = Point(point.x, point.y)
        print(f"Player at {point}")

        p1, p2 = nearest_points(poly, point)
        print(f"Closest frame hit-point: P1x: {p1.x}, P1y: {p1.y}")
        #p1 is the closest vector on the tile that the player collided with.
        # now we know where the player is, and the part of wall
        # the collided with-- lets draw a line between those two points, extend them
        # and 'push' the user back.

        print(f"Extending to {self.extend(p1, point)}")
        return ppb.Vector(self.extend(p1, point))

    @classmethod
    def pos(cls, tile, position):
        new_tile = Wall()
        new_tile.position = position
        new_tile.image = tile.image
        return new_tile

    def on_update(self, update_event, signal):
        for p in update_event.scene.get(kind=Player):
            if (p.position - self.position).length <= self.size:
                print('Collision!')

                print(p.position, self.position)
                # self.image = Image('ceramic_tile.png')
                print(p.position)
                p.position = self.collision(p.position)
                print(f"{self.collision(point=p.position)} (MOVED)")


class Player(ppb.Sprite):
    layer = 1
    image = Image('player.png')
    height = 1
    width = 1
    position = ppb.Vector(0, 0)
    direction = ppb.Vector(0, 0)
    max_speed = 4
    speed = 4
    left = keycodes.Left
    right = keycodes.Right
    up = keycodes.Up
    down = keycodes.Down
    space = keycodes.Space

    def on_update(self, update_event, signal):
        if self.speed == self.max_speed:
            self.position += self.direction * self.speed * update_event.time_delta
        else:
            self.position -= self.direction * self.max_speed * update_event.time_delta
            self.speed = self.max_speed

        # print(self.position)

    def on_button_released(self, key_event: ButtonReleased, signal):
        if key_event.button:
            print(key_event.position)

    def on_key_pressed(self, key_event: KeyPressed, signal):
        if key_event.key == self.left:
            self.direction += ppb.Vector(-1, 0)
        elif key_event.key == self.right:
            self.direction += ppb.Vector(1, 0)
        if key_event.key == self.up:
            self.direction += ppb.Vector(0, 1)
        elif key_event.key == self.down:
            self.direction += ppb.Vector(0, -1)
        if key_event.key == self.space:
            print(self.position)

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
        Tile(image=Image('flat_tile.png')),  # 0
        Tile(image=Image('cracked_tile.png')),  # 1
        Tile(image=Image('ceramic_tile.png')),  # 2
        Wall(image=Image('flat_tile_tr.png')),  # 3
        Wall(image=Image('flat_tile_t.png')),  # 4
        Wall(image=Image('flat_tile_tl.png')),  # 5
        Wall(image=Image('flat_tile_br.png')), # 6
        Wall(image=Image('flat_tile_b.png')), # 7
        Wall(image=Image('flat_tile_bl.png')), # 8
        Wall(image=Image('flat_tile_l.png')), # 9
        Wall(image=Image('flat_tile_r.png')), #10
        Wall(image=Image('ceramic_tile.png')), #11
    ]

    matrix = [
        [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3],
        [9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10],
        [9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10],
        [9, 1, 1, 11, 11, 1, 1, 1, 1, 1, 10],
        [9, 1, 1, 11, 11, 1, 1, 1, 1, 1, 10],
        [9, 1, 1, 11, 11, 1, 1, 1, 1, 1, 10],
        [9, 1, 1, 11, 11, 1, 1, 1, 1, 1, 10],
        [9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10],
        [9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10],
        [9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10],
        [8, 7, 7, 7, 7, 7, 7, 7, 7, 7,  6],
    ]

    # Create sprites for tiles:
    y = 0
    center_y = len(matrix) / 2.0

    for row in matrix:
        center_x = len(row) / 2.0
        x = 0
        for column in row:
            tile = tiles[column] # get an instance of Tile or Wall
            target_vector = ppb.Vector(x - center_x, y + center_y)
            new_tile = tile.pos(tile=tile, position=target_vector) # set position
            scene.add(new_tile) # place it!
            print(f"Placing {new_tile.image.name} at {target_vector}")
            x += 1
        y -= 1

ppb.run(
    setup=setup,
    resolution=(1024, 768)
)
