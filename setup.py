"""Package configuration."""
from setuptools import find_packages, setup

setup(
    name="write_fort20",
    version="0.1",
    packages=find_packages(),
    #packages=["src/write_fort20"],
    #package_dir={"": "src"},
    install_requires=[
        'numpy',
        'pandas',
        'geopy'],
    ## Entry point for command line and function to be executed
    entry_points={
        'console_scripts': ['write_fort20=write_fort20.fort20write:main'],
    }
)
