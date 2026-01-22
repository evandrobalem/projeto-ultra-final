import streamlit as st
import plotly.graph_objects as go
import google.generativeai as genai
import time
import requests

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Mapeamento Ultra",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. ESTILO VISUAL (CSS FORÇADO) ---
st.markdown("""
    <style>
    /* Forçar tema escuro e dourado */
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    /* Sliders Dourados */
    div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"] {
        background-color: #FFC107 !important;
        border-color: #FFC107 !important;
    }
    div.stSlider > div[data-baseweb="slider"] > div > div > div > div {
        background-color: #FFC107 !important;
    }
    /* Texto dos Sliders */
    .stSlider p {
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    /* Botão Vermelho/Dourado */
    .stButton > button {
        background-color: #FFC107 !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        padding: 15px !important;
        font-size: 20px !important;
        width: 100% !important;
        text-transform: uppercase;
        margin-top: 20px;
    }
    .stButton > button:hover {
        background-color: #ffdb58 !important;
        color: black !important;
    }
    /* Esconder menu padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DE SEGREDOS ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    SHEET_URL = st.secrets["SHEET_URL"]
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.warning(f"⚠️ Aviso de Configuração: As chaves de API não foram encontradas. O app vai rodar em modo visual. Erro: {e}")
    GOOGLE_API_KEY = ""
    SHEET_URL = ""

# --- 4. FUNÇÕES DO SISTEMA ---
def save_lead(nome, email, whatsapp, quadrante, palco, bastidor):
    if not SHEET_URL: return
    data = {
        "Data": time.strftime("%d/%m/%Y %H:%M:%S"),
        "Nome": nome,
        "Email": email,
        "WhatsApp": whatsapp,
        "Resultado": quadrante,
        "Palco": f"{palco:.1f}",
        "Bastidor": f"{bastidor:.1f}"
    }
    try:
        requests.post(SHEET_URL, json=data)
    except:
        pass

def get_ai_diagnosis(palco, bastidor, quadrante, pior_nota_nome, pior_nota_valor):
    if not GOOGLE_API_KEY:
        return "⚠️ O diagnóstico visual está pronto, mas a IA precisa da Chave de API configurada para gerar o texto personalizado."
    
    # Lógica de Tom de Voz
    if quadrante == "GIGANTE DE CRISTAL":
        tom = "Duro, direto, alerta vermelho. Aponte que ele tem sucesso fora mas é frágil dentro."
    elif quadrante == "LÍDER ANTIFRÁGIL":
        tom = "Respeito, validação, elite. Parabenize pela solidez e fale de legado."
    elif quadrante == "SONÂMBULO":
        tom = "Choque de realidade. Ele está dormindo na vida."
    else: 
        tom = "Desafio. Ele estuda muito e faz pouco."

    prompt = f"""
    Atue como Mentor do Método Ultra.
    Escreva um veredito curto (max 80 palavras) para:
    Perfil: {quadrante}
    Nota Palco (Externo): {palco:.1f}
    Nota Bastidor (Interno): {bastidor:.1f}
    Ponto Fraco: {pior_nota_nome} ({pior_nota_valor})
    
    Tom de voz: {tom}
    Use formatação Markdown com negrito nas palavras chave.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao conectar com o Mentor IA. (Código: {e})"

def feedback_visual(nota):
    if nota <= 4: return "🔴 Nível Crítico"
    elif nota <= 7: return "🟡 Atenção"
    else: return "🟢 Potência Ultra"

# --- 5. INTERFACE DO USUÁRIO ---
st.markdown("<h1 style='text-align: center; color: #FFC107;'>MAPEAMENTO ULTRA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ccc;'>Descubra a verdade por trás dos seus resultados.</p>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("### 🏛️ O PALCO (O que o mundo vê)")
q1 = st.slider("1. Resultados e Entrega", 0, 10, 5)
st.caption(feedback_visual(q1))
q2 = st.slider("2. O Peso da Coroa (Pressão)", 0, 10, 5)
st.caption(feedback_visual(q2))
q3 = st.slider("3. Reconhecimento", 0, 10, 5)
st.caption(feedback_visual(q3))
q4 = st.slider("4. Fome de Conquista", 0, 10, 5)
st.caption(feedback_visual(q4))

st.markdown("### 🧱 O BASTIDOR (O que só você sente)")
q5 = st.slider("5. Nível de Bateria (Energia)", 0, 10, 5)
st.caption(feedback_visual(q5))
q6 = st.slider("6. Controle da Mente (Ansiedade)", 0, 10, 5)
st.caption(feedback_visual(q6))
q7 = st.slider("7. Presença Real (Família)", 0, 10, 5)
st.caption(feedback_visual(q7))
q8 = st.slider("8. Sentido de Vida", 0, 10, 5)
st.caption(feedback_visual(q8))
q9 = st.slider("9. A Prova do Silêncio", 0, 10, 5)
st.caption(feedback_visual(q9))

# Cálculos
media_palco = (q1 + q2 + q3 + q4) / 4
media_bastidor = (q5 + q6 + q7 + q8 + q9) / 5

if media_palco >= 5 and media_bastidor >= 5:
    quadrante = "LÍDER ANTIFRÁGIL"
    cor_ponto = "#00FF00" # Verde
elif media_palco >= 5 and media_bastidor < 5:
    quadrante = "GIGANTE DE CRISTAL"
    cor_ponto = "#FF0000" # Vermelho
elif media_palco < 5 and media_bastidor >= 5:
    quadrante = "TEÓRICO"
    cor_ponto = "#0000FF" # Azul
else:
    quadrante = "SONÂMBULO"
    cor_ponto = "#808080" # Cinza

# Pior nota para IA
lista_notas = [q5, q6, q7, q8, q9]
lista_nomes = ["Energia", "Mente", "Presença", "Sentido", "Silêncio"]
pior_nota = min(lista_notas)
pior_nome = lista_nomes[lista_notas.index(pior_nota)]

st.markdown("---")

# --- 6. FORMULÁRIO E AÇÃO ---
with st.form("lead_form"):
    st.markdown("<h3 style='text-align: center;'>🔓 LIBERAR DIAGNÓSTICO</h3>", unsafe_allow_html=True)
    nome = st.text_input("Nome Completo")
    email = st.text_input("E-mail Corporativo")
    whatsapp = st.text_input("WhatsApp (com DDD)")
    
    # Botão de Envio dentro do Form
    submitted = st.form_submit_button("ANALISAR COERÊNCIA AGORA")
    
    if submitted:
        if not nome or not email or not whatsapp:
            st.error("⚠️ Por favor, preencha todos os campos para continuar.")
        else:
            # 1. Salvar na Planilha
            with st.spinner("Conectando ao banco de dados..."):
                save_lead(nome, email, whatsapp, quadrante, media_palco, media_bastidor)
            
            # 2. Consultar IA
            with st.spinner("O Mentor está analisando seus padrões..."):
                texto_ia = get_ai_diagnosis(media_palco, media_bastidor, quadrante, pior_nome, pior_nota)
                time.sleep(1) # Efeito visual

            # 3. Mostrar Resultado
            st.success("Análise Concluída!")
            
            st.markdown(f"<h1 style='text-align: center; color: #FFC107;'>{quadrante}</h1>", unsafe_allow_html=True)
            
            # Gráfico
            fig = go.Figure()
            # Quadrantes
            fig.add_shape(type="rect", x0=0, y0=5, x1=5, y1=10, fillcolor="red", opacity=0.2, line_width=0)
            fig.add_shape(type="rect", x0=5, y0=5, x1=10, y1=10, fillcolor="green", opacity=0.2, line_width=0)
            fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, fillcolor="gray", opacity=0.2, line_width=0)
            fig.add_shape(type="rect", x0=5, y0=0, x1=10, y1=5, fillcolor="blue", opacity=0.2, line_width=0)
            
            # Ponto
            fig.add_trace(go.Scatter(
                x=[media_bastidor], y=[media_palco],
                mode='markers',
                marker=dict(size=30, color=cor_ponto, line=dict(width=3, color='white'))
            ))
            
            fig.update_layout(
                xaxis=dict(range=[0, 10], title="BASTIDOR (Interno)", showgrid=False, zeroline=False),
                yaxis=dict(range=[0, 10], title="PALCO (Externo)", showgrid=False, zeroline=False),
                width=400, height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Veredito
            st.markdown("### 📝 A VOZ DO MENTOR")
            st.info(texto_ia)
            
            # Botão Final
            st.markdown(f"""
            <a href="https://wa.me/55999999999?text=Sou+um+{quadrante}+e+quero+ajuda" target="_blank">
                <button style="background-color:#FFC107; color:black; width:100%; padding:15px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">
                    SOLICITAR INTERVENÇÃO TÁTICA 🚀
                </button>
            </a>
            """, unsafe_allow_html=True)

# Rodapé
st.markdown("<br><hr><center style='color:#666;'>© 2026 MÉTODO ULTRA</center>", unsafe_allow_html=True)
