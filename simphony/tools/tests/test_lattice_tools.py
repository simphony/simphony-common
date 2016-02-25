import unittest
from collections import defaultdict

import numpy
from hypothesis import given, settings
from hypothesis.strategies import floats, tuples, composite
from hypothesis.strategies import fixed_dictionaries

from simphony.cuds.primitive_cell import BravaisLattice, PrimitiveCell
from simphony.tools import lattice_tools


def rotate_vectors(vectors, angle1=numpy.pi/2., angle2=0.):
    ''' Rotate the given primitive cell for ``angle1`` about z
    and then for ``angle2`` about x

    Parameters
    ----------
    vectors: tuple of float[3]
        set of vectors to be rotated, each of length 3: (x, y, z)
    angle1, angle2: float
        angles (in radian) for rotating about z and x

    Returns
    -------
    rotated_vectors : tuple of float[3]
        Rotated vectors. length = len(vectors)
    '''
    # rotate x-y for angle1 about z
    xy_rot = numpy.array([[numpy.cos(angle1), numpy.sin(angle1), 0],
                          [numpy.sin(-angle1), numpy.cos(angle1), 0],
                          [0, 0, 1]])
    # rotate y-z for angle2 about x
    yz_rot = numpy.array([[1, 0, 0],
                          [0, numpy.cos(angle2), numpy.sin(angle2)],
                          [0, numpy.sin(-angle2), numpy.cos(angle2)]])
    # rotate x-y, then y-z
    xyz_rot = numpy.inner(xy_rot, yz_rot)

    return tuple((numpy.inner(xyz_rot, vec) for vec in vectors))


def rotate_permute_flip(vectors):
    ''' randomly rotate, permute and flip a set of vectors

    Parameters
    ----------
    vectors: tuple of float[3]
        set of vectors to be rotated, each of length 3: (x, y, z)

    Returns
    -------
    rotated_vectors : tuple of float[3]
        Rotated vectors. length = len(vectors)
    '''
    alpha, beta = numpy.random.uniform(-numpy.pi, numpy.pi, 2)
    # rotating vectors
    vectors = list(rotate_vectors(vectors, alpha, beta))
    # random permutation
    numpy.random.shuffle(vectors)
    # flipping vectors
    p1, p2, p3 = numpy.random.choice((1, -1), (3, 1))*vectors
    return (p1, p2, p3)


def create_points_from_pc(p1, p2, p3, size):
    ''' Create a points array given a set of primitive vectors
    and size

    Parameters
    ----------
    p1, p2, p3: tuple of float[3]
        Primitive vectors
    size: tuple of int[3]
        dimension of the lattice

    Returns
    -------
    points : numpy ndarray (N, 3)
        where N = size[0]*size[1]*size[2]
    '''
    y, z, x = numpy.meshgrid(range(size[1]), range(size[2]), range(size[0]))
    points = numpy.zeros(shape=(x.size, 3), dtype='double')
    for idim in range(3):
        points[:, idim] += p1[idim]*x.ravel() +\
            p2[idim]*y.ravel() +\
            p3[idim]*z.ravel()
    return points


def func_pack_args(func):
    ''' Decorator for packing all arguments to a function
    into an iterable.  Required for hypothesis.strategies.filter'''
    def new_func(args):
        return func(*args)
    return new_func


