import pytest
import os
import tempfile
from click.testing import CliRunner
from project_initializer.cli import cli
from project_initializer import init_project_structure, build_project, clean_project

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_init(runner):
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, 'config.yaml')
        with open(config_path, 'w') as f:
            f.write("""
            directories:
              - src
              - tests
            files:
              - path: src/__init__.py
                content: "# Main package"
              - path: README.md
                content: "# Test Project"
            """)
        
        result = runner.invoke(cli, ['init', '-c', config_path, '-o', tmpdir])
        assert result.exit_code == 0
        assert "Project structure initialized successfully." in result.output
        
        assert os.path.exists(os.path.join(tmpdir, 'src'))
        assert os.path.exists(os.path.join(tmpdir, 'tests'))
        assert os.path.exists(os.path.join(tmpdir, 'src', '__init__.py'))
        assert os.path.exists(os.path.join(tmpdir, 'README.md'))

def test_cli_build(runner):
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(cli, ['build', '-o', tmpdir])
        assert result.exit_code == 0
        assert "Project built successfully." in result.output

def test_cli_clean(runner):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a dummy file to be cleaned
        open(os.path.join(tmpdir, 'dummy.txt'), 'w').close()
        
        result = runner.invoke(cli, ['clean', '-o', tmpdir], input='y\n')
        assert result.exit_code == 0
        assert "Project cleaned successfully." in result.output
        assert not os.path.exists(os.path.join(tmpdir, 'dummy.txt'))

def test_cli_docs(runner):
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, 'docs'))
        result = runner.invoke(cli, ['docs', '-o', os.path.join(tmpdir, 'docs', 'build')])
        assert result.exit_code == 0
        assert "Documentation generated successfully" in result.output

def test_cli_create(runner):
    result = runner.invoke(cli, ['create', '-n', 'TestComponent', '-t', 'class'])
    assert result.exit_code == 0
    assert "Created new class component: TestComponent" in result.output

# Add more tests for edge cases and error handling
def test_cli_init_invalid_config(runner):
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, 'invalid_config.yaml')
        with open(config_path, 'w') as f:
            f.write("invalid: yaml: content")
        
        result = runner.invoke(cli, ['init', '-c', config_path, '-o', tmpdir])
        assert result.exit_code != 0
        assert "Error initializing project structure" in result.output

# Add tests for init_project_structure, build_project, and clean_project functions
def test_init_project_structure():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, 'config.yaml')
        with open(config_path, 'w') as f:
            f.write("""
            directories:
              - src
            files:
              - path: src/main.py
                content: "print('Hello, World!')"
            """)
        
        init_project_structure(config_path, 'default')
        
        assert os.path.exists(os.path.join(tmpdir, 'src'))
        assert os.path.exists(os.path.join(tmpdir, 'src', 'main.py'))
        with open(os.path.join(tmpdir, 'src', 'main.py'), 'r') as f:
            assert f.read() == "print('Hello, World!')"

def test_build_project():
    with tempfile.TemporaryDirectory() as tmpdir:
        build_project(tmpdir, 'dev')
        # Add assertions based on what build_project should do

def test_clean_project():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some files and directories
        os.makedirs(os.path.join(tmpdir, 'build'))
        open(os.path.join(tmpdir, 'build', 'output.txt'), 'w').close()
        
        clean_project(tmpdir, False)
        
        assert not os.path.exists(os.path.join(tmpdir, 'build'))
