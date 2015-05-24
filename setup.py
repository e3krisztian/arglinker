#!/usr/bin/env python
# coding: utf-8
from distutils.core import setup
import io

long_description = io.open('README.md').read()

setup(
    name='glued',
    version='0.1.0',

    author='Krisztián Fekete',
    author_email='krisztian.fekete@gmail.com',
    description=(
        'py.test like automatic fixture injection'
        + ' for unittest and derivatives'),
    long_description=long_description,
    url='https://github.com/krisztianfekete/glued',

    keywords='unittest fixture injection',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    license='Unlicense',

    py_modules=['glued'],
)
