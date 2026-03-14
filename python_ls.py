"""
pyls - Python implementation of Unix ls command
Author: tonyngugi997
GitHub: https://github.com/tonyngugi997/LS
"""

import os
import argparse
import sys
from pathlib import Path
import time


class PyLS:
    def __init__(self, location="."):
        """Initialize the PyLS class"""
        self.location = location
        self.show_all = False
        self.long_format = False
        self.human_readable = False

    def make_size_human_readable(self, size_bytes):
        """Convert bytes to human readable format (B, K, M, G)"""
        if not self.human_readable:
            return str(size_bytes).rjust(8)
        
        # Define size units
        units = ['B', 'K', 'M', 'G', 'T']
        unit_index = 0
        size = float(size_bytes)
        
        # Keep dividing by 1024 until size is less than 1024
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        # Format with 1 decimal place if needed
        if size < 10:
            return f"{size:.1f}{units[unit_index]}".rjust(8)
        elif size < 100:
            return f"{size:.0f}{units[unit_index]}".rjust(8)
        else:
            return f"{size:.0f}{units[unit_index]}".rjust(8)

    def fetch_file_info(self, file):
        """Fetch file information for long listing format"""
        full_path = os.path.join(self.location, file)
        try:
            file_stat = os.stat(full_path)

            if os.path.isdir(full_path):
                file_type = 'd'
            elif os.path.islink(full_path):
                file_type = 'l'
            else:
                file_type = '-'
            
            # Get file permissions
            permissions = ''
            permissions += 'r' if file_stat.st_mode & 0o400 else '-'    
            permissions += 'w' if file_stat.st_mode & 0o200 else '-'
            permissions += 'x' if file_stat.st_mode & 0o100 else '-'
            permissions += 'r' if file_stat.st_mode & 0o40 else '-'
            permissions += 'w' if file_stat.st_mode & 0o20 else '-'
            permissions += 'x' if file_stat.st_mode & 0o10 else '-'
            permissions += 'r' if file_stat.st_mode & 0o4 else '-'     
            permissions += 'w' if file_stat.st_mode & 0o2 else '-'     
            permissions += 'x' if file_stat.st_mode & 0o1 else '-'     

            file_size = file_stat.st_size

            mod_time = time.localtime(file_stat.st_mtime)
            mod_time_str = time.strftime("%b %d %H:%M", mod_time) 

            return {
                'type': file_type,
                'permissions': permissions,
                'size': file_size,
                'size_hr': self.make_size_human_readable(file_size),
                'mod_time': mod_time_str,
                'name': file
            }
        except FileNotFoundError:
            print(f"Error: The file '{full_path}' does not exist.")
            return None
        
    def list_files(self):
        """List files in the current directory"""
        try:
            all_items = os.listdir(self.location)
            
            items_to_show = []
            for item in all_items:
                if self.show_all or not item.startswith('.'):
                    items_to_show.append(item)
            
            items_to_show.sort()
            
            if self.long_format:
                for item in items_to_show:
                    info = self.fetch_file_info(item)
                    if info:
                        if self.human_readable:
                            print(f"{info['type']}{info['permissions']} {info['size_hr']} {info['mod_time']} {info['name']}")
                        else:
                            print(f"{info['type']}{info['permissions']} {info['size']:8d} {info['mod_time']} {info['name']}")
            else:
                for item in items_to_show:
                    print(item)
                
            print(f"\nTotal: {len(items_to_show)} items")
                
        except FileNotFoundError:
            print(f"Directory '{self.location}' not found")
        except PermissionError:
            print(f"Permission denied to access '{self.location}'")    

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Python implementation of Unix ls command")
        parser.add_argument('-a', '--all', action='store_true', help='Include hidden files')
        parser.add_argument('-l', '--long', action='store_true', help='Use a long listing format')
        parser.add_argument('-H', '--human-Readable', action='store_true', help='Print human-readable sizes')
        parser.add_argument('path', nargs='?', default='.', help='Directory to list (default: current directory)')
        args = parser.parse_args()
        
        my_ls = PyLS()
        my_ls.location = args.path
        my_ls.show_all = args.all
        my_ls.long_format = args.long
        my_ls.human_readable = args.human_readable

        my_ls.list_files()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)