"""Provides a HTTP interface to OPUS."""

from __future__ import annotations
from typing import Literal, Optional
import os
import time
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
    def request(
        request: str,
        timeout: float = 10.0,
        expect_ok: bool = False,
    ) -> list[str]:
        """Send a request to the OPUS HTTP interface and return the answer.

        Commands will be send to `GET http://localhost/OpusCommand.htm?<request>`.
        This function will retry the request up to 3 times and wait 5 seconds
        inbetween retries.

        Args:
            request:    The request to send.
            timeout:    The time to wait for the answer.
            expect_ok:  Whether the first line of the answer should be "OK".

        Returns:
            The answer lines.
        """

        return OpusHTTPInterface.request_without_retry(
            request, timeout=timeout, expect_ok=expect_ok
        )

    @staticmethod
    def request_without_retry(
        request: str,
        timeout: float = 10.0,
        expect_ok: bool = False,
    ) -> list[str]:
        """Send a request to the OPUS HTTP interface and return the answer.

        Commands will be send to `GET http://localhost/OpusCommand.htm?<request>`.

        Args:
            request:    The request to send.
            timeout:    The time to wait for the answer.
            expect_ok:  Whether the first line of the answer should be "OK".

        Returns:
            The answer lines.
        """

        import socket

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
            if expect_ok:
                assert len(answer_lines) >= 1
                assert answer_lines[0] == "OK"
            s.close()
            return answer_lines
        except:
            raise ConnectionError(
                f"Invalid response from OPUS HTTP interface: "
                + ("no answer" if answer_lines is None else str(answer_lines))
            )

    @staticmethod
    def get_version() -> str:
        """Get the version number, like `20190310`."""
        answer = OpusHTTPInterface.request("GET_VERSION")
        try:
            return answer[0]
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def get_version_extended() -> str:
        """Get the extended version number, like `8.2 Build: 8, 2, 28 20190310`."""
        answer = OpusHTTPInterface.request("GET_VERSION_EXTENDED")
        try:
            return answer[0]
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def is_working() -> bool:
        """Check if the OPUS HTTP interface is working. Does NOT raise a
        `ConnectionError` but only returns `True` or `False`."""
        try:
            answer = OpusHTTPInterface.request("COMMAND_SAY hello")
            assert answer[0] == "hello"
            return True
        except:
            return False

    @staticmethod
    def get_main_thread_id() -> int:
        """Get the process ID of the main thread of OPUS."""
        answer = OpusHTTPInterface.request("FIND_FUNCTION 0", expect_ok=True)
        try:
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
                    if answer[0] == "OK":
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
        OpusHTTPInterface.request(f"LOAD_EXPERIMENT {experiment_path}", expect_ok=True)

    @staticmethod
    def start_macro(macro_path: str) -> int:
        """Start a macro. Returns the macro ID."""
        answer = OpusHTTPInterface.request(f"RUN_MACRO {macro_path}", expect_ok=True)
        try:
            return int(answer[1])
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def macro_is_running(macro_id: int) -> bool:
        """Check if the given macro is running. It runs `MACRO_RESULTS <macro_id>`
        under the hood. The OPUS documentation is ambiguous about the return value.
        It seems that 0 means "there is no result yet", i.e. the macro is still running"""
        answer = OpusHTTPInterface.request(f"MACRO_RESULTS {macro_id}", expect_ok=True)
        try:
            return int(answer[1]) == 0
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def stop_macro(macro_path_or_id: str | int) -> None:
        """Stop a macro given by its path or ID.

        Stopping a macro by its ID only works for our OPUS 8.X installations,
        but not our OPUS 7.X installations. Hence, it is recommended to always
        stop it by path."""

        if isinstance(macro_path_or_id, int):
            OpusHTTPInterface.request(f"KILL_MACRO {macro_path_or_id}", expect_ok=True)
        else:
            OpusHTTPInterface.request(
                f"KILL_MACRO {os.path.basename(macro_path_or_id)}", expect_ok=True
            )

    @staticmethod
    def unload_all_files() -> None:
        """Unload all files. This should be done before closing it."""
        OpusHTTPInterface.command_line("UnloadAll()")

    @staticmethod
    def close_opus() -> None:
        """Close OPUS."""
        OpusHTTPInterface.request("CLOSE_OPUS", expect_ok=True)

    @staticmethod
    def set_parameter_mode(variant: Literal["file", "opus"]) -> None:
        """Set the parameter mode to `FILE_PARAMETERS` or `OPUS_PARAMETERS`."""
        OpusHTTPInterface.request(f"{variant.upper()}_PARAMETERS", expect_ok=True)

    @staticmethod
    def read_parameter(parameter: str) -> str:
        """Read the value of a parameter."""
        answer = OpusHTTPInterface.request(f"READ_PARAMETER {parameter}", expect_ok=True)
        try:
            return answer[1]
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def write_parameter(parameter: str, value: str | int | float) -> None:
        """Update the value of a parameter."""
        OpusHTTPInterface.request(f"WRITE_PARAMETER {parameter} {value}", expect_ok=True)

    @staticmethod
    def get_language() -> str:
        """Get the current language."""
        answer = OpusHTTPInterface.request("GET_LANGUAGE", expect_ok=True)
        try:
            return answer[1]
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def get_username() -> str:
        """Get the current username."""
        answer = OpusHTTPInterface.request("GET_USERNAME", expect_ok=True)
        try:
            return answer[1]
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def get_path(literal: Literal["opus", "base", "data", "work"]) -> str:
        """Get the path to the given directory."""
        answer = OpusHTTPInterface.request(f"GET_{literal.upper()}PATH", expect_ok=True)
        try:
            return answer[1]
        except:
            raise ConnectionError(f"Invalid response from OPUS HTTP interface: {answer}")

    @staticmethod
    def set_processing_mode(mode: Literal["command", "execute", "request"]) -> None:
        """Set the processing mode to `COMMAND_MODE`, `EXECUTE_MODE`, or `REQUEST_MODE`."""
        OpusHTTPInterface.request(f"SET_{mode.upper()}_MODE", expect_ok=True)

    @staticmethod
    def command_line(command: str) -> Optional[str]:
        """Execute a command line command, i.e. `COMMAND_LINE <command>`."""
        answer = OpusHTTPInterface.request(f"COMMAND_LINE {command}", expect_ok=True)
        return None if len(answer) == 1 else answer[1]
