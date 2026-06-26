
import os

class Parser:
    def __init__(self):
        pass

    def get_file_type(self, file_path):
        _, ext = os.path.splitext(file_path)
        return ext.lower()

    def count_lines(self, content):
        return len(content.splitlines())
