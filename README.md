# ds FastAPI Middleware

![Python Versions](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11-blue)
[![PyPI version](https://badge.fury.io/py/ds-fastapi-middleware.svg)](https://badge.fury.io/py/ds-fastapi-middleware)
[![Build Status](https://github.com/grasp-labs/ds-fastapi-middleware/actions/workflows/python-package-unittests.yml/badge.svg)](https://github.com/grasp-labs/ds-fastapi-middleware/actions/workflows/python-package-unittests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A custom middleware for FastAPI applications project & part of the
ds project.
- audit middleware
- context middleware
- timeout middleware
- usage middleware

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
  - [Installing](#installing)
  - [Setting Up the Environment](#setting-up-the-environment)
  - [Running Tests](#running-tests)
- [License](#license)

## Installation

You can install the FastAPI Middleware package using pip:

```bash
pip install ds_fastapi_middleware
```

## Usage
To use the middleware in your FastAPI application, add it to your app as
follows:

### Context Middleware

```python
from fastapi import FastAPI
from ds_fastapi_middleware import middlewares

app = FastAPI()

app.add_middleware(middlewares.ContextMiddleware)

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}
```

### Usage Middleware

```python
from fastapi import FastAPI
from ds_fastapi_middleware.middlewares import UsageMiddleware

app = FastAPI()

app.add_middleware(
    UsageMiddleware,
    product_id="product_id",
    memory_mb=1024,
    queue_name="queue_name",
)
```

## Configuration
The middleware can be configured by setting the following environment variables:

- DS_LOGGER_NAME: The name of the logger to use. Default is "ds-logger".
- AWS_DEFAULT_REGION: The default AWS region to use. Default is "eu-north-1".

## Development
If you want to contribute to the development of this package, follow the
steps below to set up your development environment.

### Installing
Clone the repository:

```bash
git clone https://github.com/grasp-labs/ds-fastapi-middleware.git
cd ds-fastapi-middleware
```

Create a virtual environment and install dependencies:

```bash
pipenv install --dev
```

### Running Tests

```bash
pipenv run pytest
```

## License
This project is licensed under the MIT License. See the LICENSE file for more
details.

## Authors
- [Skerve](https://github.com/Skerve)
- [Yuan1979](https://github.com/yuan1979)

## Documentation
Full documentation is available at [Documentation]

## Sphinx
To build the documentation, you need to install Sphinx:

```bash
pipenv install --dev
```

To build the documentation, run:

```bash
pipenv run sphinx-apidoc -o source ds_fastapi_middleware
```
ApiDoc will generate the rst files in the source directory.

To build the html, run:

```bash
pipenv run sphinx-build -b html source _build
```
Sphinx will generate the html files in the _build directory.
