Description of YAML format
==========================

Specification version: 1.0

This document describes the format of the metadata description.
It is not meant to describe the concept of CUBA and CUDS and what they
represent. Merely to describe how their logic is represented in the
file at the YML level.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and
"OPTIONAL" in this document are to be interpreted as described in
RFC 2119. [1]_

Changelog
---------

- Initial release

Format description
------------------

The format is defined two files in yaml format:

- cuba.yml: describes basic data types that semantically enhance plain data.
  For example, a string that is used to represent a UUID. 

- simphony_metadata.yml: Describes high level objects and their external links
  to other objects, either as specialization or relationship.

The keys described in this format specification MUST be interpreted as case sensitive.

Terminology
-----------

The following terms are used in relation to the SimPhoNy metadata description:

- ``concept``: an abstract, "discourse" entity we want to describe in our ontology. 
  Example: the Lennard Jones potential, a vector, etc.
- ``CUBA data type``: a concrete (as in "formalized for our objectives") entity we define to 
  represent a ``concept`` that has no dependencies toward other ``concepts``, and it is defined 
  only by its expected data type and dimensionality (e.g. a Vector type).
  The ``CUBA data type`` has the following characteristics:

    - a unique vocabulary term (in ``CUBA key`` format) defining its type (e.g. VECTOR)
    - characteristics of shape and data type.

- ``CUDS item``: a concrete entity we define to represent a ``concept`` that has relationships
  with other concepts.  The ``CUDS item`` has the following characteristics:

        - a unique vocabulary term defining its type (e.g. LENNARD_JONES_6_12)
        - a unique identifier (e.g. a UUID which is going to be different for two distinct Lennard Jones potentials)
          to be able to distinguish specific instances of the ``CUDS item``.
        - a set of properties that are expressed as relations to other ``concepts``. Two types of properties exist:

           - ``Fixed properties``: Properties that depend only on the CUDS Item type. 
           - ``Variable properties``: Properties that depend on the specific instance of the CUDS Item.
       
The following terms are used in the remainder of this document and are prescriptive:

- ``(non-qualified) CUBA key``: a fully capitalized, underscored name to refer to a CUDS item or CUBA data type 
   (e.g. COMPUTATIONAL_MODEL).
- ``qualified CUBA key``: a CUBA key prefixed with the ``CUBA.`` string (e.g. CUBA.COMPUTATIONAL_MODEL)
- ``CUBA entry``: an entry defined in the cuba.yml file under CUBA_KEYS that represents a CUBA data type
- ``CUDS entry``: an entry defined in the simphony_remote.yml file under CUDS_KEYS that represents a CUDS item.

cuba.yml
--------

The format MUST have a root mapping with the following keys:

- ``VERSION``: string
  Contains semantic version Major.minor in format M.m with M and m positive integers.
  minor MUST be incremented when backward compatibility in the format is preserved. 
  Major MUST be incremented when backward compatibility is removed.
  Due to the strict nature of the format, a change in minor is unlikely.
  **NOTE** that this is the version of the file format, _NOT_ of the described information (CUDS).
  the addition of new CUDS entries will not require a version change, as
  long as the layout of the file complies with the standard 
  **NOTE**: The value must be explicitly quoted, as it would otherwise be interpreted
  by the yaml parser as a floating point value

- ``CUBA``: string
  Defines the type of file. The content is a free format string whose value has no 
  semantic meaning. It can be used as a comment.

- ``CUBA_KEYS``: mapping 
  contains a mapping describing the declared **CUBA entries**.
  Each key of the mapping is the non-qualified name of a CUBA entry.  The Key MUST be all
  uppercase, with underscore as separation. Numbers are allowed but not in first
  position. Valid Examples: ``FACE``, ``ANGULAR_ACCELERATION``, ``POSITION_3D``
  Each value of the mapping is a mapping whose format is detailed in the
  "CUBA entries format" section.

The root mapping MAY contain the following keys:

- ``Purpose``: string
  For human consumption. Free format string to describe the contents of the file.

- ``Resources``: mapping
  For human consumption. A mapping between a user meaninfgul entity and a string
  describing that entity, for example a link to a spec or an email address.

CUBA entries format
~~~~~~~~~~~~~~~~~~~

Each CUBA_KEYS entry MUST contain a mapping with the following keys:
    
- ``type``: string
  The type of the CUBA. MUST be one of the following
    
        - string
        - integer
        - double
        - boolean

It MAY also contain:

- ``definition``: string 
  For human consumption. Free form description of the semantic carried by the data type.

