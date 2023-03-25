char_limit = 2000


def is_connected(line_above, line_below):
    if len(line_above) > 0 and len(line_below) > 0:
        if line_above[-1] != '.' and line_below[0].islower():
            return True
    return False


def connect_paragraphs(text):
    text_split = text.split('\n')
    i = 0
    while i < len(text_split) - 1:
        line_above = text_split[i]
        line_below = text_split[i + 1]
        if is_connected(line_above, line_below):
            text_split[i] = text_split[i] + text_split[i + 1]
            del text_split[i + 1]
        else:
            i += 1
    return '\n'.join(text_split)


def get_first_word(line):
    words = line.split(' ')
    for word in words:
        if len(word) > 0:
            return word
    return ''


def argmax(array):
    return array.index(max(array))


def split_paragraphs(text):
    text_split = []
    for paragraph in text.split('\n'):
        if len(paragraph) > char_limit:
            lines = paragraph.split('.')
            first_words = [get_first_word(line) for line in lines]
            first_length = [len(word) if (len(word) > 0 and word[0].isupper()) else 0 for word in first_words]
            first_length[0] = 0
            position = argmax(first_length)
            par1 = split_paragraphs('.'.join(lines[0:position]) + '.')
            par2 = split_paragraphs('.'.join(lines[position:]))
            text_split.extend([par1, par2])
        else:
            text_split.append(paragraph)
    return '\n'.join(text_split)


def is_title(line_above, line_below):
    if len(line_above) > 0 and len(line_below) > 0:
        if line_above[-1] != '.' and (not line_above[0].islower()) and line_below[0].isupper():
            return True
    return False


def split_titles(text):
    text_split = text.split('\n')
    i = 0
    while i < len(text_split) - 1:
        line_above = text_split[i]
        line_below = text_split[i + 1]
        if is_title(line_above, line_below):
            text_split[i] = '\n\n' + text_split[i] + '\n\n'
        i += 1
    return '\n'.join(text_split)
