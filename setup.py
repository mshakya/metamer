from distutils.core import setup

setup(
    name='metamash',
    version='0.0.0',
    author='Migun Shakya',
    author_email='migun@lanl.gov',
    packages=['metamash'],
    scripts=['bin/metamash'],
    # url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='comparing metagenomes using mash',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy >= 1.15.1",
        "luigi >= 2.7.5",
        "plumbum >= 1.6.6",
        "pandas >= 0.23.4",
    ],
)