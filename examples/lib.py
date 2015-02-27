class SampleObject(object):
    '''
    A sample object used in variouse examples.

    Holds a single reference that can be used to create cycles
    and can print itself.
    '''
    def __init__(self, stuff):
        self.stuff = stuff

    def __str__(self):
        if isinstance(self.stuff, SampleObject):
            # avoid infinite recursion if cycle
            return 'SampleObj(SampleObj)'
        return 'SampleObj({})'.format(repr(self.stuff))

    __repr__ = __str__
