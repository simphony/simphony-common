"""Lattice data specification of SimPhoNy CUDS, a non-wrapper implementation.

Classes:
--------
ABCLattice:
    describes a Bravais lattice. Holds references to N data containers.
    A set of nodes is associated with each data container.
    Mediates ids describing the node sets (ids stored in the data container).
    Node index coordinates used as ids.
    Data containers are accessed with a given name.
    Lattice has a default container with a constant name (see below).
    Every lattice node is associated with the default container.
    Ids are not stored for the default container (ids retrieved implicitly).

DataContainer:
    stores data for a lattice (including ids of the associated node set).
    Data stored as keyword-value pairs.
    Data is accessed with a given keyword.

Constants:
----------
DEFAULT_LATTICE_DC_NAME: string
    name of the default data container for an ABCLattice object.
    
Routines:
---------
make_hexagonal_lattice:
    create and return a 2D hexagonal lattice.

make_square_lattice:
    create and return a 2D square lattice.

make_rectangular_lattice:
    create and return a 2D rectangular lattice.

make_cubic_lattice:
    create and return a 3D cubic lattice.

make_orthorombicp_lattice:
    create and return a 3D orthorhombic (primitive) lattice.
"""    
# ===========================================================================
# Import modules
# ===========================================================================
import numpy as np
from math import sqrt
# ===========================================================================
# Constants
# ===========================================================================
DEFAULT_LATTICE_DC_NAME = 'Lattice'
# ===========================================================================
# Class DataContainer
# ===========================================================================
class DataContainer:
    """
    Store data as keyword-value pairs.

    Parameters:
    -----------
    name: string
    """
    def __init__(self, name):
        self.name = name
        self.data = {} # dictionary

    def set_data(self, keyword, values):
        """Store values related to a given keyword.
        
        Parameters:
        -----------
        keyword: string
        values: any data
        """
        self.data[keyword] = values

    def get_keywords(self):
        """Get all keywords.
        
        Returns:
        -----------
        A list of strings.
        """
        return self.data.keys()

    def get_values(self, keyword):
        """Get values related to a given keyword.
        
        Parameters:
        -----------
        keyword: string

        Returns:
        -----------
        any data
        """
        return self.data[keyword]

    def del_data(self, keyword):
        """Delete values related to a given keyword.
        
        Parameters:
        -----------
        keyword: string
        """
        del self.data[keyword]

    def get_name(self):
        """Get name of the data container.
        
        Returns:
        --------
        string
        """
        return self.name
# end        
# ===========================================================================
# class ABCLattice
# ===========================================================================
class ABCLattice:
    """
    Defines a Bravais lattice; stores data separately for given node subsets.

    Parameters:
    -----------
    name: string
    type: string
        Bravais lattice type (should agree with the base_vect below).
    base_vect: D x float
        defines a Bravais lattice (an alternative for primitive vectors).
    size: D x size
        number of lattice nodes (in the direction of each axis).
    origin: D x float
    """
    def __init__(self, name, type, base_vect, size, origin):
        self.name = name
        self.type = type
        self.base_vect = np.array(base_vect, dtype=np.float)
        self.size = np.array(size, dtype=np.uint32)
        self.origin = np.array(origin, dtype=np.float)
        self.dcs = {} # dictionary

        dc = DataContainer(DEFAULT_LATTICE_DC_NAME)
        self.dcs[DEFAULT_LATTICE_DC_NAME] = dc

    # -----------------------------------------------------------------------
    def new_data_container(self, dc_name, node_ids):
        """Create and store a new data container for the lattice.
        
        Parameters:
        -----------
        dc_name: string
            name of the new data container.
        node_ids: an array of index coordinates (i.e. an array of D x int)
            define nodes associated with the new container.
        
        Returns:
        --------
        dc: DataContainer
            the new data container.
        """
        dc = DataContainer(dc_name)
        dc.set_data('Id',node_ids)
        self.dcs[dc_name] = dc
        return dc

    def del_data_container(self, dc_name):
        """Delete a given data container.
        
        Parameters:
        -----------
        dc_name: string
        """
        del self.dcs[dc_name]

    def get_data_containers(self):
        """Get all data containers.
        
        Returns:
        -----------
        A list of references to the data containers.
        """
        return self.dcs.values()

    def get_data_container(self, dc_name = DEFAULT_LATTICE_DC_NAME):
        """Get the data container with a given name.
        
        Parameters:
        -----------
        dc_name: string (default value = DEFAULT_LATTICE_DC_NAME)

        Returns:
        -----------
        A reference to the data container with a given name.
        """
        return self.dcs[dc_name]

    def get_D(self):
        """Get the spatial dimension of the lattice.
        
        Returns:
        -----------
        int
        """
        return self.size.shape[0]

    def get_node_ids(self, dc_name = DEFAULT_LATTICE_DC_NAME):
        """Get ids of the nodes associated with the given data container.
        
        Parameters:
        -----------
        dc_name: string (default value = DEFAULT_LATTICE_DC_NAME)

        Returns:
        -----------
        An array of index coordinates (i.e. an array of D x int).
        """
        if dc_name == DEFAULT_LATTICE_DC_NAME:
            d = self.get_D()
            if d == 1:
                return np.mgrid[0:self.size[0]].reshape(1, -1).T
            elif d == 2:
                return np.mgrid[0:self.size[0],
                                0:self.size[1]].reshape(2, -1).T
            elif d == 3:
                return np.mgrid[0:self.size[0],0:self.size[1],
                                0:self.size[2]].reshape(3, -1).T
            else:
                return ()
        else:
            return self.get_data_container(dc_name).get_values('Id')
       # end else if

    def get_node_count(self, dc_name = DEFAULT_LATTICE_DC_NAME):
        """Get number of nodes associated with the given data container.
        
        Parameters:
        -----------
        dc_name: string (default value = DEFAULT_LATTICE_DC_NAME)

        Returns:
        -----------
        int
        """
        if dc_name == DEFAULT_LATTICE_DC_NAME:
            return np.prod(self.size)
        else:
            return self.get_data_container(dc_name).get_values('Id').shape[0]
        # end else if

    def get_coordinate(self, node_id):
        """Get coordinate of the node with the given index coordinate.
        
        Parameters:
        -----------
        node_id: index coordinate (i.e. D x int)

        Returns:
        -----------
        D x float
        """
        return self.origin + self.base_vect*np.array(node_id)

    def get_name(self):
        """Get name of the lattice.
        
        Returns:
        -----------
        string
        """
        return self.name

    def get_type(self):
        """Get Bravais type of the lattice.
        
        Returns:
        -----------
        string
        """
        return self.type

    def get_base_vector(self):
        """Get the lattice base vectors.
        
        Returns:
        -----------
        D x float
        """
        return self.base_vect

    def get_size(self):
        """Get number of lattice nodes (for each axis direction).
        
        Returns:
        -----------
        D x int
        """
        return self.size

    def get_origin(self):
        """Get origin of the lattice.
        
        Returns:
        -----------
        D x float
        """
        return self.origin
