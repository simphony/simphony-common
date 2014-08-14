# -*- coding: utf-8 -*-
"""
    Module for definition of custom exceptions for Particles classes.
    The exceptions have a custom message contained in a private dictionary.
"""

"""
    Message Errors:
"""

_PC_errors = {
    'IncorrectParticlesTuple': """Incorrect length of particles tuple: \
    it shouldn\'t be empty.""",
    'ParticlesContainer_DuplicatedValue': 'Object already exists!',
    'ParticlesContainer_UnknownValue': 'Value doesn\'t exists!'
}


class PC_DuplicatedValueError(Exception):
    """This exception indicates that particle or the bond to be added already
    was in the Particle Container.
    """
    def __init__(self):
        Exception.__init__(self,
                           _PC_errors['ParticlesContainer_DuplicatedValue'])


class PC_UnknownValueError(Exception):
    """This exception indicates that particle or the bond to be updated,
    removed, etc. was not in the Particle Container.
    """
    def __init__(self):
        Exception.__init__(self, _PC_errors['ParticlesContainer_UnknownValue'])


class B_IncorrectTupleError(Exception):
    """This exception indicates that the bond to be created wasn't provided
    with a correct particle tuple.
    """
    def __init__(self):
        Exception.__init__(self, _PC_errors['IncorrectParticlesTuple'])
