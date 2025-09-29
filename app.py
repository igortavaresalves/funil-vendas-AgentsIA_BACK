import streamlit as st
import pandas as pd
import os
import yaml
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import SUPERVISOR_WELCOME, SUPERVISOR_DECISION, SUPERVISOR_REFINE, ESPECIALISTA_PROMPT, QUALIFICADOR_PROMPT

st.set_page_config(page_title="Chat | Rosalina Montenegro", page_icon="🎉", layout="centered")

with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)
os.environ['GOOGLE_API_KEY'] = config['GOOGLE_API_KEY']
googleai = ChatGoogleGenerativeAI(model='gemini-2.5-pro')

# Inicializar variáveis de sessão
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensagem de boas-vindas do Supervisor
    st.session_state.messages.append({"role": "assistant", "content": SUPERVISOR_WELCOME})

if "lead_data" not in st.session_state:
    st.session_state.lead_data = {
        "Nome": None,
        "Tipo de Festa": None,
        "Convidados": None,
        "Orçamento": None
    }

# Função para extrair dados do lead do texto
def extract_lead_data(text):
    if "casamento" in text.lower():
        st.session_state.lead_data["Tipo de Festa"] = "Casamento"
    if "15" in text.lower():
        st.session_state.lead_data["Tipo de Festa"] = "Festa de 15 anos"
    if "30" in text.lower():
        st.session_state.lead_data["Tipo de Festa"] = "Aniversário 30 anos"
    if "empresarial" in text.lower():
        st.session_state.lead_data["Tipo de Festa"] = "Corporativo"
    if "corporativo" in text.lower():
        st.session_state.lead_data["Tipo de Festa"] = "Corporativo"
    if "100" in text.lower() or "cem" in text.lower():
        st.session_state.lead_data["Convidados"] = 100
    if "200" in text.lower():
        st.session_state.lead_data["Convidados"] = 200
    if "5000" in text.lower():
        st.session_state.lead_data["Orçamento"] = 5000
    if "10000" in text.lower():
        st.session_state.lead_data["Orçamento"] = 10000

# Função para salvar os dados do lead em leads.xlsx
def save_lead():
    import pandas as pd
    import os
    df_new = pd.DataFrame([st.session_state.lead_data])
    if os.path.exists("leads.xlsx"):
        df_existing = pd.read_excel("leads.xlsx")
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_final = df_new
    df_final.to_excel("leads.xlsx", index=False, engine="openpyxl")
    st.success("Lead salvo automaticamente em leads.xlsx")

st.title("🎉 Chat - Rosalina Montenegro")

# Exibir histórico
messages = st.session_state.messages.copy()
# Garante que a mensagem de boas-vindas esteja sempre no topo
if messages and messages[0]["content"] != SUPERVISOR_WELCOME:
    messages.insert(0, {"role": "assistant", "content": SUPERVISOR_WELCOME})

for idx, msg in enumerate(messages):
    if msg["role"] == "assistant":
        col1, col2 = st.columns([0.13, 0.87])
        with col1:
            st.image("img/rosalina.jpg", width=48, caption=None)
        with col2:
            st.markdown(
                f"<div style='background: #222; padding: 16px 18px; border-radius: 12px; color: #fff; font-size: 1rem; max-width: 600px;'>{msg['content']}</div>",
                unsafe_allow_html=True
            )
        # Espaçamento após a primeira mensagem do bot
        if idx == 0 and len(messages) > 1:
            st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    elif msg["role"] == "user":
        st.markdown(
            f"<div style='background: #e74c3c; padding: 12px 16px; border-radius: 12px; color: #fff; font-size: 1rem; max-width: 600px; margin-bottom: 8px; border-left: 6px solid #e74c3c;'>"
            f"<span style='font-weight:600;'>🧑‍💬</span> {msg['content']}"
            f"</div>",
            unsafe_allow_html=True
        )

# Entrada do usuário
prompt = st.chat_input("Digite sua mensagem...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Atualiza contexto do lead
    extract_lead_data(prompt)

    # Monta contexto acumulado
    contexto = "\n".join([f"{k}: {v}" for k, v in st.session_state.lead_data.items() if v])
    faltam = [k for k, v in st.session_state.lead_data.items() if v is None]
    faltam_str = ", ".join(faltam)

    # Se todos os dados foram coletados, exibe mensagem de conclusão e não pergunta mais nada
    if not faltam:
        final_response = "Todas as informações necessárias foram coletadas! Em breve nossa equipe entrará em contato com uma proposta personalizada. Obrigado por confiar na Rosalina Montenegro!"
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        col1, col2 = st.columns([0.13, 0.87])
        with col1:
            st.image("img/rosalina.jpg", width=48, caption=None)
        with col2:
            st.markdown(
                f"<div style='background: #222; padding: 16px 18px; border-radius: 12px; color: #fff; font-size: 1rem; max-width: 600px;'>{final_response}</div>",
                unsafe_allow_html=True
            )
        save_lead()
    else:
        # SUPERVISOR decide qual agente acionar
        decision_prompt = SUPERVISOR_DECISION.format(user_message=prompt + ("\n" + contexto if contexto else ""))
        decision = googleai.invoke(decision_prompt).content.strip().lower()

        # AGENTE responde (nos bastidores)
        if decision == "qualificador":
            agent_role = QUALIFICADOR_PROMPT
        else:
            agent_role = ESPECIALISTA_PROMPT

        # Passa contexto acumulado para o agente e pede só o que falta
        agent_input = (
            agent_role +
            (f"\nContexto já coletado:\n{contexto}" if contexto else "") +
            (f"\nPergunte APENAS sobre o que falta coletar: {faltam_str}." if faltam_str else "") +
            f"\nUsuário: {prompt}"
        )
        agent_response = googleai.invoke(agent_input).content

        # SUPERVISOR refina a resposta
        supervisor_refine = SUPERVISOR_REFINE.format(agent_response=agent_response)
        final_response = googleai.invoke(supervisor_refine).content

        # Mostrar resposta final ao usuário
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        col1, col2 = st.columns([0.13, 0.87])
        with col1:
            st.image("img/rosalina.jpg", width=48, caption=None)
        with col2:
            st.markdown(
                f"<div style='background: #222; padding: 16px 18px; border-radius: 12px; color: #fff; font-size: 1rem; max-width: 600px;'>{final_response}</div>",
                unsafe_allow_html=True
            )
