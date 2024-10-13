# Directory: project_initializer/
# File: file_manager.py

import os

class FileManager:
    def __init__(self, files):
        self.files = files

    def create_files(self):
        for file in self.files:
            self.create_file(file['path'], file.get('content', ''))

    @staticmethod
    def create_file(path, content=''):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)