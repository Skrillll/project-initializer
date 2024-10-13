import os
import shutil
import logging
from typing import List, Tuple, Dict
from .config_loader import ConfigLoader
from .directory_manager import DirectoryManager
from .file_manager import FileManager

logger = logging.getLogger(__name__)

# Define template configurations
TEMPLATES: Dict[str, Dict] = {
    'default': {
        'directories': ['src', 'tests', 'docs'],
        'files': [
            {'path': 'src/__init__.py', 'content': '# Default template\n'},
            {'path': 'tests/__init__.py', 'content': '# Test directory\n'},
            {'path': 'docs/README.md', 'content': '# Project Documentation\n'},
            {'path': 'README.md', 'content': '# Default Project\n\nThis is a default project template.\n'},
        ]
    },
    'web': {
        'directories': ['src', 'tests', 'docs', 'static', 'templates'],
        'files': [
            {'path': 'src/__init__.py', 'content': '# Web project\n'},
            {'path': 'src/app.py', 'content': 'from flask import Flask\n\napp = Flask(__name__)\n\n@app.route("/")\ndef hello():\n    return "Hello, World!"\n'},
            {'path': 'tests/__init__.py', 'content': '# Test directory\n'},
            {'path': 'docs/README.md', 'content': '# Web Project Documentation\n'},
            {'path': 'README.md', 'content': '# Web Project\n\nThis is a web project template using Flask.\n'},
            {'path': 'requirements.txt', 'content': 'Flask==2.0.1\n'},
        ]
    },
    'data-science': {
        'directories': ['data', 'notebooks', 'src', 'tests', 'docs'],
        'files': [
            {'path': 'src/__init__.py', 'content': '# Data science project\n'},
            {'path': 'notebooks/example.ipynb', 'content': '{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 4}'},
            {'path': 'tests/__init__.py', 'content': '# Test directory\n'},
            {'path': 'docs/README.md', 'content': '# Data Science Project Documentation\n'},
            {'path': 'README.md', 'content': '# Data Science Project\n\nThis is a data science project template.\n'},
            {'path': 'requirements.txt', 'content': 'numpy==1.21.0\npandas==1.3.0\nmatplotlib==3.4.2\nscikit-learn==0.24.2\n'},
        ]
    },
    'cli': {
        'directories': ['src', 'tests', 'docs'],
        'files': [
            {'path': 'src/__init__.py', 'content': '# CLI project\n'},
            {'path': 'src/cli.py', 'content': 'import click\n\n@click.command()\ndef hello():\n    click.echo("Hello, World!")\n\nif __name__ == "__main__":\n    hello()\n'},
            {'path': 'tests/__init__.py', 'content': '# Test directory\n'},
            {'path': 'docs/README.md', 'content': '# CLI Project Documentation\n'},
            {'path': 'README.md', 'content': '# CLI Project\n\nThis is a CLI project template using Click.\n'},
            {'path': 'requirements.txt', 'content': 'click==8.0.1\n'},
        ]
    }
}

def init_project_structure(config_path: str, template: str = 'default'):
    """
    Initialize project structure based on the provided configuration file and template.

    Args:
        config_path (str): Path to the configuration file.
        template (str): Template to use for project initialization.
    """
    try:
        logger.info(f"Initializing project structure with template: {template}")
        logger.debug(f"Using configuration file: {config_path}")

        # Load configuration
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        config_data = ConfigLoader.load_config(config_path)
        logger.debug(f"Configuration loaded successfully")

        # Merge template configuration with user configuration
        template_config = TEMPLATES.get(template, TEMPLATES['default'])
        merged_config = {
            'directories': list(set(config_data.get('directories', []) + template_config['directories'])),
            'files': config_data.get('files', []) + template_config['files']
        }
        logger.debug(f"Merged configuration: {merged_config}")

        # Initialize managers
        dir_manager = DirectoryManager(merged_config['directories'], logger)
        file_manager = FileManager(merged_config['files'], logger)

        # Create project structure
        dir_manager.create_directories()
        file_manager.create_files()

        # Log summary
        logger.info(f"Created {len(merged_config['directories'])} directories and {len(merged_config['files'])} files")
        logger.info(f"Project structure initialized successfully using {template} template and configuration from {config_path}")
    except FileNotFoundError as e:
        logger.error(str(e))
        raise
    except KeyError as e:
        logger.error(f"Invalid template or configuration key: {str(e)}")
        raise
    except PermissionError as e:
        logger.error(f"Permission denied when creating project structure: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while initializing project structure: {str(e)}")
        raise