def get_general_primitive_cell_factories():
    ''' General (loose) definitions of all Bravais Lattice
    primitive cells

    For hypothesis.strategies random generations

    Returns
    -------
    factories: dict
        {BravaisLattice(IntEnum): (PrimitiveCell.<factory_function>,
                                   hypothesis.strategies.tuples)}
    '''

    # Tests for Error raised by PrimitiveCell should be placed separately
    # Edge lengths and angles are assumed to be valid
    edges = floats(min_value=0.1, max_value=1.).filter(lambda x: x == x)
    angles = floats(min_value=0.1,
                    max_value=numpy.pi-0.1).filter(lambda x: x == x)

    def for_rhombohedral(a, alpha):
        ''' general criteria for a rhombohedral lattice '''
        return (numpy.abs(alpha) < (numpy.pi/3.*2.) and
                not numpy.isclose(alpha, numpy.pi/2.))

    def for_triclinic(a, b, c, alpha, beta, gamma):
        ''' general criteria for a triclinic lattice '''
        a1, a2, a3 = numpy.mod((alpha, beta, gamma), numpy.pi)
        cosa, cosb, cosg = numpy.cos((alpha, beta, gamma))
        sinb, sing = numpy.sin((beta, gamma))

        return (numpy.all(numpy.greater((a1+a2, a1+a3, a2+a3),
                                        (a3, a2, a1))) and
                (sinb**2 - ((cosa-cosb*cosg) / sing)**2) > 0. and
                not numpy.isclose((alpha, beta, alpha),
                                  (gamma, gamma, beta)).any())

    # define how primitive cell should be built
    factories = {
        BravaisLattice.CUBIC:
            (PrimitiveCell.for_cubic_lattice, tuples(edges)),
        BravaisLattice.BODY_CENTERED_CUBIC:
            (PrimitiveCell.for_body_centered_cubic_lattice, tuples(edges)),
        BravaisLattice.FACE_CENTERED_CUBIC:
            (PrimitiveCell.for_face_centered_cubic_lattice, tuples(edges)),
        BravaisLattice.RHOMBOHEDRAL:
            (PrimitiveCell.for_rhombohedral_lattice,
             tuples(edges, angles).filter(func_pack_args(for_rhombohedral))),
        BravaisLattice.TETRAGONAL:
            (PrimitiveCell.for_tetragonal_lattice, tuples(edges, edges)),
        BravaisLattice.BODY_CENTERED_TETRAGONAL:
            (PrimitiveCell.for_body_centered_tetragonal_lattice,
             tuples(edges, edges)),
        BravaisLattice.HEXAGONAL:
            (PrimitiveCell.for_hexagonal_lattice, tuples(edges, edges)),
        BravaisLattice.ORTHORHOMBIC:
            (PrimitiveCell.for_orthorhombic_lattice,
             tuples(edges, edges, edges)),
        BravaisLattice.BODY_CENTERED_ORTHORHOMBIC:
            (PrimitiveCell.for_body_centered_orthorhombic_lattice,
             tuples(edges, edges, edges)),
        BravaisLattice.FACE_CENTERED_ORTHORHOMBIC:
            (PrimitiveCell.for_face_centered_orthorhombic_lattice,
             tuples(edges, edges, edges)),
        BravaisLattice.BASE_CENTERED_ORTHORHOMBIC:
            (PrimitiveCell.for_base_centered_orthorhombic_lattice,
             tuples(edges, edges, edges)),
        BravaisLattice.MONOCLINIC:
            (PrimitiveCell.for_monoclinic_lattice,
             tuples(edges, edges, edges, angles)),
        BravaisLattice.BASE_CENTERED_MONOCLINIC:
            (PrimitiveCell.for_base_centered_monoclinic_lattice,
             tuples(edges, edges, edges, angles)),
        BravaisLattice.TRICLINIC:
            (PrimitiveCell.for_triclinic_lattice,
             tuples(edges, edges,
                    edges, angles,
                    angles, angles).filter(func_pack_args(for_triclinic))),
        }
    return factories


