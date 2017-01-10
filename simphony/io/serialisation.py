import yaml
import numpy

from simphony.cuds.model import CUDS
from simphony.cuds.meta.cuds_component import CUDSComponent
from simphony.core.keywords import KEYWORDS
# from simphony.cuds.meta import *
from simphony.core.cuba import CUBA
from collections import OrderedDict
from importlib import import_module
from simphony.cuds.meta.validation import to_camel_case

_CUDSREFMAP = OrderedDict()


def save_CUDS(handle, model):
    """ Save CUDS model to a Yaml file

    Parameters
    ----------
    handle: file handle
        Yaml file where CUDS model is saved. File will be cleared.
    model: CUDS model

    """

    handle.seek(0)
    handle.truncate()

    handle.write('- NAME:')
    if model.name:
        handle.write(' "'+model.name+'"')
    else:
        handle.write(' Null')
    handle.write('\n\n')
    handle.write('- DESCRIPTION:')
    if model.description:
        handle.write(' "'+model.description+'"')
    else:
        handle.write(' Null')
    handle.write('\n')

    # Construct a map of referenced objects
    global _CUDSREFMAP
    _CUDSREFMAP.clear()
    for comp in model.iter(CUDSComponent):
        # Add component to dictionary if it's not there already
        if comp.uid not in _CUDSREFMAP.keys():
            _CUDSREFMAP[comp.uid] = []
        # Check if the component has CUDSComponents in data
        for data in comp._data.values():
            # either directly, or
            if isinstance(data, CUDSComponent):
                if data.uid not in _CUDSREFMAP.keys():
                    _CUDSREFMAP[data.uid] = []
                _CUDSREFMAP[data.uid] += [comp.uid]
            # as an element of a list
            if type(data) == list:
                for elem in data:
                    if isinstance(elem, CUDSComponent):
                        if elem.uid not in _CUDSREFMAP.keys():
                            _CUDSREFMAP[elem.uid] = []
                        _CUDSREFMAP[elem.uid] += [comp.uid]

    # Save CUDSComponents
    for comp in model.iter(CUDSComponent):
        if _CUDSREFMAP[comp.uid] is not 'saved':
            stream = ''
            stream = _CUDSComponent_to_yaml(comp, stream)
            handle.write(stream)
            _CUDSREFMAP[comp.uid] = 'saved'


def load_CUDS(handle):
    """ Load CUDS model from a Yaml file

    Parameters
    ----------
    handle: file handle
        yaml file containing CUDSComponents

    Raises
    ------
    FileError
        if yaml file contains errors

    Returns
    -------
    model: CUDS
        computational model

    """

    comp_dict = {}
    name = None
    desc = None
    for data in yaml.safe_load_all(handle):
        # Go through the dictionaries constructed from the Yaml script
        for dict_cuds in data:
            cubatype = dict_cuds.keys()[0]
            if cubatype == 'NAME':
                name = dict_cuds['NAME']
            elif cubatype == 'DESCRIPTION':
                desc = dict_cuds['DESCRIPTION']
            else:
                _dict_to_CUDSComponent(cubatype, dict_cuds[cubatype],
                                       comp_dict)

    model = CUDS(name=name, description=desc)
    for compid in comp_dict.keys():
        model.add(comp_dict[compid])

    return model


