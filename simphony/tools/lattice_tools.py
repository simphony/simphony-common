from itertools import permutations, combinations, product

import numpy
from simphony.cuds.primitive_cell import BravaisLattice


TOLERANCE = 1.e-6


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


def same_primitive_cell_config(v1, v2, v3, p1, p2, p3, permute=True):
    ''' Return True if a set of primitive vectors ``p1``, ``p2``,
    ``p3`` describe a primitive cell that is geometrically similar to
    the target primitive cell ``(v1, v2, v3)``.

    This function works by comparing length ratios and cosines
    of the angles between vectors.  Single precision applies
    by default, or change ``lattice_tools.TOLERANCE``

    Parameters
    ----------
    v1, v2, v3 : array_like (len=3)
        Target primitive vectors
    p1, p2, p3 : array_like (len=3)
        Primitive vectors
    permute: boolean
        whether p1, p2, p3 are permutated

    Returns
    -------
    match : bool
    '''
    targets = (v1, v2, v3)

    # cosine angles between pairs of the target primitive vectors
    target_cosines = numpy.abs([cosine_two_vectors(vec1, vec2)
                                for vec1, vec2 in combinations(targets, 2)])

    # length ratios between pairs of the target primitive vectors
    target_ratios = numpy.array([vector_len(vec1)/vector_len(vec2)
                                 for vec1, vec2 in combinations(targets, 2)])

    if permute:
        vectors_iter = permutations((p1, p2, p3))
    else:
        vectors_iter = ((p1, p2, p3),)

    # the cosines and ratios of the vectors p1, p2, p3
    # are permuted while being compared against the target
    for vectors in vectors_iter:
        cosines = numpy.abs([cosine_two_vectors(vec1, vec2)
                             for vec1, vec2 in combinations(vectors, 2)])
        ratios = numpy.array([vector_len(vec1)/vector_len(vec2)
                              for vec1, vec2 in combinations(vectors, 2)])
        if ((numpy.abs(cosines-target_cosines) <= TOLERANCE).all() and
                (numpy.abs(ratios-target_ratios) <= TOLERANCE).all()):
            return True
    return False


