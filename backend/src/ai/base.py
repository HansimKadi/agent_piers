from abc import ABC, abstractmethod

class AIPlatform(ABC):
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        pass # Abstract method to generate text based on a prompt will take any ai platform implementation
