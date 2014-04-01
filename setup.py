#! /usr/bin/env python
from setuptools import setup

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(name='google-measurement-protocol',
      author='Mirumee Software',
      author_email='hello@mirumee.com',
      description=('A Python implementation of'
                   ' Google Analytics Measurement Protocol'),
      license='BSD',
      version='0.1.3',
      packages=['google_measurement_protocol'],
      install_required=['requests>=2.0,<3.0a0'],
      test_suite='google_measurement_protocol.tests',
      tests_require=['httmock>=1.0,<1.1a0', 'prices>=0.5,<0.6a0'],
      classifiers=CLASSIFIERS,
      platforms=['any'])
