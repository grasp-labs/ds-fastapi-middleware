import contextlib
import io

import pytest

from ds_fastapi.utils.log.stdout import Logger


def log_messages(logger):
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")


@pytest.fixture()
def setup_logger():
    _logger = Logger()
    _logger.setup_logger(prefix=["unittest"])
    logger = _logger.LOGGER
    yield logger


def test_log_messages(setup_logger):
    log_output = io.StringIO()

    # Redirect stdout to the StringIO object
    with contextlib.redirect_stdout(log_output):
        log_messages(logger=setup_logger)

    log_contents = log_output.getvalue()
    # TODO: assert log_contents == "Expected log output"
    print("Captured Log Output:\n", log_contents)
