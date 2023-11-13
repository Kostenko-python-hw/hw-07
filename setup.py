from setuptools import setup

setup(
    name='clean_folder',
    version='0.0.1',
    author='Mykhailo Kostenko',
    author_email='kostenko.m.s@gmail.com',
    description='This utility will help you sort through the trash in your folder',
    url='https://github.com/Kostenko-python-hw/hw-06',
    entry_points={'console_scripts': ['clean-folder=clean_folder.clean:main']}
)