# -*- coding: utf-8 -*-
import sys

__author__ = 'aevlampiev'

if sys.version_info[0] == 2:
	input_function = raw_input
else:
	input_function = input


# Infinite loop:
while True:
	users_input = input_function('Загадка №1: В каком году заканчивается поддержка Python 2? ')
	if users_input =='2020':
		print('Правильно!')
		break
	else:
		print('Ответ неверный, попробуйте еще раз')
		continue

while True:
	users_input = input_function('Загадка №2: Что используется для выделения блоков в Python? ')
	if users_input =='отступ' or users_input =='отступы' or users_input =='пробел':
		print('Правильно!')
		break
	else:
		print('Ответ неверный, попробуйте еще раз')
		continue

while True:
	users_input = input_function('Загадка №3: Какого числового типа НЕ существует в Python3? ')
	if users_input =='long':
		print('Правильно!')
		break
	else:
		print('Ответ неверный, попробуйте еще раз')
		continue

while True:
	users_input = input_function('Загадка №4: По какому правилу определяются области видимости в Python? ')
	if users_input =='LEGB':
		print('Правильно!')
		break
	else:
		print('Ответ неверный, попробуйте еще раз')
		continue

while True:
	users_input = input_function('Загадка №5: Какому циклу в javascript соответсвует цикл for в Python? ')
	if users_input =='foreach':
		print('Правильно!')
		break
	else:
		print('Ответ неверный, попробуйте еще раз')
		continue

while True:
	users_input = input_function('Загадка №6: Какая команда git используется для сохранения изменений? ')
	if users_input =='git commit' or users_input =='commit' or users_input =='git commit -m':
		print('Правильно!')
		break
	else:
		print('Ответ неверный, попробуйте еще раз')
		continue

while True:
	users_input = input_function('Загадка №7: Какая команда git используется для сравнения между версиями? ')
	if users_input =='git diff' or users_input =='diff' or users_input =='git diff HEAD':
		print('Правильно!')
		break
	else:
		print('Ответ неверный, попробуйте еще раз')
		continue
