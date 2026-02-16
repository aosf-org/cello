#!/usr/bin/env python3
"""
CELLO Evaluation Framework - Main CLI
Apache 2.0 License

Usage:
    python run_evaluation.py --all
    python run_evaluation.py --model claude-sonnet-4.5 --project buffer
    python run_evaluation.py --dry-run
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from framework.config_loader import get_enabled_models, get_enabled_projects, get_evaluation_config
from providers.anthropic_provider import AnthropicProvider
from providers.google_provider import GoogleProvider

# Import evaluation logic from cello-eval
cello_eval_path = Path.home() / ".openclaw/workspace/cello-eval/evaluations"
sys.path.insert(0, str(cello_eval_path))

# Import existing evaluation modules
from transpile_and_evaluate import TranspilationEvaluator

def get_provider(model_id, model_config):
    """Get the appropriate provider for a model"""
    provider_type = model_config['provider']
    
    if provider_type == 'anthropic':
        return AnthropicProvider(model_config)
    elif provider_type == 'google':
        return GoogleProvider(model_config)
    else:
        raise ValueError(f"Unknown provider: {provider_type}")

def run_evaluation(model_id, model_config, project_id, project_config, eval_config, output_dir):
    """Run evaluation for a specific model+project combination"""
    
    print(f"\n{'='*60}")
    print(f"Evaluating: {model_config['name']} on {project_config['name']}")
    print(f"{'='*60}\n")
    
    # Load C code (resolve path relative to cello root)
    cello_root = Path(__file__).parent.parent
    c_file = cello_root / project_config['source_file']
    if not c_file.exists():
        print(f"❌ Source file not found: {c_file}")
        return None
    
    c_code = c_file.read_text()
    
    # Get provider and transpile
    try:
        provider = get_provider(model_id, model_config)
        prompt_template = eval_config['transpilation']['prompt_template']
        
        print(f"🤖 Transpiling with {model_config['name']}...")
        rust_code = provider.transpile(c_code, prompt_template)
        
        # Evaluate using existing logic
        evaluator = TranspilationEvaluator(c_file)
        scores = evaluator.evaluate_rust_code(rust_code)
        
        result = {
            "project": project_id,
            "model": model_id,
            "model_name": model_config['name'],
            "timestamp": datetime.now().isoformat(),
            "c_code_size": len(c_code),
            "rust_code": rust_code,
            "rust_code_size": len(rust_code),
            "scores": scores
        }
        
        # Save result
        output_file = output_dir / f"{project_id}_{model_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        import json
        output_file.write_text(json.dumps(result, indent=2))
        
        print(f"✅ Evaluation complete: {scores['total']}/100")
        print(f"💾 Results saved to: {output_file}\n")
        
        return result
        
    except Exception as e:
        print(f"❌ Evaluation failed: {e}\n")
        import traceback
        traceback.print_exc()
        return None

def main():
    parser = argparse.ArgumentParser(description="CELLO Evaluation Framework")
    parser.add_argument("--model", help="Specific model to evaluate")
    parser.add_argument("--project", help="Specific project to evaluate")
    parser.add_argument("--all", action="store_true", help="Evaluate all enabled models/projects")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be evaluated")
    parser.add_argument("--output-dir", default="../results", help="Output directory")
    
    args = parser.parse_args()
    
    # Load configurations
    config_dir = Path(__file__).parent.parent / "config"
    models = get_enabled_models(config_dir)
    projects = get_enabled_projects(config_dir)
    eval_config = get_evaluation_config(config_dir)
    
    # Determine what to evaluate
    if args.all or (not args.model and not args.project):
        models_to_run = models
        projects_to_run = projects
    else:
        models_to_run = {args.model: models[args.model]} if args.model and args.model in models else models
        projects_to_run = {args.project: projects[args.project]} if args.project and args.project in projects else projects
    
    # Dry run
    if args.dry_run:
        print("🔍 Dry run - would evaluate:")
        for project_id in projects_to_run:
            for model_id in models_to_run:
                print(f"  - {models_to_run[model_id]['name']} on {projects_to_run[project_id]['name']}")
        return
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run evaluations
    results = []
    for project_id, project_config in projects_to_run.items():
        for model_id, model_config in models_to_run.items():
            result = run_evaluation(model_id, model_config, project_id, project_config, eval_config, output_dir)
            if result:
                results.append(result)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"EVALUATION SUMMARY")
    print(f"{'='*60}\n")
    print(f"Completed: {len(results)} evaluations")
    print(f"Results saved to: {output_dir}\n")

if __name__ == "__main__":
    main()
