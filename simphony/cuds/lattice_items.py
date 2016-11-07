from simphony.core import DataContainer


class LatticeNode(object):
    """A single node of a lattice.

    Attributes
    ----------
    index : tuple of int[3]
        node index coordinate
    data : DataContainer

    """
    def __init__(self, index, data=None):
        self.index = index[0], index[1], index[2]

        if data is None:
            self.data = DataContainer()
        else:
            self.data = DataContainer(data)
