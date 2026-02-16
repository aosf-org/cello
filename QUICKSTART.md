# CELLO Quick Start

Get CELLO running in 5 minutes.

## View the Website

**Option 1: View Online**
```
https://aosf-org.github.io/cello/
```

**Option 2: View Locally**
```bash
git clone https://github.com/aosf-org/cello.git
cd cello
open index.html
```

## Reproduce Evaluations (Optional)

### Prerequisites

- Python 3.10+
- Rust toolchain (rustc 1.93+)
- API keys for LLM providers

### Setup

**1. Install Rust:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
rustc --version
```

**2. Install Python Dependencies:**
```bash
cd evaluations
pip install -r requirements.txt
```

**3. Configure API Keys:**
```bash
cp .env.example .env
# Edit .env and add your API keys (NEVER commit this file!)
```

### Run Evaluations

**Run everything:**
```bash
python run_evaluation.py --all
```

**Run specific combinations:**
```bash
# One model on all projects
python run_evaluation.py --model claude-sonnet-4.5

# All models on one project  
python run_evaluation.py --project buffer

# Specific combination
python run_evaluation.py --model gemini-2.0-flash --project string_utils

# Preview what would run
python run_evaluation.py --dry-run
```

### View Results

Results are saved to `../results/` as timestamped JSON files.

For detailed instructions, see [EVALUATION.md](EVALUATION.md).

## Add New Models or Projects

**Add a new model** (no code changes):
```yaml
# Edit config/models.yaml
gpt-4o:
  name: "GPT-4o"
  provider: openai
  model_id: "gpt-4o"
  api_key_env: "OPENAI_API_KEY"
  enabled: true
```

**Add a new project:**
1. Add C file to `test-projects/c/my_project.c`
2. Edit `config/projects.yaml` with project details

That's it! The framework is fully config-driven.

## Next Steps

- 📖 Read [EVALUATION.md](EVALUATION.md) for detailed evaluation guide
- 📊 Browse [detailed reports](https://aosf-org.github.io/cello/reports/)
- 🤝 Contribute: [GitHub Issues](https://github.com/aosf-org/cello/issues)

## Questions?

See the full [README.md](README.md) or open an issue on GitHub.