def get_specific_primitive_cell_factories():
    ''' Specific (strict) definitions of all Bravais Lattice
    primitive cells. For hypothesis.strategies random generations

    e.g. a tetragonal lattice cell cannot have all edges of the same
    length (otherwise it is a cubic lattice)

    Returns
    -------
    factories: dict
        {BravaisLattice(IntEnum): (PrimitiveCell.<factory_function>,
                                   hypothesis.strategies.tuples)}
    '''
    criteria = {}

    criteria[BravaisLattice.TETRAGONAL] = lambda a, c: not numpy.isclose(a, c)

    criteria[BravaisLattice.BODY_CENTERED_TETRAGONAL] = (
        lambda a, c: not numpy.isclose(a, c))

    criteria[BravaisLattice.ORTHORHOMBIC] = (
        lambda a, b, c: not numpy.isclose((a, b, c), (b, c, a)).any())

    criteria[BravaisLattice.BODY_CENTERED_ORTHORHOMBIC] = (
        criteria[BravaisLattice.ORTHORHOMBIC])

    criteria[BravaisLattice.FACE_CENTERED_ORTHORHOMBIC] = (
        criteria[BravaisLattice.ORTHORHOMBIC])

    criteria[BravaisLattice.BASE_CENTERED_ORTHORHOMBIC] = (
        lambda a, b, c: not numpy.isclose(3.*a**2., b**2.))

    criteria[BravaisLattice.MONOCLINIC] = (
        lambda a, b, c, alpha: (not numpy.isclose(alpha, numpy.pi/2.) and
                                not numpy.isclose(a, c) and
                                not (numpy.isclose(alpha, numpy.pi/3.) and
                                     numpy.isclose((a, b, c),
                                                   (b, c, a)).any())))

    criteria[BravaisLattice.BASE_CENTERED_MONOCLINIC] = (
        criteria[BravaisLattice.MONOCLINIC])

    factories = get_general_primitive_cell_factories()

    # Apply filters to the arguments of factories
    for bravais_lattice, filter_func in criteria.items():
        factory, elements = factories[bravais_lattice]
        elements = elements.filter(func_pack_args(filter_func))
        factories[bravais_lattice] = (factory, elements)

    return factories


def builder(factories, bravais_lattices=BravaisLattice):
    '''
    Return a hypothesis.strategies.fixed_dictionaries containing
    lattice primitive cells

    Parameters
    ----------
    factories: dict
        {BravaisLattice(IntEnum): (PrimitiveCell.<factory_function>,
                                   hypothesis.strategies.tuples)}
    bravais_lattices: iterable
        iterable of BravaisLattice(IntEnum) for selecting a subset of
        BravaisLattice.  Default: all BravaisLattice

    Returns
    -------
    lattice: fixed_dictionary
        {BravaisLattice(IntEnum): PrimitiveCell}
    '''

    @composite
    def builds_unpack(draw, factory, elements):
        ''' Similar to hypothesis.strategies.builds except
        it unpacks the arguments '''
        args = elements.example()
        return factory(*args)

    lattices = {}
    for bravais_lattice in bravais_lattices:
        factory, elements = factories[bravais_lattice]
        lattices[bravais_lattice] = builds_unpack(factory, elements)

    return fixed_dictionaries(lattices)


# A list of general lattices and their special cases
# e.g. cubic and face-centered-cubic are special cases
# of the rhombohedral lattice
specific_map2_general = defaultdict(
    tuple, {
        BravaisLattice.CUBIC: (
            BravaisLattice.RHOMBOHEDRAL,
            BravaisLattice.TETRAGONAL,
            BravaisLattice.ORTHORHOMBIC,
            BravaisLattice.BASE_CENTERED_ORTHORHOMBIC,
            BravaisLattice.MONOCLINIC,
            BravaisLattice.TRICLINIC),
        BravaisLattice.FACE_CENTERED_CUBIC: (
            BravaisLattice.RHOMBOHEDRAL,
            BravaisLattice.FACE_CENTERED_ORTHORHOMBIC,
            BravaisLattice.TRICLINIC),
        BravaisLattice.BODY_CENTERED_CUBIC: (
            BravaisLattice.BODY_CENTERED_TETRAGONAL,
            BravaisLattice.BODY_CENTERED_ORTHORHOMBIC,
            BravaisLattice.TRICLINIC),
        BravaisLattice.TETRAGONAL: (
            BravaisLattice.ORTHORHOMBIC,
            BravaisLattice.BASE_CENTERED_ORTHORHOMBIC,
            BravaisLattice.MONOCLINIC,
            BravaisLattice.TRICLINIC),
        BravaisLattice.HEXAGONAL: (
            BravaisLattice.BASE_CENTERED_ORTHORHOMBIC,
            BravaisLattice.MONOCLINIC,
            BravaisLattice.BASE_CENTERED_MONOCLINIC,
            BravaisLattice.TRICLINIC),
        BravaisLattice.ORTHORHOMBIC: (
            BravaisLattice.MONOCLINIC,
            BravaisLattice.TRICLINIC),
        BravaisLattice.BODY_CENTERED_TETRAGONAL: (
            BravaisLattice.BODY_CENTERED_ORTHORHOMBIC,
            BravaisLattice.TRICLINIC),
        BravaisLattice.BASE_CENTERED_ORTHORHOMBIC: (
            BravaisLattice.MONOCLINIC,
            BravaisLattice.BASE_CENTERED_MONOCLINIC,
            BravaisLattice.TRICLINIC)})


