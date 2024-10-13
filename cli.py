import click
import os
import logging
from .config_loader import ConfigLoader
from . import init_project_structure

def setup_logging(verbose, log_file):
    """Set up logging configuration."""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    root_logger.addHandler(console_handler)

    # File handler (if log_file is specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        file_handler.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)

    return root_logger

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
@click.pass_context
def init(ctx, config, output):
    """Initialize project structure based on the configuration file."""
    logger = ctx.obj['LOGGER']
    
    logger.info("Initializing project structure...")
    logger.debug(f"Using configuration file: {config}")
    logger.debug(f"Output directory: {output}")

    # Change the current working directory to the output directory
    os.chdir(output)

    try:
        init_project_structure(config)
        logger.info("Project structure initialized successfully.")
        click.echo("Project structure initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing project structure: {str(e)}", exc_info=True)
        click.echo(f"Error initializing project structure. Check the log for details.", err=True)

@cli.command()
@click.option('--output', '-o', type=click.Path(exists=True), default='.', help='Project directory to build.')
@click.pass_context
def build(ctx, output):
    """Build the project."""
    logger = ctx.obj['LOGGER']
    logger.info(f"Building project in {output}...")
    # Add your build logic here
    logger.info("Project built successfully.")
    click.echo("Project built successfully.")

@cli.command()
@click.option('--output', '-o', type=click.Path(exists=True), default='.', help='Project directory to clean.')
@click.confirmation_option(prompt='Are you sure you want to clean the project directory?')
@click.pass_context
def clean(ctx, output):
    """Clean the project directory."""
    logger = ctx.obj['LOGGER']
    logger.info(f"Cleaning project in {output}...")
    # Add your cleaning logic here
    logger.info("Project cleaned successfully.")
    click.echo("Project cleaned successfully.")

@cli.command()
@click.pass_context
def docs(ctx):
    """Generate project documentation."""
    logger = ctx.obj['LOGGER']
    logger.info("Generating documentation...")
    os.chdir('docs')
    os.system('make html')
    logger.info("Documentation generated successfully.")
    click.echo("Documentation generated successfully in docs/build/html/")

if __name__ == '__main__':
    cli()
