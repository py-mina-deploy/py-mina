# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="py-mina",
    version="0.0.7",
    description="Python library for deploying applications on remote server",
    license="MIT",
    author="Cidevant Von Goethe",
    author_email="cidevant@mail.ru",
    url="https://github.com/py-mina-deploy/py-mina",
    packages=find_packages(),
    install_requires=[
		'fabric3',
    ],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ]
)
