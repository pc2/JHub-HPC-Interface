import setuptools;
import site;
import sys;

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read();

site.ENABLE_USER_SITE = '--user' in sys.argv[1:];

setuptools.setup(
name="jh_hpc_interface",
version="1.3",
author="Paderborn Center for Parallel Computing",
include_package_data=True,
packages=['jh_hpc_interface'],
scripts=['bin/jh_wrapper', 'bin/jh_slurm_wizard'],
description="JupyterHub + High-Performace Computing",
long_description=long_description,
long_description_content_type="text/markdown",
url="https://github.com/pc2/JHub-HPC-Interface",
install_requires=['batchspawner', 'notebook'],
project_urls={
    "Bug Tracker": "https://github.com/pc2/JHub-HPC-Interface/issues",
},
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
],
)
