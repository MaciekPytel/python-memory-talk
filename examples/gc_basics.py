import gc
import weakref

from lib import SampleObject


def simple_reference_cycle():
    '''
    Illustrate how python garbage collector can break a reference cycle.

    In python an object is deallocated immediately when its reference count
    drops to 0, but that will never happen if we have a reference cycle...
    There is a separate garbage collector to break those cycles.
    We can mess with it using gc module.
    '''
    # normally gc triggers automatically every once in a while
    # we can disable it so we have a deterministic behaviour in our example
    gc.disable()

    obj1 = SampleObject(None)
    obj2 = SampleObject(obj1)
    obj1.stuff = obj2
    ref = weakref.ref(obj1)
    print 'After object creation: {}'.format(ref())

    obj1 = None
    obj2 = None
    # object still exists due to reference cycle
    print 'Removed external references: {}'.format(ref())

    gc.collect()  # force garbage collection
    # gc broke the cycle and objects have been deallocated
    print 'After garbage collection: {}'.format(ref())

    gc.enable()  # reenable normal gc


def gc_generations():
    '''
    Illustrate how python uses generational model in gc.

    A generational gc is a common gc optimisation, based on assumption that
    most objects' lifetime is either very long or very short.
    When an object is first created it is a generation 0 object.
    If it leaves through a garbage collection it's promoted to the generation
    of that collection + 1 (up to generation 2).

    A generation 0 garbage collection only looks at generation 0 objects,
    a generation 1 gc looks at gen0 and gen1 objects and
    a generation 2 gc looks at everything.
    '''
    gc.disable()
    gc.collect()  # clean any hanging stuff so we have a cleaner picture

    obj1 = SampleObject(None)
    obj2 = SampleObject(obj1)
    obj1.stuff = obj2
    ref = weakref.ref(obj1)
    print 'After object creation: {}'.format(ref())

    # gc.collect takes generation as optional parameter;
    # by default a manual gc is gen2 - so if we just called
    # gc.collect() (or gc.collect(1) or gc.collect(2))
    # our objects would immediately get promoted to gen2;
    # now they'll get promoted to gen1
    gc.collect(0)

    obj1 = None
    obj2 = None
    # reference cycle keeps objects alive (as expected)
    print 'External references removed: {}'.format(ref())

    # there is no reference to our objects, but they are gen1 now, so
    # a gen0 gc won't even look at them
    gc.collect(0)
    print 'After gen0 gc: {}'.format(ref())

    # but a gen1 collection can (and will) deallocate them
    gc.collect(1)
    print 'After gen1 gc: {}'.format(ref())


if __name__ == '__main__':
    print '***** simple reference cycle *****'
    print
    simple_reference_cycle()
    print
    print '***** gc generations *****'
    print
    gc_generations()
    print
