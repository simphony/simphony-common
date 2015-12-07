from simphony.cuds.material import Material


class Materials(object):
    """A class that contains materials.

    Class manages the materials.

    """
    def __init__(self):
        self._materials = {}

    def add_material(self, material):
        """Add a material

        Parameters
        ----------
        material : Material
            the material to be added.

        Raises
        ------
        ValueError:
            If a material with the same uid already exists

        """
        try:
            self._materials[material.uid] = Material.from_material(material)
        except KeyError:
            raise ValueError

    def remove_material(self, uid):
        """ Remove a material

        Parameters
        ----------
        uid: uuid.UUID
            the id of the material to be deleted

        Raises
        ------
        KeyError:
            If there is no material with the given uid

        """
        del self._materials[uid]

    def update_material(self, material):
        """ Update a material

        Parameters
        ----------
        material : Material
            the material to be updated.

        Raises
        ------
        ValueError:
            If a material with this uid does not exist

        """
        self._materials[material.uid] = Material.from_material(material)

    def get_material(self, uid):
        """ Get the material

        Parameters
        ----------
        uid: uuid.UUID
            the id of the material to be retrieved.

        Returns
        -------
        material

        Raises
        ------
        KeyError:
            If there is no material with the given uid

        """
        return Material.from_material(self._materials[uid])

    def iter_materials(self, uids=None):
        """ Returns an iterator over a subset or all of the materials.

        Parameters
        ----------
        uids : sequence of uids, optional
            uids of specific material to be iterated over. If uids is not
            given, then all materials will be iterated over.

        """
        if uids is None:
            for material in self._materials.itervalues():
                yield material
        else:
            for uid in uids:
                yield self.get_material(uid)
