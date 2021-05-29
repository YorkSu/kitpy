# -*- coding: utf-8 -*-
"""The setup script."""

import os
from setuptools import setup, find_packages

HERE = os.path.dirname(os.path.abspath(__file__))

# Get the long description from the README file
with open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(os.path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='kitpy',
    version='0.2.3',
    description='Kit of Python',
    author='York Su',
    author_email='york_su@qq.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='kitpy',
    url='https://github.com/YorkSu/kitpy',
    packages=find_packages(include=['kitpy', 'kitpy.*']),
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
    zip_safe=False,
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    license="MIT license",
)
