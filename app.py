import streamlit as st
import plotly.graph_objects as go
import google.generativeai as genai
import time
import requests

# --- 1. CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="Mapeamento Ultra", page_icon="💎", layout="centered", initial_sidebar_state="collapsed")

# --- 2. CSS "FERRARI" (VISUAL DE LUXO) ---
st.markdown("""
    <style>
    /* Fundo Preto Profundo */
    .stApp {
        background-color: #050505;
        color: #E0E0E0;
    }
    
    /* Remover marcas do Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Cards das Perguntas (Caixas Estilizadas) */
    .pergunta-card {
        background-color: #111;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #333;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .pergunta-titulo {
        color: #FFC107;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .pergunta-texto {
        color: #BBB;
        font-size: 15px;
        line-height: 1.5;
        margin-bottom: 15px;
    }
    
    /* Botões Dourados Premium */
    .stButton > button {
        background: linear-gradient(45deg, #FFC107, #FFD54F);
        color: #000;
        font-weight: 900;
        border: none;
        padding: 18px;
        font-size: 18px;
        text-transform: uppercase;
        width: 100%;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(255, 193, 7, 0.3);
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(255, 193, 7, 0.5);
    }

    /* Inputs de Texto (Formulário) */
    .stTextInput > div > div > input {
        background-color: #1A1A1A !important;
        color: #FFF !important;
        border: 1px solid #444 !important;
        border-radius: 8px;
        padding: 12px;
    }
    
    /* Sliders Dourados */
    div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"] {
        background-color: #FFC107 !important;
        box-shadow: 0 0 10px #FFC107;
    }
    div.stSlider > div[data-baseweb="slider"] > div > div > div > div {
        background-color: #333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. CONEXÃO E SISTEMA ANTIFRÁGIL ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    SHEET_URL = st.secrets["SHEET_URL"]
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    pass

def get_mentor_voice_antifragil(palco, bastidor, quadrante, pior_area):
    if not GOOGLE_API_KEY:
        return "⚠️ Erro: Chave de API não configurada."
    
    prompt = f"""
    Aja como o Mentor do 'Método Ultra'. Seja curto, visceral e estratégico.
    Perfil: {quadrante} (Palco: {palco:.1f}, Bastidor: {bastidor:.1f}).
    Ponto Fraco: {pior_area}.
    Escreva um veredito de 2 frases impactantes. Vá na dor.
    """
    
    # TENTATIVA 1: Modelo Flash (Mais Rápido)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(prompt).text
    except:
        # TENTATIVA 2: Modelo Pro (Fallback de Segurança)
        try:
            model = genai.GenerativeModel('gemini-pro')
            return model.generate_content(prompt).text
        except Exception as e:
            return f"O Mentor está em silêncio tático. (Erro: {e})"

def save_lead(dados):
    if not SHEET_URL: return
    try:
        requests.post(SHEET_URL, json={
            "Data": time.strftime("%d/%m/%Y"),
            "Nome": dados['nome'], "Email": dados['email'], "Whatsapp": dados['whatsapp'],
            "Resultado": dados['quadrante'], "Palco": f"{dados['palco']:.1f}", "Bastidor": f"{dados['bastidor']:.1f}"
        })
    except: pass

# --- 4. O APLICATIVO ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'd' not in st.session_state: st.session_state.d = {}

def render_pergunta(titulo, texto, key):
    st.markdown(f"""
    <div class="pergunta-card">
        <div class="pergunta-titulo">{titulo}</div>
        <div class="pergunta-texto">{texto}</div>
    </div>
    """, unsafe_allow_html=True)
    val = st.slider("", 0, 10, 5, key=key)
    return val

# TELA 1: CAPA IMPACTANTE
if st.session_state.step == 1:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 55px; margin-bottom: 0;'>MÉTODO ULTRA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 16px; color: #888; letter-spacing: 2px;'>ENGENHARIA DE LUCIDEZ BRUTAL</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #111; padding: 25px; border-left: 4px solid #FFC107; border-radius: 8px;">
        <p style="margin:0; font-size: 18px; color: #DDD;">
        <b>O paradoxo do líder moderno:</b><br><br>
        Vencer o jogo de fora (Dinheiro, Status) e perder o jogo de dentro (Paz, Propósito).<br>
        Este diagnóstico vai revelar a sua <b>Sustentação Real</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("INICIAR PROTOCOLO 🚀"):
        st.session_state.step = 2
        st.rerun()

# TELA 2: O TESTE (VISUAL CARD)
elif st.session_state.step == 2:
    st.progress(50, text="ANALISANDO PERFIL...")
    st.markdown("<h3 style='color:#FFC107; text-align:center'>O IMPÉRIO (PALCO)</h3>", unsafe_allow_html=True)
    
    q1 = render_pergunta("1. Entrega Real", "Comparado à média do mercado, o quanto você realmente entrega? Você é insubstituível?", "q1")
    q2 = render_pergunta("2. O Peso da Coroa", "Qual o tamanho da pressão e responsabilidade sobre seus ombros hoje?", "q2")
    q3 = render_pergunta("3. Autoridade", "Quando falam seu nome, qual o nível de respeito imediato?", "q3")
    q4 = render_pergunta("4. Ambição", "Sua fome de conquista está viva ou você se acomodou?", "q4")

    st.markdown("<br><h3 style='color:#FFC107; text-align:center'>O HOMEM (BASTIDOR)</h3>", unsafe_allow_html=True)

    q5 = render_pergunta("5. Energia Vital", "Ao acordar, você tem bateria cheia ou já começa no modo economia?", "q5")
    q6 = render_pergunta("6. Domínio Mental", "Quem manda: você ou sua ansiedade/pensamentos?", "q6")
    q7 = render_pergunta("7. Presença", "Com sua família, você está lá de corpo e alma ou apenas de corpo?", "q7")
    q8 = render_pergunta("8. Propósito", "Você sente que sua vida tem um sentido maior ou é só boleto?", "q8")
    q9 = render_pergunta("9. O Silêncio", "1 hora sozinho sem celular: Paz absoluta ou tortura mental?", "q9")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("PROCESSAR DADOS ➡️"):
        st.session_state.d = {'q1':q1, 'q2':q2, 'q3':q3, 'q4':q4, 'q5':q5, 'q6':q6, 'q7':q7, 'q8':q8, 'q9':q9}
        st.session_state.step = 3
        st.rerun()

# TELA 3: CADASTRO PREMIUM
elif st.session_state.step == 3:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #FFF;'>🔒 ACESSO RESTRITO</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Identifique-se para acessar o Veredito do Mentor.</p>", unsafe_allow_html=True)
    
    with st.container():
        nome = st.text_input("Nome Completo")
        email = st.text_input("E-mail Profissional")
        zap = st.text_input("WhatsApp")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("LIBERAR VEREDITO 🔓"):
        if nome and email and zap:
            # Lógica
            d = st.session_state.d
            palco = (d['q1']+d['q2']+d['q3']+d['q4'])/4
            bastidor = (d['q5']+d['q6']+d['q7']+d['q8']+d['q9'])/5
            
            if palco >= 5 and bastidor >= 5: quad = "LÍDER ANTIFRÁGIL"
            elif palco >= 5 and bastidor < 5: quad = "GIGANTE DE CRISTAL"
            elif palco < 5 and bastidor >= 5: quad = "TEÓRICO"
            else: quad = "SONÂMBULO"
            
            notas = [d['q5'], d['q6'], d['q7'], d['q8'], d['q9']]
            labels = ["Energia", "Mente", "Presença", "Sentido", "Silêncio"]
            pior_area = labels[notas.index(min(notas))]

            st.session_state.d.update({'nome':nome, 'email':email, 'whatsapp':zap, 'quadrante':quad, 'palco':palco, 'bastidor':bastidor, 'pior_area':pior_area})
            st.session_state.step = 4
            st.rerun()
        else:
            st.warning("Preenchimento obrigatório.")

# TELA 4: PROCESSAMENTO
elif st.session_state.step == 4:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    with st.spinner("Conectando à Inteligência Ultra..."):
        save_lead(st.session_state.d)
        dados = st.session_state.d
        dados['texto_ia'] = get_mentor_voice_antifragil(dados['palco'], dados['bastidor'], dados['quadrante'], dados['pior_area'])
        time.sleep(1)
        st.session_state.step = 5
        st.rerun()

# TELA 5: RESULTADO FINAL (FERRARI)
elif st.session_state.step == 5:
    d = st.session_state.d
    cor = "#FF0000" if d['quadrante'] == "GIGANTE DE CRISTAL" else "#00FF00"
    if d['quadrante'] == "SONÂMBULO": cor = "#888"
    if d['quadrante'] == "TEÓRICO": cor = "#0000FF"

    # Cabeçalho do Resultado
    st.markdown(f"<div style='text-align:center; padding:10px;'><span style='font-size:16px; color:#888'>SEU ARQUÉTIPO É:</span><br><h1 style='color:{cor}; font-size:42px; margin:0'>{d['quadrante']}</h1></div>", unsafe_allow_html=True)
    
    # Gráfico
    fig = go.Figure()
    fig.add_shape(type="rect", x0=0, y0=5, x1=5, y1=10, fillcolor="red", opacity=0.15, line_width=0)
    fig.add_shape(type="rect", x0=5, y0=5, x1=10, y1=10, fillcolor="green", opacity=0.15, line_width=0)
    fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, fillcolor="gray", opacity=0.15, line_width=0)
    fig.add_shape(type="rect", x0=5, y0=0, x1=10, y1=5, fillcolor="blue", opacity=0.15, line_width=0)
    
    fig.add_trace(go.Scatter(
        x=[d['bastidor']], y=[d['palco']],
        mode='markers',
        marker=dict(size=35, color=cor, line=dict(width=4, color='white'))
    ))
    
    fig.update_layout(
        xaxis=dict(range=[0, 10], title="BASTIDOR", showgrid=False, fixedrange=True, zeroline=False),
        yaxis=dict(range=[0, 10], title="PALCO", showgrid=False, fixedrange=True, zeroline=False),
        width=350, height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        dragmode=False
    )
    st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})

    # Cartão do Mentor (Veredito)
    st.markdown(f"""
    <div style="background-color: #111; padding: 25px; border-radius: 12px; border: 1px solid {cor}; margin-top: 10px;">
        <h3 style="color: #FFC107; margin-top: 0; font-size: 20px;">📝 A VOZ DO MENTOR</h3>
        <p style="font-size: 16px; color: #EEE; line-height: 1.6; margin-bottom: 0;">{d.get('texto_ia', 'Erro na IA')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("SOLICITAR INTERVENÇÃO TÁTICA 🚀", f"https://wa.me/55999999999?text=Sou+um+{d['quadrante']}+e+preciso+de+ajuda")
    
    if st.button("REFAZER TESTE ↺"):
        st.session_state.step = 1
        st.rerun()

st.markdown("<br><br><center style='color:#333; font-size:10px;'>MÉTODO ULTRA ® 2026</center>", unsafe_allow_html=True)
