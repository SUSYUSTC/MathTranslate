import charset_normalizer
force_utf8 = False


def get_file_encoding(filename):
    """
    This function takes a filename as input and returns the encoding of the file.
    The function reads the file in binary mode, detects the encoding using charset_normalizer library,
    and returns the detected encoding as a string.

    :param filename: A string representing the path of the file to be read
    :return: A string representing the encoding of the file
    """
    if force_utf8:
        return 'utf-8'
    else:
        with open(filename, "rb") as f:
            data = f.read()
            result = charset_normalizer.detect(data)
            current_encoding = result["encoding"]
            if result['confidence'] < 0.9:
                print(f'file {filename} may have wrong encoding')
        return current_encoding
