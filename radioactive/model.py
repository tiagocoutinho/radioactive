import weakref
import collections


class Dict:

    def __init__(self, *args, **kwargs):
        if args:
            assert len(args) == 1
            data = dict(args[0])
            data.update(kwargs)
        else:
            data = kwargs
        self._data = data
        self._listeners = collections.defaultdict(
            lambda : dict(persistent=set(), weak=weakref.WeakSet()))

    def __listeners(self, key, weak=True):
        return self._listeners[key]['weak' if weak else 'persistent']

    def connect(self, key, listener, weak=True):
        listeners = self.__listeners(key, weak=weak)
        listeners.add(listener)

    def disconnect(self, key, listener, weak=True):
        listeners = self.__listeners(key, weak=weak)
        listeners.remove(listener)

    def emit(self, key, value):
        for weak in (True, False):
            for listener in self.__listeners(key, weak=weak):
                try:
                    listener(self, key, value)
                except Exception as error:
                    print(f'Error in listener: {error!r}')

    def __setitem__(self, key, value):
        self._data[key] = value
        self.emit(key, value)

    def __getitem__(self, key):
        return self._data[key]

    def update(self, other):
        self._data.update(other)
        for key, value in other.items():
            self.emit(key, value)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()


