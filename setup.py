try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

NAME = 'Cyther'
VERSION = '0.8.dev12'
INSTALL_REQUIRES = ['cython']
SHORT_DESCRIPTION = 'The Cross-Platform Cython/Python Compiler'
LONG_DESCRIPTION = open('README.txt').read()
AUTHOR = 'Nicholas C. Pandolfi'
AUTHOR_EMAIL = 'npandolfi@wpi.edu'
URL = 'https://github.com/nickpandolfi/Cyther'
LICENSE = 'MIT'

PACKAGES = ['cyther']

PACKAGE_DATA = {'cyther': ['../*.txt', '../README.txt']}

ENTRY_POINTS = {'console_scripts': ['cyther = cyther.__main__:main']}

PLATFORMS = ['Windows', 'MacOS', 'POSIX', 'Unix']

KEYWORDS = ['Cyther', 'Cython', 'Python', 'MinGW32',
            'vcvarsall.bat', 'vcvarsall not found',
            'setup.py', 'gcc', 'Python 3',
            'user-friendly', 'command-line',
            'script', 'auto-compiler', 'compiler', 'integration']

CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Environment :: Console',
               'Topic :: Software Development :: Compilers',
               'Topic :: Software Development :: Build Tools',
               'Topic :: Desktop Environment :: File Managers',
               'Intended Audience :: Developers',
               'Intended Audience :: Science/Research',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.4',
               'Programming Language :: Python :: 3.3',
               'Programming Language :: Cython',
               'License :: OSI Approved :: MIT License']

setup(name=NAME,
      version=VERSION,
      install_requires=INSTALL_REQUIRES,
      description=SHORT_DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      packages=PACKAGES,
      package_data=PACKAGE_DATA,
      entry_points=ENTRY_POINTS,
      platforms=PLATFORMS,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      license=LICENSE,
      keywords=KEYWORDS,
      classifiers=CLASSIFIERS)
