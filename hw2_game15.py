# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import random  # see https://docs.python.org/2/library/random.html



EMPTY_MARK = 'empty'
DIMENSION = 4

cur_pos = [0,0]

__author__ = 'aevlampiev'

if sys.version_info[0] == 2:
	input_function = raw_input
else:
	input_function = input





def shuffle_field():
    """
    This method is used to create a field at the very start of the game.
    :return: list with 16 randomly shuffled tiles,
    one of which is a empty space.
    """
    x = list(range(1,16))
    x.append(EMPTY_MARK)
    random.shuffle(x)

    field = []
    for row in range(DIMENSION):
        new_row = []
        for i in range(DIMENSION):
            new_row.append(x[row*4+i])
        field.append(new_row)
    return field



def print_field(field):
    """
    This method prints field to user.
    :param field: current field state to be printed.
    :return: None
    """
    for row in range(DIMENSION):
        print('\n|', end=' ')
        for i in range(DIMENSION):
             print(' '+str(field[row][i])+' |', end=' ')
    print('\n')



def is_game_finished(field):
    """
    This method checks if the game is finished.
    :param field: current field state.
    :return: True if the game is finished, False otherwise.
    """
    flag = True
    for row in range(DIMENSION):
        for i in range(DIMENSION):
            if row == DIMENSION-1 and i == DIMENSION-1 and flag:
                break
            if field[row][i] != row*DIMENSION+i+1:
                flag = False

    return flag

def perform_move(field, key):
    """
    Moves empty-tile inside the field.
    :param field: current field state.
    :param key: move direction.
    :return: new field state (after the move).
    :raises: IndexError if the move can't me done.
    """

    if key == 'w':
        if cur_pos[0] == 0:
            raise IndexError
        else:
            tmp = field[cur_pos[0]-1][cur_pos[1]]
            field[cur_pos[0]-1][cur_pos[1]] = EMPTY_MARK
            field[cur_pos[0]][cur_pos[1]] = tmp
            cur_pos[0] -= 1
    elif key == 's':
        if cur_pos[0] == DIMENSION-1:
            raise IndexError
        else:
            tmp = field[cur_pos[0]+1][cur_pos[1]]
            field[cur_pos[0]+1][cur_pos[1]] = EMPTY_MARK
            field[cur_pos[0]][cur_pos[1]] = tmp
            cur_pos[0] += 1
    elif key == 'a':
        if cur_pos[1] == 0:
            raise IndexError
        else:
            tmp = field[cur_pos[0]][cur_pos[1]-1]
            field[cur_pos[0]][cur_pos[1]-1] = EMPTY_MARK
            field[cur_pos[0]][cur_pos[1]] = tmp
            cur_pos[1] -= 1
    elif key == 'd':
        if cur_pos[1] == DIMENSION-1:
            raise IndexError
        else:
            tmp = field[cur_pos[0]][cur_pos[1]+1]
            field[cur_pos[0]][cur_pos[1]+1] = EMPTY_MARK
            field[cur_pos[0]][cur_pos[1]] = tmp
            cur_pos[1] += 1

    return field



def handle_user_input():
    """
    Handles user input. List of accepted moves:
    'w' - up, 's' - down,
    'a' - left, 'd' - right
    :return: <str> current move.
    """
    while True:
        try:
            char = input_function('Move: ')
            if char not in ['w','s','a','d']:
                raise ValueError
        except Exception:
            print('Invalid input')
            continue
        break
    return char


def main():
    """
    The main method.
    :return: None
    """

    step_count = 0
    field = shuffle_field()
    print_field(field)

    #find empty field
    for row in range(DIMENSION):
        for i in range(DIMENSION):
            if field[row][i] == EMPTY_MARK:
                cur_pos[0] = row
                cur_pos[1] = i

    while True:
        cur_input = handle_user_input()
        try:
            field = perform_move(field, cur_input)
            step_count += 1
        except:
            print('Wrong move')
        print_field(field)
        if is_game_finished(field):
            print("You have completed game in "+str(step_count) +" steps.")
            break

    return None



if __name__ == '__main__':
    main()
