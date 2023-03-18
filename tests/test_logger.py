import os
import shutil
from typing import Any
import pytest
import tum_esm_utils

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR_PATH = os.path.join(PROJECT_DIR, "logs")
LOGFILE_PATH = os.path.join(LOG_DIR_PATH, "current-logs.log")
LOG_ARCHIVE_PATH = os.path.join(LOG_DIR_PATH, "archive")


@pytest.fixture
def empty_log_dir() -> Any:
    if os.path.exists(LOG_DIR_PATH):
        shutil.rmtree(LOG_DIR_PATH)
    os.makedirs(LOG_ARCHIVE_PATH)
    os.system(f"touch {LOGFILE_PATH}")

    yield

    shutil.rmtree(LOG_DIR_PATH)


def test_logger(empty_log_dir: Any) -> None:
    generated_log_lines = [
        "pytests                 - DEBUG         - some message a",
        "pytests                 - INFO          - some message b",
        "pytests                 - WARNING       - some message c",
        "pytests                 - ERROR         - some message d",
        "pytests                 - EXCEPTION     - ZeroDivisionError: division by zero",
        "pytests                 - EXCEPTION     - customlabel, ZeroDivisionError: division by zero",
    ]

    tum_esm_utils.testing.expect_file_contents(
        LOGFILE_PATH, forbidden_content_blocks=generated_log_lines
    )

    # -------------------------------------------------------------------------
    # check whether logs lines were written correctly

    logger = tum_esm_utils.logging.Logger(
        origin="pytests", logfile_directory=LOG_DIR_PATH
    )
    logger.debug("some message a")
    logger.info("some message b")
    logger.warning("some message c")
    logger.error("some message d")
    try:
        30 / 0
    except Exception:
        logger.exception()
        logger.exception(label="customlabel")

    tum_esm_utils.testing.expect_file_contents(
        LOGFILE_PATH, required_content_blocks=generated_log_lines
    )


def test_log_message_details_format(empty_log_dir: Any) -> None:
    message_block = (
        "pytests                 - INFO          - some message xy\n"
        + "--- details: ---------------------------\n"
        + "somedetails\n"
        + "----------------------------------------"
    )

    tum_esm_utils.testing.expect_file_contents(
        LOGFILE_PATH, forbidden_content_blocks=[message_block]
    )

    # -------------------------------------------------------------------------
    # check whether logs lines were written correctly

    logger = tum_esm_utils.logging.Logger(
        origin="pytests", logfile_directory=LOG_DIR_PATH
    )
    logger.info("some message xy", details="somedetails")

    tum_esm_utils.testing.expect_file_contents(
        LOGFILE_PATH, required_content_blocks=[message_block]
    )
