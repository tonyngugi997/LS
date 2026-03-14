"""
pyls - Python implementation of Unix ls command
Author: tonyngugi997
GitHub: https://github.com/tonyngugi997/LS
"""

import os
import argparse
import sys
from pathlib import Path


class PyLS:
    def __init__(self, location="."):
        """Initialize the PyLS class"""
        self.location = location

    def list_files(self):
        """List files in the specified location"""
        try:
            files = os.listdir(self.location)

            for file in files:
                print(file)

        except FileNotFoundError:
            print(f"ERROR: The directory {self.location} does not exist.")

        except PermissionError:
            print(f"ERROR: Permission denied for: {self.location}.")


if __name__ == "__main__":
    my_ls = PyLS()
    my_ls.list_files()