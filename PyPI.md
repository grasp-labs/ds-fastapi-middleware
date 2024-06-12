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