- ``shape``: inline sequence of positive integers
  The represented CUBA data is an array, rather than a scalar. 
  `shape` defines the shape of this array. MUST be a list of positive integers. 
  If not present, the default is the list ``[1]``

- ``length``: integer
  This key MUST be present if the type is ``string``. It MUST NOT be present otherwise.
  It constraints the length of the string to the specified amount.

simphony_metadata.yml
---------------------

The format MUST have a root level mapping with the following keys:

- ``VERSION``: as in cuba.yml

- ``CUDS``: As in cuba.yml ``CUBA`` entry

- ``CUDS_KEYS``: as in cuba.yml
    Contains individual declarations for CUDS Items, in the form of CUDS entries. 
    Each key of the mapping is the name of a CUDS entry.  The Key MUST be all
    uppercase, with underscore as separation. Numbers are allowed but not in first
    position. Each value of the mapping is a mapping whose format is detailed in the
    "CUDS entries format" section.

it MAY contain the following entries

- ``Purpose``: string
  As in cuba.yml

- ``Resources``: string
  As in cuba.yml

CUDS entries format
~~~~~~~~~~~~~~~~~~~

Each ``CUDS entry`` MUST contain a mapping.  The keys of the mapping represent properties of the ``CUDS Item``. 

- ``Fixed properties`` use simple, lowercase names as keys. 
- ``Variable properties`` use ``qualified CUBA key`` as keys.

The following ``Fixed properties`` keys MUST be present:
    
- ``parent``: ``qualified CUBA key`` or empty (None) 
  The parent CUDS of a inheritance (is-a) hierarchy. MUST be either:

    - a string referring to another entry. for example::

      parent: CUBA.PAIR_POTENTIAL

    - or, an empty entry (yaml meaning: None), for the start of the hierarchy (parentless).

Apart from the above keys, other Fixed properties keys MAY be present, and their 
content is specified in "Fixed Properties entries format". They represents properties 
whose value is fixed and hardcoded. 

Some Fixed properties keys have however particular semantic meaning and are commonly used.
Refer to "Semantic rules" for additional information.

The entry MAY contain Variable properties in the form:

- **qualified CUBA key**: mapping
  Describe the existence of a relation toward a specified ``CUBA data type``
  or ``CUDS Item``. Each key:

     - MUST be a ``qualified CUBA key``
     - MUST have been defined in one of the files.
     - SHOULD be specified only once in the ``CUDS entry`` (by nature of the mapping, only the last entry will be used)
     - when converted to non-qualified lowercase, MUST NOT be equal to a ``fixed property`` key.

All the CUBA properties are variable properties

Fixed Property entries format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The content of a fixed property can be either a mapping, or some other entity. In the case 
of a mapping the following keys MAY be present

