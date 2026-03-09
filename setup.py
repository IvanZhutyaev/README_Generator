"""Setup script for README Generator Pro."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="readme-generator-pro",
    version="0.2.0",
    author="Ivan Zhutyaev",
    author_email="gitivanzhutyaev@gmail.com",
    description="Advanced README generator for GitHub projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IvanZhutyaev/README_Generator",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
    ],
    python_requires=">=3.6",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=6.0", "pytest-cov>=2.0"],
    },
    entry_points={
        "console_scripts": [
            "readme-gen=generator.cli:main",
        ],
    },
    package_data={
        "generator": ["templates/*.md"],
    },
)