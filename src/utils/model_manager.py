from typing import Protocol
from .logger import log
from .settings import get_config

from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek


class PredictableModel(Protocol):
    def parse(self, prompt: str) -> str:
        ...


class DeepSeekWrapper(PredictableModel):
    def __init__(self, model):
        log("Initializing DeepSeekWrapper with provided model instance")
        self.model = model

    def parse(self, prompt: str) -> str:
        log(f"DeepSeekWrapper received prompt: {prompt}")
        try:
            response = self.model.predict(prompt)
            log(f"DeepSeekWrapper response: {response}")
            return response
        except Exception as e:
            log(f"DeepSeekWrapper failed to parse prompt: {e}")
            return ""


class GroqWrapper(PredictableModel):
    def __init__(self, model):
        log("Initializing GroqWrapper with provided model instance")
        self.model = model

    def parse(self, prompt: str) -> str:
        log(f"GroqWrapper received prompt: {prompt}")
        try:
            response = self.model([HumanMessage(content=prompt)])
            log(f"GroqWrapper response: {response.content}")
            return response.content
        except Exception as e:
            log(f"GroqWrapper failed to parse prompt: {e}")
            return ""


def get_model() -> PredictableModel | None:
    log("Retrieving model configuration")

    models = get_config("models")
    if models is None:
        log("Failed to retrieve 'models' configuration")
        return None

    default_model = get_config("default_model")
    if default_model is None:
        log("Failed to retrieve 'default_model' configuration")
        return None

    log(f"Looking for default model '{default_model}' in configured models")
    model = next((x for x in models if x['name'] == default_model), None)
    if model is None:
        log(f"Default model '{default_model}' not found in configuration")
        return None

    log(f"Using model configuration: {model}")

    if model['name'] == "DeepSeek":
        log("Creating DeepSeekWrapper instance")
        return DeepSeekWrapper(
            ChatDeepSeek(
                model="deepseek-chat",
                api_key=model["api_key"],
                temperature=0.7,
                max_tokens=4096,
                timeout=60,
                max_retries=2,
            )
        )

    if model['name'] == "Groq":
        log("Creating GroqWrapper instance")
        return GroqWrapper(
            ChatOpenAI(
                model=model["model_name"],
                base_url="https://api.groq.com/openai/v1",
                api_key=model["api_key"],
                temperature=0.7,
                max_tokens=4096,
                timeout=60,
                max_retries=2,
            )
        )

    log(f"Model name '{model['name']}' is not supported")
    return None
