from setuptools import find_packages,setup

setup(name='arm_diags',
      version='4.0',
      description='An ARM data-oriented package for climate model evaluation',
      url='https://github.com/ARM-DOE/arm-gcm-diagnostics',
      author='Cheng Tao, Jill Chengzhu Zhang, Shaocheng Xie and Zeshawn Shaheen',
      author_email='tao4@llnl.gov, zhang40@llnl.gov, and xie2@llnl.gov',
      license='LLNL and ARM',
      packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
      zip_safe=False)
