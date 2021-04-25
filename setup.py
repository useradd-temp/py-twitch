from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name="py-twitch",
    version="0.1.0",
    author="TEMP USER",
    author_email="useradd.temp@gmail.com",
    description="Twitch API Python client",
    url="https://github.com/helloracoon/py-twitch",
    packages=find_packages(),
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
