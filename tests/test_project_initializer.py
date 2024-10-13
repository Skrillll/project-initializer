import pytest
import tempfile
import os
from project_initializer import init_project_structure, build_project, clean_project

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
