"""
Setup script for torero-api.

This script is used to build and install the torero-api package.
"""

from setuptools import setup, find_packages

setup(
    name="torero-api",
    version="0.1.0",
    description="RESTful API for torero service management",
    author="William Collins",
    author_email="opensource@itential.com",
    url="https://github.com/torerodev/torero-api",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi>=0.111.0,<0.112.0",
        "uvicorn[standard]>=0.29.0,<0.30.0",
        "pydantic>=2.0.0,<3.0.0",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "torero-api=torero_api.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: FastAPI",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Networking",
    ],
)