def _CUDSComponent_to_yaml(comp, stream):
    """ Convert CUDSComponent containing data to Yaml script

    Parameters
    ----------
    comp: CUDSComponent
        CUDSComponent that will be converted to Yaml
    stream: str
        A string to which new Yaml script is added

    Returns
    -------
    str
        A string containing Yaml script of the added CUDSComponent and it's
        sub-components

    """

    # Use global (at module level) dictionary for bookkeeping of the
    # references and of the saved components
    global _CUDSREFMAP
    yaml_comp = '\n'
    yaml_comp += '- ' + str(comp.cuba_key).replace('CUBA.', '') + ':'

    # Check if 'comp' is referenced by some other CUDSComponent in the model
    # and create an alias if needed
    if _CUDSREFMAP[comp.uid]:
        refnum = _CUDSREFMAP.keys().index(comp.uid) + 1
        yaml_comp += ' &' + str(refnum)
    yaml_comp += '\n'

    # Go through the keys in the component
    cdata = comp._data
    for key in cdata.keys():
        # Check if the data is a list or numpy types or CUDSComponents
        if type(cdata[key]) == list:
            # List of simple types?
            if KEYWORDS[key._name_].dtype in [numpy.float64,
                                              numpy.int32, bool]:
                items = []
                for item in cdata[key]:
                    items.append(item.tolist())
                value = str(items)

            # List of CUDSComponents
            else:
                value = '['
                for item in cdata[key]:
                    if isinstance(item, CUDSComponent):
                        if len(value) > 1:
                            value += ', '
                        # CUDSComponent will be referenced by a small int
                        # number in the Yaml script
                        refnum = _CUDSREFMAP.keys().index(item.uid) + 1
                        value += '*' + str(refnum)

                        # Check from _CUDSREFMAP dictionary if the object
                        # referenced is not already saved
                        if _CUDSREFMAP[item.uid] is not 'saved' or []:
                            _CUDSREFMAP[item.uid] = 'saved'
                            # Generate Yaml script for this component
                            stream = _CUDSComponent_to_yaml(item, stream)
                value += ']'

        # Only one CUDSComponent?
        elif isinstance(cdata[key], CUDSComponent):
            refnum = _CUDSREFMAP.keys().index(cdata[key].uid) + 1
            value = '*' + str(refnum)

            # Use _CUDSREFMAP dictionary to mark already saved
            # referenced objects
            if _CUDSREFMAP[cdata[key].uid] is not 'saved' or []:
                _CUDSREFMAP[cdata[key].uid] = 'saved'
                # Generate Yaml script for this component
                stream = _CUDSComponent_to_yaml(cdata[key], stream)

        # Any of the simple data types?
        elif type(cdata[key]) == str:
            value = '"' + str(cdata[key]) + '"'
        elif type(cdata[key]) == numpy.ndarray:
            value = str(cdata[key].tolist())
        elif cdata[key] is None:
            value = None
        else:
            value = str(cdata[key])

        # Write only key-value pairs where value is not None
        if value:
            yaml_comp += '    ' + str(key).replace('CUBA.', '') + \
                ': ' + value + '\n'
    stream = stream + yaml_comp
    return stream


def _dict_to_CUDSComponent(cubatype, comp, comp_dict={}):
    """ Generate a CUDSComponent on the basis of a dictionary
    provided by PyYaml library.

    Parameters
    ----------
    cubatype: str
        CUBA key (name) of the CUDSComponent in the format use in Yaml file
    comp: dict
        Dictionary object containing the parameters of the component.
    comp_dict: dict
        Dictionary where constructed CUDSComponents are added
        with a Python id as reference: key-value pairs are of the format
            id(CUDSComponent): CUDSComponent

    """

    # Check that comp does not refer to one of the components that
    # have been already constructed
    if id(comp) in comp_dict.keys():
        return

    if cubatype in KEYWORDS.keys():
        # Find corresponding module and instantiate the class
        mod = import_module('simphony.cuds.meta.%s' % cubatype.lower())
        comp_class = getattr(mod, to_camel_case(cubatype))
        # Get parameter names for __init__ method
        init_params = comp_class.__init__.func_code.co_varnames

        # Go through the keys and values in comp dictionary and
        # add supported ones to data_dict
        init_kwargs = {}
        system_managed_keys = {}
        supp_params = [str(e).replace('CUBA.', '')
                       for e in comp_class.supported_parameters()]
        # Don't accept UUID entry from the yaml file
        supp_params.remove('UID')
        for key in comp.keys():
            # Check if the key is supported
            if key in supp_params:
                # Check if value contains other CUDSComponents or data
                value = comp[key]
                if type(value) is list:
                    tmp = []
                    for subcomp in value:
                        if type(subcomp) is dict:
                            # Construct the subcomponent before it can be
                            # added to the host component
                            _dict_to_CUDSComponent(key, subcomp, comp_dict)
                            tmp.append(comp_dict[id(subcomp)])
                        else:
                            # validation.validate_cuba_keyword(subcomp, key)
                            tmp.append(subcomp)
                    if key.lower() in init_params:
                        init_kwargs[key.lower()] = tmp
                    else:
                        cubaname = CUBA[key]
                        system_managed_keys[cubaname] = tmp
                elif type(value) is dict:
                    _dict_to_CUDSComponent(key, value, comp_dict)
                    tmp = value
                else:
                    # validation.validate_cuba_keyword(value, key)
                    tmp = value

                if key.lower() in init_params:
                    init_kwargs[key.lower()] = tmp
                else:
                    cubaname = CUBA[key]
                    system_managed_keys[cubaname] = tmp

            else:
                message = 'Unknown CUDSComponent "{}" as a subcomponent'
                raise ValueError(message.format(key))

        # Instantiate component with its subcomponents
        comp_inst = comp_class(**init_kwargs)
        # Add system managed components by updating the DataContainer
        data = comp_inst.data
        data.update(system_managed_keys)
        comp_inst.data = data
    else:
        message = 'Unknown CUDSComponent "{}"'
        raise ValueError(message.format(cubatype))

    # Store component under the key representing it's memory location
    # so that correct object references from the yaml file are preserved
    comp_dict[id(comp)] = comp_inst
