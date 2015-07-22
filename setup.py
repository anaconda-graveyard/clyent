from setuptools import setup, find_packages
import versioneer

setup(
    name='clyent',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Continuum Analytics',
    author_email='srossross@gmail.com',
    url='http://github.com/binstar/clyent',
    description='Command line client Library for windwos and posix',
    packages=find_packages(),
    license="BSD",
)

