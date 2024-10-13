# Directory: project_initializer/
# File: directory_manager.py

import os
import logging

class DirectoryManager:
    def __init__(self, directories, logger=None):
        self.directories = directories
        self.logger = logger or logging.getLogger(__name__)

    def create_directories(self):
        self.logger.info(f"Creating {len(self.directories)} directories")
        for directory in self.directories:
            self.create_directory(directory)

    def create_directory(self, path):
        try:
            os.makedirs(path, exist_ok=True)
            self.logger.debug(f"Created directory: {path}")
        except PermissionError as e:
            self.logger.error(f"Permission denied when creating directory {path}: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error creating directory {path}: {str(e)}")
            raise
