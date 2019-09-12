#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()


setup(
    name='aiohttp-oauth-client',
    version='0.1.0',
    author='Hsiaoming Yang',
    author_email='me@lepture.com',
    url='https://github.com/authlib/aiohttp-oauth-client',
    packages=['aiohttp_oauth_client'],
    description=(
        'OAuth 1.0, OAuth 2.0 and Assertion OAuth Client for aiohttp'
    ),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    long_description=readme,
    license='BSD-3-Clause',
    install_requires=['Authlib==0.12', 'aiohttp'],
    project_urls={
        'Website': 'https://authib.org/',
        'Blog': 'https://blog.authlib.org/',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
