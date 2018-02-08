# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='sportamore_toolbox',
    packages=find_packages(),
    description='Sportamore Toolbox',
    url='https://github.com/Sportamore/sportamore_toolbox',
    version='1.1.0',
    author='Oscar Linderoth',
    install_requires=[
        'django >= 1.6.8',
        'pytz >= 2015.6',
        'furl >= 0.5.6',
    ],
)
