#%%
import streamlit as st # type: ignore
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

#%%
#
# ler o dot-env
load_dotenv()
#%%


#%%

def get_response(user_query, chat_history, modelo = 'llama'):

    template = """
    Você é um assistente pessoal sobre a prefeitura de fortaleza, ceará. Responda as 
    questões que seguem baseado na história da conversa:

    história da conversa: {chat_history}

    Pergunta do usuário: {user_question}.

    
    """

    prompt = ChatPromptTemplate.from_template(template)

    if modelo == 'openai':
        llm = ChatOpenAI()
    else:
        llm = ChatOpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", 
                   model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF")
        
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })


#
# funções abaixo só podem ser testadas no streamlit
#

# app config
st.set_page_config(page_title="TESTE DE CHATBOT NO STREAMLIT", page_icon="🤖", layout="wide")
st.title("FORTALEZA-CE - Chatbot Da Peste")

# Aplicar estilo CSS
st.markdown(
    """
    <style>
    body {
        background-color: #00FF00;
    }
    .header {
        background-color: #004400;
        padding: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header .icon {
        font-size: 24px;
        color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Cabeçalho com ícones
st.markdown(
    """
    <div class="header">
        <div class="icon">🚀</div>
        <h1>
        EMBRAPII - Bureau Tecnologia
        </h1>
        <div class="icon">🚀</div>
    </div>
    """,
    unsafe_allow_html=True
)


# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Olá. Em que posso ajudá-lo?"),
    ]

    
# conversa
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# entrada do usuário
user_query = st.chat_input("Digite a sua mensagem aqui...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(content=response))

