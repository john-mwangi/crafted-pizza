from setuptools import find_packages, setup

setup(
    name="crafted-pizza-app",
    packages=find_packages(exclude=["tests*", "tests.*"]),
    version="1.0.0",
    description="Crafted Pizza App",
    author="John Mwangi",
    license="",
    author_email="mail.mwangi@gmail.com",
)
