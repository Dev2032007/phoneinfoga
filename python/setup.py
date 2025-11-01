"""Setup script for PhoneInfoga."""

from setuptools import setup, find_packages

setup(
    name="phoneinfoga",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "colorama>=0.4.4",
        "phonenumbers>=8.12.0",
        "python-dotenv>=0.19.0",
        "requests>=2.26.0",
        "flask>=2.0.0",
        "flask-cors>=3.0.10",
    ],
    entry_points={
        "console_scripts": [
            "phoneinfoga=phoneinfoga.cli:main",
        ],
    },
    python_requires=">=3.8",
)
