# ds FastAPI Middleware

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
pip install fastapi-middleware

## Usage
To use the middleware in your FastAPI application, add it to your app as
follows:

```python
from fastapi import FastAPI
from fastapi_middleware import CustomMiddleware

app = FastAPI()

app.add_middleware(CustomMiddleware)

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
git clone https://github.com/grasp-labs/fastapi-middleware.git
cd fastapi-middleware
```

Create a virtual environment and install dependencies:

```bash
pipenv install --dev
```

### Running Tests

```bash
pipenv run pytest
```

License
This project is licensed under the MIT License. See the LICENSE file for more
details.
