class Qualificador:
    def __init__(self):
        self.contexto = {}

    def coletar_dados(self, mensagem):
        # Simulação de coleta de dados do cliente
        # Exemplo: tipo de festa, número de convidados, data
        if "festa" in mensagem:
            self.contexto["tipo_festa"] = mensagem
        # Adicione lógica para coletar outros dados
        return self.contexto
