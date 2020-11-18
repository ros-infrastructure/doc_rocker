#!/usr/bin/env python3

from setuptools import setup

install_requires = [
    'rocker',
]


kwargs = {
    'name': 'doc_rocker',
    'version': '0.0.1',
    'packages': ['doc_rocker'],
    'package_dir': {'': 'src'},
    'package_data': {'doc_rocker': ['templates/*.em', 'files/*']},
    'entry_points': {
        'console_scripts': [
            'doc_rocker_package = doc_rocker.main:main',
        ],
        'rocker.extensions': [
            'doc_rocker = doc_rocker.package_documentation_extension:ROS2Doc',
        ]
    },
    'author': 'Tully Foote',
    'author_email': 'tfoote@osrfoundation.org',
    'keywords': ['Docker'],
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License'
    ],
    'description': 'A tool to generate documentation in ROS 2',
    'long_description': 'A tool to generate documetation in ROS 2.',
    'license': 'Apache License 2.0',
    'python_requires': '>=3.0',

    'install_requires': install_requires,
    'url': 'https://github.com/ros-infrastructure/doc_rocker'
}

setup(**kwargs)
