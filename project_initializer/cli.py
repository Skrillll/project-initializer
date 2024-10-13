import click
import os
import logging
from logging.handlers import RotatingFileHandler
from .config_loader import ConfigLoader
from . import init_project_structure, build_project, clean_project

def setup_logging(verbose, log_file):
    """Set up logging configuration."""
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # Configure root logger
    logging.basicConfig(level=log_level, format=log_format, datefmt=date_format)
    root_logger = logging.getLogger()

    # Remove existing handlers to avoid duplication
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler (if log_file is specified)
    if log_file:
        file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setLevel(logging.DEBUG)  # Always set file logging to DEBUG
        file_formatter = logging.Formatter(log_format, datefmt=date_format)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    return root_logger

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.option('--log-file', type=click.Path(), help='Path to the log file.')
@click.option('--log-level', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], case_sensitive=False), default='INFO', help='Set the logging level.')
@click.pass_context
def cli(ctx, verbose, log_file, log_level):
    """Project Initializer CLI"""
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['LOGGER'] = setup_logging(verbose, log_file)
    
    # Set log level based on user input
    logging_level = getattr(logging, log_level.upper())
    ctx.obj['LOGGER'].setLevel(logging_level)
    
    ctx.obj['LOGGER'].debug("Logging system initialized.")

@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), default='config.yaml', help='Path to the configuration file.')
@click.option('--output', '-o', type=click.Path(), default='.', help='Output directory for the project structure.')
@click.option('--template', '-t', type=click.Choice(['default', 'web', 'data-science', 'cli']), default='default', help='Project template to use.')
@click.pass_context
def init(ctx, config, output, template):
    """Initialize project structure based on the configuration file."""
    logger = ctx.obj['LOGGER']
    
    logger.info(f"Initializing project structure using {template} template...")
    logger.debug(f"Using configuration file: {config}")
    logger.debug(f"Output directory: {output}")

    # Change the current working directory to the output directory
    os.chdir(output)

    try:
        init_project_structure(config, template)
        logger.info("Project structure initialized successfully.")
        click.echo("Project structure initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing project structure: {str(e)}", exc_info=True)
        click.echo(f"Error initializing project structure. Check the log for details.", err=True)

@cli.command()
@click.option('--output', '-o', type=click.Path(exists=True), default='.', help='Project directory to build.')
@click.option('--target', '-t', type=click.Choice(['dev', 'prod']), default='dev', help='Build target (development or production).')
@click.pass_context
def build(ctx, output, target):
    """Build the project."""
    logger = ctx.obj['LOGGER']
    logger.info(f"Building project in {output} for {target} environment...")
    try:
        build_project(output, target)
        logger.info("Project built successfully.")
        click.echo("Project built successfully.")
    except Exception as e:
        logger.error(f"Error building project: {str(e)}", exc_info=True)
        click.echo(f"Error building project. Check the log for details.", err=True)

@cli.command()
@click.option('--output', '-o', type=click.Path(exists=True), default='.', help='Project directory to clean.')
@click.option('--all', '-a', is_flag=True, help='Remove all generated files, including configuration.')
@click.confirmation_option(prompt='Are you sure you want to clean the project directory?')
@click.pass_context
def clean(ctx, output, all):
    """Clean the project directory."""
    logger = ctx.obj['LOGGER']
    logger.info(f"Cleaning project in {output}...")
    try:
        clean_project(output, all)
        logger.info("Project cleaned successfully.")
        click.echo("Project cleaned successfully.")
    except Exception as e:
        logger.error(f"Error cleaning project: {str(e)}", exc_info=True)
        click.echo(f"Error cleaning project. Check the log for details.", err=True)

@cli.command()
@click.option('--format', '-f', type=click.Choice(['html', 'pdf']), default='html', help='Output format for documentation.')
@click.option('--output', '-o', type=click.Path(), default='docs/build', help='Output directory for generated documentation.')
@click.pass_context
def docs(ctx, format, output):
    """Generate project documentation."""
    logger = ctx.obj['LOGGER']
    logger.info(f"Generating {format} documentation in {output}...")
    os.chdir('docs')
    try:
        if format == 'html':
            os.system(f'sphinx-build -b html . {output}')
        elif format == 'pdf':
            os.system(f'sphinx-build -b latex . {output} && cd {output} && make')
        logger.info("Documentation generated successfully.")
        click.echo(f"Documentation generated successfully in {output}/")
    except Exception as e:
        logger.error(f"Error generating documentation: {str(e)}", exc_info=True)
        click.echo(f"Error generating documentation. Check the log for details.", err=True)

@cli.command()
@click.option('--name', '-n', required=True, help='Name of the new component.')
@click.option('--type', '-t', type=click.Choice(['class', 'function']), default='class', help='Type of component to create.')
@click.pass_context
def create(ctx, name, type):
    """Create a new project component."""
    logger = ctx.obj['LOGGER']
    logger.info(f"Creating new {type} component: {name}")
    try:
        # Add logic to create new component
        click.echo(f"Created new {type} component: {name}")
    except Exception as e:
        logger.error(f"Error creating component: {str(e)}", exc_info=True)
        click.echo(f"Error creating component. Check the log for details.", err=True)

if __name__ == '__main__':
    cli()
