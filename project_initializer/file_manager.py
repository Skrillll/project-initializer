# Directory: project_initializer/
# File: file_manager.py

import os
import logging

class FileManager:
    def __init__(self, files, logger=None):
        self.files = files
        self.logger = logger or logging.getLogger(__name__)

    def create_files(self):
        self.logger.info(f"Creating {len(self.files)} files")
        for file in self.files:
            self.create_file(file['path'], file.get('content', ''))

    def create_file(self, path, content=''):
        try:
            if not path:
                self.logger.warning(f"Skipping file creation due to empty path")
                return

            # Handle files in the root directory
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            # Create the file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.debug(f"Created file: {path}")
        except IOError as e:
            self.logger.error(f"Error creating file {path}: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error creating file {path}: {str(e)}")
