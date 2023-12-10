#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
from setuptools import setup, find_packages

VERSION = '4.6.0'

with io.open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

requires = [
    'lxml',
    'func_timeout'
]

setup(
    name='pyadbui',
    version=VERSION,
    description='pyadbui 是一个基于 adb 的 python 库, 特色是可以通过安卓原生 uiautomator 获取界面属性, xpath, ocr 等元素.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Hao',
    author_email='zhao5638@gmail.com',
    url='https://github.com/CallmeLins/pyadbui',
    keywords='testing android uiautomator ocr minicap',
    install_requires=requires,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing'
    ]
)