"""Setup script for stems audio processing toolkit."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="stems",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Audio processing toolkit for YouTube downloads and stem separation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/stems",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "yt-dlp>=2023.0.0",
    ],
    extras_require={
        "audio": ["essentia>=2.1b6"],
        "scraping": [
            "undetected-chromedriver>=3.5.0",
            "selenium>=4.0.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "pylint>=2.17.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "stems-yt=src.cli.yt_cli:main",
            "stems-split=src.cli.split_stems_cli:main",
        ],
    },
)

