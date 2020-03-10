import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drf-core',
    version='0.0.1',

    description='Provide reusable modules of Django REST framework.',
    long_description=README,

    url='git@github.com:tranquochuy/drf-core.git',
    download_url = 'git@github.com:tranquochuy/drf-core.git',
    author='Huy Tran',
    author_email='huy.tranquoc@asnet.com.vn',

    license='MIT',

    packages=['drf_core',],
    include_package_data=True,
    install_requires=[
        'Django>=3.0.4',
        'djangorestframework>=3.11.0'
    ],

    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
    ],

    keywords='API REST framework core modules',
)
