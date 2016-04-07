# -*- coding: utf-8 -*-
import glob

from setuptools import setup, find_packages

setup(
    name='shaibos',
    version='0.1',
    url='https://github.com/pypt/shaibos',
    license='LGPL',
    author='Linas Valiukas <pypt at pypt dot lt>',
    author_email='pypt@pypt.lt',
    description='Individualios veiklos pagal pažymą mokesčių skaičiuoklė kompiuterastams',
    long_description=open('README.rst', 'rt').read(),
    keywords='vmi gpm psd vsd tax accounting lithuania individuali veikla',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: Lithuanian',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Financial :: Accounting',
    ],
    test_suite='tests',
    packages=find_packages(exclude=['tests']),
    scripts=glob.glob('bin/shaibos-*'),
)
