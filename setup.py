#! /usr/bin/env python
from setuptools import setup

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='google-measurement-protocol',
    author='Mirumee Software',
    author_email='hello@mirumee.com',
    description=(
        'A Python implementation of Google Analytics Measurement Protocol'),
    license='BSD',
    version='1.1.0',
    packages=['google_measurement_protocol'],
    install_requires=['requests>=2.0,<3.0a0', 'prices>=1.0.0', 'typing>=3.6.0;python_version<"3.5"'],
    classifiers=CLASSIFIERS,
    platforms=['any'])
