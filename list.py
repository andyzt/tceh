# -*- coding: utf-8 -*-

import sys
import collections

#lists
not_a_list = (1,2,)
list1 = [1,2]
list2 = list(not_a_list)  # show __builtin__
# get the tuple back by: 'new_tuple = tuple(list2)

print(list1 == list2, not_a_list == list1)
print('list() is iterable: ', isinstance(list1, collections.Iterable))

# list operations:

# add:
# Note the difference between .append and += for tuples

list1.append(3)
print('append() returns None: ', list1.append(4))
print(list1)

list1.append(list2)
print(list1)

list1.extend(list2)
print(list1)

list1.insert(1, 'inserted value')
