#!/usr/bin/env python3
# CELLO Evaluation Framework - Google Gemini Provider
# Apache 2.0 License

import os
import google.generativeai as genai
from .base_provider import BaseLLMProvider

class GoogleProvider(BaseLLMProvider):
    """Google Gemini provider"""
    
    def __init__(self, model_config):
        super().__init__(model_config)
        api_key = os.getenv(model_config['api_key_env'])
        if not api_key:
            raise ValueError(f"API key not found: {model_config['api_key_env']}")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.model_id)
    
    def transpile(self, c_code, prompt_template):
        """Transpile C code to Rust using Gemini"""
        prompt = prompt_template.format(c_code=c_code)
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=self.model_config.get('temperature', 0.1),
            )
        )
        
        response_text = response.text
        return self.extract_rust_code(response_text)
