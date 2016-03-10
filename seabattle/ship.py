# -*- coding: utf-8 -*-


class Ship(object):
    def __init__(self, x, y, length, orient):
        self.x = x
        self.y = y
        self.length = length
        self.orientation = orient
        self.damage = 0

    def valid_ship_position(self, field_size):
            for cords in self:
                if any(cord >= field_size for cord in cords):
                    return False
            return True

    def __iter__(self):
        if self.orientation == '-':
            vector = ((self.x + d, self.y) for d in range(self.length))
        else:
            vector = ((self.x, self.y + d) for d in range(self.length))

        return vector

    def intersects(self, other):
        for x, y in self:
            for x1, y1 in other:
                d_x = abs(x - x1)
                d_y = abs(y - y1)
                if d_x <= 1 and d_y <= 1:
                    return True
        return False

    def take_shot(self, x, y):
        for x1, y1 in self:
            if x == x1 and y == y1:
                self.damage += 1
                if self.damage == self.length:
                    return 'DEAD'
                else:
                    return 'HALFDEAD'

        return 'MISS'
