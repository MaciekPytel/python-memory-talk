import sys
import weakref

from lib import SampleObject


def basic_weakref():
    '''
    Create a weak reference and observe when an object is deleted.

    In python it happens immediately after last
    reference is dropped (weakrefs don't count)
    '''
    obj = SampleObject('example')
    ref = weakref.ref(obj)
    print ref()
    obj = None
    print ref()  # after the object is deleted weakref returns None


def weakref_to_base_types():
    '''
    Create weakrefs to various builtin types.

    Oops, some of them can't be weak referenced!
    '''
    dict_inst = {'a': 1}
    try:
        ref = weakref.ref(dict_inst)
        print 'created reference to dict: {}'.format(ref())
    except TypeError:
        print 'failed to create weakref to dict'

    str_inst = 'some string'
    try:
        ref = weakref.ref(str_inst)
        print 'created reference to str: {}'.format(ref())
    except TypeError:
        print 'failed to create weakref to str'

    set_inst = set((1, 2, 3))
    try:
        ref = weakref.ref(set_inst)
        print 'created reference to set: {}'.format(ref())
    except TypeError:
        print 'failed to create weakref to set'

    # in some cases (dict) you can create a weakref to subclass
    # in some other (str, tuple) you can't
    DictType = type('DictType', (dict, ), {})  # simple class derived from dict
    dict_inst = DictType(a=1)
    try:
        ref = weakref.ref(dict_inst)
        print 'created reference to dict subclass: {}'.format(ref())
    except TypeError:
        print 'failed to create weakref to dict subclass'

    StrType = type('StrType', (str, ), {})
    str_inst = StrType('string subclass')
    try:
        ref = weakref.ref(str_inst)
        print 'created reference to str subclass: {}'.format(ref())
    except TypeError:
        print 'failed to create weakref to str subclass'

    # in general you can weakref most class instances and python functions
    # but you can't weakref many builtins
    # like dict, tuple, string (but you can weakref set...).
    # In some cases simple subclassing solves the issue, in some it doesn't...
    # All this is because of C implementation details.

    # In case you're interested in more detailed explanaition:
    # there is a cost to allowing weakrefs (you need to store extra data
    # in class header) and python devs decided against it for types used a lot
    # internally.
    # Subclassing helps for classes not stored as a single, continous chunk
    # of memory (like dicts) - in this case the necessary field will be added
    # to header when subclassing.
    # However, if a header and body is in a single continous memory segment
    # (like string) no new fields will be added to header when subclassing.


def weakref_callbacks():
    '''
    Weakrefs can register a callback that will be called after the
    referenced object gets deallocated.

    The callback gets the weakref that registered it as a single parameter.
    However, the weakref is already 'dead' - so we can't access the object
    we're referencing in callback.
    '''

    # simple callback printing a predefined message
    def print_cb(msg):
        def cb(ref):
            print msg
        return cb

    # all callbacks will be called once an object is deallocated
    # in reverse order of when they were registered
    obj = SampleObject('example')
    ref1 = weakref.ref(obj, print_cb('obj freed'))
    ref2 = weakref.ref(obj, print_cb('obj freed - 2nd callback'))
    obj = None

    # the only parameter to callback is the reference itself
    # but the callback is called after the object is deallocated,
    # so it will point to None
    obj2 = SampleObject('example2')
    ref3 = weakref.ref(obj2,
                       lambda x: sys.stdout.write(str(x()) + '\n'))
    obj2 = None

    # callback won't be called if weakref itself was deallocated first
    obj3 = SampleObject('example3')
    ref4 = weakref.ref(obj3, print_cb('obj3 freed'))
    ref4 = None
    obj3 = None


if __name__ == '__main__':
    print '***** basic_weakfef - simple weakref test *****'
    print
    basic_weakref()
    print
    print '***** weakrefs to different types *****'
    print
    weakref_to_base_types()
    print
    print '***** weakrefs callbacks *****'
    weakref_callbacks()
