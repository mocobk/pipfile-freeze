import io
from setuptools import setup

with io.open("README.md", encoding="utf-8") as f:
    README = f.read()


setup(
    name="pipfile-freeze",
    version="0.1.3",
    description="A CLI tool to convert Pipfile/Pipfile.lock to requirments.txt",
    url="https://github.com/mocobk/pipfile-freeze",
    long_description=README,
    long_description_content_type="text/markdown",
    author="mocobk",
    py_modules=["pipfile_freeze"],
    author_email="mailmzb@163.com",
    license="MIT",
    install_requires=["requirementslib", "tomlkit <= 0.5.3"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["pipfile = pipfile_freeze:main"]},
)
