import setuptools
import os.path

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as fh:
    version_num = fh.read().strip()

setuptools.setup(
    name="ppx",
    version=version_num,
    author="William E Fondrie",
    author_email="fondriew@gmail.com",
    description="A Python interface to the ProteomeXchange Repository",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wfondrie/ppx",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ]
)
