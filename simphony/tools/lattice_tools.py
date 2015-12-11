from itertools import permutations, combinations

import numpy
from simphony.cuds.primitive_cell import PrimitiveCell, BravaisLattice


def vector_len(vec):
    ''' Length of vector

    Parameter
    ---------
    vec : array_like

    Returns
    -------
    length : ndarray
    '''
    return numpy.sqrt(numpy.dot(vec, vec))


def cosine_two_vectors(vec1, vec2):
    ''' Return the cosine of the acute angle between two vectors

    Parameters
    ----------
    vec1 : array_like
    vec2 : array_like


    Returns
    -------
    cosine : numpy ndarray
    '''
    vec1_length = vector_len(vec1)
    vec2_length = vector_len(vec2)
    return numpy.dot(vec1, vec2)/vec1_length/vec2_length


def same_lattice_type(target_pc, p1, p2, p3, permute=True):
    ''' Return True if a set of primitive vectors ``p1``, ``p2``,
    ``p3`` describes the same type of lattice as the target
    primitive cell ``target_pc`` does.  Single precision applies.

    Parameters
    ----------
    target_pc : PrimitiveCell
        Target lattice's primitive cell
    p1, p2, p3 : array_like (len=3)
        Primitive vectors
    permute: boolean
        whether p1, p2, p3 are permutated

    Returns
    -------
    match : bool
    '''
    pcs = (target_pc.p1, target_pc.p2, target_pc.p3)

    # cosine angles between pairs of the target primitive vectors
    target_cosines = tuple(numpy.abs(cosine_two_vectors(vec1, vec2))
                           for vec1, vec2 in combinations(pcs, 2))

    # length ratios between pairs of the target primitive vectors
    target_ratios = tuple(vector_len(vec1)/vector_len(vec2)
                          for vec1, vec2 in permutations(pcs, 2))

    if permute:
        iter_func = permutations
    else:
        iter_func = combinations

    for iperm, perms in enumerate(iter_func((p1, p2, p3), 3)):
        cosines = tuple(numpy.abs(cosine_two_vectors(vec1, vec2))
                        for vec1, vec2 in combinations(perms, 2))
        ratios = tuple(vector_len(vec1)/vector_len(vec2)
                       for vec1, vec2 in permutations(perms, 2))

        # single precision
        atol = numpy.finfo(numpy.float32).resolution
        if (numpy.allclose(cosines, target_cosines, atol=atol) and
                numpy.allclose(ratios, target_ratios, atol=atol)):
            return True
    return False


def guess_primitive_vectors(points):
    ''' Guess the primitive vectors underlying a given array of
    lattice points (N, 3).

    Parameter
    ----------
    points : numpy ndarray (N, 3)
        Coordinates of lattice nodes
        Assumed to be arranged in C-contiguous order so that the
        first point is the origin, the last point is furthest
        away from the origin

    Returns
    -------
    p1, p2, p3 : 3 x tuple of float[3]
        primitive vectors

    Raises
    ------
    IndexError
        (1) if the lattice dimension cannot be determined
        (2) if the points are not ordered contiguously
    '''
    def find_jump(arr1d):
        ''' Return the index where the first derivation changes '''
        sec_dev = numpy.diff(arr1d, n=2)
        return numpy.where(~numpy.isclose(sec_dev, 0.))[0][0]+2

    for idim in range(3):
        try:
            nx = find_jump(points[:, idim])
            break
        except IndexError:   # numpy.where is empty
            continue
    else:
        message = "Failed to deduce the first lattice dimension"
        raise IndexError(message)

    for idim in range(3):
        try:
            ny = find_jump(points[::nx, idim])
            break
        except IndexError:   # numpy.where is empty
            continue
    else:
        message = "Failed to deduce the second lattice dimension"
        raise IndexError(message)

    # Test if the lattice points are ordered as expected
    if not (numpy.allclose(numpy.diff(points[:nx, 0], n=2), 0.) and
            numpy.allclose(numpy.diff(points[::nx, 1][:ny], n=2), 0.) and
            numpy.allclose(numpy.diff(points[::nx*ny, 2], n=2), 0.)):
        message = ("Deduction of the primitive vectors requires the "
                   "lattice nodes to be ordered in a C-contiguous fashion.")
        raise IndexError(message)

    # Primitive vectors
    return tuple((points[ipoint, 0]-points[0, 0],
                  points[ipoint, 1]-points[0, 1],
                  points[ipoint, 2]-points[0, 2]) for ipoint in (1, nx, nx*ny))


def is_cubic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a cubic lattice

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # if all lengths close to each other
    a, b, c = map(vector_len, (p1, p2, p3))
    if not numpy.allclose((b, c), a):
        return False

    # all angles close to 90 degree
    cosines = map(cosine_two_vectors,
                  (p1, p2, p3), (p2, p3, p1))
    return numpy.isclose(cosines, 0.).all()


