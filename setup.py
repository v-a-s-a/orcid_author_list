from setuptools import setup, find_packages

setup(name='orcid_author_list',
      version='0.1',
      description='Generate a formatted author list from a set of ORCIDs.',
      url='https://github.com/vtrubets/orcid_author_list',
      author='Vasa Trubetskoy',
      author_email='',
      license='MIT',
      packages=find_packages(),
      scripts=['src/orcid_author_list.py'],
      zip_safe=False)
