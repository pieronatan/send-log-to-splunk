import re


def split_by_space_with_quotes(line):
    pattern = r'("[^"]+"|\S+)'
    return re.findall(pattern, line)
