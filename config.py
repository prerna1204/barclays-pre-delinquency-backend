# config.py

import os
import sys


MODE = os.environ.get("BARCLAYS_MODE", "DEV")  # DEV or DEMO


class OutputFilter:
    def __init__(self, allow=True):
        self.allow = allow
        self.original = sys.stdout

    def write(self, text):
        if self.allow:
            self.original.write(text)

    def flush(self):
        self.original.flush()


def setup_mode():
    """
    Configure output based on mode
    """

    global MODE

    print(f"[CONFIG] Running in {MODE} mode")

    if MODE == "DEMO":
        # Hide noisy logs
        sys.stdout = OutputFilter(allow=True)
        sys.stderr = OutputFilter(allow=False)

    elif MODE == "DEV":
        # Show everything
        pass