def is_body_centered_cubic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a body centered cubic lattice

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # exactly two sides of equal lengths
    a, b, c = map(vector_len, (p1, p2, p3))
    equal_len_pairs = numpy.isclose((a, b, c), (b, c, a))

    if not equal_len_pairs.sum() == 1:
        return False

    return same_lattice_type(PrimitiveCell.for_body_centered_cubic_lattice(1.),
                             p1, p2, p3)


def is_face_centered_cubic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a face centered cubic lattice

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # all sides of equal lengths
    a, b, c = map(vector_len, (p1, p2, p3))
    if not numpy.allclose((a, b), c):
        return False

    # all angles close to 60 degree
    cosines = numpy.abs(map(cosine_two_vectors,
                            (p1, p2, p3), (p2, p3, p1)))
    return numpy.allclose(cosines, 0.5)


def is_rhombohedral_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a rhombohedral lattice

    Also returns True for vectors describing a cubic or face centered
    cubic lattice

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # all sides of equal lengths
    a, b, c = map(vector_len, (p1, p2, p3))
    if not numpy.allclose((a, b), c):
        return False

    # all angles close to each other
    cosa, cosb, cosc = numpy.abs(map(cosine_two_vectors,
                                     (p1, p2, p3), (p2, p3, p1)))
    return numpy.allclose((cosa, cosb), cosc)


def is_tetragonal_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a tetragonal lattice

    Also returns True for vectors describing a cubic lattice

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # at least two sides of equal lengths
    a, b, c = map(vector_len, (p1, p2, p3))
    equal_lengths = numpy.isclose((a, b, c), (b, c, a))

    if not equal_lengths.any():
        return False

    # all angles close to 90 degrees
    cosines = map(cosine_two_vectors,
                  (p1, p2, p3), (p2, p3, p1))
    return numpy.allclose(cosines, 0.)


def is_body_centered_tetragonal_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a body centered tetragonal
    lattice

    Also returns True for vectors describing a body centered cubic
    lattice

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # at least two sides of equal lengths
    a, b, c = map(vector_len, (p1, p2, p3))
    equal_len_pairs = numpy.isclose((a, b, c), (b, c, a))

    if not equal_len_pairs.any():
        return False
    elif equal_len_pairs.all():
        factory = PrimitiveCell.for_body_centered_tetragonal_lattice
        return same_lattice_type(factory(1., 1.), p1, p2, p3)
    else:
        # only one pair of equal edges
        # mapping for the vectors and edges
        pair_other = {0: ((p1, p2), p3, (a, c)),
                      1: ((p2, p3), p1, (b, a)),
                      2: ((p1, p3), p2, (a, b))}

        # v1 and v2 should be perpendicular vectors of the same lengths
        # the another vector make the same angle with the other two
        (v1, v2), v3, (a, b) = pair_other[numpy.where(equal_len_pairs)[0][0]]

        return (numpy.isclose(cosine_two_vectors(v1, v2), 0.) and
                numpy.allclose((numpy.abs(cosine_two_vectors(v1, v3)),
                                numpy.abs(cosine_two_vectors(v2, v3))),
                               0.5*a/b))


def is_hexagonal_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a hexagonal lattice

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # at least two sides of equal lengths
    a, b, c = map(vector_len, (p1, p2, p3))
    equal_len_pairs = numpy.isclose((a, b, c), (b, c, a))

    if not equal_len_pairs.any():
        return False
    elif equal_len_pairs.all():
        factory = PrimitiveCell.for_hexagonal_lattice
        return same_lattice_type(factory(1., 1.), p1, p2, p3)
    else:
        # only one pair of equal edges
        pair_other = {0: ((p1, p2), p3),
                      1: ((p2, p3), p1),
                      2: ((p1, p3), p2)}
        # v1 and v2 have the same length
        (v1, v2), v3 = pair_other[numpy.where(equal_len_pairs)[0][0]]
        # check if v1 and v2 make an angle of 60 degree
        # v3 makes a right angle with both v1 and v2
        return (numpy.isclose(numpy.abs(cosine_two_vectors(v1, v2)), 0.5) and
                numpy.allclose((cosine_two_vectors(v1, v3),
                                cosine_two_vectors(v2, v3)), 0.))


def is_orthorhombic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe an orthorhombic lattice

    Also returns True for vectors describing a cubic or tetragonal
    lattice

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # all angles close to 90 degrees
    cosines = map(cosine_two_vectors,
                  (p1, p2, p3), (p2, p3, p1))
    return numpy.allclose(cosines, 0.)


