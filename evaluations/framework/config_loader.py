#!/usr/bin/env python3
# CELLO Evaluation Framework - Configuration Loader
# Apache 2.0 License

import yaml
from pathlib import Path

def load_config(config_path):
    """Load YAML configuration file"""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(path) as f:
        return yaml.safe_load(f)

def get_enabled_models(config_dir="../config"):
    """Get all enabled models from models.yaml"""
    models_config = load_config(f"{config_dir}/models.yaml")
    return {k: v for k, v in models_config['models'].items() if v.get('enabled', True)}

def get_enabled_projects(config_dir="../config"):
    """Get all enabled projects from projects.yaml"""
    projects_config = load_config(f"{config_dir}/projects.yaml")
    return {k: v for k, v in projects_config['projects'].items() if v.get('enabled', True)}

def get_evaluation_config(config_dir="../config"):
    """Get evaluation configuration"""
    return load_config(f"{config_dir}/evaluation.yaml")
