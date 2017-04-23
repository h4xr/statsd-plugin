"""A simple library to write plugins for statsd

Author: Saurabh Badhwar <sbsaurabhbadhwar9@gmail.com>
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

base_path = path.abspath(path.dirname(__file__))

#Get the project long description from the README
with open(path.join(base_path, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='statsd-plugin',
    version='0.1.1',
    description='A simple library to write plugins for statsd',
    long_description=long_description,
    url='https://github.com/h4xr/statsd-plugin',
    author='Saurabh Badhwar',
    author_email='sbsaurabhbadhwar9@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='statsd plugin development',
    packages=find_packages(exclude=['docs','tests','temp']),
    install_requires=['statsd'],
)
