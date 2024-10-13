# Directory: project_initializer/
# File: directory_manager.py

import os

class DirectoryManager:
    def __init__(self, directories):
        self.directories = directories

    def create_directories(self):
        for directory in self.directories:
            self.create_directory(directory)

    @staticmethod
    def create_directory(path):
        os.makedirs(path, exist_ok=True)