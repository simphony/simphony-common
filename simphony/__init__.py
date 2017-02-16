# -*- coding: utf-8 -*-
"""SimPhoNy: Simulation framework for multi-scale phenomena in micro-
 and nanosystems.

SimPhoNy is an EU-project funded by the 7th Framework Programme (Project
 number 604005) under the call NMP.2013.1.4-1: "Development of an integrated
 multi-scale modelling environment for nanomaterials and systems by design".
 SimPhoNy is a collaborative research project running from January 1st 2014
 until December 31st 2016.

For more information see: http://www.simphony-project.eu/.

:copyright: (c) 2014, 2015, 2016 SimPhoNy Consortium
:license: BSD, see LICENSE for more details.
"""
# Load engines in the beginning.
# TODO: make engine loader explicit
import simphony.engine  # noqa

from .core import CUBA
from .cuds import CUDS, Simulation

__all__ = ['CUBA', 'CUDS', 'Simulation']
