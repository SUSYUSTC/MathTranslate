import chardet


def get_file_encoding(filename):
    """
    This function takes a filename as input and returns the encoding of the file.
    The function reads the file in binary mode, detects the encoding using chardet library,
    and returns the detected encoding as a string.
    
    :param filename: A string representing the path of the file to be read
    :return: A string representing the encoding of the file
    """
    with open(filename, "rb") as f:
        data = f.read()
        result = chardet.detect(data)
        current_encoding = result["encoding"]
    return current_encoding
