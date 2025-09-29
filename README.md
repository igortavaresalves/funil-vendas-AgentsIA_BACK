# funil-vendas-AgentsIA_BACK
BACKEND DO FUNIL DE VENDAS PERSONALIZADO

## Funil de Vendas - Rosa

Pequeno projeto de funil de vendas para festas e eventos. Frontend atual em Streamlit (chat) e backend com lógica de supervisão/especialista/qualificador.

Arquivos principais:
- `app.py` - aplicação Streamlit principal
- `prompts.py` - prompts do Supervisor/Especialista/Qualificador
- `especialista.py`, `qualificador.py` - módulos auxiliares (lógica simulada)
- `config.yaml` - chaves e configurações (não commitar em repositórios públicos)

Pré-requisitos
- Python 3.10+ (recomendado)
- Virtualenv ou venv

Instalação (Windows PowerShell)
```powershell
# Criar e ativar venv
python -m venv .venv
& .venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

Configuração
- Preencha `config.yaml` com suas chaves de API (Google API Key, etc.).

Executando
```powershell
& .venv\Scripts\Activate.ps1
streamlit run app.py
```

Notas
- Caso use outro provedor (OpenAI, Pinecone), configure as chaves em `config.yaml`.
- As funções de agente estão em estado simulado; ajustar integração com LangChain/Gemini conforme necessário.

Suporte
- Se precisar de um frontend React/TypeScript separado, posso gerar outro projeto em `Frontend/`.

