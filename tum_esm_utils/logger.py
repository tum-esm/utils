"""Implements custom logging functionality, because the
standard logging module is hard to configure for special
cases.

Implements: `Logger`"""

from __future__ import annotations
from typing import Literal, Optional
import os
import sys
import traceback
import datetime
import filelock


# duplicate method because lazydocs complains when using relative imports
def _pad_string(
    text: str,
    min_width: int,
    pad_position: Literal["left", "right"] = "left",
    fill_char: Literal["0", " ", "-", "_"] = " ",
) -> str:
    if len(text) >= min_width:
        return text
    else:
        pad = fill_char * (min_width - len(text))
        return (pad + text) if (pad_position == "left") else (text + pad)


# duplicate method because lazydocs complains when using relative imports
def _get_utc_offset() -> float:
    """Returns the UTC offset of the system"""
    return round((datetime.datetime.now() -
                  datetime.datetime.utcnow()).total_seconds() / 3600, 1)


# The logging module behaved very weird with the setup we have
# therefore I am just formatting and appending the log lines
# manually. Doesn't really make a performance difference.


def _log_line_has_date(log_line: str) -> bool:
    """Checks whether a given log line (string) starts with a valid date.

    This is not true for exception tracebacks. This log line time is used
    to determine which file to archive logs lines into"""
    try:
        datetime.datetime.strptime(log_line[: 10], "%Y-%m-%d")
        return True
    except:
        return False


class Logger:
    last_archive_time = datetime.datetime.now()

    def __init__(
        self,
        origin: str,
        logfile_directory: str,
        write_to_files: bool = True,
        print_to_console: bool = False,
    ) -> None:
        self.origin: str = origin

        self.filelock = filelock.FileLock(
            os.path.join(logfile_directory, "logging.lock"), timeout=30
        )
        self.current_logfile_path = os.path.join(
            logfile_directory, "current-logs.log"
        )
        self.log_archive_path = os.path.join(logfile_directory, "archive")

        self.write_to_files = write_to_files
        self.print_to_console = print_to_console

    def horizontal_line(
        self, fill_char: Literal["-", "=", ".", "_"] = "="
    ) -> None:
        """writes a horizonal line wiht `-`/`=`/... characters"""
        self._write_log_line("INFO", fill_char * 46)

    def debug(
        self,
        message: str,
        details: Optional[str] = None,
    ) -> None:
        """writes a debug log line"""
        self._write_log_line("DEBUG", message, details=details)

    def info(
        self,
        message: str,
        details: Optional[str] = None,
    ) -> None:
        """writes an info log line"""
        self._write_log_line("INFO", message, details=details)

    def warning(
        self,
        message: str,
        details: Optional[str] = None,
    ) -> None:
        """writes a warning log line"""
        self._write_log_line("WARNING", message, details=details)

    def error(
        self,
        message: str,
        details: Optional[str] = None,
    ) -> None:
        """writes an error log line, sends the message via
        MQTT when config is passed (required for revision number)
        """
        self._write_log_line("ERROR", message, details=details)

    def exception(
        self,
        label: Optional[str] = None,
        details: Optional[str] = None,
    ) -> None:
        """logs the traceback of an exception; output will be
        formatted like this:

        ```
        (label, )ZeroDivisionError: division by zero
        --- details: -----------------
        ...
        --- traceback: ---------------
        ...
        ------------------------------
        ```
        """
        exc_type, exc, exc_traceback = sys.exc_info()
        exception_name = traceback.format_exception_only(exc_type,
                                                         exc)[0].strip()
        exception_traceback = "\n".join(
            traceback.format_exception(exc_type, exc, exc_traceback)
        ).strip()

        subject_string = (
            exception_name if label is None else f"{label}, {exception_name}"
        )

        self._write_log_line(
            "EXCEPTION",
            subject_string,
            details=details,
            traceback=exception_traceback,
        )

    def _write_log_line(
        self,
        level: str,
        message: str,
        **kwargs: Optional[str],
    ) -> None:
        """Formats the log line string and writes it to `logs/current-logs.log`.
        All keyword arguments will be added to the log message with horizontal
        dividers. With `kwargs={"a": "somevalue", "b": None}` the log message will
        look like this:

        ```
        time UTC±X - origin - level - message
        --- a: ---------------------------------
        somevalue
        ----------------------------------------
        ```
        """
        now = datetime.datetime.now()
        utc_offset = _get_utc_offset()
        if utc_offset % 1 == 0:
            utc_offset = round(utc_offset)

        additional_log_items = [(k, v)
                                for k, v in kwargs.items() if v is not None]
        if len(additional_log_items) > 0:
            message += "\n"
            for label, value in additional_log_items:
                message += _pad_string(
                    f"--- {label}: ---",
                    min_width=40,
                    pad_position="right",
                    fill_char="-",
                )
                message += "\n" + value + "\n"
            message += "-" * 40

        log_string = (
            f"{str(now)[:-3]} UTC{'-' if utc_offset < 0 else '+'}{abs(utc_offset)} "
            +
            f"- {_pad_string(self.origin, min_width=23, pad_position='right')} "
            + f"- {_pad_string(level, min_width=13, pad_position='right')} " +
            f"- {message}"
        )
        if self.print_to_console:
            print(log_string)
        else:
            with self.filelock:
                with open(self.current_logfile_path, "a") as f1:
                    f1.write(log_string + "\n")

                # Archive lines older than 60 minutes, every 10 minutes
                if (now - Logger.last_archive_time).total_seconds() > 600:
                    self._archive()

    def _archive(self) -> None:
        """moves old log lines in "logs/current-logs.log" into an
        archive file "logs/archive/YYYYMMDD.log". log lines from
        the last hour will remain"""

        with open(self.current_logfile_path) as f:
            log_lines_in_file = f.readlines()
        if len(log_lines_in_file) == 0:
            return

        lines_to_be_kept, lines_to_be_archived = [], []
        latest_time = str(datetime.datetime.now() - datetime.timedelta(hours=1))
        line_time = log_lines_in_file[0][: 26]
        for index, line in enumerate(log_lines_in_file):
            if _log_line_has_date(line):
                line_time = line[: 26]
            if line_time > latest_time:
                lines_to_be_archived = log_lines_in_file[: index]
                lines_to_be_kept = log_lines_in_file[index :]
                break

        with open(self.current_logfile_path, "w") as f:
            f.writelines(lines_to_be_kept)

        if len(lines_to_be_archived) == 0:
            return

        archive_log_date_groups: dict[str, list[str]] = {}
        line_date = lines_to_be_archived[0][: 10].replace("-", "")
        for line in lines_to_be_archived:
            if _log_line_has_date(line):
                line_date = line[: 10].replace("-", "")
            if line_date not in archive_log_date_groups.keys():
                archive_log_date_groups[line_date] = []
            archive_log_date_groups[line_date].append(line)

        for date in archive_log_date_groups.keys():
            filename = os.path.join(self.log_archive_path, f"{date}.log")
            with open(filename, "a") as f:
                f.writelines(archive_log_date_groups[date] + [""])

        Logger.last_archive_time = datetime.datetime.now()
