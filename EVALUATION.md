# Running CELLO Evaluations

Complete guide to running and extending the CELLO evaluation framework.

## ⚠️ Current Status

This is a **proof-of-concept evaluation** demonstrating the methodology with:

- **2 models** (Claude Sonnet 4.5, Gemini 2.0 Flash)
- **3 test projects** (small C programs: 1.7KB - 3.3KB)
- **Real compilation** with rustc 1.93+
- **6 quality dimensions** (compilation, safety, quality, correctness, maintainability, performance)

For production use, expand to:
- More models (GPT-4o, Qwen2.5-Coder, DeepSeek, CodeLlama, etc.)
- Larger projects (1K-10K+ lines of code)
- Multiple source languages (Python, JavaScript, etc.)

---

## Prerequisites

### System Requirements

- **Python:** 3.10 or higher
- **Rust:** 1.93 or higher (with rustc and cargo)
- **Git:** For cloning the repository
- **API Keys:** For LLM providers you want to evaluate

### Install Rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
rustc --version  # Should show 1.93+
```

### Install Python Dependencies

```bash
cd evaluations
pip install -r requirements.txt
```

This installs:
- `anthropic` — Claude API client
- `google-generativeai` — Gemini API client  
- `pyyaml` — YAML configuration parser
- `python-dotenv` — Environment variable loader

---

## Configuration

### API Keys

CELLO uses environment variables for API keys (never hardcoded).

**1. Copy the template:**
```bash
cd evaluations
cp .env.example .env
```

**2. Edit `.env` with your keys:**
```bash
# Anthropic API Key (for Claude models)
# Get from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE

# Google Gemini API Key
# Get from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=YOUR_KEY_HERE

# Optional: OpenAI (for future expansion)
# OPENAI_API_KEY=sk-YOUR_KEY_HERE
```

**⚠️ IMPORTANT:** The `.env` file is git-ignored. **NEVER commit API keys to GitHub!**

### Models Configuration

Models are defined in `config/models.yaml`:

```yaml
models:
  claude-sonnet-4.5:
    name: "Claude Sonnet 4.5"
    provider: anthropic
    model_id: "claude-sonnet-4-5-20250929"
    api_key_env: "ANTHROPIC_API_KEY"
    max_tokens: 4000
    temperature: 0.1
    enabled: true
```

**To add a new model**, just add a new entry (no code changes needed).

### Projects Configuration

Test projects are defined in `config/projects.yaml`:

```yaml
projects:
  string_utils:
    name: "String Utilities"
    description: "String manipulation functions"
    source_language: c
    target_language: rust
    source_file: "test-projects/c/string_utils.c"
    complexity: low
    enabled: true
```

**To add a new project:**
1. Add source file to `test-projects/c/`
2. Add entry to `config/projects.yaml`

### Evaluation Configuration

Scoring dimensions and prompts are in `config/evaluation.yaml`:

- Scoring weights (compilation: 25%, safety: 20%, etc.)
- Compilation settings (timeout, compiler flags)
- Transpilation prompt template

---

## Running Evaluations

### Basic Usage

```bash
cd evaluations
python run_evaluation.py --all
```

This evaluates **all enabled models** on **all enabled projects**.

### Specific Combinations

**One model on all projects:**
```bash
python run_evaluation.py --model claude-sonnet-4.5
```

**All models on one project:**
```bash
python run_evaluation.py --project buffer
```

**Specific model + project:**
```bash
python run_evaluation.py --model gemini-2.0-flash --project string_utils
```

### Preview Mode

**See what would be evaluated without running:**
```bash
python run_evaluation.py --dry-run
```

Output:
```
🔍 Dry run - would evaluate:
  - Claude Sonnet 4.5 on String Utilities
  - Gemini 2.0 Flash on String Utilities
  - Claude Sonnet 4.5 on Dynamic Buffer
  ...
```

### Custom Output Directory

```bash
python run_evaluation.py --all --output-dir ../results/my-run
```

---

## Results

### Output Format

Results are saved as timestamped JSON files in `../results/`:

```
results/
├── string_utils_claude-sonnet-4.5_20260216_135252.json
├── buffer_gemini-2.0-flash_20260216_135324.json
└── ...
```

### Result Schema

Each JSON file contains:

```json
{
  "project": "buffer",
  "model": "claude-sonnet-4.5",
  "model_name": "Claude Sonnet 4.5",
  "timestamp": "2026-02-16T13:53:17.123456",
  "c_code_size": 1997,
  "rust_code": "...",
  "rust_code_size": 1976,
  "scores": {
    "compilation": 25,
    "safety": 18,
    "quality": 14,
    "correctness": 7,
    "maintainability": 3,
    "performance": 10,
    "total": 77,
    "details": { ... }
  }
}
```

---

## Evaluation Methodology

### Workflow

1. **Load C Code** — Read source file from `test-projects/`
2. **LLM Transpilation** — Send to configured LLM with standard prompt
3. **Rustc Compilation** — Verify generated code compiles
4. **Quality Scoring** — Evaluate across 6 dimensions
5. **Save Results** — Write JSON with full details

### Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| **Compilation** | 25% | Does it compile with rustc? |
| **Safety** | 20% | Memory safety (unsafe blocks, error handling) |
| **Quality** | 20% | Idiomatic Rust patterns, documentation |
| **Correctness** | 15% | Functional equivalence, edge cases, tests |
| **Maintainability** | 10% | Code organization, API clarity |
| **Performance** | 10% | Efficiency patterns (minimal cloning, references) |

**Total:** 100 points

### Compilation Verification

Uses real `rustc` compiler:

```bash
rustc --crate-type lib generated_code.rs
```

- **25 points** if compiles successfully
- **0 points** if compilation fails (with full error text captured)

### Safety Analysis

Checks for:
- ✅ No/minimal unsafe blocks
- ✅ Result types for error handling
- ✅ Option types for nullable values
- ✅ Smart pointers (Box, Rc, Arc)
- ❌ Raw pointers (`*mut`, `*const`)

### Quality Analysis

Checks for:
- ✅ snake_case naming conventions
- ✅ Documentation comments (`///`, `//!`)
- ✅ `?` operator for error propagation
- ✅ Iterator/functional patterns
- ✅ Proper type definitions (struct, enum, impl)

