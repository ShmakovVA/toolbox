# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='sportamore_toolbox',
    packages=find_packages(),
    description='Sportamore Toolbox',
    url='https://github.com/Sportamore/toolbox',
    author='Oscar Linderoth',
    install_requires=[
        'pytz >= 2015.6',
        'furl >= 0.5.6',
    ],
    setup_requires=[
        'vcversioner'
    ],
    vcversioner={
        'version_module_paths': [
            'toolbox/_vcs.py'
        ],
    },
)
