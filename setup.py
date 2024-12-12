#!/usr/bin/env python
import warnings

"""The setup script."""

from setuptools import find_packages, setup

try:
    with open("README.md") as readme_file:
        readme = readme_file.read()
except FileNotFoundError:
    warnings.warn("README.md not found", stacklevel=2)
    readme = None

REQUIREMENTS_FILES = ["requirements.txt"]


def get_version():
    version_dict = {}
    with open("grafter/version.py") as f:
        exec(f.read(), version_dict)
    return ".".join(map(str, version_dict["VERSION"]))


VERSION = get_version()


def load_requirements():
    requirements = set()
    for requirement_file in REQUIREMENTS_FILES:
        with open(requirement_file) as f:
            requirements.update(line.strip() for line in f)
    return list(requirements)


setup(
    name="grafter",
    version=VERSION,
    description="GRaph-based frAmework for Feature calculaTion and Event tRiggers.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Kyzis Tse",
    author_email="kyzistse@gmail.com",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=load_requirements(),
    zip_safe=False,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.12",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.12, <4",
)
