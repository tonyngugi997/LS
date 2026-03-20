import shutil
import os

if os.name == "nt":
    os.system("")




def get_terminal_width(default_width=80):
    """Get the current terminal width"""
    try:
        columns, _ = shutil.get_terminal_size()
        return columns
    except:
        return default_width
    

def format_columns(items, path=".", use_color=True):
    """Format items into columns with optional colors"""
    if not items:
        return

    # Get terminal width
    width = get_terminal_width()

    # Calculate visible length of each item (without color codes)
    def visible_length(text):
        """Remove ANSI color codes to get visible length"""
        import re
        return len(re.sub(r'\x1b\[[0-9;]*m', '', text))
    
    # Create colored items if needed
    colored_items = []
    for item in items:
        if use_color:
            color = get_color_for_file(path, item)
            colored_items.append(f"{color}{item}{Colors.RESET}")
        else:
            colored_items.append(item)
    
    # Find longest visible length
    if use_color:
        max_len = max(visible_length(item) for item in colored_items)
    else:
        max_len = max(len(item) for item in items)
    
    # Calculate how many columns fit
    col_width = max_len + 2  # Add 2 spaces between columns
    num_cols = max(1, width // col_width)
    
    # Calculate rows needed
    num_rows = (len(colored_items) + num_cols - 1) // num_cols
    
    # Print in columns
    for row in range(num_rows):
        line = ""
        for col in range(num_cols):
            idx = row + col * num_rows
            if idx < len(colored_items):
                item = colored_items[idx]
                # Calculate how much padding needed based on visible length
                if use_color:
                    visible_len = visible_length(item)
                    padding = max_len - visible_len
                    line += item + " " * (padding + 2)
                else:
                    line += item.ljust(max_len + 2)
        print(line.rstrip())


# Color codes for terminal output
class Colors:
    RESET = '\033[0m'
    BLUE = '\033[34m'      # Directories
    GREEN = '\033[32m'      # Executables
    CYAN = '\033[36m'       # Symlinks
    WHITE = '\033[37m'      # Regular files
    YELLOW = '\033[33m'     # Devices/other
    RED = '\033[31m'        # Archives/compressed

def get_color_for_file(path, filename):
    """Return color code based on file type"""
    full_path = os.path.join(path, filename)
    
    if os.path.isdir(full_path):
        return Colors.BLUE
    elif os.path.islink(full_path):
        return Colors.CYAN
    elif os.access(full_path, os.X_OK):
        return Colors.GREEN
    else:
        # Check for common compressed files
        if filename.endswith(('.gz', '.bz2', '.xz', '.zip', '.tar', '.rar')):
            return Colors.RED
        return Colors.WHITE
        