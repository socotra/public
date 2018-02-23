from setuptools import setup, find_packages
import os

# Try to load version from local version file
version_filename = 'VERSION'
setup_path = os.path.dirname(os.path.realpath(__file__))
version_path = os.path.join(setup_path, version_filename)
version_file = open(version_path)
version = version_file.read().strip()

# Configure the distribution
setup(name='socotratools',
      version=version,
      description='Socotra Tools',
      packages=find_packages(),
      scripts=[],
      url='https://www.socotra.com',
      maintainer='Dinesh Shenoy',
      maintainer_email='dinesh.shenoy@socotra.com',
      license='all rights reserved',
      long_description=open('README.md', 'rt').read(),
      install_requires=['requests==2.9.1'])
