#!/usr/bin/env python3
# CELLO Evaluation Framework - Base Provider Interface
# Apache 2.0 License

from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    """Base class for LLM providers"""
    
    def __init__(self, model_config):
        self.model_config = model_config
        self.model_id = model_config['model_id']
        self.name = model_config['name']
    
    @abstractmethod
    def transpile(self, c_code, prompt_template):
        """Transpile C code to Rust using the LLM"""
        pass
    
    def extract_rust_code(self, response_text):
        """Extract Rust code from markdown code blocks"""
        if "```rust" in response_text:
            start = response_text.find("```rust") + 7
            end = response_text.find("```", start)
            return response_text[start:end].strip()
        return response_text.strip()
