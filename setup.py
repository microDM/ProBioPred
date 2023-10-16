#!/usr/bin/env python

from setuptools import setup
from glob import glob
import os

__copyright__ = "Copyright 2018-2019, ProBioPred"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Dattatray Mongad"

long_description = ("ProBioPred can predict the potential probiotic candidates from genome sequence based on Support Vector Machine (SVM) trained models")

files = [os.path.join(r,i).replace('probiopred/','') for r,d,f in os.walk('probiopred/data/') for i in f ]

setup(name='ProBioPred',
      version=__version__,
      description=('Probiotic candidate prediction'),
      maintainer=__maintainer__,
      url='https://github.com/microDM/ProBioPred',
      packages=['probiopred'],
      scripts=glob('scripts/*py'),
      install_requires=['biopython==1.81', 'pandas==2.1.1'],
      package_data={'probiopred': files},
      long_description=long_description)