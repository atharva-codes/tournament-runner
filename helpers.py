

class Model(object):
    attributes = None
    def __init__(self, *args, **kwargs):
        self._data = dict(*args, **kwargs)
    def __getattr__(self, attr):
        if attr not in self.attributes:
            raise ValueError('Unknown attribute <{}>'.format(attr))
        return self._data[attr]
    def __setattr__(self, attr, value):
        if attr in self.attributes:
            self._data[attr] = value
        else:
            super(Model, self).__setattr__(attr, value)


# see https://stackoverflow.com/questions/434287/what-is-the-most-pythonic-way-to-iterate-over-a-list-in-chunks
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

