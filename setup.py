# file functional with Python3  
from setuptools import find_packages,setup

setup(name='arm_diags',
      version='2.0',
      description='An ARM data-oriented package for climate model evaluation',
      url='https://github.com/ARM-DOE/arm-gcm-diagnostics',
      author='Jill Chengzhu Zhang, Cheng Tao, Shaocheng Xie and Zeshawn Shaheen',
      author_email='zhang40@llnl.gov, tao4@llnl.gov and  xie2@llnl.gov',
      license='LLNL and ARM',
      packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
      zip_safe=False)
