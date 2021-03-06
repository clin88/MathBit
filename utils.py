from collections import Iterator, Iterable, OrderedDict, Callable
from itertools import chain
from functools import wraps


class GenHelper(Iterator):
    """Adds utility functions for working with generators.

    Can be decorated onto generator functions with @genhelper.
    """

    def __init__(self, genf, args, kwargs):
        self._gen = genf(*args, **kwargs)

    def __next__(self):
        return next(self._gen)

    def __iter__(self):
        return self

    def eval(self):
        """Consume entire generator and get return value.
        """
        while True:
            try:
                next(self._gen)
            except StopIteration as e:
                return e.value


def genhelper(f):
    @wraps(f)
    def __(*args, **kwargs):
        return GenHelper(f, args, kwargs)

    return __


class OrderedDefaultDict(OrderedDict):
    """Hybrid of OrderedDict and defaultdict.

    From this StackOverflow question:
    http://stackoverflow.com/questions/6190331/can-i-do-an-ordered-default-dict-in-python
    """

    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
                not isinstance(default_factory, Callable)):
            raise TypeError('first argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy

        return type(self)(self.default_factory,
                          copy.deepcopy(self.items()))

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_factory,
                                               OrderedDict.__repr__(self))


def cat(*iters, flatten=Iterable):
    """Concatenates iters. Flattens iters if instance of type.

    Note: Also has the ability to concatenate non-iterable items.
    """
    unpackif = lambda iter: iter if isinstance(iter, flatten) else (iter,)
    unpacked = map(unpackif, iters)
    return tuple(chain(*unpacked))


def flatten(node):
    """Flattens nested nodes of same type.
    """
    cls = type(node)
    unpackif = lambda child: child if isinstance(child, cls) else (child,)
    unpacked = map(unpackif, node)
    return cls(*chain(*unpacked))


def identityiter(arg):
    if False:
        yield
    return arg

def identity(arg):
    return arg

def istypef(type):
    return lambda arg: isinstance(arg, type)