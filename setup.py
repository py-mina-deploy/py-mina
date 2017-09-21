# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="py-mina",
    version="0.0.2",
    description="Python library for deploying applications to remote server",
    license="MIT",
    author="Cidevant Von Goethe",
    author_email="cidevant@mail.ru",
    url="https://github.com/py-mina-deploy/py-mina",
    packages=find_packages(),
    install_requires=[
		'fabric',
    ],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
