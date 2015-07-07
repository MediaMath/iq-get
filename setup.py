#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = ['qds_sdk == 1.3.4']

setup(
    name='iq-get',
    version='0.1.0',
    author='MediaMath',
    description=('Python script to download Hive command results from Qubole Data Service (QDS)'),
    keywords='qubole sdk iq',
    install_requires=requirements,
    scripts=['bin/iq-get'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Operating System :: OS Independent'
    ]
)
