"""Base storage mechanism for accessing CUDS entities, mainly datasets.

This module contains the base class for implementing different access
strategies for CUDS,notably MemoryStore and ProxyStore.
"""
import abc


class ABCStateDataStore(object):
    """Abstract base class for all stores.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def add(self, dataset, *args, **kwargs):
        """Add the dataset to the store."""

    @abc.abstractmethod
    def get(self, name):
        """Return the dataset with the given name."""

    @abc.abstractmethod
    def remove(self, name):
        """Remove the dataset with the given name."""

    @abc.abstractmethod
    def get_names(self):
        """Return names of the existing datasets."""

    @abc.abstractmethod
    def iter_datasets(self, names=None):
        """Iterate over all or a subset of datasets."""


class MemoryStateDataStore(ABCStateDataStore):
    """A dataset store that keeps everything in memory."""
    def __init__(self, *args, **kwargs):
        self._datasets = {}

    def __contains__(self, key):
        return key in self._datasets

    def __delitem__(self, key):
        del self._datasets[key]

    def __getitem__(self, key):
        return self._datasets[key]

    def add(self, dataset, *args, **kwargs):
        """Add the dataset to the store."""
        if dataset.name in self._datasets:
            raise Exception('Dataset %s already exists.' % dataset.name)
        self._datasets[dataset.name] = dataset

    def get(self, name):
        """Return the dataset with the given name."""
        return self._datasets.get(name)

    def remove(self, name):
        """Remove the dataset with the given name."""
        del self._datasets[name]

    def get_names(self):
        """Return names of the existing datasets."""
        return self._datasets.keys()

    def iter_datasets(self, names=None):
        """Iterate over all or a subset of datasets."""
        if not names:
            names = self._datasets.keys()

        for key in self._datasets:
            if key in names:
                yield self._datasets[key]


class ProxyStateDataStore(ABCStateDataStore):
    """A dataset store that reads its values from a wrapper."""
    def __init__(self, wrapper, *args, **kwargs):
        self._wrapper = wrapper

    def add(self, dataset, *args, **kwargs):
        """Add the dataset to the store."""
        self._wrapper.add_dataset(dataset)

    def get(self, name):
        """Return the dataset with the given name."""
        return self._wrapper.get_dataset(name)

    def remove(self, name):
        """Remove the dataset with the given name."""
        self._wrapper.remove_dataset(name)

    def get_names(self):
        """Return names of the existing datasets."""
        return self._wrapper.get_dataset_names()

    def iter_datasets(self, names=None):
        """Iterate over all or a subset of datasets."""
        return self._wrapper.iter_datasets(names=names)
