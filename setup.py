from setuptools import setup, find_packages


setup(
    name='dggs',
    author='Jeff Albrecht',
    author_email='jeffalbrecht9@gmail.com',
    version=0.1,
    url='https://github.com/geospatial-jeff/dggs',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['dggs=main:cli']
    }
)