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
        self.show_all = False

    def list_files(self):
        " List files in the specified location"
        try:
            all_files = os.listdir(self.location)
            files_to_display = []

            for file in all_files:
                if self.show_all or not file.startswith('.'):
                    files_to_display.append(file)
            for file in sorted(files_to_display):
                print(file)
        except FileNotFoundError:
            print(f"Error: The directory '{self.location}' does not exist.")
        except PermissionError:
            print(f"Error: You do not have permission to access '{self.location}'.")    


       


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description = "Python implementation of Unix ls command")
        parser.add_argument('-a', '--all', action='store_true', help='Include hidden files')
        parser.add_argument('path', nargs='?', default='.', help='Directory to list (default: current directory)')
        args = parser.parse_args()
        
        my_ls = PyLS()
        my_ls.locatopn = args.path
        my_ls.show_all = args.all

        my_ls.list_files()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
        
