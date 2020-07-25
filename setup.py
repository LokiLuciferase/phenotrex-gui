#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
from pkg_resources import parse_requirements

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements/prod.txt') as prod_req:
    requirements = [str(ir) for ir in parse_requirements(prod_req)]
with open('requirements/test.txt') as test_req:
    test_requirements = [str(ir) for ir in parse_requirements(test_req)]

setup(
    author="Lukas Lüftinger",
    author_email='lukas.lueftinger@outlook.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A user-friendly interface for Metagenomic Phenotype Prediction with phenotrex.",
    entry_points={
        'console_scripts': [
            'phenotrex-gui=phenotrex_gui:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    include_package_data=True,
    keywords='phenotrex-gui',
    name='phenotrex-gui',
    packages=find_packages(include=['phenotrex_gui', 'phenotrex_gui.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/LokiLuciferase/phenotrex_gui',
    version='0.0.1',
    zip_safe=False,
)
