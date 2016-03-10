# -*- coding: utf-8 -*-

from players import Player, AIPlayer
from utils import *


class Controller(object):

    def __init__(self, size=10):
        self.players = []

#       create 2 players
        player_name = get_input('Enter first player name, type AI1 for Computer player: ')
        if player_name == 'AI1':
            first_player = AIPlayer(player_name, size)
        else:
            first_player = Player(player_name, size)
        self.players.append(first_player)

        player_name = get_input('Enter second player name, type AI2 for Computer player: ')
        if player_name == 'AI2':
            second_player = AIPlayer(player_name, size)
        else:
            second_player = Player(player_name, size)
        self.players.append(second_player)

#        for each player place ships
        for player in self.players:
            player.place_ships()

    def start_game(self):
        shooter, waiter = self.players

        print('Game is starting!')
        while not self.is_game_finished(waiter):
            shooter.draw_fields()
            x, y = shooter.make_move()
            result = waiter.my_field.check_shot(x, y, waiter.ships)
            shooter.enemy_field.place_result(x, y, result, waiter.ships)
            if result == 'MISS':
                waiter, shooter = shooter, waiter

        shooter.draw_fields()
        print('Game is finished, player '+shooter.name+' wins!')


    def is_game_finished(self, player):
        for ship in player.ships:
            if ship.damage != ship.length:
                return False
        return True


def main():
    controller = Controller(size=10)
    controller.start_game()


if __name__ == '__main__':
    main()
