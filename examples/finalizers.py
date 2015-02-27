import functools
import gc
import sys
import weakref

from lib import SampleObject

# NOTE: everything in this file is meant to illustrate how
# finalizers work in python; in real life every case here
# should be solved with a context manager ('with')


# this class sounds 'a bit' made up for the example
# the idea is just to have a class holding a resource
# that can be a part of reference cycle
# NOTE: more often than not such a thing is a sign of bad design
# and you should just decompose the class
class CustomFileWrapper(object):
    '''
    Abstract class.

    Takes a file object and makes sure '---' gets written at the end
    of the file (just before calling close).
    Also takes another object and provides dump() method to write
    it's string representation to a file.
    '''
    def __init__(self, file_object, obj):
        self._f = file_object
        self._obj = obj

    def write(self, stuff):
        self._f.write(stuff)

    def dump(self):
        self._f.write(str(self._obj) + '\n')

    def close(self):
        self._f.write('---\n')
        self._f.close()


class CustomFileWrapperWithDel(CustomFileWrapper):
    ''' Uses __del__ to fulfill CustomFileWrapper contract. '''
    def __del__(self):
        self.close()


class CustomFileWrapperWithoutDel(object):
    '''
    Uses weakref callback instead of __del__ to fulfill CustomFileWrapper
    contract.

    This is safe to use with reference cycles, just beware - if you have
    multiple classes using this technique in the same cycle the order of
    calls is undefined! Also the weakref callback happens after the
    weakref is invalidated - meaning we have to preserve the resources
    we won't to close properly - in this case we keep file inside
    functools.partial.

    This is meant as an illustration / proof of concept.
    Don't (over)use that or similar patterns - really, it's a hack.
    Just use 'with' where you can.
    '''
    _weakrefs = set()

    @classmethod
    def _delegated_close(cls, file_object, w):
        file_object.write('---\n')
        file_object.close()
        cls._weakrefs.remove(w)

    def __init__(self, file_object, obj):
        self._f = file_object
        self._obj = obj
        self._weakrefs.add(weakref.ref(self,
                                       functools.partial(self._delegated_close,
                                                         self._f)))


def del_without_ref_cycles():
    ''' Use an object with a finalizer to close a resource. '''
    # __del__ method will be called when object is dereferenced
    o = SampleObject('test')
    c = CustomFileWrapperWithDel(sys.stdout, o)
    c = None


def del_with_ref_cycle():
    '''
    Create a reference cycle containing objects with finalizers.

    If at least a single object in reference cycle has __del__
    method defined gc will not break the cycle - effectively
    creating a memory leak.
    '''
    gc.disable()

    o = SampleObject('test')
    c = CustomFileWrapperWithDel(sys.stdout, o)
    o.stuff = c
    w = weakref.ref(o)

    o = None
    c = None

    # nothing was freed - as expected in case of cycle
    print 'Removed external references: {}'.format(w())

    gc.collect()
    # still nothing got collected - __del__ method of CustomFileWrapperWithDel
    # prevented breaking the cycle
    print 'After garbage collection: {}'.format(w())

    # a garbage collector will place any objects stopping a cycle from
    # being broken by defining __del__ method on garbage list - this is
    # extremly useful for debugging!
    # NOTE: entry in gc.garbage is a reference to the object - if you
    # want to deallocate an object you need to break reference cycle manually
    # AND delete it from this list!!!
    print 'garbage: ', gc.garbage


def finalize_without_del():
    '''
    Use weakref callbacks instead of __del__ for finalization.

    This is a hack, don't use it unless you're positive it's the
    right thing to do.
    '''
    gc.disable()

    o = SampleObject('test')
    c = CustomFileWrapperWithoutDel(sys.stdout, o)
    o.stuff = c
    w = weakref.ref(c)

    o = None
    c = None

    # still there
    print 'Removed external references: {}'.format(w())

    # deallocated now :)
    print 'Will run gc:'
    gc.collect()


if __name__ == '__main__':
    # NOTE in those examples we close sys.stdout,
    # so don't try to call more than one function -
    # it will just give you an IO related ValueError
    del_without_ref_cycles()
    # del_with_ref_cycle()
    # finalize_without_del()
