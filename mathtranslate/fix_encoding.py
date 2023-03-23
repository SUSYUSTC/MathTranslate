import os
import chardet


def fix_file_encoding(filename, target_encoding="UTF-8"):
    """
    Fixes the encoding of a file with Chinese characters.
    """
    # detect the current encoding of the file
    with open(filename, "rb") as f:
        data = f.read()
        result = chardet.detect(data)
        current_encoding = result["encoding"]
    if current_encoding is None:
        print(f"Error: Could not detect encoding for {filename}")
        return
    if current_encoding.upper() == target_encoding.upper():
        return
    # read the file in the current encoding and write it back in the target encoding
    with open(filename, "r", encoding=current_encoding, errors="replace") as f:
        text = f.read()
    with open(filename, "w", encoding=target_encoding) as f:
        f.write(text)
    print(f"{filename} encoding fixed from {current_encoding} to {target_encoding}.")
