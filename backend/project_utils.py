import os
import datetime

def find_last_project(scan_directory: str) -> str | None:
    """
    Scans the first level of subdirectories in a given path and returns
    the one with the most recent modification time.

    Args:
        scan_directory: The absolute path to the directory to scan (e.g., "/Users/sahil/Documents/dev").

    Returns:
        The path of the most recently modified subdirectory, or None if not found.
    """
    latest_time = 0
    latest_project_path = None

    # Ensure the scan directory exists
    if not os.path.isdir(scan_directory):
        print(f"Error: Scan directory '{scan_directory}' not found.")
        return None

    # Iterate over items in the scan directory
    for item in os.scandir(scan_directory):
        if item.is_dir():
            try:
                # Get the modification time of the directory
                mod_time = item.stat().st_mtime
                if mod_time > latest_time:
                    latest_time = mod_time
                    latest_project_path = item.path
            except OSError:
                # Ignore directories we can't access
                continue
    
    return latest_project_path