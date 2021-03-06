#!/usr/bin/env python3

from setuptools import setup

readme = open('README.md').read()

setup(
    name='rogdrv',
    version='0.0.4',
    description='ASUS ROG userspace driver',
    url='https://github.com/kyokenn/rogdrv',
    author='Kyoken',
    author_email='kyoken@kyoken.ninja',
    license='GPL',
    long_description=readme,
    entry_points={
        'console_scripts': [
            'rogdrv=rogdrv.__main__:rogdrv',
            'rogdrv-config=rogdrv.__main__:rogdrv_config',
        ]
    },
    packages=[
        'rogdrv',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: GPL License',
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment',
    ],
    include_package_data=True,
    zip_safe=False,
)
