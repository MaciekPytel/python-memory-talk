import functools
import gc
import sys
import weakref


class SampleObject(object):
    '''
    This is just some sample object.

    Each instance has a unique id based on a global counter.

    It uses 'weakref finalizer' pattern discussed in earlier example,
    so that we can see exactly when the object gets deallocated.
    '''
    weakrefs = set()
    counter = 0

    @classmethod
    def delegated_finalize(cls, ref, instance_id):
        print 'Object deleted: {}'.format(instance_id)
        cls.weakrefs.remove(ref)

    def __init__(self):
        self._id = self.counter
        # we want to increase class variable, not create
        # instance variable
        self.__class__.counter += 1
        print 'Object created: {}'.format(self._id)
        cb = functools.partial(self.delegated_finalize, instance_id=self._id)
        self.weakrefs.add(weakref.ref(self, cb))

    def get_id(self):
        return self._id

    def __str__(self):
        return 'SampleObject{}'.format(self._id)

    __repr__ = __str__


def do_stuff():
    '''Loop inner function.'''
    obj = SampleObject()
    if obj.get_id() == 3:
        raise ValueError("I don't like number 3")

def loop():
    '''
    Main loop.

    Note what happens with object with id == 3 (when is it deallocated).
    Now imagine it's a server with infinite main loop running for weeks
    and there is a large number of objects created on stack...
    '''
    for i in xrange(10):
        try:
            do_stuff()
        except ValueError as e:
            print 'Got error: {}'.format(e)
    print 'loop finished\n'

    etype, einst, tb = sys.exc_info()
    # what is this guy doing here ???
    print tb.tb_next.tb_frame.f_locals['obj']
    # you can clear the exception data by calling sys.exc_clear()

if __name__ == '__main__':
    gc.disable()
    loop()
    print 'loop function finished\n'

    # sys.exc_info() is gone once we left the frame
    print sys.exc_info()

    # but there are cycles inside traceback object
    # so stuff won't get cleared before gc kicks in
    print 'before gc'
    gc.collect()
    print 'after gc'

