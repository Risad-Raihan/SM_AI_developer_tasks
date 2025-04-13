from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
from langchain_core.outputs import Generation, LLMResult
import requests
import json
import asyncio

class GeminiLLM(LLM):
    gemini_api_key: str
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.5
    max_tokens: int = 512
    
    @property
    def _llm_type(self) -> str:
        return "gemini"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.gemini_api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        if self.temperature is not None:
            data["generationConfig"] = {"temperature": self.temperature}
        
        if self.max_tokens is not None:
            if "generationConfig" not in data:
                data["generationConfig"] = {}
            data["generationConfig"]["maxOutputTokens"] = self.max_tokens
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code != 200:
            raise ValueError(f"Error from Gemini API: {response.text}")
        
        response_json = response.json()
        
        try:
            generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            return generated_text
        except (KeyError, IndexError) as e:
            raise ValueError(f"Unexpected response format from Gemini API: {str(e)}")
            
    async def agenerate(self, prompts: List[str], stop: Optional[List[str]] = None) -> LLMResult:
        """Generate text asynchronously using Gemini API."""
        # Since we don't have native async support, we'll use asyncio.to_thread
        # to run the synchronous method in a separate thread
        generations = []
        for prompt in prompts:
            text = await asyncio.to_thread(self._call, prompt, stop)
            generations.append([Generation(text=text)])
        
        return LLMResult(generations=generations)
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        } 