### Correctness Analysis

Checks for:
- ✅ Test modules (`#[cfg(test)]`)
- ✅ Edge case handling (`is_empty()`, `len()`)
- ✅ Pattern matching

### Maintainability Analysis

Checks for:
- ✅ Module organization
- ✅ Clear public API (`pub fn`, `pub struct`)
- ✅ Constants for magic values
- ✅ Type aliases for clarity

### Performance Analysis

Checks for:
- ✅ Minimal use of `.clone()`
- ✅ Reference usage (`&str`, `&[T]`)
- ❌ Excessive cloning (penalized)

---

## Extending CELLO

### Add a New Model

**1. Edit `config/models.yaml`:**

```yaml
gpt-4o:
  name: "GPT-4o"
  provider: openai
  model_id: "gpt-4o"
  api_key_env: "OPENAI_API_KEY"
  max_tokens: 4000
  temperature: 0.1
  enabled: true
```

**2. If using a new provider, create provider class:**

```python
# evaluations/providers/openai_provider.py
from .base_provider import BaseLLMProvider
import openai

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, model_config):
        super().__init__(model_config)
        # ... setup

    def transpile(self, c_code, prompt_template):
        # ... implementation
```

**3. Register provider in `run_evaluation.py`:**

```python
elif provider_type == 'openai':
    return OpenAIProvider(model_config)
```

### Add a New Project

**1. Add source file:**

```bash
# Add your C code
echo 'int add(int a, int b) { return a + b; }' > test-projects/c/calculator.c
```

**2. Edit `config/projects.yaml`:**

```yaml
calculator:
  name: "Simple Calculator"
  description: "Basic arithmetic operations"
  source_language: c
  target_language: rust
  source_file: "test-projects/c/calculator.c"
  complexity: low
  size_bytes: 42
  enabled: true
```

**3. Run:**

```bash
python run_evaluation.py --project calculator
```

### Customize Prompts

Edit `config/evaluation.yaml` to modify the transpilation prompt or scoring weights.

---

## Troubleshooting

### "API key not found"

Make sure `.env` exists and contains your keys:
```bash
cat evaluations/.env
```

### "rustc not found"

Install Rust:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### "Module not found"

Install dependencies:
```bash
pip install -r evaluations/requirements.txt
```

### Compilation Always Fails

Check if rustc is in PATH:
```bash
which rustc
rustc --version
```

---

## Best Practices

### Reproducibility

- Use specific model versions (not `latest`)
- Document environment (Python version, rustc version)
- Save all results with timestamps
- Include full compiler output in results

### Fair Comparison

- Use same temperature (0.1) for all models
- Use same prompt template
- Run multiple times to account for LLM non-determinism
- Document any model-specific parameters

### Scaling Up

For large-scale evaluations:
- Use batch processing
- Implement rate limiting for APIs
- Cache compilation results
- Parallelize evaluations (careful with API limits)

---

## Example: Full Evaluation Run

```bash
# Setup
cd evaluations
cp .env.example .env
# Edit .env with API keys

# Preview
python run_evaluation.py --dry-run

# Run full evaluation
python run_evaluation.py --all

# View results
ls -lh ../results/

# Check specific result
cat ../results/buffer_claude-sonnet-4.5_*.json | jq '.scores'
```

Expected output:
```json
{
  "compilation": 25,
  "safety": 18,
  "quality": 14,
  "correctness": 7,
  "maintainability": 3,
  "performance": 10,
  "total": 77
}
```

---

## Next Steps

- 📊 Generate reports: See report generation scripts
- 🌐 Update website: See website update instructions
- 📈 Analyze results: Compare models, identify patterns
- 🤝 Contribute: Add models, projects, or improve scoring

## Questions?

- Read the [README](README.md)
- Check [QUICKSTART](QUICKSTART.md)
- Open an [issue on GitHub](https://github.com/aosf-org/cello/issues)
