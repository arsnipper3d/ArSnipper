from setuptools import setup,find_packages

REQUIRES_PACKAGES = ['flask']

setup(
    name='flask-restplus',
    version='0.0.1',
    description='Flask RESTplus',
    packages=find_packages(),
    install_requires=REQUIRES_PACKAGES
)

