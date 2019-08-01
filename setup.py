import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gpioone",
    version="0.1.0",
    install_requires=["RPi.GPIO", "gpiozero", "spidev", "unscii"],
    author="Grant T. Olson",
    author_email="kgo@grant-olson.net",
    description="Interfaces for various GPIO devices on Raspberry PI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grant-olson/gpioone",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
