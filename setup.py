from setuptools import setup, find_packages
from os.path import dirname, abspath, join


name = 'cavia'
version = '0.0.1'
package = join(
    dirname(abspath(__file__)), name
)


with open(join(package, '__init__.py'), 'w') as f:
    f.write("__version__ = '{}'\n".format(version))


setup(
    name=name,
    version=version,
    # description='',
    author='Peter Badida',
    author_email='keyweeusr@gmail.com',
    url='https://github.com/KeyWeeUsr/' + name,
    download_url=(
        'https://github.com/KeyWeeUsr/' + name + '/tarball/'
        '{}'.format(version)
    ),
    packages=find_packages(),
    install_requires=['beautifulsoup4 >= 4.6.0'],
    extras_require={
        'dev': ['pycodestyle', 'pylint']
    },
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    # keywords=[name, ],
    license="License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
)
