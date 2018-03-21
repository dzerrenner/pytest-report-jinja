#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-report-jinja',
    version='0.1',
    author='David Zerrenner',
    author_email='david.zerrenner@t-systems.com',
    maintainer='David Zerrenner',
    maintainer_email='dazer017@gmail.com',
    license='MIT',
    url='https://github.com/dzerrenner/pytest-report-jinja',
    description='Makes pytest reports via the Jinja2 templating engine',
    long_description=read('README.md'),
    packages=['pytest_report_jinja'],
    install_requires=['pytest>=3.2.5', 'Jinja2>=2.10'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'pytest-report-jinja=pytest_report_jinja.plugin',
        ],
    },
)