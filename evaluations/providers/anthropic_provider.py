#!/usr/bin/env python3
# CELLO Evaluation Framework - Anthropic Provider
# Apache 2.0 License

import os
import anthropic
from .base_provider import BaseLLMProvider

class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude provider"""
    
    def __init__(self, model_config):
        super().__init__(model_config)
        api_key = os.getenv(model_config['api_key_env'])
        if not api_key:
            raise ValueError(f"API key not found: {model_config['api_key_env']}")
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def transpile(self, c_code, prompt_template):
        """Transpile C code to Rust using Claude"""
        prompt = prompt_template.format(c_code=c_code)
        
        message = self.client.messages.create(
            model=self.model_id,
            max_tokens=self.model_config.get('max_tokens', 4000),
            temperature=self.model_config.get('temperature', 0.1),
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        response_text = message.content[0].text
        return self.extract_rust_code(response_text)
