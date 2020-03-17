import os
from setuptools import setup, find_packages

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
long_description = f.read()
f.close()

setup(
    name='drf-core',
    version='0.0.1',
    description='Provide reusable modules of Django REST framework.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/drf-tools/drf-core',
    download_url = 'https://github.com/drf-tools/drf-core/archive/v_001.tar.gz',
    author='Huy Tran',
    author_email='huy.tranquoc@asnet.com.vn',
    license='MIT',
    packages=['drf_core',],
    include_package_data=True,
    python_requires=">=3.7.*",
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
