import os
import yaml
from pathlib import Path
import logging

def init_project_structure(config_path, template='default'):
    """Initialize project structure based on the configuration file."""
    logger = logging.getLogger(__name__)
    
    # Load configuration
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    logger.info(f"Initializing project structure using {template} template...")
    
    # Create base directories
    for directory in config.get('directories', []):
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Created directory: {directory}")
    
    # Create base files
    for file_info in config.get('files', []):
        file_path = file_info['path']
        content = file_info['content']
        
        # Replace placeholders in content
        content = content.replace('${project_name}', config.get('project_name', 'My Project'))
        
        with open(file_path, 'w') as f:
            f.write(content)
        logger.debug(f"Created file: {file_path}")
    
    # Apply template-specific configuration
    if template in config.get('templates', {}):
        template_config = config['templates'][template]
        
        # Create additional directories
        for directory in template_config.get('additional_directories', []):
            os.makedirs(directory, exist_ok=True)
            logger.debug(f"Created template directory: {directory}")
        
        # Create additional files
        for file_info in template_config.get('additional_files', []):
            file_path = file_info['path']
            content = file_info['content']
            
            # Replace placeholders in content
            content = content.replace('${project_name}', config.get('project_name', 'My Project'))
            
            with open(file_path, 'w') as f:
                f.write(content)
            logger.debug(f"Created template file: {file_path}")
    
    logger.info("Project structure initialized successfully.")
