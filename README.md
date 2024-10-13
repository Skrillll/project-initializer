# Project Initializer

Project Initializer is a powerful command-line tool designed to streamline the process of setting up new project structures. It allows users to define project templates and quickly initialize new projects based on these templates.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Development](#development)
- [Project Structure](#project-structure)
- [Security](#security)
- [Continuous Integration and Deployment](#continuous-integration-and-deployment)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Features

- Initialize project structures based on YAML configuration files
- Flexible directory and file creation
- User-friendly command-line interface
- Verbose mode for detailed logging
- Build and clean project commands
- Generate project documentation
- Create new project components
- Automated testing and security checks

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed on your system
- pip (Python package installer)
- Git (for version control and installation from GitHub)

## Installation

You can install Project Initializer using pip:

```bash
pip install git+https://github.com/skrillll/project-initializer.git
```

For development purposes, clone the repository and install in editable mode:

```bash
git clone https://github.com/skrillll/project-initializer.git
cd project-initializer
pip install -e .
```

## Usage

### Initializing a Project

To initialize a new project structure:

```bash
project-initializer init --config path/to/config.yaml --output path/to/project
```

Options:
- `--config`, `-c`: Path to the configuration file (default: config.yaml)
- `--output`, `-o`: Output directory for the project structure (default: current directory)
- `--template`, `-t`: Project template to use (choices: default, web, data-science, cli; default: default)

### Building a Project

To build a project:

```bash
project-initializer build --output path/to/project
```

Options:
- `--output`, `-o`: Project directory to build (default: current directory)
- `--target`, `-t`: Build target (choices: dev, prod; default: dev)

### Cleaning a Project

To clean a project:

```bash
project-initializer clean --output path/to/project
```

Options:
- `--output`, `-o`: Project directory to clean (default: current directory)
- `--all`, `-a`: Remove all generated files, including configuration

### Global Options

These options can be used with any command:

- `--verbose`, `-v`: Enable verbose mode for detailed logging
- `--log-file`: Specify a file for logging output
- `--log-level`: Set the logging level (choices: DEBUG, INFO, WARNING, ERROR, CRITICAL; default: INFO)

For more detailed usage instructions, refer to the [CLI documentation](docs/cli.md).

## Configuration

Project structures are defined using YAML configuration files. Here's an example:

```yaml
directories:
  - src
  - tests
  - docs

files:
  - path: src/__init__.py
    content: "# Main package"
  - path: README.md
    content: "# My New Project\n\nThis is a new project."
```

For more complex configuration examples, refer to the `examples/` directory in the repository.

## Development

To set up the development environment:

1. Clone the repository:
   ```bash
   git clone https://github.com/skrillll/project-initializer.git
   cd project-initializer
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. Run tests:
   ```bash
   make test
   ```

5. Run linter:
   ```bash
   make lint
   ```

6. Format code:
   ```bash
   make format
   ```

7. Run security scan:
   ```bash
   make security-check
   ```

8. Run all checks:
   ```bash
   make check
   ```

For more detailed information on the development process, refer to the [SETUP_NOTES.md](SETUP_NOTES.md) file.

## Project Structure

```
project-initializer/
├── .github/
│   └── workflows/
│       └── ci_cd.yml
├── docs/
│   └── ...
├── project_initializer/
│   ├── __init__.py
│   ├── cli.py
│   └── ...
├── scripts/
│   └── security_check.py
├── tests/
│   └── test_project_initializer.py
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
├── SECURITY.md
├── SETUP_NOTES.md
├── requirements.txt
├── requirements-dev.txt
└── setup.py
```

For a detailed explanation of the project structure, see [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md).

## Security

We take the security of this project seriously. If you discover a security vulnerability, please follow the guidelines in our [Security Policy](SECURITY.md).

Key security features:
- Regular security scans using Bandit, Safety, and Pip-audit
- Automated security checks in CI/CD pipeline
- Secure coding practices enforced through linting and code reviews

To run a local security check, use:
```bash
make security-check
```

## Continuous Integration and Deployment

This project uses GitHub Actions for continuous integration and deployment. The workflow is defined in [.github/workflows/ci_cd.yml](.github/workflows/ci_cd.yml) and includes:

- Automated testing on multiple Python versions
- Linting and code formatting checks
- Security scans
- Automated builds and deployments to PyPI (for releases)

For more details on the CI/CD process, refer to the [CI_CD_NOTES.md](docs/CI_CD_NOTES.md) file.

## Contributing

We welcome contributions to the Project Initializer! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have any questions, please [open an issue](https://github.com/skrillll/project-initializer/issues) on our GitHub repository.

For more detailed guides and documentation, check out the `docs/` directory in the repository.

## Additional Resources

- [Makefile Guide](makefile_guide.md): Detailed explanation of the Makefile and available commands.
- [pyproject.toml](pyproject.toml): Configuration file for Python packaging and tools.
- [requirements.txt](requirements.txt): List of production dependencies.
- [requirements-dev.txt](requirements-dev.txt): List of development dependencies.

Remember to review and update the [SETUP_NOTES.md](SETUP_NOTES.md) file as your project evolves!

## Development Setup

### Line Endings

This project uses LF (Unix-style) line endings. Please configure your Git client as follows:

- For Windows: `git config --global core.autocrlf true`
- For Unix/Linux: `git config --global core.autocrlf input`

We also use a `.gitattributes` file to enforce consistent line endings. Please do not modify this file without team discussion.
