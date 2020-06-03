from setuptools import setup, find_packages

setup(
    # Application name:
    name="python_project",
    # Version number:
    version="1.0.0",
    # Application author details:
    author="Umba",
    author_email="tiernan@umba.com",
    # Packages
    packages=find_packages(),
    # Include additional files into the package
    include_package_data=True,
    # Details
    url="https://github.com/UmbaMobile/python_project",
    description="Umba test API",
)
