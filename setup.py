# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = "Deployer and server automation tool."

setup(
    name="py_mina",
    version="0.1.7",
    description="Python library for deploying applications on remote server",
    long_description=long_description,
    license="MIT",
    author="Cidevant Von Goethe",
    author_email="cidevant@mail.ru",
    url="https://github.com/py-mina-deploy/py-mina",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'py_mina = py_mina.cli.cli:run',
        ]
    },
    install_requires=[
		'fabric3',
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ]
)
