# ds-fastapi

![Python Versions](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11-blue)
[![PyPI version](https://badge.fury.io/py/ds-fastapi-middleware.svg)](https://badge.fury.io/py/ds-fastapi-middleware)
[![Build Status](https://github.com/grasp-labs/ds-fastapi-middleware/actions/workflows/python-package-unittests.yml/badge.svg)](https://github.com/grasp-labs/ds-fastapi-middleware/actions/workflows/python-package-unittests.yml)
[![codecov](https://codecov.io/gh/grasp-labs/ds-fastapi-middleware/graph/badge.svg?token=8YLGSYG3JQ)](https://codecov.io/gh/grasp-labs/ds-fastapi-middleware)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


The package contains custom utilites for FastAPI applications and is a part of the
ds project.
- Authentication and authorization
- Audit middleware
- Context middleware
- Timeout middleware
- Usage middleware

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
  - [Installing](#installing)
  - [Running Tests](#running-tests)
- [License](#license)

## Installation

You can install the FastAPI Middleware package using pip:

```bash
pip install ds_fastapi
```

## Usage
To use the package in your FastAPI application, add it to your app as
follows:

### Authentication

```python
from fastapi import FastAPI
from ds_fastapi.auth import (
    Authentication,
    Context,
    get_ctx,
    permission_filter,
)

def get_key():
    # Implement your logic to retrieve the public JWT key here

"""
Be sure to use the same authentication instance across all routes
as this will avoid attemting to fetch the public key each time a
request is made.
"""
authentication = Authentication(
    jwt_key=get_key(),
)

app = FastAPI()

@app.get("/", dependencies=[Depends(authentication)])
async def read_root():
    return {"Hello": "World"}

# Protected route
@app.get("/protected", dependencies=[Depends(authentication)])
@permission_filter(["service.cm.user"])
async def forbidden(
    context: Context = Depends(get_ctx),
):
    return {"iam":"protected"}

```

### Context Middleware

```python
from fastapi import FastAPI
from ds_fastapi.middlewares import ContextMiddleware

app = FastAPI()

app.add_middleware(middlewares.ContextMiddleware)

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}
```

### Usage Middleware

```python
from fastapi import FastAPI
from ds_fastapi.middlewares import UsageMiddleware, ContextMiddleware

app = FastAPI()

app.add_middleware(
    UsageMiddleware,
    product_id="product_id",
    memory_mb=1024,
    queue_name="queue_name",
)
app.add_middleware(middlewares.ContextMiddleware)
```

### TimeoutMiddleware

```python
from fastapi import FastAPI
from ds_fastapi.middlewares import TimeoutMiddleware

app = FastAPI()

app.add_middleware(TimeoutMiddleware)
```

### AuditMiddleware

```python
from fastapi import FastAPI
from ds_fastapi.auth import Authentication, get_ctx, Context
from ds_fastapi.middlewares import AuditMiddleware, ContextMiddleware
from ds_fastapi.utils.log.audit import init


logger = init("unittest-audit")

app = FastAPI()

authentication = Authentication(jwt_key="jwt_key")

app.add_middleware(AuditMiddleware, logger=logger, networks=["192.168.0.0/16"])
app.add_middleware(ContextMiddleware)

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

# Protected route
@app.get("/protected", dependencies=[Depends(authentication)])
async def forbidden(
    context: Context = Depends(get_ctx),
):
    return {"iam":"protected"}
```

## Configuration
Environment variables:

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
set PYTHONPATH=src/
pipenv run pytest
```

You can also use [nektosact](https://nektosact.com/introduction.html) to execute the test workflow in Docker.
This will execute tests across the supported python interpreters.

```bash
act -W '.github/workflows/test.yml'
```
You can select a single interpreter by running
```bash
act -W '.github/workflows/test.yml' --matrix python-version:3.9
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

To build the html, run:

```bash
cd docs
pipenv run make html
```
Sphinx will generate the html files in the docs/build directory.

The ``sphinx-autoapi``  extension takes care of building a complete
API reference for all packages under the ``src`` directory. The package
path can be modified by changing the ``autoapi_dirs`` variable in ``docs/soruce/conf.py``
