from setuptools import setup, find_packages

setup(
    name='kaggleway',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    # packages=find_packages(include=['src/kaggleway', 'src/kaggleway/*'])
)