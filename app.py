import streamlit as st
import plotly.graph_objects as go
import google.generativeai as genai
import time
import requests

# --- 1. CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Mapeamento Ultra", page_icon="💎", layout="centered", initial_sidebar_state="collapsed")

# --- 2. ESTILO VISUAL (CSS DARK & GOLD) ---
st.markdown("""
    <style>
    .stApp {background-color: #0E1117; color: #FAFAFA;}
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Botões */
    .stButton > button {
        background-color: #FFC107 !important; color: black !important;
        font-weight: 800 !important; text-transform: uppercase;
        width: 100%; padding: 18px !important; border-radius: 8px; border: none;
    }
    
    /* Sliders */
    div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"] {
        background-color: #FFC107 !important; box-shadow: 0 0 10px #FFC107;
    }
    div.stSlider > div[data-baseweb="slider"] > div > div > div > div {
        background-color: #FFC107 !important;
    }
    
    /* Textos das Perguntas */
    .pergunta-titulo {font-size: 18px; font-weight: bold; color: #FFC107; margin-bottom: 5px;}
    .pergunta-desc {font-size: 14px; color: #CCC; margin-bottom: 15px;}
    </style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO API ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    SHEET_URL = st.secrets["SHEET_URL"]
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    GOOGLE_API_KEY = ""
    SHEET_URL = ""

# --- 4. FUNÇÕES DE SUPORTE ---
def feedback_visual(nota):
    if nota <= 4: return "🔴 Crítico"
    elif nota <= 7: return "🟡 Atenção"
    else: return "🟢 Ultra"

def get_mentor_voice(palco, bastidor, quadrante, pior_area):
    if not GOOGLE_API_KEY:
        return "⚠️ O Mentor IA precisa da Chave de API configurada no 'Secrets' do Streamlit para falar."
    
    prompt = f"""
    Aja como um Mentor de Elite (Método Ultra). Seja curto, visceral e direto.
    Analise: Líder perfil '{quadrante}'.
    Palco (Sucesso Externo): {palco:.1f}/10. Bastidor (Paz Interna): {bastidor:.1f}/10.
    Ponto mais fraco: {pior_area}.
    
    Dê um veredito de 2 frases impactantes. Sem saudações.
    """
    try:
        # VOLTAMOS PARA O GEMINI-PRO (COMPATIBILIDADE TOTAL)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro de conexão IA: {e}"

def save_lead(dados):
    if not SHEET_URL: return
    try:
        requests.post(SHEET_URL, json={
            "Data": time.strftime("%d/%m/%Y"), "Nome": dados['nome'],
            "Email": dados['email'], "Whatsapp": dados['whatsapp'],
            "Resultado": dados['quadrante']
        })
    except: pass

# --- 5. CONTROLE DE ESTADO (WIZARD) ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'd' not in st.session_state: st.session_state.d = {}

# ================= TELA 1: CAPA =================
if st.session_state.step == 1:
    st.markdown("<br><h1 style='text-align:center; color:#FFC107'>MÉTODO ULTRA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>Você venceu o jogo de fora.<br>Mas e o jogo de dentro?</p>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("INICIAR MAPEAMENTO 🚀"):
        st.session_state.step = 2
        st.rerun()

# ================= TELA 2: PERGUNTAS (TEXTOS COMPLETOS) =================
elif st.session_state.step == 2:
    st.markdown("### 🏛️ O PALCO (Externo)")
    
    st.markdown("<div class='pergunta-titulo'>1. Resultados e Entrega</div>", unsafe_allow_html=True)
    st.markdown("<div class='pergunta-desc'>Sendo brutalmente honesto: comparado à média do mercado, o quanto você realmente entrega de resultado?</div>", unsafe_allow_html=True)
    q1 = st.slider("", 0, 10, 5, key="q1")
    st.caption(feedback_visual(q1))
    
    st.markdown("<div class='pergunta-titulo'>2. O Peso da Coroa</div>", unsafe_allow_html=True)
    st.markdown("<div class='pergunta-desc'>Qual o tamanho da pressão e responsabilidade que está sobre os seus ombros hoje?</div>", unsafe_allow_html=True)
    q2 = st.slider("", 0, 10, 5, key="q2")
    st.caption(feedback_visual(q2))

    st.markdown("<div class='pergunta-titulo'>3. Reconhecimento</div>", unsafe_allow_html=True)
    st.markdown("<div class='pergunta-desc'>Quando citam o seu nome na sua área, qual o nível de respeito e autoridade que você tem?</div>", unsafe_allow_html=True)
    q3 = st.slider("", 0, 10, 5, key="q3")
    
    st.markdown("<div class='pergunta-titulo'>4. Fome de Conquista</div>", unsafe_allow_html=True)
    st.markdown("<div class='pergunta-desc'>O quanto você ainda quer crescer? Sua ambição está viva ou você se acomodou?</div>", unsafe_allow_html=True)
    q4 = st.slider("", 0, 10, 5, key="q4")

    st.markdown("---")
    st.markdown("### 🧱 O BASTIDOR (Interno)")

    st.markdown("<div class='pergunta-titulo'>5. Bateria Real</div>", unsafe_allow_html=True)
    st.markdown("<div class='pergunta-desc'>Ao acordar na segunda-feira, qual seu nível real de energia vital?</div>", unsafe_allow_html=True)
    q5 = st.slider("", 0, 10, 5, key="q5")
    st.caption(feedback_visual(q5))

    st.markdown("<div class='pergunta-titulo'>6. Controle da Mente</div>", unsafe_allow_html=True)
    st.markdown("<div class='pergunta-desc'>Quem está no comando: você ou sua ansiedade/pensamentos acelerados?</div>", unsafe_allow_html=True)
    q6 = st.slider("", 0, 10, 5, key="q6")

    st.markdown("<div class='pergunta-titulo'>7. Presença Real</div>", unsafe_allow_html=True)
    st.markdown("<div class='pergunta-desc'>Quando você está com quem ama, você está lá de corpo e alma ou está no celular/trabalho?</div>", unsafe_allow_html=True)
    q7 = st.slider("", 0, 10, 5, key="q7")

    st.markdown("<div class='pergunta-titulo'>8. Sentido</div>", unsafe_allow_html=True)
    st.markdown("<div class='pergunta-desc'>No fundo, você sente que o que faz tem um propósito maior ou é apenas pelo dinheiro?</div>", unsafe_allow_html=True)
    q8 = st.slider("", 0, 10, 5, key="q8")

    st.markdown("<div class='pergunta-titulo'>9. O Silêncio</div>", unsafe_allow_html=True)
    st.markdown("<div class='pergunta-desc'>Se você ficar 1 hora sozinho, em silêncio absoluto. Você sente Paz ou Angústia?</div>", unsafe_allow_html=True)
    q9 = st.slider("", 0, 10, 5, key="q9")

    if st.button("ANALISAR PERFIL ➡️"):
        st.session_state.d = {'q1':q1, 'q2':q2, 'q3':q3, 'q4':q4, 'q5':q5, 'q6':q6, 'q7':q7, 'q8':q8, 'q9':q9}
        st.session_state.step = 3
        st.rerun()

# ================= TELA 3: CADASTRO =================
elif st.session_state.step == 3:
    st.markdown("<h3 style='text-align:center'>🔒 DADOS PARA ANÁLISE</h3>", unsafe_allow_html=True)
    nome = st.text_input("Nome")
    email = st.text_input("Email Corporativo")
    zap = st.text_input("WhatsApp")
    
    if st.button("REVELAR DIAGNÓSTICO"):
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

            # Salvar sessão
            st.session_state.d.update({'nome':nome, 'email':email, 'whatsapp':zap, 'quadrante':quad, 'palco':palco, 'bastidor':bastidor, 'pior_area':pior_area})
            st.session_state.step = 4
            st.rerun()
        else:
            st.error("Preencha todos os campos.")

# ================= TELA 4: PROCESSAMENTO =================
elif st.session_state.step == 4:
    with st.spinner("🤖 O Mentor está analisando seus padrões..."):
        save_lead(st.session_state.d) # Planilha
        st.session_state.d['texto_ia'] = get_mentor_voice(st.session_state.d['palco'], st.session_state.d['bastidor'], st.session_state.d['quadrante'], st.session_state.d['pior_area'])
        time.sleep(2)
        st.session_state.step = 5
        st.rerun()

# ================= TELA 5: RESULTADO (GRÁFICO TRAVADO) =================
elif st.session_state.step == 5:
    d = st.session_state.d
    cor = "#FF0000" if d['quadrante'] == "GIGANTE DE CRISTAL" else "#00FF00"
    if d['quadrante'] == "SONÂMBULO": cor = "#888"
    if d['quadrante'] == "TEÓRICO": cor = "#00F"

    st.markdown(f"<h1 style='text-align:center; color:{cor}'>{d['quadrante']}</h1>", unsafe_allow_html=True)
    
    # GRÁFICO TRAVADO (STATIC PLOT)
    fig = go.Figure()
    # Quadrantes
    fig.add_shape(type="rect", x0=0, y0=5, x1=5, y1=10, fillcolor="red", opacity=0.2, line_width=0)
    fig.add_shape(type="rect", x0=5, y0=5, x1=10, y1=10, fillcolor="green", opacity=0.2, line_width=0)
    fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, fillcolor="gray", opacity=0.2, line_width=0)
    fig.add_shape(type="rect", x0=5, y0=0, x1=10, y1=5, fillcolor="blue", opacity=0.2, line_width=0)
    
    # Ponto do Usuário
    fig.add_trace(go.Scatter(
        x=[d['bastidor']], y=[d['palco']],
        mode='markers', marker=dict(size=30, color=cor, line=dict(width=4, color='white'))
    ))
    
    # Configuração para TRAVAR O ZOOM (Mobile Friendly)
    fig.update_layout(
        xaxis=dict(range=[0, 10], title="BASTIDOR", showgrid=False, fixedrange=True), # fixedrange trava o eixo
        yaxis=dict(range=[0, 10], title="PALCO", showgrid=False, fixedrange=True),
        width=400, height=400,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False, margin=dict(l=20, r=20, t=20, b=20),
        dragmode=False # Desativa arrastar
    )
    
    # Exibe o gráfico travado
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})

    # Veredito IA
    st.markdown(f"""
    <div style="background-color:#222; padding:20px; border-radius:10px; border-left:5px solid {cor}">
        <b style="color:#FFC107">VEREDITO:</b><br>{d['texto_ia']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("SOLICITAR INTERVENÇÃO 🚀", f"https://wa.me/55999999999?text=Sou+{d['quadrante']}")
    
    if st.button("REFAZER"):
        st.session_state.step = 1
        st.rerun()
