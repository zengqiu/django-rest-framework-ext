# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


with open('README.md', 'r') as fh:
    readme = fh.read()

setup(
    name='djangorestframework-ext',
    version='0.7',
    url='https://github.com/zengqiu/django-rest-framework-ext',
    license='MIT',
    author='zengqiu',
    author_email='zengqiu@qq.com',
    description='Extensions of Django Rest framework',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    platforms='any',
    install_requires=['django>=2.2', 'djangorestframework>=3.10.0'],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)