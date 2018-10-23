# coding: utf-8
from setuptools import setup

setup(
    name='toolbox',
    packages=['toolbox'],
    description='Sportamore Toolbox',
    url='https://github.com/ShmakovVA/toolbox',
    author='No',
    version='2.1.1',
    install_requires=[
        'pytz >= 2015.6',
        'furl >= 0.5.6',
    ],
    include_package_data=True,
    extras_require={
        ':python_version == "2.7"': ['futures']
    },
)
