from typing import Any
import time
import signal

print("starting")


def _graceful_teardown(*args: Any) -> None:
    print("starting graceful teardown")
    time.sleep(3)
    print("finished graceful teardown")
    exit(0)


print("registering teardown handlers")

signal.signal(signal.SIGINT, _graceful_teardown)
signal.signal(signal.SIGTERM, _graceful_teardown)

print("waiting")

time.sleep(15)

print("stopping")
