from setuptools import find_packages,setup

setup(name='arm_diags',
      version='2.0',
      description='An ARM data-oriented package for climate model evaluation',
      url='https://github.com/ARM-DOE/arm-gcm-diagnostics',
      author='Chengzhu Zhang, Zeshawn Shaheen and Shaocheng Xie',
      author_email='zhang40@llnl.gov, shaheen2@llnl.gov and  xie2@llnl.gov',
      license='LLNL and ARM',
      packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
      zip_safe=False)
