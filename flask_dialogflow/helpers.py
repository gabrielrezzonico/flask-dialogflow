
class TypedList(list):
    """List that force typing on its elements. 

    Arguments:
        type -- The type to force
    """

    def __init__(self, type):
        self.type = type

    def _check_type(self, item):
        if not isinstance(item, self.type):
            raise Exception(TypeError, 'item is not of type %s' % self.type)

    def append(self, item):
        self._check_type(item)
        super(TypedList, self).append(item)

    def insert(self, pos, item):
        self._check_type(item)
        super(TypedList, self).insert(pos, item)