def is_body_centered_orthorhombic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a body centered orthorhombic
    lattice

    Also returns True for vectors describing a body centered cubic or
    a body centered tetragonal lattice

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    vec_lengths = map(vector_len, (p1, p2, p3))
    factory = PrimitiveCell.for_body_centered_orthorhombic_lattice

    for alpha, beta, gamma in permutations(vec_lengths):
        delta = 4*gamma**2.-alpha**2.-beta**2.
        if (delta > 0. and
                same_lattice_type(factory(alpha, beta, numpy.sqrt(delta)),
                                  p1, p2, p3)):
            return True
    return False


def is_face_centered_orthorhombic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a face centered orthorhombic
    lattice

    Also returns True for vectors describing a face centered cubic
    lattice

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    vec_lengths = map(vector_len, (p1, p2, p3))
    factory = PrimitiveCell.for_face_centered_orthorhombic_lattice

    alpha, beta, gamma = vec_lengths
    a2 = 2.*(gamma**2.+beta**2.-alpha**2.)
    b2 = 2.*(alpha**2.+gamma**2.-beta**2.)
    c2 = 2.*(alpha**2.+beta**2.-gamma**2.)

    if a2 <= 0 or b2 <= 0 or c2 <= 0:
        return False

    abc = map(numpy.sqrt, (a2, b2, c2))
    return same_lattice_type(factory(*abc), p1, p2, p3, permute=False)


def is_base_centered_orthorhombic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a base centered orthorhombic
    lattice

    Also returns True for vectors describing a hexagonal lattice

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    vec_lengths = map(vector_len, (p1, p2, p3))
    factory = PrimitiveCell.for_base_centered_orthorhombic_lattice

    for alpha, beta, gamma in permutations(vec_lengths, 3):
        delta = 4.*beta**2.-alpha**2.
        if (delta > 0. and
                same_lattice_type(factory(alpha, numpy.sqrt(delta), gamma),
                                  p1, p2, p3)):
            return True
    return False


def is_monoclinic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a monoclinic lattice

    Also returns True for vectors describing a cubic, hexagonal,
    tetragonal, orthorhombic or base centered orthorhombic lattice

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    cosines = map(cosine_two_vectors,
                  (p1, p2, p3), (p2, p3, p1))

    # base on loose definition: at least 2 angles are 90 degrees
    return (numpy.isclose(cosines, 0.).sum() >= 2 and
            not numpy.isclose(cosines, 1.).any() and
            not numpy.isclose(cosines, -1.).any())


def is_base_centered_monoclinic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a base centered monoclinic
    lattice

    Also returns True for vectors describing a base centered
    orthorhombic lattice or a hexagonal lattice

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    vec_lengths = map(vector_len, (p1, p2, p3))
    cosines = numpy.abs(map(cosine_two_vectors,
                            (p1, p2, p3), (p2, p3, p1)))

    for ivectors in permutations(range(3)):
        alpha, beta, gamma = (vec_lengths[i] for i in ivectors)
        delta2 = 4.*beta**2.-alpha**2.
        if delta2 <= 0.:
            continue

        # cosines are compared directly instead of using
        # `same_lattice_type`.  This is because the latter requires
        # creating a target base centered monoclinic cell
        # and additional cosine and sine operations within the
        # primitive cell factory functions lead to additional numerical
        # errors

        # In order to minimise numerical errors, cosine(special angle)
        # is taken directly from the given vectors
        # There are two possible positions for the special angle
        expected_cosines1 = tuple((alpha/beta/2.,
                                   alpha*cosines[ivectors[-1]]/beta/2.,
                                   cosines[ivectors[-1]]))
        expected_cosines2 = tuple((alpha/beta/2.,
                                   alpha*cosines[ivectors[0]]/beta/2.,
                                   cosines[ivectors[0]]))
        for actual_cosines in permutations(cosines):
            if (numpy.allclose(expected_cosines1, actual_cosines) or
                    numpy.allclose(expected_cosines2, actual_cosines)):
                return True
    return False


def is_triclinic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a triclinic lattice

    Also returns True for vectors describing any other types of Bravais
    lattices

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    edges = tuple(map(vector_len, (p1, p2, p3)))
    factory = PrimitiveCell.for_triclinic_lattice

    alpha, beta, gamma = (numpy.arccos(cosine_two_vectors(p2, p3)),
                          numpy.arccos(cosine_two_vectors(p1, p3)),
                          numpy.arccos(cosine_two_vectors(p1, p2)))
    a1 = alpha % numpy.pi
    a2 = beta % numpy.pi
    a3 = gamma % numpy.pi

    return (numpy.all(numpy.greater((a1+a2, a1+a3, a2+a3), (a3, a2, a1))) and
            same_lattice_type(factory(*(edges+(alpha, beta, gamma))),
                              p1, p2, p3))


