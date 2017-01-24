"""The core CUDS entities based on SimPhoNy metadata."""
from .cuba import CUBA
from .data_container import DataContainer


class Default():
    pass


__all__ = ['CUBA', 'DataContainer']
