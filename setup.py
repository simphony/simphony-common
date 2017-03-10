import os
import contextlib
import textwrap
from subprocess import check_call, CalledProcessError

from setuptools import setup, find_packages
from distutils.cmd import Command

# Read description
with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()

# Setup version
VERSION = '0.6.1'


@contextlib.contextmanager
def cd(path):
    """Change directory and returns back to cwd once the operation is done."""
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


class BuildMeta(Command):
    user_options = [('repopath=', None,
                     "Directory where to look for the local "
                     "simphony-metadata repository clone"),
                    ('repourl=', None, "URL to the github repo for cloning"),
                    ('repotag=', None, "Tag to checkout before building")]

    def initialize_options(self):
        self.repopath = None
        self.repourl = "https://github.com/simphony/simphony-metadata/"
        self.repotag = None

    def finalize_options(self):
        if self.repopath is None:
            self.repopath = os.path.join(os.getcwd(), "simphony-metadata/")

    def run(self):
        try:
            if not os.path.exists(self.repopath):
                print("Checking out {}".format(self.repopath))
                check_call(["git", "clone", self.repourl])
        except OSError:
            print("Failed to run git clone. "
                  "Make sure it is installed in your environment")
            raise
        except CalledProcessError:
            print("Failed to run git clone.")
            raise

        if self.repotag is not None:
            with cd(self.repopath):
                try:
                    print("Stashing possible changes.")
                    check_call(["git", "stash"])
                except CalledProcessError:
                    print("Failed to run git stash.")
                    raise

                try:
                    print("Fetching")
                    check_call(["git", "fetch"])
                except CalledProcessError:
                    print("Failed to fetch")
                    raise

                try:
                    print("Checking out {}".format(self.repotag))
                    check_call(["git", "checkout", self.repotag])
                except CalledProcessError:
                    print("Failed to checkout {}".format(self.repotag))
                    raise

        metadata_yml = os.path.join(
            self.repopath,
            "yaml_files",
            "simphony_metadata.yml")
        cuba_yml = os.path.join(
            self.repopath,
            "yaml_files",
            "cuba.yml")

        if not (os.path.exists(cuba_yml) and os.path.exists(metadata_yml)):
            print(textwrap.dedent("""
                Cannot open simphony-metadata YAML files.
                Please specify an appropriate path to the simphony-metadata
                git repository in setup.cfg.
                """))
            raise RuntimeError("Unrecoverable error.")

        print("Building classes")
        with open(metadata_yml, 'rb') as simphony_metadata:
            from scripts.cli.generator import meta_class
            meta_class.callback(simphony_metadata, "simphony/cuds/meta/", True)

        print("Building keywords")
        with open(metadata_yml, 'rb') as simphony_metadata, \
                open(cuba_yml, 'rb') as cuba, \
                open("simphony/core/keywords.py", "wb") as keywords_out:

            from scripts.cli.generator import keywords
            keywords.callback(cuba, simphony_metadata, keywords_out)

        print("Building enums")
        with open(metadata_yml, 'rb') as simphony_metadata, \
                open(cuba_yml, 'rb') as cuba, \
                open("simphony/core/cuba.py", "wb") as cuba_out:

            from scripts.cli.generator import cuba_enum
            cuba_enum.callback(cuba, simphony_metadata, cuba_out)

        print("Running yapf")
        cmd_args = ["yapf", "--style", "pep8", "--in-place"]
        try:
            check_call(cmd_args + ["simphony/core/keywords.py"])
            check_call(cmd_args + ["simphony/core/keywords.py"])
            check_call(cmd_args + ["--recursive", "simphony/cuds/meta/"])
        except OSError:
            print(textwrap.dedent("""
                Failed to run yapf. Make sure it is installed in your
                python environment, by running

                pip install yapf
                """))
            raise


def write_version_py(filename=None):
    if filename is None:
        filename = os.path.join(
            os.path.dirname(__file__), 'simphony', 'version.py')
    ver = """\
version = '%s'
"""
    fh = open(filename, 'wb')
    try:
        fh.write(ver % VERSION)
    finally:
        fh.close()


write_version_py()


# main setup configuration class
setup(
    name='simphony',
    version=VERSION,
    author='SimPhoNy, EU FP7 Project (Nr. 604005) www.simphony-project.eu',
    description='The native implementation of the SimPhoNy cuds objects',
    long_description=README_TEXT,
    install_requires=[
        "enum34>=1.0.4",
        "stevedore>=1.2.0",
        "numpy>=1.11.1"],
    extras_require={
        'H5IO': ["tables>=3.1.1"],
        'CUBAGen': ["click >= 3.3", "pyyaml >= 3.11"]},
    packages=find_packages(),
    cmdclass={
        'build_meta': BuildMeta,
    },
    entry_points={
        'console_scripts': [
            ('simphony-meta-generate = '
             'scripts.cli.generator:cli')]},
    )
