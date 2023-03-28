import chardet


def get_file_encoding(filename):
    with open(filename, "rb") as f:
        data = f.read()
        result = chardet.detect(data)
        current_encoding = result["encoding"]
    return current_encoding