- ``scope``: string
    Controlled dictionary. Allowed strings:

        - ``CUBA.USER``: Default if not specified. Indicates that this
          property is available for setting at construction. Its initial 
          value is the appropriate default.
        - ``CUBA.SYSTEM`: Indicates that this property cannot be specified 
          by the user (i.e. is not available for setting at construction)
          and its value is set by internal code. If this key is present, 
          the ``default`` key MUST NOT be present. The generator will use
          the associated Property key to produce the appropriate 
          initialization code. Examples of these properties are the 
          Fixed property ``data`` and the Variable property CUBA.UID.

- ``default``: any
    Indicates the hardcoded value for the property.
    The value is used as specified. 
    If ``scope`` is ``CUBA.SYSTEM``, this entry MUST NOT be present 
    If ``scope`` is ``CUBA.USER``, this entry MUST be present 

If the content is not a mapping (e.g. string, list, numerical value), it is interpreted 
as equivalent to a mapping-type specification where 

- ``default`` is the specified entity
- ``scope`` is ``CUBA.USER``

For example, these two writings of definition are equivalent::

    BASIS:
      parent: CUBA.CUDS_COMPONENT
      definition: Space basis vectors (row wise)

    BASIS:
      parent: CUBA.CUDS_COMPONENT
      definition: 
        scope: CUBA.USER
        default: Space basis vectors (row wise)

            
Variable Property entries format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each Property entry of a given property is a mapping that MAY have the following keys:

- ``scope``: string
    as in Fixed properties entries

- ``shape``: sequence of positive ints or "colon" notation.
    Specifies the shape of the container holding the contained CUBA type. Default is the
    list [1]. Examples:

        - ``[3]`` : A vector of three entities.
        - ``[3,3]`` : array of 3x3 CUBA entities. 

   To define arrays of arbitrary length on one or multiple dimensions, the following "colon"
   notation is used. Note that parentheses are used insted of square brackets. This is
   due to how the colon would be interpreted by the yaml parser:

        - ``(:,:)`` : an arbitrary size matrix.
        - ``(3,:)`` : a 3xn matrix.
        - ``(:)`` : an arbitrary size vector.

- ``default``: 
    Indicates the default value for the property once the ``CUDS Item`` has 
    been instantiated.
    The default MUST be type compatible with the property entry key 
    (eg. integers if the data is an integer)
    If the key refers to a CUBA data, the default must match shape, type and length 
    requirements specified for the CUBA data, keeping into account the shape of the CUBA data 
    itself. 
    If the key refers to a CUDS item, the default must belong to the hierarchy defined by
    the CUDS item designated in the key.
    if the ``scope`` is ``CUBA.SYSTEM``, this key MUST NOT be present


Examples
~~~~~~~~

The following entry specifies that BASIS links against 3 VECTOR objects, where VECTOR is a ``CUBA data type``. 
Each VECTOR has shape 3, so the required default is 3x3 ::

    BASIS:
      parent: CUBA.CUDS_COMPONENT
      definition: Space basis vectors (row wise)
      CUBA.VECTOR:
        shape: [3]
        default: [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

The following example specifies that the NEUMANN ``CUDS Item`` refers to an unlimited list of 
MATERIAL (where MATERIAL is a ``CUDS Item``). The default is to refer to no MATERIAL object::

    NEUMANN:
      # ...
      CUBA.MATERIAL:
        shape: (:)
        default: []

Semantic format
---------------

Semantic rules
~~~~~~~~~~~~~~

This section details additional requirements that go beyond the low level file format, but should be considered by
the parser to validate the final format.

- ``CUDS parent``: 

    - The file MUST contain one and only one parentless entry.
    - There MUST NOT be loops in the hierarchy.

- ``CUDS models``: The strings contained in this list MUST refer to
  CUDS Items that are children of CUBA.COMPUTATIONAL_MODEL. 

- ``CUDS variables``: entries must refer to data types as defined in the cuba.yml file.

- ``CUDS physics_equations``:
    - The entries contained in this list MUST refer to a child of PHYSICS_EQUATION.

    - The entry is only valid for ``COMPUTATIONAL_METHOD`` and its children.
      An error MUST be raised if found under any other keyword.

- ``CUDS properties defaults``:
    When specifying a CUDS property (e.g. CLASS_A) default and the default is non-trivial (e.g. None)
    it MUST refer to a subclass (e.g. CLASS_A1) of the property type. In other words::

        CLASS_A: 
            parent: CUBA.SOMETHING
        
        CLASS_A1:
            parent: CUBA.CLASS_A

        CLASS_A2:
            parent: CUBA.CLASS_A

        CLASS_C:
            parent: CUBA.SOMETHING_ELSE
            CLASS_A:
                default: CLASS_A1

Semantically defined fixed property keys and their contents:

- ``definition``: string 
    For human consumption. Free form description of the carried semantics.

- ``models``: sequence of ``qualified CUBA key``.
    Describes the computational models this ``CUDS Item`` is relevant for.
    Each entry MUST be fully qualified with the ``CUBA.`` prefix. 
    See ``Semantic rules`` for additional requirements of this entry.

- ``physics_equations``: sequence of ``qualified CUBA keys``.
    Describes the physics equations associated to this computational method.
    Each entry MUST be qualified with the ``CUBA.`` prefix.
    See ``Semantic rules`` for additional requirements of this entry.

- ``variables``: sequence of ``qualified CUBA keys``.
    Defines metainformation of required data for this ``CUDS Item`` to be valuable.
    This entry is just presented as metadata. It is up to the client code to interpret 
    it appropriately.  The concrete, "hard numbers" data is stored somewhere else.
    See ``Semantic rules`` for additional requirements of this entry.

- ``data``: mapping
    Defines the presence of a "data" property which collects all the transient
    (i.e. user defineable) data.
    This entry MUST be present only on the root object (parent is empty). 
    It MUST NOT be present anywhere else.
    Its mapping MUST contain:

        - ``scope``: MUST be ``CUBA.SYSTEM``.
  
Parser behavior
---------------

An error MUST be reported, and parsing stopped when the following circumstances occur:

- non-compliance with the yaml format
- non-compliance with the format described in this specification.
- Unrecognized keys 
- Duplicated keys
- Violation of semantic rules.

References
----------
.. [1] https://www.ietf.org/rfc/rfc2119.txt
