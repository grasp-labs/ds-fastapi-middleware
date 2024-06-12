.. ds-fastapi-middleware documentation master file, created by
   sphinx-quickstart on Tue May 28 13:11:08 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ds-fastapi-middleware's documentation!
=================================================

ds-fastapi-middleware is a Python project that provides middleware components for FastAPI applications. This middleware is designed to enhance the functionality and performance of your FastAPI application by providing common features such as context, usage, audit and timeout.

High-Level Overview
-------------------
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. Middleware in FastAPI allows you to process requests before they reach your endpoint logic and responses before they are sent to the client. Middleware can be used to implement cross-cutting concerns like authentication, logging, error handling, and more.

Key Features
------------
- **Audit Logging**: Automatically log incoming requests.
- **Context Management**: Manage request context data.
- **Timeout Handling**: Set a timeout for incoming requests and handle timeouts gracefully.
- **Service Usage**: Track and report usage statistics for your API.

Getting Started
---------------
To get started with ds-fastapi-middleware, you need to have Python and FastAPI installed. You can install FastAPI and other dependencies using pip:

.. code-block:: bash

    pip install fastapi
    pip install uvicorn  # ASGI server for FastAPI
    pip install ds-fastapi-middleware

Then, you can create a simple FastAPI application and add middleware to it:

.. code-block:: python

    from fastapi import FastAPI
    from ds_fastapi_middleware import ContextMiddleware

    app = FastAPI()

    app.add_middleware(ContextMiddleware)

    @app.get("/")
    async def read_root():
        return {"Hello": "World"}

Save the above code in a file, say `main.py`, and run it using an ASGI server like Uvicorn:

.. code-block:: bash

    uvicorn main:app --reload

This will start your FastAPI application with the added middleware.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   _autogen/modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
