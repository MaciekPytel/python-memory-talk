## Examples showing various memory behaviours in python.

Suggested reading order:

1. **weakrefs.py** - show you what weakrefs are (they're used in other examples)
2. **gc_basics.py** - basics examples of python garbage collector at work
3. **finalizers.py** - shows how you can use finalizers (\_\_del\_\_ method) to free resources associated with object; also shows how doing so breaks garbage collector (as a rule of thumb: _don't_ use \_\_del\_\_ method)
4. **cat.py** - show how you can use finaliser to resurrect an object
