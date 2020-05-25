from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="urlgen",
    version="0.1.0",
    license="MIT",
    author="kazukazuprogram",
    packages=find_packages(),
    description="Get download URL from cloud storage service URL.",
    long_description=long_description,
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX'
    ],
    entry_points={
        "console_scripts": [
            "urlgen = urlgen.__init__:wrapper",
        ]
    }
)
