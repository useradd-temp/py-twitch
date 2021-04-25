from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="py-twitch",
    version="0.0.1",
    author="TEMP USER",
    author_email="useradd.temp@gmail.com",
    description="Twitch API Python client",
    url="https://github.com/helloracoon/py-twitch",
    packages=find_packages(),
    install_requires=requirements,
)
