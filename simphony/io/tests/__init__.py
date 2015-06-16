def load_tests(loader, standard_tests, pattern):
    # Skip io tests when Pytables is not available.

    # hide imports since they are only needed during testing
    import warnings
    import os

    try:
        import tables  # noqa
    except ImportError:
        warnings.warn(
            "Skipping IO tests since PyTables is not installed",
            RuntimeWarning)
        return standard_tests
    else:
        this_dir = os.path.dirname(__file__)
        package_tests = loader.discover(start_dir=this_dir, pattern=pattern)
        return package_tests
