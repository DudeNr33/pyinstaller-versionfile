"""
Setup script for pyinstaller-versionfile.
"""
import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION.txt", "r") as fh:
    version = fh.read().strip()

with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

with open("CHANGELOG.md", "r") as fh:
    changelog = fh.read()


def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('./src/pyinstaller_versionfile')


setuptools.setup(
    name="pyinstaller_versionfile",
    version=version,
    author="Andreas Finkler",
    author_email="andi.finkler@gmail.com",
    description="Create a version file from a simple YAML config file",
    long_description=long_description + "\n\n" + changelog,
    long_description_content_type="text/markdown",
    url="https://github.com/DudeNr33/pyinstaller-versionfile",
    packages=setuptools.find_packages(where="src"),
    package_dir={'': 'src'},
    include_package_data=True,
    entry_points={
          'console_scripts': [
              'create-version-file = pyinstaller_versionfile.__main__:main'
          ]
      },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Environment :: Console",
    ],
    python_requires='>=3.6'
)
