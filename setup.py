from setuptools import find_packages, setup

setup(
    name="crafted-pizza",
    version="1.2.0",
    description="Crafted Pizza App",
    url="https://github.com/john-mwangi/crafted-pizza",
    author="John Mwangi",
    license="",
    author_email="mail.mwangi@gmail.com",
    packages=find_packages(exclude=["tests*", "testing*"]),
    py_modules=["main"],
    entry_points={"console_scripts": ["crafted-pizza-cli=main:main"]},
)
