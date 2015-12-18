#! /usr/bin/env python
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    test_args = []

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='google-measurement-protocol',
    author='Mirumee Software',
    author_email='hello@mirumee.com',
    description=('A Python implementation of'
                 ' Google Analytics Measurement Protocol'),
    license='BSD',
    version='0.1.5',
    packages=['google_measurement_protocol'],
    install_required=['requests>=2.0,<3.0a0'],
    tests_require=['httmock>=1.0,<1.1a0', 'prices>=0.5,<0.6a0', 'pytest'],
    classifiers=CLASSIFIERS,
    cmdclass={
        'test': PyTest},
    platforms=['any'])
