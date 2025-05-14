from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama.chat_models import ChatOllama


class AIModelSingleton:
    _model_instances: dict[str, BaseChatModel] = {}

    def __new__(cls, *args, **kwargs) -> BaseChatModel:
        model = kwargs.get("model", "")

        if model not in cls._model_instances:
            cls._model_instances[model] = ChatOllama(model=model, temperature=0)

        return cls._model_instances[model]
