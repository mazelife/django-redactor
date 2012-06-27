#!/usr/bin/env python

from os import path
from distutils.core import setup


version = '1.1'

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: Other/Proprietary License",
    "Programming Language :: Python",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
    "Environment :: Web Environment",
    "Framework :: Django",
]

root_dir = path.dirname(__file__)
long_desc = open(root_dir + '/README.rst').read()


setup(
    name='django-redactor',
    version=version,
    url='http://github.com/mazelife/django-redactor/',
    author='James Stevenson',
    author_email='james.m.stevenson at gmail dot com',
    license='CC licence, see LICENSE.txt',
    packages=['redactor'],
    description=(
        'Integrates the Redactor Javascript WYSIWYG editor with Django.'
    ),
    classifiers=classifiers,
    long_description=long_desc,
    install_requires=['django>=1.3'],
    include_package_data=True,
    zip_safe=False
)
