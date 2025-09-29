from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

class Supervisor:
    def __init__(self, googleai):
        self.googleai = googleai

    def greet_user(self):
        return "Olá! Seja bem-vindo ao nosso serviço de festas. Como posso ajudar você hoje?"

    def refine_response(self, response):
        # Refina a resposta para ser clara, concisa e respeitosa
        prompt = PromptTemplate.from_template("Refine a resposta para ser clara, concisa e respeitosa: {response}")
        return self.googleai.invoke(prompt.format(response=response))

    def decide_agent(self, user_message):
        # Decide se aciona o Qualificador ou Especialista
        if any(word in user_message.lower() for word in ["data", "convidado", "tipo"]):
            return "qualificador"
        else:
            return "especialista"