def guess_primitive_vectors(points):
    ''' Guess the primitive vectors underlying a given array of
    lattice points (N, 3).

    Parameter
    ----------
    points : numpy ndarray (N, 3)
        A flattened array of the coordinates of the N(=n1*n2*n3)
        lattice nodes, where (n1, n2, n3) is the lattice size.
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
        return numpy.where(numpy.abs(sec_dev) > TOLERANCE)[0][0]+2

    # find where the x increments are discontinuous
    # keep the smallest value
    nx = points.shape[0]
    for idim in range(3):
        try:
            size = find_jump(points[:, idim])
        except IndexError:
            continue
        if size < nx:
            nx = size

    # find where the y increments are discontinuous
    # keep the smallest value
    ny = points.shape[0]
    for idim in range(3):
        try:
            size = find_jump(points[::nx, idim])
        except IndexError:
            continue
        if size < ny:
            ny = size

    nz = points.shape[0] // nx // ny
    if nx*ny*nz != points.shape[0]:
        message = "Failed to deduce the lattice dimensions"
        raise IndexError(message)

    # Test if the lattice points are ordered as expected
    # Does not test all points, otherwise slow for large data
    x_not_ordered = (numpy.abs(numpy.diff(points[:nx, 0],
                                          n=2)) > TOLERANCE).any()
    y_not_ordered = (numpy.abs(numpy.diff(points[::nx, 1][:ny],
                                          n=2)) > TOLERANCE).any()
    z_not_ordered = (numpy.abs(numpy.diff(points[::nx*ny, 2],
                                          n=2)) > TOLERANCE).any()
    if x_not_ordered or y_not_ordered or z_not_ordered:
        message = ("Deduction of the primitive vectors requires the "
                   "lattice nodes to be ordered in a C-contiguous fashion.")
        raise IndexError(message)

    # Primitive vectors
    return tuple((points[ipoint, 0]-points[0, 0],
                  points[ipoint, 1]-points[0, 1],
                  points[ipoint, 2]-points[0, 2]) for ipoint in (1, nx, nx*ny))


def is_cubic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a cubic lattice

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

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
    if numpy.abs(a-b) > TOLERANCE or numpy.abs(c-a) > TOLERANCE:
        return False

    # all angles close to 90 degree
    cosines = map(cosine_two_vectors, (p1, p2, p3), (p2, p3, p1))
    return (numpy.abs(cosines) <= TOLERANCE).all()


def is_body_centered_cubic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a body centered cubic lattice

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # two possible primitive cells for BCC
    # type 1: p1=(a, 0, 0), p2=(0, a, 0), p3=(a/2, a/2, a/2)
    # type 2: p1=0.5a(1, 1, -1), p2=0.5a(1, -1, 1), p3=0.5a(-1, 1, 1)

    # need the lengths of vectors and counts of pairs of equal lengths
    a, b, c = map(vector_len, (p1, p2, p3))
    equal_lengths = numpy.abs((a-b, b-c, c-a)) <= TOLERANCE

    # need the number of right angles
    dot_products = numpy.abs(map(numpy.dot, (p1, p2, p3), (p2, p3, p1)))
    right_angles = dot_products < TOLERANCE
    one_right_angle = numpy.count_nonzero(right_angles) == 1

    if sum(equal_lengths) == 1 and one_right_angle:
        # type 1
        # i) the ratio of |p3|/|p1| should be sqrt(3)/2
        # ii) the pair of perpendicular vectors have same length
        len_ratio = {0: c/a, 1: a/b, 2: b/a}
        i_pair = numpy.where(equal_lengths)[0][0]
        return (i_pair == numpy.where(right_angles)[0][0] and
                numpy.abs(len_ratio[i_pair]-numpy.sqrt(3.)/2.) < TOLERANCE)
    elif all(equal_lengths) and not one_right_angle:
        # type 2
        # all dot products == (|p1|**2.)/3
        return (numpy.abs(dot_products*3. - a*a) <= TOLERANCE).all()
    else:
        return False


def is_face_centered_cubic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a face centered cubic lattice

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

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
    if numpy.abs(a-c) > TOLERANCE or numpy.abs(b-c) > TOLERANCE:
        return False

    # all angles close to 60 degree
    cosines = numpy.abs(map(cosine_two_vectors,
                            (p1, p2, p3), (p2, p3, p1)))
    return (numpy.abs(cosines - 0.5) <= TOLERANCE).all()


def is_rhombohedral_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a rhombohedral lattice

    Also returns True for vectors describing a cubic or face centered
    cubic lattice

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

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
    if numpy.abs(a-c) > TOLERANCE or numpy.abs(b-c) > TOLERANCE:
        return False

    # all angles close to each other
    cosa, cosb, cosc = numpy.abs(map(cosine_two_vectors,
                                     (p1, p2, p3), (p2, p3, p1)))
    return (numpy.abs((cosa-cosc, cosb-cosc)) <= TOLERANCE).all()


def is_tetragonal_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a tetragonal lattice

    Also returns True for vectors describing a cubic lattice

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # at least two sides of equal lengths
    lenA, lenB, lenC = map(vector_len, (p1, p2, p3))
    equal_lengths = numpy.abs((lenA-lenB, lenB-lenC, lenC-lenA)) <= TOLERANCE

    if not equal_lengths.any():
        return False

    # all angles close to 90 degrees
    cosines = numpy.abs(map(cosine_two_vectors, (p1, p2, p3), (p2, p3, p1)))
    return (cosines <= TOLERANCE).all()


def is_body_centered_tetragonal_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a body centered tetragonal
    lattice

    Also returns True for vectors describing a body centered cubic
    lattice

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # two type of primitive cells
    # type 1: p1=(a, 0, 0), p2=(0, a, 0), p3=(a/2, a/2, c/2)
    # type 2: p1=0.5(a, a, -c), p2=0.5(a, -a, c), p3=0.5(-a, a, c)

    # lengths of the vectors
    lenA, lenB, lenC = map(vector_len, (p1, p2, p3))
    all_length_equal = (numpy.abs(lenA-lenB) <= TOLERANCE and
                        numpy.abs(lenB-lenC) <= TOLERANCE)

    # dot products of vectors
    # want to know which pair of dot products are equal
    # and the number of right angles
    dot_products = numpy.abs(map(numpy.dot, (p1, p2, p3), (p2, p3, p1)))
    dot_products_diff = numpy.abs(dot_products-dot_products[[1, 2, 0]])
    equal_dot_products = dot_products_diff <= TOLERANCE
    right_angles = dot_products < TOLERANCE
    one_right_angle = numpy.count_nonzero(right_angles) == 1

    if right_angles.all():
        return False

    elif one_right_angle:
        # type 1
        # find the only pair of vectors that make a right angle
        # mapping for the conventional sides (a, b, c)
        mapping = {0: (lenB, lenA, lenC),
                   1: (lenB, lenC, lenA),
                   2: (lenA, lenC, lenB)}
        a, b, c = mapping[numpy.where(right_angles)[0][0]]

        # the rest of the dot products should match 0.5a**2 and 0.5b**2
        expected = numpy.array((0.5*a*a, 0.5*b*b))
        dot_products = dot_products[~right_angles]
        angle_match = (numpy.abs(dot_products-expected) < TOLERANCE).all()

        edge_match = (numpy.abs(a-b) < TOLERANCE or
                      numpy.abs(c*c-(0.5*b*b + a*a/4.)) < TOLERANCE or
                      numpy.abs(c*c-(0.5*a*a + b*b/4.)) < TOLERANCE)
        return angle_match and edge_match

    elif all_length_equal and equal_dot_products.all():
        # type 2
        # the length of vector should be 3 times of the dot product
        return numpy.abs(dot_products[0]*3.-lenA*lenA) <= TOLERANCE

    elif all_length_equal and equal_dot_products.any():
        # type 2
        # deduce sides a and c for type 2 cell
        # at least two of the dot products are equal
        # they should equal c**2.
        c_square = dot_products[numpy.where(equal_dot_products)[0][0]]
        a_square = (lenA*lenA-c_square)/2.

        if a_square < TOLERANCE or c_square < TOLERANCE:
            # lengths are invalid
            return False
        else:
            # equal_dot_products is computed from comparing
            # (dot_products[0], dot_products[1])
            # (dot_products[1], dot_products[2])
            # (dot_products[2], dot_products[0])
            # find the dot product that is the odd one out
            mapping = {0: dot_products[2], 1: dot_products[0],
                       2: dot_products[1]}
            other_dot_product = mapping[numpy.where(equal_dot_products)[0][0]]
            expected = numpy.abs(c_square - 2.*a_square)
            return numpy.abs(other_dot_product-expected) < TOLERANCE
    else:
        return False


def is_hexagonal_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a hexagonal lattice

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # at least two sides of equal lengths
    lenA, lenB, lenC = map(vector_len, (p1, p2, p3))
    equal_lengths = numpy.abs((lenA-lenB, lenB-lenC, lenC-lenA)) <= TOLERANCE

    dot_products = numpy.abs(map(numpy.dot, (p1, p2, p3), (p2, p3, p1)))
    right_angles = dot_products <= TOLERANCE

    if not right_angles.sum() == 2 or not equal_lengths.any():
        return False
    else:
        # find the pair of vectors that should make 60 degrees
        # check that their lengths are equal
        mapping = {0: (lenA, lenB), 1: (lenB, lenC), 2: (lenC, lenA)}
        i_not_right_angle = numpy.where(~right_angles)[0][0]
        a, b = mapping[i_not_right_angle]
        cosine = dot_products[i_not_right_angle]/a/b
        return (numpy.abs(a-b) <= TOLERANCE and
                numpy.abs(cosine-0.5) <= TOLERANCE)


def is_orthorhombic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe an orthorhombic lattice

    Also returns True for vectors describing a cubic or tetragonal
    lattice

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # all angles close to 90 degrees
    cosines = numpy.abs(map(cosine_two_vectors,
                            (p1, p2, p3), (p2, p3, p1)))
    return (cosines <= TOLERANCE).all()


def is_body_centered_orthorhombic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a body centered orthorhombic
    lattice

    Also returns True for vectors describing a body centered cubic or
    a body centered tetragonal lattice

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # dot products of vectors
    dot_products = numpy.abs(map(numpy.dot, (p1, p2, p3), (p2, p3, p1)))
    right_angles = dot_products <= TOLERANCE
    one_right_angle = right_angles.sum() == 1

    # lengths of the vectors
    lenA, lenB, lenC = map(vector_len, (p1, p2, p3))
    all_length_equal = (numpy.abs(lenA-lenC) < TOLERANCE and
                        numpy.abs(lenB-lenC) < TOLERANCE)
    if one_right_angle:
        # type 1: as given by the PrimitiveCell class method
        # p1: (a, 0, 0), p2: (0, b, 0), p3: (a/2, b/2, c/2)
        # mapping for the lengths of vectors that make right angle
        # the nonzero dot products are a**2./2 and b**2./2 respectively
        nonzero_dot = dot_products[~right_angles]

        # find a and b
        mapping = {0: (lenA, lenB), 1: (lenB, lenC), 2: (lenC, lenA)}
        lengths = numpy.array(mapping[numpy.where(right_angles)[0][0]])
        expected = 0.5*lengths**2.
        return ((numpy.abs(nonzero_dot-expected) <= TOLERANCE).all() or
                (numpy.abs(nonzero_dot[::-1]-expected) <= TOLERANCE).all())
    elif all_length_equal and not one_right_angle:
        # type 2
        # p1: 0.5(a, b, -c), p2: 0.5(a, -b, c), p3: 0.5(-a, b, c)
        # p1, p2, p3 may be flipped and there exists a choice of signs
        # where
        #    p1.p2 + p2.p3 + p1.p3 == |p1|**2. == |p2|**2. == |p3|**2.
        for signs in product(*((1, -1),)*3):
            if numpy.abs((dot_products*signs).sum() + lenA*lenA) <= TOLERANCE:
                return True
        return False
    else:
        return False


def is_face_centered_orthorhombic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a face centered orthorhombic
    lattice

    Also returns True for vectors describing a face centered cubic
    lattice

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    alpha2, beta2, gamma2 = map(numpy.dot, (p1, p2, p3), (p1, p2, p3))
    a2 = 2.*(gamma2+beta2-alpha2)
    b2 = 2.*(alpha2+gamma2-beta2)
    c2 = 2.*(alpha2+beta2-gamma2)

    if a2 <= 0 or b2 <= 0 or c2 <= 0:
        return False

    # expected squared lengths of vectors
    expected_len2 = 0.25*numpy.array((b2+c2, a2+c2, a2+b2))
    lengths_square = (alpha2, beta2, gamma2)
    if not (numpy.abs(lengths_square-expected_len2) <= TOLERANCE).all():
        return False

    # expected dot products
    expected_dot_prod = numpy.array((c2/4., a2/4., b2/4.))
    dot_products = numpy.abs(map(numpy.dot, (p1, p2, p3), (p2, p3, p1)))
    return (numpy.abs(dot_products-expected_dot_prod) <= TOLERANCE).all()


def is_base_centered_orthorhombic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a base centered orthorhombic
    lattice

    Also returns True for vectors describing a cubic, tetragonal,
    or hexagonal lattice

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    # there are two types of primitive cells
    # type 1: (a, 0, 0), (a/2, b/2, 0), (0, 0, c)
    # type 2: (a/2, -b/2, 0), (a/2, b/2, 0), (0, 0, c)

    dot_products = numpy.abs(map(numpy.dot, (p1, p2, p3), (p2, p3, p1)))
    right_angles = dot_products <= TOLERANCE
    if right_angles.sum() < 2:
        return False

    lenA, lenB, lenC = map(vector_len, (p1, p2, p3))
    equal_lengths = numpy.abs((lenA-lenB, lenB-lenC, lenC-lenA)) <= TOLERANCE

    if equal_lengths.any() and right_angles.all():
        return True
    elif equal_lengths.any():
        # find the pair of vectors that don't make a right angle
        # if it is the type 2 cell, they should be equal length
        if equal_lengths[numpy.where(~right_angles)[0][0]]:
            return True

    # not type 2 cell, try type 1
    if not right_angles.all():
        # find the two vectors that don't make right angles with the others
        # the projection of one vector is half the another vector
        not_right_angle = numpy.where(~right_angles)[0][0]
        dot_product = dot_products[not_right_angle]
        vec_mapping = {0: (p1, p2), 1: (p2, p3), 2: (p1, p3)}
        v1, v2 = vec_mapping[not_right_angle]
        return (numpy.abs(dot_product - numpy.dot(v1, v1)*0.5) < TOLERANCE or
                numpy.abs(dot_product - numpy.dot(v2, v2)*0.5) < TOLERANCE)
    else:
        return False


def is_monoclinic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a monoclinic lattice

    Also returns True for vectors describing a cubic, hexagonal,
    tetragonal, orthorhombic or base centered orthorhombic lattice

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    cosines = numpy.abs(map(cosine_two_vectors,
                            (p1, p2, p3), (p2, p3, p1)))

    # base on loose definition: at least 2 angles are 90 degrees
    return (cosines <= TOLERANCE).sum() >= 2


def is_base_centered_monoclinic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a base centered monoclinic
    lattice

    Also returns True for vectors describing a base centered
    orthorhombic lattice or a hexagonal lattice

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

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
        expected1 = numpy.array((alpha/beta/2.,
                                 alpha*cosines[ivectors[-1]]/beta/2.,
                                 cosines[ivectors[-1]]))
        expected2 = numpy.array((alpha/beta/2.,
                                 alpha*cosines[ivectors[0]]/beta/2.,
                                 cosines[ivectors[0]]))
        for actual_cosines in permutations(cosines):
            if ((numpy.abs(expected1-actual_cosines) <= TOLERANCE).all() or
                    (numpy.abs(expected2-actual_cosines) <= TOLERANCE).all()):
                return True
    return False


def is_triclinic_lattice(p1, p2, p3):
    ''' Test if primitive vectors describe a triclinic lattice

    Also returns True for vectors describing any other types of Bravais
    lattices

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

    Parameters
    ----------
    p1, p2, p3: array_like
        primitive vectors

    Returns
    -------
    output : bool
    '''
    a, b, c = map(vector_len, (p1, p2, p3))

    alpha, beta, gamma = (numpy.arccos(cosine_two_vectors(p2, p3)),
                          numpy.arccos(cosine_two_vectors(p1, p3)),
                          numpy.arccos(cosine_two_vectors(p1, p2)))
    a1 = alpha % numpy.pi
    a2 = beta % numpy.pi
    a3 = gamma % numpy.pi

    if numpy.all(numpy.greater((a1+a2, a1+a3, a2+a3), (a3, a2, a1))):
        # copied from primitive_cell.py for_triclinic_lattice
        # faster to skip the checking already fulfilled here
        cosa = numpy.cos(alpha)
        cosb = numpy.cos(beta)
        sinb = numpy.sin(beta)
        cosg = numpy.cos(gamma)
        sing = numpy.sin(gamma)
        v1 = (a, 0, 0)
        v2 = (b*cosg, b*sing, 0)
        v3 = (c*cosb, c*(cosa-cosb*cosg) / sing,
              c*numpy.sqrt(sinb**2 - ((cosa-cosb*cosg) / sing)**2))
        return same_primitive_cell_config(v1, v2, v3, p1, p2, p3)
    else:
        return False


def find_lattice_type(p1, p2, p3):
    ''' Return the lattice type as BravaisLattice(IntEnum)
    given a set of primitive vectors

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

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

    Numerical errors are tolerated within ``lattice_tools.TOLERANCE``

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
