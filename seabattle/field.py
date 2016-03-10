# -*- coding: utf-8 -*-


class Field(object):
    INITIAL_STATE = '.'
    SHIP_STATE = 'H'

    MISS = '+'
    HIT = 'X'
    FAKE_SHOT = ':'

    def __init__(self, size, is_enemy):
        self.size = size
        self.is_enemy = is_enemy
        self.field = []
        for x in range(size):
            row = []
            for y in range(size):
                row.append(self.__class__.INITIAL_STATE)
            self.field.append(row)

    def add_ship(self, ship):
        for x, y in ship:
            self.field[x][y] = self.__class__.SHIP_STATE

    def draw_field(self):
        letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

#       draw header
        s_buffer = '     '
        for x in range(self.size):
            s_buffer += letters[x]+'_'
        print(s_buffer)

#        draw main

        for y in range(self.size):
            s_buffer = str(y+1)+': |'
            if y+1 < 10:
                s_buffer = '0'+s_buffer
            for x in range(self.size):
                s_buffer += self.field[x][y]+self.field[x][y]
            s_buffer += '| ' + str(y+1)
            print(s_buffer)

    def check_shot(self, x, y, ships):
        if self.field[x][y] in (self.__class__.MISS, self.__class__.HIT):
            print("You've already fired at this square, try again! ")
            return 'DOUBLESHOT'
        elif self.field[x][y] in (self.__class__.INITIAL_STATE, self.__class__.FAKE_SHOT):
            self.field[x][y] = self.__class__.MISS
            print("You've missed, changing active player!")
            return 'MISS'
        else: #state = HIT
            self.field[x][y] = self.__class__.HIT
            for ship in ships:
                r = ship.take_shot(x,y)
                if r != 'MISS':
                    print("This ship is "+r)
                    return r

    def place_result(self, x, y, result, ships):
        if result == 'MISS':
            self.field[x][y] = self.__class__.MISS
        elif result == 'HALFDEAD':
            self.field[x][y] = self.__class__.HIT
        elif result == 'DEAD':
            self.field[x][y] = self.__class__.HIT
            for ship in ships:
                for a, b in ship:
                    if x == a and y == b:
                        self.place_fake_shots(ship)
                        break

    def place_fake_shots(self, ship):
        for x, y in ship:
            for k, m in [(a, b) for a in range(3) for b in range(3)]:
                if x+k-1 < 0 or x+k-1 >= self.size or y+m-1 < 0 or y+m-1 >= self.size:
                    continue
                if self.field[x+k-1][y+m-1] == self.__class__.INITIAL_STATE:
                    self.field[x+k-1][y+m-1] = self.__class__.FAKE_SHOT




