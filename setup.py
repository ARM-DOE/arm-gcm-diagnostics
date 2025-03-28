from setuptools import find_packages, setup
import os

# Read the long description from README.rst
with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='arm_diags',
    version='4.0.0',
    description='An ARM data-oriented package for earth system model evaluation',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/ARM-DOE/arm-gcm-diagnostics',
    author='Cheng Tao, Jill Chengzhu Zhang, Shaocheng Xie and Zeshawn Shaheen',
    author_email='tao4@llnl.gov, zhang40@llnl.gov, xie2@llnl.gov',
    license='LLNL and ARM',
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'cdms2',
        'cdutil',
        'genutil',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'arm-diags=arm_diags.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Topic :: Scientific/Engineering :: Earth Sciences',
    ],
    include_package_data=True,
    zip_safe=False
)
