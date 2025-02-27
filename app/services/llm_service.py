from transformers import AutoModelForCausalLM, AutoTokenizer

_llm_service = None

class LlamaService:
    def __init__(self, model_name="meta-llama/llama-2-7b-chat-hf"):
        print("Inicializando LlamaService - cargando modelo...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        print("Modelo cargado correctamente")
    
    def generate_response(self, context, max_new_tokens=200):
        tokens = self.tokenizer(context, return_tensors="pt")
        salida = self.model.generate(**tokens, max_new_tokens=max_new_tokens)
        return self.tokenizer.decode(salida[0])

def get_llm_service():
    global _llm_service
    if _llm_service is None:
        _llm_service = LlamaService()
    return _llm_service