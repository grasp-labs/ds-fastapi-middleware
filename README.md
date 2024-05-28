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

## Usage
To use the middleware in your FastAPI application, add it to your app as
follows:

```python
from fastapi import FastAPI
from ds_fastapi_middleware import middleware

app = FastAPI()

app.add_middleware(middleware.ContextMiddleware)

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}
```

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
