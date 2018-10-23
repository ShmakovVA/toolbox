# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='toolbox',
    packages=find_packages(),
    description='Sportamore Toolbox',
    url='https://github.com/ShmakovVA/toolbox',
    author='No',
    install_requires=[
        'pytz >= 2015.6',
        'furl >= 0.5.6',
    ],
    include_package_data=True,
    extras_require={
        ':python_version == "2.7"': ['futures']
    },
    setup_requires=[
        'vcversioner'
    ],
    vcversioner={
        'version_module_paths': [
            'toolbox/_vcs.py'
        ],
    },
)
