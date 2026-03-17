from langchain_ollama import OllamaLLM

model=OllamaLLM(model="lfm2")
res=model.invoke(input="你是谁，你能做什么?")
print(res)


