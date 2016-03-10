# -*- coding: utf-8 -*-
from utils import *
from ship import Ship
from field import Field
import random

SHIPS_SET = ((4, 1), (3, 2), (2, 3), (1, 4))


class Player(object):
    def __init__(self, name, size):
        self.name = name
        self.ships = []
        self.field_size = size
        self.my_field = Field(size, is_enemy=False)
        self.enemy_field = Field(size, is_enemy=True)
        self.verbose = True

    def __str__(self):
        return self.name

    def print_for_player(self, message):
        if self.verbose:
            print(message)

    def place_ships(self):
        self.print_for_player("Now it's time for "+self.name+' to place ships!')
        for length, count in SHIPS_SET:
            for _ in range(count):
                while True:
                    try:
                        ship = self.__class__.ship_input(length, self.field_size)
                        if not ship.valid_ship_position(self.field_size):
                            self.print_for_player('Ship is out of field.')
                            continue
                        for other_ship in self.ships:
                            if other_ship.intersects(ship):
                                raise IndexError
                        self.ships.append(ship)
                        self.print_for_player('Ship is added!')
                        self.my_field.add_ship(ship)
                        if self.verbose:
                            self.my_field.draw_field()
                    except ValueError:
                        self.print_for_player('Bad input.')
                        continue
                    except IndexError:
                        self.print_for_player('Ship is intersecting with other ship')
                        continue
                    else:
                        break

    @staticmethod
    def ship_input(length, field_size):
        print('Place ship with length '+str(length))
        orientation = '-'
        if length != 1:
            orientation = get_input('Enter orientation, | or - :')
            if orientation not in ['|', '-']:
                raise ValueError()
        cords = get_input('Enter coordinates of upper-left corner of ship (F7 for example):')
        x = letter_to_int(cords[0])
        y = int(cords[1:])-1
        if (x not in range(0, field_size)) or (y not in range(0, field_size)):
            raise ValueError()
        ship = Ship(x, y, length, orientation)
        return ship

    def draw_fields(self):
        print('Your field:')
        self.my_field.draw_field()
        print('Your shots:')
        self.enemy_field.draw_field()

    def make_move(self):
        while True:
            try:
                cords = get_input(self.name+', take a shot! Enter shot coordinates (A1 for example):')
                x = letter_to_int(cords[0])
                y = int(cords[1:])-1
                if (x not in range(0, self.field_size)) or (y not in range(0, self.field_size)):
                    raise ValueError()
            except ValueError:
                print('Bad input.')
                continue
            else:
                break

        return x, y


class AIPlayer(Player):
    def __init__(self, name, size):
        super(AIPlayer, self).__init__(name, size)
        self.verbose = False

    @staticmethod
    def ship_input(length, field_size):
        orient_vals = ['-', '|', '-', '|']
        random.shuffle(orient_vals)
        orientation = orient_vals[0]
        x = int(random.uniform(0, field_size))
        y = int(random.uniform(0, field_size))
        ship = Ship(x, y, length, orientation)
        return ship

    def make_move(self):
        print(self.name+', take a shot!')
        while True:
            x = int(random.uniform(0, self.field_size))
            y = int(random.uniform(0, self.field_size))
            if self.enemy_field.field[x][y] == Field.INITIAL_STATE:
                break
        print('Shot is ( '+str(x+1)+', '+str(y+1)+' )')
        return x, y