# end
# ===========================================================================
# Functions for creating Bravais lattices
# ===========================================================================
def make_hexagonal_lattice(name, h, size, origin = (0,0)):
    """Create and return a 2D hexagonal lattice.
    
    Parameters:
    -----------
    name: string
    h: float
        lattice spacing.
    size: 2 x int
        number of lattice nodes (in each axis direction).
    origin: 2 x float (default value = (0,0))
        lattice origin.

    Returns:
    -----------
    A reference to an ABCLattice object.
    """
    return ABCLattice(name,'Hexagonal',(0.5*h,0.5*sqrt(3)*h),size,origin)

def make_square_lattice(name, h, size, origin = (0,0)):
    """Create and return a 2D square lattice.
    
    Parameters:
    -----------
    name: string
    h: float
        lattice spacing.
    size: 2 x int
        number of lattice nodes (in each axis direction).
    origin: 2 x float (default value = (0,0))
        lattice origin.

    Returns:
    -----------
    A reference to an ABCLattice object.
    """
    return ABCLattice(name,'Square', (h,h), size, origin)

def make_rectangular_lattice(name, hs, size, origin = (0,0)):
    """Create and return a 2D rectangular lattice.
    
    Parameters:
    -----------
    name: string
    hs: 2 x float
        lattice spacings (in each axis direction).
    size: 2 x int
        number of lattice nodes (in each axis direction).
    origin: 2 x float (default value = (0,0))
        lattice origin.

    Returns:
    -----------
    A reference to an ABCLattice object.
    """
    return ABCLattice(name,'Rectangular', hs, size, origin)

def make_cubic_lattice(name, h, size, origin = (0,0,0)):
    """Create and return a 3D cubic lattice.
    
    Parameters:
    -----------
    name: string
    h: float
        lattice spacing.
    size: 3 x int
        number of lattice nodes (in each axis direction).
    origin: 3 x float (default value = (0,0,0))
        lattice origin.

    Returns:
    -----------
    A reference to an ABCLattice object.
    """
    return ABCLattice(name,'Cubic', (h,h,h), size, origin)

def make_orthorombicp_lattice(name, hs, size, origin = (0,0,0)):
    """Create and return a 3D orthorombic primitive lattice.
    
    Parameters:
    -----------
    name: string
    hs: 3 x float
        lattice spacings (in each axis direction).
    size: 3 x int
        number of lattice nodes (in each axis direction).
    origin: 3 x float (default value = (0,0,0))
        lattice origin.

    Returns:
    -----------
    A reference to an ABCLattice object.
    """
    return ABCLattice(name,'OrthorombicP', hs, size, origin)
# ===========================================================================
# Keijo Mattila & Tuomas Puurtinen, SimPhoNy, JYU, 2014.
# ===========================================================================