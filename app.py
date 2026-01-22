import streamlit as st
import plotly.graph_objects as go
import google.generativeai as genai
import time
import requests

# --- 1. CONFIGURAÇÃO VISUAL DE ELITE ---
st.set_page_config(page_title="Mapeamento Ultra", page_icon="💎", layout="centered", initial_sidebar_state="collapsed")

# CSS PERSONALIZADO (A MÁGICA DO DESIGN)
st.markdown("""
    <style>
    /* Fundo Escuro Profundo */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    
    /* Esconder menus do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Títulos Dourados */
    h1, h2, h3 {
        color: #FFC107 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
    }
    
    /* Botões de Ação (Estilo Militar) */
    .stButton > button {
        background-color: #FFC107 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border: none !important;
        padding: 16px !important;
        font-size: 18px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        border-radius: 5px;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.2);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #FFD54F !important;
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 193, 7, 0.4);
    }

    /* Sliders Personalizados */
    div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"] {
        background-color: #FFC107 !important;
        box-shadow: 0 0 10px #FFC107;
    }
    div.stSlider > div[data-baseweb="slider"] > div > div > div > div {
        background-color: #444 !important;
    }
    
    /* Caixas de Texto (Perguntas) */
    .pergunta-box {
        background-color: #161B22;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #FFC107;
        margin-bottom: 20px;
    }
    .pergunta-titulo {
        font-size: 18px;
        font-weight: bold;
        color: #FFC107;
        margin-bottom: 8px;
    }
    .pergunta-texto {
        font-size: 14px;
        color: #CCCCCC;
        line-height: 1.5;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background-color: #0E1117 !important;
        color: white !important;
        border: 1px solid #FFC107 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. CONFIGURAÇÃO TÉCNICA ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    SHEET_URL = st.secrets["SHEET_URL"]
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    pass # Falha silenciosa se não tiver chave, mostra erro visual depois

# --- 3. LÓGICA DO MENTOR (IA) ---
def get_mentor_voice(palco, bastidor, quadrante, pior_area):
    if not GOOGLE_API_KEY:
        return "⚠️ ERRO TÉCNICO: A Chave de API não foi detectada. Verifique os 'Secrets' no Streamlit."
    
    # Prompt Blindado
    prompt = f"""
    Aja como o Mentor do 'Método Ultra'. Sua persona é direta, visceral e estratégica.
    Analise este líder:
    - Perfil: {quadrante}
    - Potência Externa (Palco): {palco:.1f}/10
    - Sustentação Interna (Bastidor): {bastidor:.1f}/10
    - Ponto Fraco Crítico: {pior_area}

    Escreva um veredito de IMPACTO (máximo 50 palavras).
    Não dê "parabéns". Vá direto na dor ou na estratégia.
    Use formatação Markdown (**negrito**) para destacar o importante.
    """
    try:
        # Tenta o modelo mais novo (Flash)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Fallback de segurança
        return f"O Mentor está recalculando a rota. (Erro: {e})"

def save_lead(dados):
    if not SHEET_URL: return
    try:
        requests.post(SHEET_URL, json={
            "Data": time.strftime("%d/%m/%Y"),
            "Nome": dados['nome'],
            "Email": dados['email'],
            "WhatsApp": dados['whatsapp'],
            "Resultado": dados['quadrante'],
            "Palco": f"{dados['palco']:.1f}",
            "Bastidor": f"{dados['bastidor']:.1f}"
        })
    except: pass

# --- 4. FLUXO DO APLICATIVO (WIZARD) ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'd' not in st.session_state: st.session_state.d = {}

def feedback_visual(nota):
    if nota <= 4: return "🔴 Crítico"
    elif nota <= 7: return "🟡 Atenção"
    else: return "🟢 Potência"

# TELA 1: CAPA
if st.session_state.step == 1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 50px;'>MÉTODO ULTRA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #aaa;'>MAPEAMENTO DE COERÊNCIA</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p>Você venceu o jogo de fora. Mas e o jogo de dentro?</p>
        <p>Este não é um teste de vaidade. É um diagnóstico de <b>sustentação</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("INICIAR DIAGNÓSTICO 🚀"):
        st.session_state.step = 2
        st.rerun()

# TELA 2: PERGUNTAS (LAYOUT RICO)
elif st.session_state.step == 2:
    st.markdown("### 🏛️ O PALCO (O que o mundo vê)")
    
    # Pergunta 1
    st.markdown("""
    <div class="pergunta-box">
        <div class="pergunta-titulo">1. Resultados e Entrega</div>
        <div class="pergunta-texto">Sendo brutalmente honesto: comparado à média do mercado, o quanto você realmente entrega de resultado? Você é insubstituível?</div>
    </div>
    """, unsafe_allow_html=True)
    q1 = st.slider("", 0, 10, 5, key="q1")
    st.caption(feedback_visual(q1))
    
    # Pergunta 2
    st.markdown("""
    <div class="pergunta-box">
        <div class="pergunta-titulo">2. O Peso da Coroa</div>
        <div class="pergunta-texto">Qual o tamanho da pressão e responsabilidade que está sobre os seus ombros hoje? Quanto custa errar na sua posição?</div>
    </div>
    """, unsafe_allow_html=True)
    q2 = st.slider("", 0, 10, 5, key="q2")

    # Pergunta 3
    st.markdown("""
    <div class="pergunta-box">
        <div class="pergunta-titulo">3. Reconhecimento</div>
        <div class="pergunta-texto">Quando citam o seu nome na sua área, qual o nível de respeito e autoridade que você tem? Você é uma referência?</div>
    </div>
    """, unsafe_allow_html=True)
    q3 = st.slider("", 0, 10, 5, key="q3")
    
    # Pergunta 4
    st.markdown("""
    <div class="pergunta-box">
        <div class="pergunta-titulo">4. Fome de Conquista</div>
        <div class="pergunta-texto">O quanto você ainda quer crescer? Sua ambição está viva ou você se acomodou no conforto?</div>
    </div>
    """, unsafe_allow_html=True)
    q4 = st.slider("", 0, 10, 5, key="q4")

    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("### 🧱 O BASTIDOR (O que só você sente)")

    # Pergunta 5
    st.markdown("""
    <div class="pergunta-box">
        <div class="pergunta-titulo">5. Bateria Real</div>
        <div class="pergunta-texto">Ao acordar na segunda-feira, qual seu nível real de energia vital? Você acorda pronto ou já cansado?</div>
    </div>
    """, unsafe_allow_html=True)
    q5 = st.slider("", 0, 10, 5, key="q5")
    st.caption(feedback_visual(q5))

    # Pergunta 6
    st.markdown("""
    <div class="pergunta-box">
        <div class="pergunta-titulo">6. Controle da Mente</div>
        <div class="pergunta-texto">Quem está no comando: você ou sua ansiedade? Sua mente é uma aliada ou uma tortura constante?</div>
    </div>
    """, unsafe_allow_html=True)
    q6 = st.slider("", 0, 10, 5, key="q6")

    # Pergunta 7
    st.markdown("""
    <div class="pergunta-box">
        <div class="pergunta-titulo">7. Presença Real</div>
        <div class="pergunta-texto">Quando você está com quem ama (filhos, esposa), você está lá de corpo e alma ou está no celular/trabalho?</div>
    </div>
    """, unsafe_allow_html=True)
    q7 = st.slider("", 0, 10, 5, key="q7")

    # Pergunta 8
    st.markdown("""
    <div class="pergunta-box">
        <div class="pergunta-titulo">8. Sentido</div>
        <div class="pergunta-texto">No fundo, você sente que o que faz tem um propósito maior ou é apenas uma corrida pelo dinheiro?</div>
    </div>
    """, unsafe_allow_html=True)
    q8 = st.slider("", 0, 10, 5, key="q8")

    # Pergunta 9
    st.markdown("""
    <div class="pergunta-box">
        <div class="pergunta-titulo">9. O Silêncio</div>
        <div class="pergunta-texto">Se você ficar 1 hora sozinho, em silêncio absoluto, sem celular. O que acontece? Paz ou Angústia?</div>
    </div>
    """, unsafe_allow_html=True)
    q9 = st.slider("", 0, 10, 5, key="q9")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("ANALISAR MEU PERFIL ➡️"):
        st.session_state.d = {'q1':q1, 'q2':q2, 'q3':q3, 'q4':q4, 'q5':q5, 'q6':q6, 'q7':q7, 'q8':q8, 'q9':q9}
        st.session_state.step = 3
        st.rerun()

# TELA 3: CADASTRO
elif st.session_state.step == 3:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>🔒 RELATÓRIO CONFIDENCIAL</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#aaa;'>Para gerar seu veredito personalizado, identifique-se.</p>", unsafe_allow_html=True)
    
    nome = st.text_input("Seu Nome Completo")
    email = st.text_input("Seu Melhor E-mail")
    zap = st.text_input("WhatsApp (com DDD)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("REVELAR A VERDADE 🔓"):
        if nome and email and zap:
            # Cálculos
            d = st.session_state.d
            palco = (d['q1']+d['q2']+d['q3']+d['q4'])/4
            bastidor = (d['q5']+d['q6']+d['q7']+d['q8']+d['q9'])/5
            
            if palco >= 5 and bastidor >= 5: quad = "LÍDER ANTIFRÁGIL"
            elif palco >= 5 and bastidor < 5: quad = "GIGANTE DE CRISTAL"
            elif palco < 5 and bastidor >= 5: quad = "TEÓRICO"
            else: quad = "SONÂMBULO"
            
            # Pior nota
            notas = [d['q5'], d['q6'], d['q7'], d['q8'], d['q9']]
            labels = ["Energia", "Mente", "Presença", "Sentido", "Silêncio"]
            pior_area = labels[notas.index(min(notas))]

            # Salva
            st.session_state.d.update({'nome':nome, 'email':email, 'whatsapp':zap, 'quadrante':quad, 'palco':palco, 'bastidor':bastidor, 'pior_area':pior_area})
            st.session_state.step = 4
            st.rerun()
        else:
            st.error("⚠️ Preencha todos os campos para liberar o acesso.")

# TELA 4: PROCESSAMENTO
elif st.session_state.step == 4:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    with st.spinner("🔄 Conectando ao Banco de Dados Ultra..."):
        save_lead(st.session_state.d)
        time.sleep(1)
    
    with st.spinner("🧠 O Mentor está escrevendo seu veredito..."):
        dados = st.session_state.d
        texto = get_mentor_voice(dados['palco'], dados['bastidor'], dados['quadrante'], dados['pior_area'])
        st.session_state.d['texto_ia'] = texto
    
    st.session_state.step = 5
    st.rerun()

# TELA 5: RESULTADO
elif st.session_state.step == 5:
    d = st.session_state.d
    
    # Cores Dinâmicas
    cor = "#FF0000" if d['quadrante'] == "GIGANTE DE CRISTAL" else "#00FF00"
    if d['quadrante'] == "SONÂMBULO": cor = "#888"
    if d['quadrante'] == "TEÓRICO": cor = "#00F"

    st.markdown(f"<h1 style='text-align: center; color: {cor}; font-size: 45px;'>{d['quadrante']}</h1>", unsafe_allow_html=True)
    
    # GRÁFICO (TRAVADO PARA MOBILE)
    fig = go.Figure()
    # Quadrantes
    fig.add_shape(type="rect", x0=0, y0=5, x1=5, y1=10, fillcolor="red", opacity=0.15, line_width=0)
    fig.add_shape(type="rect", x0=5, y0=5, x1=10, y1=10, fillcolor="green", opacity=0.15, line_width=0)
    fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, fillcolor="gray", opacity=0.15, line_width=0)
    fig.add_shape(type="rect", x0=5, y0=0, x1=10, y1=5, fillcolor="blue", opacity=0.15, line_width=0)
    
    # Ponto
    fig.add_trace(go.Scatter(
        x=[d['bastidor']], y=[d['palco']],
        mode='markers',
        marker=dict(size=35, color=cor, line=dict(width=4, color='white'))
    ))
    
    # Configuração MOBILE FRIENDLY (Static)
    fig.update_layout(
        xaxis=dict(range=[0, 10], title="BASTIDOR (Interno)", showgrid=False, fixedrange=True),
        yaxis=dict(range=[0, 10], title="PALCO (Externo)", showgrid=False, fixedrange=True),
        width=400, height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=20, r=20, t=10, b=10),
        dragmode=False
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})

    # Veredito IA (Box Estilizado)
    st.markdown(f"""
    <div style="background-color: #161B22; padding: 25px; border-radius: 10px; border-left: 5px solid {cor}; margin-top: 20px;">
        <h3 style="color: #FFC107; margin: 0 0 10px 0;">📝 VEREDITO DO MENTOR:</h3>
        <p style="font-size: 16px; color: #EEE; line-height: 1.6;">{d['texto_ia']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("SOLICITAR INTERVENÇÃO TÁTICA 🚀", f"https://wa.me/55999999999?text=Sou+um+{d['quadrante']}+e+preciso+de+ajuda")
    
    if st.button("REFAZER TESTE ↺"):
        st.session_state.step = 1
        st.rerun()

# RODAPÉ
st.markdown("<br><br><center style='color:#444; font-size:12px;'>© 2026 MÉTODO ULTRA ®</center>", unsafe_allow_html=True)
