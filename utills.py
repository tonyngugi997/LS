import shutil

def get_terminal_width(default_width=80):
    """Get the current terminal width"""
    try:
        columns, _ = shutil.get_terminal_size()
        return columns
    except:
        return default_width
    
def format_columns(items):
    """Format items into columns"""
    if not items:
        return

    # Get terminal width
    width = get_terminal_width()

    # Find longest filename
    max_len = max(len(item) for item in items)

    # Calculate how many columns fit
    col_width = max_len + 2  # Add 2 spaces between columns
    num_cols = max(1, width // col_width)

    # Calculate rows needed
    num_rows = (len(items) + num_cols - 1) // num_cols

    # Print in columns
    for row in range(num_rows):
        line = ""
        for col in range(num_cols):
            idx = row + col * num_rows
            if idx < len(items):
                line += items[idx].ljust(max_len + 2)
        print(line.rstrip())
        