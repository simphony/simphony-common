import warnings

from . import CUBA as CUDSItem


warnings.warn("Deprecation warning: {}"
              .format('CUDSItem is deprecated. Use CUBA instead.'))

# In order to maintain backward compatibility
__all__ = ['CUDSItem']
