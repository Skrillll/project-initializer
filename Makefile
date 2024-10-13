# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := pytest
FLAKE8 := flake8
BLACK := black
SPHINX_BUILD := sphinx-build

# Determine the operating system
ifeq ($(OS),Windows_NT)
    VENV_ACTIVATE := venv\Scripts\activate
else
    VENV_ACTIVATE := . venv/bin/activate
endif

# Targets
.PHONY: all venv install install-dev test lint format clean docs build deploy

all: venv install test lint docs build

venv:
	$(PYTHON) -m venv venv

install: venv
	. $(VENV_ACTIVATE) && $(PIP) install -r requirements.txt

install-dev: venv
	. $(VENV_ACTIVATE) && $(PIP) install -r requirements-dev.txt

test: install-dev
	. $(VENV_ACTIVATE) && $(PYTEST)

lint: install-dev
	. $(VENV_ACTIVATE) && $(FLAKE8) project_initializer tests

format: install-dev
	. $(VENV_ACTIVATE) && $(BLACK) project_initializer tests

security-scan:
	bandit -r project_initializer -f custom

check: lint format security-scan

clean:
	rm -rf build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs: install-dev
	. $(VENV_ACTIVATE) && cd docs && make html

build: clean install
	. $(VENV_ACTIVATE) && $(PYTHON) setup.py sdist bdist_wheel

deploy: build
	@echo "Deploying... (Add your deployment commands here)"

# Help target
help:
	@echo "Available targets:"
	@echo "  all        : Set up environment, install dependencies, run tests, lint, build docs, and build package"
	@echo "  venv       : Create a virtual environment"
	@echo "  install    : Install project dependencies"
	@echo "  install-dev: Install development dependencies"
	@echo "  test       : Run tests"
	@echo "  lint       : Run linter"
	@echo "  format     : Format code with Black"
	@echo "  clean      : Remove build artifacts and cache files"
	@echo "  docs       : Build documentation"
	@echo "  build      : Build the package"
	@echo "  deploy     : Deploy the package (placeholder)"
	@echo "  help       : Show this help message"
