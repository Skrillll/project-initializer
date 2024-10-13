# Directory: project_initializer/
# File: __init__.py

# Import necessary modules
from .file_manager import FileManager
from .directory_manager import DirectoryManager
from .config_loader import ConfigLoader
from .cli import cli

# Initialize the project structure
def init_project_structure(config_path):
    config = ConfigLoader.load_config(config_path)
    dir_manager = DirectoryManager(config['directories'])
    file_manager = FileManager(config['files'])

    dir_manager.create_directories()
    file_manager.create_files()

    print("Advanced project structure initialized successfully.")

# Placeholder functions for build and clean operations
def build_project(directory):
    # Add your build logic here
    pass

def clean_project(directory):
    # Add your cleaning logic here
    pass

# Make the CLI and other functions available when the package is imported
__all__ = ['cli', 'init_project_structure', 'build_project', 'clean_project']
