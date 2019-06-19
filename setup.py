from setuptools import setup, find_packages

setup(
    name='metamer',
    version='0.0.0',
    author='Migun Shakya',
    author_email='migun@lanl.gov',
    packages=find_packages(),
    scripts=['bin/metamer'],
    url='https://github.com/mshakya/metamer',
    license='LICENSE.txt',
    description='a suite that compare metagenomes',
    keywords="metagenome k-mers minhash",
    long_description=open('README.md').read(),
    install_requires=[
        "numpy >= 1.15.1",
        "scipy >= 1.3.0",
        "luigi >= 2.7.5",
        "plumbum >= 1.6.6",
        "pandas >= 0.23.4",
        "pathlib >= 1.0.1",
        "matplotlib >= 3.1.0",
        "Seaborn >= 0.9.0""
    ],
)
