class Especialista:
    def __init__(self):
        pass

    def sugerir_inspiracoes(self, contexto):
        # Simulação de sugestão de pacotes e inspirações
        if "tipo_festa" in contexto:
            return f"Veja inspirações para {contexto['tipo_festa']}!" 
        return "Posso sugerir pacotes e diferenciais para sua festa."
