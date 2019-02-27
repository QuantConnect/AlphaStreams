# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

# https://github.com/QuantConnect/AlphaStream/blob/master/LICENSE
with open('../LICENSE') as f:
    license = f.read()

with open('README.rst') as f:
    readme = f.read()

setup(
     name='quantconnect-alphastream',
     version='0.7',
     description = 'QuantConnect AlphaStream API',
     long_description=readme,
     author = 'QuantConnect Python Team',
     author_email = 'support@quantconnect.com',
     url='https://www.quantconnect.com/alpha',
     license=license,
     packages = find_packages(exclude=('tests', 'docs')),
     install_requires=['matplotlib', 'pandas', 'requests']
     )
