.. ds-fastapi documentation master file, created by
   sphinx-quickstart on Tue May 28 13:11:08 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the ds-fastapi documentation!
=================================================

.. toctree::
    :maxdepth: 4

ds-fastapi is a Python project that provides FastAPI utilites such as middlewares.
The middlewares are designed to enhance the functionality and performance of your
FastAPI application by providing common features such as context, usage, audit and timeout.

High-Level Overview
-------------------
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. Middleware in FastAPI allows you to process requests before they reach your endpoint logic and responses before they are sent to the client. Middleware can be used to implement cross-cutting concerns like authentication, logging, error handling, and more.

Key Features
------------
- **Authentication**: Requires users to be authenticated before accessing your API.
- **Authorization**: Restricts access to certain endpoints based on user roles.
- **Audit Logging**: Automatically log incoming requests.
- **Context Management**: Manage request context data.
- **Timeout Handling**: Set a timeout for incoming requests and handle timeouts gracefully.
- **Service Usage**: Track and report usage statistics for your API.

Getting Started
---------------
To get started with ds-fastapi, you need to have Python and FastAPI installed. You can install FastAPI and other dependencies using pip:

.. code-block:: bash

    pip install fastapi
    pip install uvicorn  # ASGI server for FastAPI
    pip install ds-fastapi

Then, you can create a simple FastAPI application and add authentication and middleware to it:

.. code-block:: python

    from fastapi import FastAPI
    from ds_fastapi.middlewares import (
        AuditMiddleware,
        ContextMiddleware,
        TimeoutMiddleware,
        UsageMiddleware
    )
    from ds_fastapi.auth import (
        Authentication,
        Context,
        premission_filter,
        get_ctx,
    )
    from ds_fastapi.utils.log.audit import init


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

    # Add an audit logger
    audit_logger = init("unittest-audit")
    app.add_middleware(
        AuditMiddleware,
        logger=audit_logger,
        networks=[""],
    )

    # Add the timeout middleware
    app.add_middleware(TimeoutMiddleware)

    # Add the usage middleware
    app.add_middleware(
        UsageMiddleware,
        product_id="product_id",
        memory_mb=1024,
        queue_name="queue_name",
    )

    # Add the context middleware
    app.add_middleware(ContextMiddleware)
    # Note: Add the context middleware last so that it is executed first.


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

Save the above code in a file, say `main.py`, and run it using an ASGI server like Uvicorn:

.. code-block:: bash

    uvicorn main:app --reload

This will start your FastAPI application with the added middleware.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
