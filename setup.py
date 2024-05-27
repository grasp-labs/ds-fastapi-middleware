from setuptools import setup, find_packages


setup(
    name="ds_fastapi_middleware",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "boto3",
        "requests",
    ],
    tests_require=[
        "pytest",
        "moto",
        "coverage",
        "httpx",
    ],
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
