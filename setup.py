"""
Setup script for Jarvis
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="jarvis-assistant",
    version="1.0.0",
    author="explosiverdx",
    description="An intelligent AI-powered voice assistant and automation system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/explosiverdx/Jarvis",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Home Automation",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-dotenv==1.0.0",
        "pyyaml==6.0.1",
        "SpeechRecognition==3.10.0",
        "pyttsx3==2.90",
        "nltk==3.8.1",
        "requests==2.31.0",
        "APScheduler==3.10.4",
        "loguru==0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.0",
            "pytest-cov==4.1.0",
            "black==23.7.0",
            "flake8==6.0.0",
            "pylint==2.17.5",
        ],
        "ai": [
            "torch==2.0.1",
            "transformers==4.30.2",
            "openai==0.27.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "jarvis=jarvis.main:main",
        ],
    },
)
