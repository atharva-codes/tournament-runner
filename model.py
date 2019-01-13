

class ModelError(Exception):
    pass


def _readable(value):
    try:
        value = int(value)
        value = '{:2}'.format(value)
    except:
        pass  # it was a string, not an int.
    return value

class Model(object):
    attributes = None
    def __init__(self, *args, **kwargs):
        self._data = dict(*args, **kwargs)

    def __str__(self):
        return '[{}]'.format(
            ', '.join(['{}:{}'.format(attr, _readable(self._data[attr])) for attr in self._data])
        )

    def __getattr__(self, attr):
        if attr not in self.attributes:
            raise ModelError('Unknown attribute <{}> for <{}>'.format(attr, self.__class__))
        return self._data[attr]

    def __setattr__(self, attr, value):
        if attr in self.attributes:
            self._data[attr] = value
        else:
            super(Model, self).__setattr__(attr, value)