def find_lattice_type(p1, p2, p3):
    ''' Return the lattice type as BravaisLattice(IntEnum)
    given a set of primitive vectors

    Parameters
    ----------
    p1, p2, p3 : 3 x float[3]
        primitive vectors

    Returns
    -------
    BravaisLattice(IntEnum)

    Raises
    ------
    TypeError
        if none of the predefined BravaisLattice matches
        the given primitive vectors
    '''
    # Should be ordered from the most specific lattice
    # to the most general ones
    if is_cubic_lattice(p1, p2, p3):
        return BravaisLattice.CUBIC
    elif is_body_centered_cubic_lattice(p1, p2, p3):
        return BravaisLattice.BODY_CENTERED_CUBIC
    elif is_face_centered_cubic_lattice(p1, p2, p3):
        return BravaisLattice.FACE_CENTERED_CUBIC
    elif is_rhombohedral_lattice(p1, p2, p3):
        return BravaisLattice.RHOMBOHEDRAL
    elif is_tetragonal_lattice(p1, p2, p3):
        return BravaisLattice.TETRAGONAL
    elif is_body_centered_tetragonal_lattice(p1, p2, p3):
        return BravaisLattice.BODY_CENTERED_TETRAGONAL
    elif is_hexagonal_lattice(p1, p2, p3):
        return BravaisLattice.HEXAGONAL
    elif is_orthorhombic_lattice(p1, p2, p3):
        return BravaisLattice.ORTHORHOMBIC
    elif is_body_centered_orthorhombic_lattice(p1, p2, p3):
        return BravaisLattice.BODY_CENTERED_ORTHORHOMBIC
    elif is_face_centered_orthorhombic_lattice(p1, p2, p3):
        return BravaisLattice.FACE_CENTERED_ORTHORHOMBIC
    elif is_base_centered_orthorhombic_lattice(p1, p2, p3):
        return BravaisLattice.BASE_CENTERED_ORTHORHOMBIC
    elif is_monoclinic_lattice(p1, p2, p3):
        return BravaisLattice.MONOCLINIC
    elif is_base_centered_monoclinic_lattice(p1, p2, p3):
        return BravaisLattice.BASE_CENTERED_MONOCLINIC
    elif is_triclinic_lattice(p1, p2, p3):
        return BravaisLattice.TRICLINIC
    else:
        message = ("None of the predefined Bravais Lattices matches the "
                   "given primitive vectors")
        raise TypeError(message)


def is_bravais_lattice_consistent(p1, p2, p3, bravais_lattice):
    ''' Test if the bravais lattice is consistent with the
    primitive vectors given

    Parameters
    ----------
    p1, p2, p3 : array_like
        Primitive vectors
    bravais_lattice : BravaisLattice(IntEnum)

    Returns
    -------
    consistent : bool
        True if the bravais lattice is consistent with the
        primitive vectors given

    Raises
    ------
    TypeError
        if bravais_lattice is not a member of BravaisLattice


    See Also
    --------
    is_cubic_lattice, is_body_centered_cubic_lattice,
    is_face_centered_cubic_lattice, is_rhombohedral_lattice,
    is_tetragonal_lattice, is_body_centered_tetragonal_lattice,
    is_hexagonal_lattice, is_orthorhombic_lattice,
    is_body_centered_orthorhombic_lattice,
    is_face_centered_orthorhombic_lattice,
    is_base_centered_orthorhombic_lattice,
    is_monoclinic_lattice, is_base_centered_monoclinic_lattice,
    is_triclinic_lattice
    '''
    check_functions = {
        BravaisLattice.CUBIC: is_cubic_lattice,
        BravaisLattice.BODY_CENTERED_CUBIC: is_body_centered_cubic_lattice,
        BravaisLattice.FACE_CENTERED_CUBIC: is_face_centered_cubic_lattice,
        BravaisLattice.RHOMBOHEDRAL: is_rhombohedral_lattice,
        BravaisLattice.TETRAGONAL: is_tetragonal_lattice,
        BravaisLattice.BODY_CENTERED_TETRAGONAL:
            is_body_centered_tetragonal_lattice,
        BravaisLattice.HEXAGONAL: is_hexagonal_lattice,
        BravaisLattice.ORTHORHOMBIC: is_orthorhombic_lattice,
        BravaisLattice.BODY_CENTERED_ORTHORHOMBIC:
            is_body_centered_orthorhombic_lattice,
        BravaisLattice.FACE_CENTERED_ORTHORHOMBIC:
            is_face_centered_orthorhombic_lattice,
        BravaisLattice.BASE_CENTERED_ORTHORHOMBIC:
            is_base_centered_orthorhombic_lattice,
        BravaisLattice.MONOCLINIC: is_monoclinic_lattice,
        BravaisLattice.BASE_CENTERED_MONOCLINIC:
            is_base_centered_monoclinic_lattice,
        BravaisLattice.TRICLINIC: is_triclinic_lattice}

    return check_functions[bravais_lattice](p1, p2, p3)
