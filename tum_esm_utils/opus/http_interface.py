"""Provides a HTTP interface to OPUS."""

from __future__ import annotations
from typing import Literal, Optional
import os
import time
import socket
import tenacity


class OpusHTTPInterface:
    """Interface to the OPUS HTTP interface.

    It uses the socket library, because the HTTP interface of OPUS does not
    reuturn valid HTTP/1 or HTTP/2 headers. It opens and closes a new socket
    because OPUS closes the socket after the answer has been sent.

    Raises:
        ConnectionError: If the connection to the OPUS HTTP interface fails or
                         if the response is invalid.
    """

    @staticmethod
    @tenacity.retry(
        retry=tenacity.retry_if_exception_type(ConnectionError),
        reraise=True,
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_fixed(5),
    )
    def request(request: str, timeout: float = 10.0) -> list[str]:
        """Send a request to the OPUS HTTP interface and return the answer.

        The request will wait up to `timeout` seconds. This function will
        retry the request up to 3 times and wait 5 seconds inbetween retries."""

        return OpusHTTPInterface.request_without_retry(request, timeout=timeout)

    @staticmethod
    def request_without_retry(request: str, timeout: float = 10.0) -> list[str]:
        """Send a request to the OPUS HTTP interface and return the answer.

        The request will wait up to `timeout` seconds."""

        answer_lines: Optional[list[str]] = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect(("localhost", 80))
            url = f"/OpusCommand.htm?{request.replace(' ', '%20')}"
            s.sendall(f"GET {url}\r\nHost: localhost\r\n\r\n".encode("utf-8"))
            answer = s.recv(4096).decode("utf-8").strip("\r\n\t ")
            answer_lines = [l.strip(" \r\t") for l in answer.split("\n")]
            answer_lines = [l for l in answer_lines if len(l) > 0]
            s.close()
            return answer_lines
        except:
            raise ConnectionError(
                f"Invalid response from OPUS HTTP interface: "
                + ("no answer" if answer_lines is None else str(answer_lines))
            )

    @staticmethod
    def get_version() -> str:
        """Get the version number, like `20190310`"""

        answer = OpusHTTPInterface.request("GET_VERSION")
        try:
            assert len(answer) == 1
            return answer[0]
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def get_version_extended() -> str:
        """Get the extended version number, like `8.2 Build: 8, 2, 28 20190310`."""

        answer = OpusHTTPInterface.request("GET_VERSION_EXTENDED")
        try:
            assert len(answer) == 1
            return answer[0]
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def is_working() -> bool:
        """Check if the OPUS HTTP interface is working. Does NOT raise a
        `ConnectionError` but only returns `True` or `False`."""

        try:
            answer = OpusHTTPInterface.request("COMMAND_SAY hello")
            assert len(answer) == 1
            assert answer[0] == "hello"
            return True
        except:
            return False

    @staticmethod
    def get_main_thread_id() -> int:
        """Get the process ID of the main thread of OPUS. This can be used if
        any other threads are running"""

        answer = OpusHTTPInterface.request("FIND_FUNCTION 0")
        try:
            assert len(answer) == 2
            assert answer[0] == "OK"
            return int(answer[1])
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def some_macro_is_running() -> bool:
        """Check if any macro is currently running.

        In theory, we could also check whether the correct macro is running using
        `READ_PARAMETER MPT` and `READ_PARAMETER MFN`. However, these variables do
        not seem to be updated right away, so we cannot rely on them."""

        main_thread_id = OpusHTTPInterface.get_main_thread_id()
        active_thread_ids: set[int] = set()

        # some common functions executed inside Macro routines that take some time
        common_functions = [
            "MeasureReference",
            "MeasureSample",
            "MeasureRepeated",
            "MeasureRapidTRS",
            "MeasureStepScanTrans",
            "UserDialog",
            "Baseline",
            "PeakPick",
            "Timer",
            "SendCommand",
        ]

        # check twice for any thread that is executing a common function
        for i in range(2):
            for function in common_functions:
                answer = OpusHTTPInterface.request(f"FIND_FUNCTION {function}")
                try:
                    assert len(answer) >= 1
                    assert answer[0] == "OK"
                    for thread_id in answer[1:]:
                        active_thread_ids.add(int(thread_id))
                except:
                    raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")
            if i == 0:
                time.sleep(3)

        # the main thread always runs some common functions for some reason
        if main_thread_id in active_thread_ids:
            active_thread_ids.remove(main_thread_id)

        # if there is any thread that is not the main thread, then a macro is running
        return len(active_thread_ids) > 0

    @staticmethod
    def get_loaded_experiment() -> str:
        """Get the path to the currently loaded experiment."""

        OpusHTTPInterface.set_parameter_mode("opus")
        xpp_value = OpusHTTPInterface.read_parameter("XPP")
        exp_value = OpusHTTPInterface.read_parameter("EXP")
        return os.path.join(xpp_value, exp_value)

    @staticmethod
    def load_experiment(experiment_path: str) -> None:
        """Load an experiment file."""

        answer = OpusHTTPInterface.request(f"LOAD_EXPERIMENT {experiment_path}")
        try:
            assert answer is not None
            assert len(answer) == 1
            assert answer[0] == "OK"
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def start_macro(macro_path: str) -> int:
        """Start a macro. Returns the macro ID."""

        answer = OpusHTTPInterface.request(f"RUN_MACRO {macro_path}")
        try:
            assert len(answer) == 2
            assert answer[0] == "OK"
            return int(answer[1])
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def macro_is_running(macro_id: int) -> bool:
        """Check if the given macro is running."""

        answer = OpusHTTPInterface.request(f"MACRO_RESULTS {macro_id}")
        # The OPUS documentation is ambiguous about the return value. It
        # seems that 0 means "there is no result yet", i.e. the macro is
        # still running
        try:
            assert len(answer) == 2
            assert answer[0] == "OK"
            return int(answer[1]) == 0
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def stop_macro(macro_path: str) -> None:
        """Stop a macro."""

        answer = OpusHTTPInterface.request(f"KILL_MACRO {os.path.basename(macro_path)}")
        try:
            assert len(answer) == 1
            assert answer[0] == "OK"
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def unload_all_files() -> None:
        """Unload all files. This should be done before closing it."""

        answer = OpusHTTPInterface.request("COMMAND_LINE UnloadAll()")
        try:
            assert len(answer) >= 1
            assert answer[0] == "OK"
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def close_opus() -> None:
        """Close OPUS."""

        answer = OpusHTTPInterface.request("CLOSE_OPUS")
        try:
            assert len(answer) >= 1
            assert answer[0] == "OK"
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def set_parameter_mode(variant: Literal["file", "opus"]) -> None:
        """Set the parameter mode to `FILE_PARAMETERS` or `OPUS_PARAMETERS`."""

        answer = OpusHTTPInterface.request(f"{variant.upper()}_PARAMETERS")
        try:
            assert len(answer) == 1
            assert answer[0] == "OK"
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def read_parameter(parameter: str) -> str:
        """Read the value of a parameter."""

        answer = OpusHTTPInterface.request(f"READ_PARAMETER {parameter}")
        try:
            assert len(answer) == 2
            assert answer[0] == "OK"
            return answer[1]
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def write_parameter(parameter: str, value: str | int | float) -> None:
        """Update the value of a parameter."""

        answer = OpusHTTPInterface.request(f"WRITE_PARAMETER {parameter} {value}")
        try:
            assert len(answer) == 1
            assert answer[0] == "OK"
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def get_language() -> str:
        """Get the current language."""

        answer = OpusHTTPInterface.request("GET_LANGUAGE")
        try:
            assert len(answer) == 2
            assert answer[0] == "OK"
            return answer[1]
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def get_username() -> str:
        """Get the current username."""

        answer = OpusHTTPInterface.request("GET_USERNAME")
        try:
            assert len(answer) == 2
            assert answer[0] == "OK"
            return answer[1]
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def get_path(literal: Literal["opus", "base", "data", "work"]) -> str:
        """Get the path to the given directory."""

        answer = OpusHTTPInterface.request(f"GET_{literal.upper()}PATH")
        try:
            assert len(answer) == 2
            assert answer[0] == "OK"
            return answer[1]
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def set_processing_mode(mode: Literal["command", "execute", "request"]) -> None:
        """Set the processing mode to `COMMAND_MODE`, `EXECUTE_MODE`, or `REQUEST_MODE`."""

        answer = OpusHTTPInterface.request(f"SET_{mode.upper()}_MODE")
        try:
            assert len(answer) == 1
            assert answer[0] == "OK"
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")
