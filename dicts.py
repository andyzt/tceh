# -*- coding: utf-8 -*-


import collections

this_is_dict = {'key': 'value'}
this_is_also_dict = dict([('key', 'value',),])

print(this_is_dict == this_is_also_dict)

print('dict() is iterable:',
      isinstance(this_is_dict,collections.Iterable))

#  dicts are mutable!

var = {1:'value'}
new_var = var
var.update({2:'new value'})
var[1] = 'mutated value'
print(new_var)

#  operations with dicts:
# add
this_is_dict.update({'name': 'Super Mario'})

print('Name is "{}"'.format(this_is_dict['name']))

print('Name is "{}"'.format(this_is_dict.get('name', 'Default Name')))

#get only keys
print(this_is_dict.keys())

print(this_is_dict.values())

#remove
test_dict = {'pop-by-key':1, 'pop-by-item':2, 'to-del':3}

del test_dict['to-del']
print(test_dict)

popped = test_dict.pop('pop-by-key')
print(popped)

popped = test_dict.pop('non-exists', 'default-value')
print(popped)

missing = test_dict.popitem()
print(missing)