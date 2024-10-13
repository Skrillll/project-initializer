import click
import logging
import os
from .core import init_project_structure, build_project, clean_project
from .config_loader import ConfigLoader
from .directory_manager import DirectoryManager
from .file_manager import FileManager

logger = logging.getLogger(__name__)

def setup_logging(verbose, log_file):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(file_handler)
    
    # Ensure all loggers are set to the correct level
    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).setLevel(log_level)
    
    return logger

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.option('--log-file', type=click.Path(), help='Path to the log file.')
@click.pass_context
def cli(ctx, verbose, log_file):
    """Project Initializer CLI"""
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['LOGGER'] = setup_logging(verbose, log_file)

@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), default='config.yaml', help='Path to the configuration file.')
@click.option('--output', '-o', type=click.Path(), default='.', help='Output directory for the project structure.')
@click.option('--template', '-t', type=click.Choice(['default', 'web', 'data-science', 'cli']), default='default', help='Project template to use.')
@click.pass_context
def init(ctx, config, output, template):
    """Initialize project structure based on the configuration file and template."""
    logger = ctx.obj['LOGGER']
    
    try:
        logger.info(f"Initializing project structure using {template} template...")
        logger.debug(f"Using configuration file: {config}")
        logger.debug(f"Output directory: {output}")

        # Get absolute paths
        config_abs_path = os.path.abspath(config)
        output_abs_path = os.path.abspath(output)

        # Create the output directory if it doesn't exist
        os.makedirs(output_abs_path, exist_ok=True)
        
        # Change to the output directory
        original_dir = os.getcwd()
        os.chdir(output_abs_path)

        init_project_structure(config_abs_path, template)
        logger.info(f"Project structure initialized successfully using {template} template.")
        click.echo(f"Project structure initialized successfully using {template} template.")
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config}", exc_info=True)
        click.echo(f"Error: Configuration file '{config}' not found. Please make sure the file exists and the path is correct.", err=True)
    except PermissionError:
        logger.error(f"Permission denied when creating project structure in {output}", exc_info=True)
        click.echo(f"Error: Permission denied when creating project structure. Please check your permissions for the output directory.", err=True)
    except Exception as e:
        logger.error(f"Error initializing project structure: {str(e)}", exc_info=True)
        click.echo(f"Error initializing project structure: {str(e)}", err=True)
    finally:
        # Change back to the original directory
        os.chdir(original_dir)

@cli.command()
@click.option('--config', default='config.yaml', help='Path to the configuration file')
@click.option('--output', default='.', help='Output directory for the project')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def init_project(config, output, verbose):
    """Initialize project structure based on configuration."""
    if verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.info(f"Initializing project structure using configuration from {config}")
    
    try:
        # Create the output directory if it doesn't exist
        os.makedirs(output, exist_ok=True)
        
        # Change to the output directory
        os.chdir(output)
        
        # Load configuration
        config_data = ConfigLoader.load_config(config)
        
        # Initialize managers
        dir_manager = DirectoryManager(config_data.get('directories', []))
        file_manager = FileManager(config_data.get('files', []))
        
        # Create project structure
        dir_manager.create_directories()
        file_manager.create_files()
        
        logger.info(f"Project structure initialized successfully in {output}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise click.ClickException(str(e))

@cli.command()
@click.option('--directory', '-d', type=click.Path(exists=True), default='.', help='Directory of the project to build.')
@click.option('--dry-run', is_flag=True, help='Show what would be done without making actual changes.')
@click.pass_context
def build(ctx, directory, dry_run):
    """Build the project."""
    logger = ctx.obj['LOGGER']
    logger.info(f"Building project in {directory}")
    
    if dry_run:
        click.echo("Dry run: showing what would be done without making changes.")
    
    success, actions = build_project(directory)
    
    for action in actions:
        click.echo(action)
    
    if success:
        logger.info("Project built successfully.")
        click.echo("Project built successfully.")
    else:
        logger.error("Error building project. See above for details.")
        click.echo("Error building project. See above for details.", err=True)

@cli.command()
@click.option('--directory', '-d', type=click.Path(exists=True), default='.', help='Directory of the project to clean.')
@click.option('--all', 'all_files', is_flag=True, help='Remove all generated files, including caches.')
@click.option('--dry-run', is_flag=True, help='Show what would be done without making actual changes.')
@click.confirmation_option(prompt='Are you sure you want to clean the project?')
@click.pass_context
def clean(ctx, directory, all_files, dry_run):
    """Clean the project."""
    logger = ctx.obj['LOGGER']
    logger.info(f"Cleaning project in {directory}")
    
    if dry_run:
        click.echo("Dry run: showing what would be done without making changes.")
    
    success, actions = clean_project(directory, all_files)
    
    for action in actions:
        click.echo(action)
    
    if success:
        logger.info("Project cleaned successfully.")
        click.echo("Project cleaned successfully.")
    else:
        logger.error("Error cleaning project. See above for details.")
        click.echo("Error cleaning project. See above for details.", err=True)

if __name__ == '__main__':
    cli()
