
def decorator(function):
    def _inner(value):
        print(value)

    print('called')
    return _inner

decorated = decorator(len)
print(decorated([1,2,3]))