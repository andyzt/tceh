# -*- coding: utf-8 -*-


def get_input(message):
    try:
        input_function = raw_input
    except NameError:
        input_function = input

    return input_function(message)


def letter_to_int(letter):
    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return letters.index(letter)