# 1. The health check for "taking too long to generate samples"
# should be skipped:
#      The collection of primitive cell samples take too long to generate.
#      However skipping some of the samples make the tests less robust
# 2. The health check for using other random modules *can* be skipped:
#      `numpy.random` module is used for randomly rotating primitive
#      vectors for testing functions that are spatial invariant.
#      Although it is desirable for failed tests to be reproducible,
#      the many `hypothesis.random` instances make the code complicated.
#      In this case, readability outweighs reproducibility.  If the test
#      fails on a particular set of random values but passes on the next,
#      we will get a Flaky error and that is still good.

# Right now, we can't choose which health checks to skip
# The following skips all of them (4)
settings.perform_health_check = False


class TestLatticeTools(unittest.TestCase):

    @staticmethod
    def _get_primitive_vectors(primitive_cell):
        return map(numpy.array,
                   (primitive_cell.p1, primitive_cell.p2, primitive_cell.p3))

    @given(builder(get_specific_primitive_cell_factories()))
    def test_find_lattice_type_specific(self, lattices):
        ''' Test getting the most specific lattice type correctly'''
        for expected, primitive_cell in lattices.items():
            # given
            aligned_vectors = self._get_primitive_vectors(primitive_cell)
            p1, p2, p3 = rotate_permute_flip(aligned_vectors)

            # when
            actual = lattice_tools.find_lattice_type(p1, p2, p3, 1.e-8)

            # then
            self.assertEqual(actual, expected)

    @given(builder(get_specific_primitive_cell_factories(),
                   specific_map2_general.keys()))
    def test_subtype_of_general_lattices(self, lattices):
        ''' Test if more symmetric lattices are part of more general lattices
        '''
        for specific, primitive_cell in lattices.items():
            # given
            aligned_vectors = self._get_primitive_vectors(primitive_cell)
            p1, p2, p3 = rotate_permute_flip(aligned_vectors)

            # then
            msg = "Expected {!r} to be a symmetric case of {!r}. False."
            for general in specific_map2_general[specific]:
                self.assertTrue(
                    lattice_tools.is_bravais_lattice_consistent(p1, p2, p3,
                                                                general),
                    msg.format(specific, general))

    def test_incompatible_lattice_type(self):
        ''' Test if some specific lattices are incompatible with some others

        e.g. a strict BravaisLattice.TRICLINIC lattice
        cannot be considered as any other lattice of higher symmetry
        All other lattices are triclinic in its loose definition
        '''
        lattices = builder(get_specific_primitive_cell_factories()).example()

        for bravais_lattice, primitive_cell in lattices.items():
            # given
            aligned_vectors = self._get_primitive_vectors(primitive_cell)
            p1, p2, p3 = rotate_permute_flip(aligned_vectors)

            # when
            exclusives = (set(BravaisLattice) -
                          set(specific_map2_general[bravais_lattice]) -
                          set([bravais_lattice, BravaisLattice.TRICLINIC]))

            # then
            # bravais_lattice cannot be compatible with lattice
            # types in `exclusive`
            msg = "Expected {!r} not be considered as {!r}"
            for exclusive in exclusives:
                self.assertFalse(
                    lattice_tools.is_bravais_lattice_consistent(p1, p2, p3,
                                                                exclusive),
                    msg.format(bravais_lattice, exclusive))

    def test_alternative_primitive_cell_settings(self):
        '''Test against alternative primitive cells not in PrimitiveCell'''

        ######################
        # body-centered cubic
        ######################
        bcc_vectors = ((1., 1., -1.), (1., -1., 1.), (-1., 1., 1.))
        p1, p2, p3 = rotate_permute_flip(bcc_vectors)
        self.assertEqual(lattice_tools.find_lattice_type(p1, p2, p3),
                         BravaisLattice.BODY_CENTERED_CUBIC)

        ###########################
        # body-centered tetragonal
        ###########################
        bc_tetra_vectors = ((1., 1., -2.), (1., -1., 2.), (-1., 1., 2.))
        p1, p2, p3 = rotate_permute_flip(bc_tetra_vectors)
        self.assertEqual(lattice_tools.find_lattice_type(p1, p2, p3),
                         BravaisLattice.BODY_CENTERED_TETRAGONAL)

        #############################
        # body-centered orthorhombic
        #############################
        bc_orthor_vectors = ((1., 3., -2.), (1., -3., 2.), (-1., 3., 2.))
        p1, p2, p3 = rotate_permute_flip(bc_orthor_vectors)
        self.assertEqual(lattice_tools.find_lattice_type(p1, p2, p3),
                         BravaisLattice.BODY_CENTERED_ORTHORHOMBIC)

        ##############################
        # base-centered orthorhombic
        ##############################
        base_orthor_vectors = ((1., 2., 0.), (-1., 2., 0.), (0., 0., 3.))
        p1, p2, p3 = rotate_permute_flip(base_orthor_vectors)
        self.assertEqual(lattice_tools.find_lattice_type(p1, p2, p3),
                         BravaisLattice.BASE_CENTERED_ORTHORHOMBIC)

    def test_exception_no_matching_lattice_too_strict_tolerance(self):
        # given
        p1 = numpy.array([0.5+1.e-4, 0.5, 0.])
        p2 = numpy.array([0., 0.5, 0.5])
        p3 = numpy.array([0.5, 0., 0.5])

        # then
        with self.assertRaises(TypeError):
            lattice_tools.find_lattice_type(p1, p2, p3, tolerance=1.e-20)

    def test_exception_for_vectors_with_nan(self):
        # given
        p1, p2, p3 = ((numpy.nan, 0., 0.),)*3

        # then
        for bravais_lattice in BravaisLattice:
            with self.assertRaises(ValueError):
                lattice_tools.is_bravais_lattice_consistent(p1, p2, p3,
                                                            bravais_lattice)

    def test_exception_for_vectors_with_inf(self):
        # given
        p1, p2, p3 = ((numpy.inf, 0., 0.),)*3

        # then
        for bravais_lattice in BravaisLattice:
            with self.assertRaises(ValueError):
                lattice_tools.is_bravais_lattice_consistent(p1, p2, p3,
                                                            bravais_lattice)

    def test_exception_zero_length_vectors(self):
        # given
        p1, p2, p3 = (0., 1., 0.), (0., 0., 0.), (1., 0., 0.)

        # then
        for bravais_lattice in BravaisLattice:
            with self.assertRaises(ValueError):
                lattice_tools.is_bravais_lattice_consistent(p1, p2, p3,
                                                            bravais_lattice)

    @given(builder(get_specific_primitive_cell_factories()))
    def test_guess_primitive_vectors(self, lattices):
        for primitive_cell in lattices.values():
            # given
            aligned_vectors = self._get_primitive_vectors(primitive_cell)
            p1, p2, p3 = rotate_permute_flip(aligned_vectors)

            # when
            points = create_points_from_pc(p1, p2, p3, (4, 5, 3))

            # then
            actual = lattice_tools.guess_primitive_vectors(points)
            numpy.testing.assert_allclose(actual, (p1, p2, p3))

    def test_guess_primitive_vectors_special_case(self):
        # given
        p1, p2, p3 = (0., 0., 1.), (0., 2., 0.), (1., 0., 0.)

        # when
        points = create_points_from_pc(p1, p2, p3, (4, 5, 3))

        # then
        actual = lattice_tools.guess_primitive_vectors(points)
        numpy.testing.assert_allclose(actual, (p1, p2, p3))

    def test_exception_guess_vectors_with_unsorted_points(self):
        # given
        primitive_cell = PrimitiveCell.for_rhombohedral_lattice(0.1, 0.7)

        # when
        p1, p2, p3 = self._get_primitive_vectors(primitive_cell)
        points = create_points_from_pc(p1, p2, p3, (4, 5, 3))
        numpy.random.shuffle(points)

        # then
        with self.assertRaises(ValueError):
            lattice_tools.guess_primitive_vectors(points)

    def test_exception_guess_vectors_with_no_first_jump(self):
        # given
        points = numpy.zeros((20, 3))

        # then
        with self.assertRaises(ValueError):
            lattice_tools.guess_primitive_vectors(points)

    def test_exception_guess_vectors_with_no_second_jump(self):
        # given
        points = numpy.zeros((20, 3))
        points[1, 0] = 2

        # then
        with self.assertRaises(ValueError):
            lattice_tools.guess_primitive_vectors(points)

    def test_exception_guess_vectors_with_wrong_shape_points(self):
        # given
        points = numpy.zeros((10, 2))

        # then
        with self.assertRaises(ValueError):
            lattice_tools.guess_primitive_vectors(points)

    @given(builder(get_specific_primitive_cell_factories(),
                   {BravaisLattice.CUBIC, BravaisLattice.BODY_CENTERED_CUBIC,
                    BravaisLattice.FACE_CENTERED_CUBIC,
                    BravaisLattice.RHOMBOHEDRAL, BravaisLattice.HEXAGONAL}))
    def test_changing_tolerance_lattice_type(self, lattices):
        for lattice_type, primitive_cell in lattices.items():
            # double precision (numpy.float64)
            p1, p2, p3 = self._get_primitive_vectors(primitive_cell)

            # given perturbation
            p1[0] += 1.e-4

            # when
            tolerance = 1.e-6

            # then
            actual = lattice_tools.is_bravais_lattice_consistent(p1, p2, p3,
                                                                 lattice_type,
                                                                 tolerance)
            self.assertFalse(actual)

            # when
            tolerance = 1.e-3

            # then
            actual = lattice_tools.is_bravais_lattice_consistent(p1, p2, p3,
                                                                 lattice_type,
                                                                 tolerance)
            self.assertTrue(actual)

    def test_changing_tolerance_guess_primitive_vectors(self):
        # given
        p1 = numpy.array([1.5, 0., 0.])
        p2 = numpy.array([0., 0.5, 0.5])
        p3 = numpy.array([0.5, 0., 0.5])
        points = create_points_from_pc(p1, p2, p3, (4, 5, 3))
        npoints = points.shape[0]

        # when
        # add some defects
        ndeflects = npoints/2
        indices = numpy.random.choice(xrange(npoints), ndeflects, False)
        points[indices] += numpy.random.rand(ndeflects, 3)*1.e-4
        tolerance = 1.e-6

        # then
        with self.assertRaises(ValueError):
            lattice_tools.guess_primitive_vectors(points, tolerance)

        # when
        tolerance = 1.e-3

        # then
        actual = lattice_tools.guess_primitive_vectors(points, tolerance)
        numpy.testing.assert_allclose(actual, (p1, p2, p3),
                                      atol=tolerance)
