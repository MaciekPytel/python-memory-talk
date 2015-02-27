alive = {}


class Cat(object):
    ''' Every cat has nine lives, right?'''
    def __init__(self):
        self._lives = 9
        alive['cat'] = self

    def __del__(self):
        if self._lives > 0:
            self._lives -= 1
            alive['cat'] = self


if __name__ == '__main__':
    Cat()
    i = 0
    while 'cat' in alive:
        del alive['cat']
        i += 1
    print 'Cat has {} lives'.format(i-1)
