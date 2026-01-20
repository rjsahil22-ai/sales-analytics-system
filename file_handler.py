import os

def read_sales_file(file_path):
    """
    Reads messy sales file with encoding issues.
    Returns list of lines.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Try multiple encodings (non-UTF8 handling)
    encodings_to_try = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]

    for enc in encodings_to_try:
        try:
            with open(file_path, "r", encoding=enc) as f:
                lines = f.read().splitlines()
            return lines
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError("Unable to decode file with common encodings")
