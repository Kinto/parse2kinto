#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

with codecs.open(os.path.join(here, 'CHANGELOG.rst'), encoding='utf-8') as f:
    history = f.read()

requirements = [
    'kinto-http',
]

test_requirements = [
    'mock',
    'unittest2'
]

ENTRY_POINTS = {
    'console_scripts': [
        'parse2kinto = parse2kinto.__main__:main'
    ],
}


setup(
    name='parse2kinto',
    version='0.1.0.dev0',
    description="Import Parse objects into a Kinto collection.",
    long_description=readme + '\n\n' + history,
    author="Mozilla",
    author_email='kinto@mozilla.org',
    url='https://github.com/Kinto/parse2kinto',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="Apache License (2.0)",
    zip_safe=False,
    keywords='kinto',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='parse2kinto.tests',
    tests_require=test_requirements,
    entry_points=ENTRY_POINTS
)
