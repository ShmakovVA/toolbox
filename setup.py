# coding: utf-8
from setuptools import setup

setup(
    name='sportamore_toolbox',
    packages=['toolbox'],
    description='Sportamore Toolbox',
    url='https://github.com/Sportamore/sportamore_toolbox',
    version='0.1',
    author='Oscar Linderoth',
    install_requires=[
        'django >= 1.6.8',
        'pytz >= 2015.6',
    ],
)