def build_project(directory: str) -> Tuple[bool, List[str]]:
    """
    Build the project in the specified directory.
    
    Args:
        directory (str): The directory of the project to build.
    
    Returns:
        Tuple[bool, List[str]]: A tuple containing a success flag and a list of actions taken.
    """
    actions = []
    try:
        logger.info(f"Building project in directory: {directory}")

        # Run setup.py if it exists
        setup_path = os.path.join(directory, 'setup.py')
        if os.path.exists(setup_path):
            logger.debug(f"Running 'python setup.py build'")
            os.system(f"python {setup_path} build")
            actions.append("Ran 'python setup.py build'")
        else:
            logger.debug("No setup.py found, skipping Python build")
            actions.append("No setup.py found, skipping Python build")
        
        # Run npm install if package.json exists
        package_json_path = os.path.join(directory, 'package.json')
        if os.path.exists(package_json_path):
            logger.debug("Running 'npm install'")
            os.system("npm install")
            actions.append("Ran 'npm install'")
        else:
            logger.debug("No package.json found, skipping npm install")
            actions.append("No package.json found, skipping npm install")
        
        logger.info("Project built successfully")
        return True, actions
    except Exception as e:
        logger.error(f"Error during project build: {str(e)}", exc_info=True)
        actions.append(f"Error: {str(e)}")
        return False, actions

def clean_project(directory: str, all_files: bool = False) -> Tuple[bool, List[str]]:
    """
    Clean the project in the specified directory.

    Args:
        directory (str): The directory of the project to clean.
        all_files (bool): If True, remove all generated files. If False, keep some cache files.

    Returns:
        Tuple[bool, List[str]]: A tuple containing a success flag and a list of actions taken.
    """
    actions = []
    try:
        logger.info(f"Cleaning project in directory: {directory}")
        logger.debug(f"Cleaning all files: {all_files}")

        dirs_to_clean = ['build', 'dist', '__pycache__']
        files_to_clean = ['*.pyc', '*.pyo', '*.pyd', '*.so']
        
        if all_files:
            dirs_to_clean.extend(['.pytest_cache', '.mypy_cache', '.tox'])
            files_to_clean.extend(['.coverage'])

        for root, dirs, files in os.walk(directory):
            for d in dirs_to_clean:
                if d in dirs:
                    dir_path = os.path.join(root, d)
                    logger.debug(f"Removing directory: {dir_path}")
                    shutil.rmtree(dir_path)
                    actions.append(f"Removed directory: {dir_path}")
            
            for pattern in files_to_clean:
                for f in files:
                    if f.endswith(pattern[1:]):
                        file_path = os.path.join(root, f)
                        logger.debug(f"Removing file: {file_path}")
                        os.remove(file_path)
                        actions.append(f"Removed file: {file_path}")

        if not actions:
            logger.info("No files or directories needed cleaning")
            actions.append("No files or directories needed cleaning")
        else:
            logger.info("Project cleaned successfully")

        return True, actions
    except PermissionError as e:
        logger.error(f"Permission denied when cleaning project: {str(e)}", exc_info=True)
        actions.append(f"Error: Permission denied - {str(e)}")
        return False, actions
    except Exception as e:
        logger.error(f"Error during project cleaning: {str(e)}", exc_info=True)
        actions.append(f"Error: {str(e)}")
        return False, actions
