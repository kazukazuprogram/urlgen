from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="urlgen",
    version="0.0.0",
    license="MIT",
    author="kazukazuprogram",
    packages=find_packages(),
    description="Get download URL from cloud storage service URL.",
    long_description=long_description,
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        "console_scripts": [
            "urlgen = urlgen.__init__:wrapper",
        ]
    }
)
