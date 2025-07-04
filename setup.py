"""
Setup script for Borel package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="borel",
    version="1.0.0",
    author="Borel Team",
    author_email="team@borel.com",
    description="A CLI application that parses Markdown formatted text and generates print-ready notes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/borel",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Markup",
        "Topic :: Software Development :: Documentation",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "pypandoc>=1.11",
        "weasyprint>=60.0",
        "jinja2>=3.0.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "borel=borel.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "borel": ["templates/*.html"],
    },
    keywords="markdown pdf documentation cli",
    project_urls={
        "Bug Reports": "https://github.com/your-org/borel/issues",
        "Source": "https://github.com/your-org/borel",
        "Documentation": "https://github.com/your-org/borel#readme",
    },
) 