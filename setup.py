import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

classifiers = [
    'Development Status :: 3 - Alpha',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.11',
    'Topic :: Software Development :: Embedded Systems',
]

setup(
    name = 'lps22hh',
    version = '0.3.0',
    author = 'Chris Braissant',
    author_email = 'chrisbraissant@gmail.com',
    description = 'Raspberry Pi Pico Micropyhton library to interact with the ST LPS22HH Barometric pressure sensor',
    license = 'MIT',
    url='https://github.com/cbraissant/lps22hh_pico_driver',
    install_requires = [],
    classifiers=classifiers,
    long_description=readme,
    long_description_content_type = 'text/markdown'
)