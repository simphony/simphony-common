import warnings
import importlib
from functools import wraps
from .meta import api

_CUBA_CUDS_MAP = None


def deprecated(func):
    @wraps(func)
    def _deprecated(*args, **kwargs):
        warnings.warn("Deprecation warning: {}".format(func.__name__))
        return func(*args, **kwargs)

    return _deprecated


def map_cuba_key_to_cuds_class(cuba_key):
	"""Return the equivalent CUDS class for the given CUBA key.

	Parameters
	----------
	cuba_key: CUBA
		The key to find its equivalent CUDS class.

	Raises
	------
	ValueError:
		If no CUDS exists for the given CUBA key.

	Returns
	-------
	object: type
	"""
	global _CUBA_CUDS_MAP
	if not _CUBA_CUDS_MAP:
		_fill_cuba_cuds_map()

	if cuba_key not in _CUBA_CUDS_MAP:
		raise ValueError('No CUDS class exist for {cuba_key}'
			.format(cuba_key=cuba_key))

	return _CUBA_CUDS_MAP[cuba_key]


def _fill_cuba_cuds_map():
	"""Fill the cuba-cuds map."""
	api_mod = importlib.import_module('simphony.cuds.meta.api')
	global _CUBA_CUDS_MAP
	_CUBA_CUDS_MAP = \
		dict([(cls.cuba_key, cls) for name, cls \
			in api_mod.__dict__.items() \
			if isinstance(cls, type) and issubclass(cls, api.CUDSItem)])
