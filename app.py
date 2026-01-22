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

# --- 2. CONTROLE DE NAVEGAÇÃO (MÁGICA DO PASSO A PASSO) ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'dados' not in st.session_state:
    st.session_state.dados = {}

def next_step():
    st.session_state.step += 1

# --- 3. ESTILO VISUAL PREMIUM ---
st.markdown("""
    <style>
    /* Fundo Escuro Absoluto */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Esconder Elementos Padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Botões Dourados */
    .stButton > button {
        background-color: #FFC107 !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border: none !important;
        padding: 20px !important;
        font-size: 20px !important;
        text-transform: uppercase;
        width: 100%;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
    }
    .stButton > button:hover {
        background-color: #FFD54F !important;
        transform: scale(1.02);
    }

    /* Sliders */
    div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
        background-color: #FFC107 !important;
    }
    div.stSlider > div[data-baseweb="slider"] > div > div > div > div {
        background-color: #FFC107 !important;
    }
    
    /* Caixas de Texto (Inputs) */
    .stTextInput > div > div > input {
        background-color: #1E1E1E !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. CONFIGURAÇÃO API ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    SHEET_URL = st.secrets["SHEET_URL"]
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    GOOGLE_API_KEY = ""
    SHEET_URL = ""

# --- 5. FUNÇÕES LÓGICAS ---
def get_ai_diagnosis(palco, bastidor, quadrante, pior_nota_nome):
    if not GOOGLE_API_KEY:
        return "⚠️ IA Desconectada. Configure a Chave de API no Streamlit."
    
    tom = "Cirúrgico, direto e impactante."
    if quadrante == "LÍDER ANTIFRÁGIL": tom = "Validar a força, mas alertar sobre a arrogância."
    if quadrante == "GIGANTE DE CRISTAL": tom = "Alerta vermelho. Sucesso externo vs Vazio interno."

    prompt = f"""
    Atue como Mentor do Método Ultra.
    Analise este perfil:
    - Arquétipo: {quadrante}
    - Palco (Externo): {palco:.1f}
    - Bastidor (Interno): {bastidor:.1f}
    - Ponto Fraco: {pior_nota_nome}
    
    Diretrizes: {tom}
    Escreva um veredito curto (max 60 palavras) usando Markdown e Negrito.
    """
    try:
        # VOLTAMOS PARA O GEMINI-PRO (MAIS ESTÁVEL)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except:
        return "O Mentor está em silêncio. (Erro de Conexão IA)"

def save_lead(dados):
    if not SHEET_URL: return
    try:
        payload = {
            "Data": time.strftime("%d/%m/%Y %H:%M:%S"),
            "Nome": dados['nome'],
            "Email": dados['email'],
            "WhatsApp": dados['whatsapp'],
            "Resultado": dados['quadrante'],
            "Palco": f"{dados['palco']:.1f}",
            "Bastidor": f"{dados['bastidor']:.1f}"
        }
        requests.post(SHEET_URL, json=payload)
    except: pass

def feedback_visual(nota):
    if nota <= 4: return "🔴 Crítico"
    elif nota <= 7: return "🟡 Atenção"
    else: return "🟢 Ultra"

# ==========================================
# --- FLUXO DO APLICATIVO (WIZARD) ---
# ==========================================

# --- PASSO 1: INTRODUÇÃO ---
if st.session_state.step == 1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #FFC107; font-size: 50px;'>MÉTODO ULTRA</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white;'>MAPEAMENTO DE COERÊNCIA</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ccc; margin-top: 20px;'>Descubra se o seu sucesso é sólido ou se você é um Gigante de Cristal.</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("INICIAR MAPEAMENTO 🚀"):
        next_step()
        st.rerun()

# --- PASSO 2: AS PERGUNTAS ---
elif st.session_state.step == 2:
    st.markdown("### 🏛️ O PALCO (O que o mundo vê)")
    q1 = st.slider("1. Resultados e Entrega", 0, 10, 5)
    st.caption(feedback_visual(q1))
    q2 = st.slider("2. Pressão e Responsabilidade", 0, 10, 5)
    st.caption(feedback_visual(q2))
    q3 = st.slider("3. Reconhecimento e Respeito", 0, 10, 5)
    st.caption(feedback_visual(q3))
    q4 = st.slider("4. Ambição e Fome", 0, 10, 5)
    st.caption(feedback_visual(q4))

    st.markdown("---")
    st.markdown("### 🧱 O BASTIDOR (O que só você sente)")
    q5 = st.slider("5. Nível de Energia Real", 0, 10, 5)
    st.caption(feedback_visual(q5))
    q6 = st.slider("6. Controle da Ansiedade", 0, 10, 5)
    st.caption(feedback_visual(q6))
    q7 = st.slider("7. Presença com a Família", 0, 10, 5)
    st.caption(feedback_visual(q7))
    q8 = st.slider("8. Sentido e Propósito", 0, 10, 5)
    st.caption(feedback_visual(q8))
    q9 = st.slider("9. Paz no Silêncio", 0, 10, 5)
    st.caption(feedback_visual(q9))

    if st.button("CONTINUAR PARA ANÁLISE ➡️"):
        # Salvar notas na sessão
        st.session_state.dados.update({
            'q1':q1, 'q2':q2, 'q3':q3, 'q4':q4,
            'q5':q5, 'q6':q6, 'q7':q7, 'q8':q8, 'q9':q9
        })
        next_step()
        st.rerun()

# --- PASSO 3: CADASTRO ---
elif st.session_state.step == 3:
    st.markdown("<h2 style='text-align: center;'>🔒 RELATÓRIO CONFIDENCIAL</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Seus dados estão seguros. Preencha para liberar o acesso.</p>", unsafe_allow_html=True)
    
    nome = st.text_input("Nome Completo")
    email = st.text_input("E-mail Corporativo")
    whatsapp = st.text_input("WhatsApp (com DDD)")

    if st.button("REVELAR A VERDADE 🔓"):
        if not nome or not email or not whatsapp:
            st.error("Preencha todos os campos.")
        else:
            # Cálculos
            d = st.session_state.dados
            media_palco = (d['q1'] + d['q2'] + d['q3'] + d['q4']) / 4
            media_bastidor = (d['q5'] + d['q6'] + d['q7'] + d['q8'] + d['q9']) / 5
            
            if media_palco >= 5 and media_bastidor >= 5: quadrante = "LÍDER ANTIFRÁGIL"
            elif media_palco >= 5 and media_bastidor < 5: quadrante = "GIGANTE DE CRISTAL"
            elif media_palco < 5 and media_bastidor >= 5: quadrante = "TEÓRICO"
            else: quadrante = "SONÂMBULO"

            # Encontrar pior nota
            notas = [d['q5'], d['q6'], d['q7'], d['q8'], d['q9']]
            nomes = ["Energia", "Mente", "Presença", "Propósito", "Silêncio"]
            pior_val = min(notas)
            pior_nome = nomes[notas.index(pior_val)]

            # Salvar tudo na sessão
            st.session_state.dados.update({
                'nome': nome, 'email': email, 'whatsapp': whatsapp,
                'palco': media_palco, 'bastidor': media_bastidor,
                'quadrante': quadrante, 'pior_nome': pior_nome
            })
            
            next_step()
            st.rerun()

# --- PASSO 4: PROCESSAMENTO (ANIMAÇÃO) ---
elif st.session_state.step == 4:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    with st.spinner("🔄 Conectando ao Banco de Dados Ultra..."):
        save_lead(st.session_state.dados) # Salva na planilha
        time.sleep(1.5)
    
    with st.spinner("🧠 O Mentor está analisando seus padrões..."):
        # Gera texto IA
        dados = st.session_state.dados
        texto = get_ai_diagnosis(dados['palco'], dados['bastidor'], dados['quadrante'], dados['pior_nome'])
        st.session_state.dados['texto_ia'] = texto
        time.sleep(1.5)
    
    next_step()
    st.rerun()

# --- PASSO 5: RESULTADO FINAL ---
elif st.session_state.step == 5:
    dados = st.session_state.dados
    
    # Título do Resultado
    cor = "#FFC107"
    if dados['quadrante'] == "GIGANTE DE CRISTAL": cor = "#FF4B4B" # Vermelho
    if dados['quadrante'] == "LÍDER ANTIFRÁGIL": cor = "#00FF00" # Verde

    st.markdown(f"<h1 style='text-align: center; color: {cor};'>{dados['quadrante']}</h1>", unsafe_allow_html=True)
    
    # Gráfico
    fig = go.Figure()
    fig.add_shape(type="rect", x0=0, y0=5, x1=5, y1=10, fillcolor="#FF4B4B", opacity=0.2, line_width=0)
    fig.add_shape(type="rect", x0=5, y0=5, x1=10, y1=10, fillcolor="#00FF00", opacity=0.2, line_width=0)
    fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, fillcolor="#808080", opacity=0.2, line_width=0)
    fig.add_shape(type="rect", x0=5, y0=0, x1=10, y1=5, fillcolor="#0000FF", opacity=0.2, line_width=0)
    
    fig.add_trace(go.Scatter(
        x=[dados['bastidor']], y=[dados['palco']],
        mode='markers',
        marker=dict(size=35, color=cor, line=dict(width=3, color='white'))
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 10], title="BASTIDOR", showgrid=False, zeroline=False),
        yaxis=dict(range=[0, 10], title="PALCO", showgrid=False, zeroline=False),
        width=400, height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Texto da IA
    st.markdown(f"""
    <div style="background-color: #222; padding: 25px; border-radius: 10px; border-left: 5px solid {cor};">
        <h3 style="color: #FFC107; margin-top: 0;">📝 VEREDITO:</h3>
        <p style="font-size: 16px; line-height: 1.6;">{dados.get('texto_ia', 'Erro ao carregar')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Botão WhatsApp
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("SOLICITAR INTERVENÇÃO TÁTICA 🚀", f"https://wa.me/55999999999?text=Sou+um+{dados['quadrante']}+e+preciso+de+ajuda")

    if st.button("REFAZER TESTE ↺"):
        st.session_state.step = 1
        st.rerun()

# Rodapé
st.markdown("<br><hr><center style='color:#666; font-size:12px;'>© 2026 MÉTODO ULTRA ®</center>", unsafe_allow_html=True)
