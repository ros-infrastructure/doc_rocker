#!/usr/bin/env python3

import os
from setuptools import setup

install_requires = [
    'rocker',
]


kwargs = {
    'name': 'ros2doc',
    'version': '0.0.1',
    'packages': ['ros2doc'],
    'package_dir': {'': 'src'},
    'package_data': {'ros2doc': ['templates/*.em', 'files/*']},
    'entry_points': {
        'console_scripts': [
            'ros2doc_package = ros2doc.main:main',
	    ],
        'rocker.extensions': [
            'ros2doc = ros2doc.package_documentation_extension:ROS2Doc',
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
    'url': 'https://github.com/osrf/ros2doc'
}

setup(**kwargs)