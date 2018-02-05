import re
from setuptools import setup, find_packages

with open('vote_networks/__init__.py') as f:
    versionString = re.search(r"__version__ = '(.+)'", f.read()).group(1)

setup(name='vote_networks',
    version = versionString,
    author="Reid McIlroy-Young",
    author_email = "reidmcy@uchicago.edu",
    license = 'GPL',
    url="https://github.com/reidmcy/vote_networks",
    download_url = "https://github.com/reidmcy/vote_networks/archive/{}.tar.gz".format(versionString),
    keywords= '',
    classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Environment :: MacOS X',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Education',
    ],
    install_requires= ['datetime', 'requests'],
    packages = find_packages(),
    entry_points={'console_scripts': [
              'vote_networks = vote_networks.main:main',
    ]},
)
