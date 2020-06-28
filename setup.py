# -*- coding: utf-8 -*-
import glob

from setuptools import setup, find_packages


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_requirements = parse_requirements('requirements.txt')


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
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Financial :: Accounting',
    ],
    install_requires=install_requirements,
    test_suite='tests',
    packages=find_packages(exclude=['tests']),
    scripts=glob.glob('bin/shaibos-*'),
    package_dir={
        'shaibos': 'shaibos',
    },
    package_data={
        'shaibos': [
            'logging.conf',
            'templates/*.jinja2',
            'samples/1-lt-simple/shaibos.yaml',
            'samples/2-lt-multiple-activities/shaibos.yaml',
            'samples/3-multiple-countries/shaibos.yaml',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
