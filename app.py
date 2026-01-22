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

# --- 2. ESTILO VISUAL PREMIUM (GOLD DARK) ---
st.markdown("""
    <style>
    /* Fundo e Texto Geral */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Sliders Dourados e Grandes */
    div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
        background-color: #FFC107 !important;
        box-shadow: 0 0 10px #FFC107;
    }
    div.stSlider > div[data-baseweb="slider"] > div > div > div > div {
        background-color: #FFC107 !important;
    }
    
    /* Títulos e Perguntas */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stMarkdown p {
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Botão de Ação (Estilo Militar/Urgente) */
    .stButton > button {
        background-color: #FFC107 !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border: 1px solid #FFC107 !important;
        padding: 18px !important;
        font-size: 18px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        margin-top: 20px;
        border-radius: 8px;
    }
    .stButton > button:hover {
        background-color: #FFD54F !important;
        box-shadow: 0 0 15px #FFC107;
    }

    /* Link Final (WhatsApp) */
    .link-btn {
        text-decoration: none;
        display: inline-block;
        width: 100%;
    }
    
    /* Rodapé */
    .footer {
        text-align: center;
        color: #666;
        font-size: 12px;
        margin-top: 50px;
        border-top: 1px solid #333;
        padding-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DE SEGREDOS ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    SHEET_URL = st.secrets["SHEET_URL"]
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    GOOGLE_API_KEY = ""
    SHEET_URL = ""

# --- 4. FUNÇÕES ---
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
    try: requests.post(SHEET_URL, json=data)
    except: pass

def get_ai_diagnosis(palco, bastidor, quadrante, pior_nota_nome, pior_nota_valor):
    if not GOOGLE_API_KEY:
        return "⚠️ O diagnóstico visual está pronto. Para ver a análise da IA, configure a Chave de API."
    
    # Lógica de Personalidade
    if quadrante == "GIGANTE DE CRISTAL":
        tom = "Alerta Vermelho. Cirúrgico. Duro. Aponte a hipocrisia de vencer fora e perder dentro."
    elif quadrante == "LÍDER ANTIFRÁGIL":
        tom = "Respeito Máximo. Validação. Elite. Reconheça que ele é uma anomalia positiva. Fale de Legado."
    elif quadrante == "SONÂMBULO":
        tom = "Choque de Realidade. Despertador. Ele está sobrevivendo, não vivendo."
    else: 
        tom = "Desafio à Ação. Ele tem paz mas não tem impacto. Chame para o jogo."

    prompt = f"""
    Atue como um Mentor Sênior de Alta Performance (Método Ultra).
    Escreva um diagnóstico curto (máximo 80 palavras) e impactante.
    
    PERFIL DO LÍDER:
    - Arquétipo: {quadrante}
    - Potência Externa (Palco): {palco:.1f}/10
    - Sustentação Interna (Bastidor): {bastidor:.1f}/10
    - Ponto de Ruptura (Pior Área): {pior_nota_nome} (Nota {pior_nota_valor})

    DIRETRIZES:
    {tom}

    REGRAS DE OURO:
    1. NUNCA use termos como "Eixo X", "Nota", "Score".
    2. Use "PALCO" e "BASTIDOR".
    3. Use Markdown e NEGRITO para destacar palavras-chave.
    4. Seja direto e visceral.
    """
    try:
        # ATUALIZADO PARA O NOVO MODELO (CORREÇÃO DO ERRO 404)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"O Mentor está em silêncio estratégico. (Erro técnico: {e})"

def feedback_visual(nota):
    if nota <= 4: return ":red[🔴 Crítico]"
    elif nota <= 7: return ":orange[🟡 Atenção]"
    else: return ":green[🟢 Potência Ultra]"

# --- 5. INTRODUÇÃO IMPACTANTE ---
st.markdown("<h1 style='text-align: center; color: #FFC107;'>MAPEAMENTO DE COERÊNCIA ULTRA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ccc;'>Descubra a verdade por trás dos seus resultados.</p>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
<div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; border-left: 5px solid #FFC107;">
    <p style="margin:0;">
    Muitos líderes vencem o jogo de fora, mas perdem o jogo de dentro. 
    Este mapeamento não é sobre julgar seu sucesso, é sobre medir sua <b>sustentação</b>.
    <br><br>
    Esqueça o personagem "Líder" por um minuto. Responda como o Ser Humano que carrega o peso.
    </p>
</div>
""", unsafe_allow_html=True)
st.divider()

# --- 6. AS PERGUNTAS (HUMANIZADAS) ---
st.markdown("### 🏛️ O PALCO (O que o mundo vê)")

q1 = st.slider("1. Resultados e Entrega: Sendo sincero, comparado à média, o quanto você entrega?", 0, 10, 5)
st.caption(feedback_visual(q1))

q2 = st.slider("2. O Peso da Coroa: Qual o tamanho da responsabilidade que você carrega?", 0, 10, 5)
st.caption(feedback_visual(q2))

q3 = st.slider("3. Reconhecimento: Quando falam seu nome, qual o nível de respeito?", 0, 10, 5)
st.caption(feedback_visual(q3))

q4 = st.slider("4. Fome de Conquista: O quanto você ainda quer crescer?", 0, 10, 5)
st.caption(feedback_visual(q4))

st.markdown("---")
st.markdown("### 🧱 O BASTIDOR (O que só você sente)")

q5 = st.slider("5. Nível de Bateria: Ao acordar, como está sua energia real?", 0, 10, 5)
st.caption(feedback_visual(q5))

q6 = st.slider("6. Controle da Mente: Quem manda: você ou sua ansiedade?", 0, 10, 5)
st.caption(feedback_visual(q6))

q7 = st.slider("7. Presença Real: Com quem você ama, você está lá de verdade?", 0, 10, 5)
st.caption(feedback_visual(q7))

q8 = st.slider("8. Sentido de Vida: No fundo, você sente paz ou vazio?", 0, 10, 5)
st.caption(feedback_visual(q8))

q9 = st.slider("9. A Prova do Silêncio: 1 hora sozinho, sem celular. Angústia ou Paz?", 0, 10, 5)
st.caption(feedback_visual(q9))

# --- CÁLCULOS ---
media_palco = (q1 + q2 + q3 + q4) / 4
media_bastidor = (q5 + q6 + q7 + q8 + q9) / 5

if media_palco >= 5 and media_bastidor >= 5:
    quadrante = "LÍDER ANTIFRÁGIL"
    cor_ponto = "#00FF00"
elif media_palco >= 5 and media_bastidor < 5:
    quadrante = "GIGANTE DE CRISTAL"
    cor_ponto = "#FF0000"
elif media_palco < 5 and media_bastidor >= 5:
    quadrante = "TEÓRICO"
    cor_ponto = "#0000FF"
else:
    quadrante = "SONÂMBULO"
    cor_ponto = "#808080"

# Pior Nota para IA
notas = [q5, q6, q7, q8, q9]
nomes = ["Energia", "Controle Mental", "Presença", "Propósito", "Silêncio"]
min_val = min(notas)
pior_area = nomes[notas.index(min_val)]

# --- 7. FORMULÁRIO BLINDADO E RESULTADO ---
st.divider()

# Abertura do Formulário
with st.form("lead_form"):
    st.markdown("<h3 style='text-align: center; color: #FFC107;'>🔐 LIBERAR DIAGNÓSTICO</h3>", unsafe_allow_html=True)
    st.write("Preencha para receber sua análise completa.")
    
    nome = st.text_input("Nome Completo")
    email = st.text_input("E-mail Corporativo")
    whatsapp = st.text_input("WhatsApp (com DDD)")
    
    # Botão de Envio (Dentro do Form)
    submitted = st.form_submit_button("REVELAR A VERDADE")
    
    if submitted:
        if not nome or not email or not whatsapp:
            st.error("⚠️ Por favor, preencha todos os campos para continuar.")
        else:
            # 1. Salvar Lead
            with st.spinner("Conectando ao servidor Ultra..."):
                save_lead(nome, email, whatsapp, quadrante, media_palco, media_bastidor)
            
            # 2. IA Pensa
            placeholder = st.empty()
            placeholder.markdown("<div style='text-align: center; padding: 20px;'>⚙️ O Mentor está analisando seus padrões...</div>", unsafe_allow_html=True)
            
            texto_ia = get_ai_diagnosis(media_palco, media_bastidor, quadrante, pior_area, min_val)
            time.sleep(1)
            placeholder.empty()
            
            # 3. Mostrar Resultados (Fora do Spinner)
            st.success("Análise Concluída.")
            
            st.markdown(f"<h1 style='text-align: center; color: #FFC107; font-size: 40px;'>{quadrante}</h1>", unsafe_allow_html=True)
            
            # Gráfico Alvo
            fig = go.Figure()
            fig.add_shape(type="rect", x0=0, y0=5, x1=5, y1=10, fillcolor="#FF0000", opacity=0.15, line_width=0)
            fig.add_shape(type="rect", x0=5, y0=5, x1=10, y1=10, fillcolor="#00FF00", opacity=0.15, line_width=0)
            fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, fillcolor="#808080", opacity=0.15, line_width=0)
            fig.add_shape(type="rect", x0=5, y0=0, x1=10, y1=5, fillcolor="#0000FF", opacity=0.15, line_width=0)
            
            fig.add_trace(go.Scatter(
                x=[media_bastidor], y=[media_palco],
                mode='markers',
                marker=dict(size=30, color=cor_ponto, line=dict(width=4, color='white'))
            ))
            
            fig.update_layout(
                xaxis=dict(range=[0, 10], title="BASTIDOR (Interno)", showgrid=False, zeroline=False),
                yaxis=dict(range=[0, 10], title="PALCO (Externo)", showgrid=False, zeroline=False),
                width=450, height=450,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Diagnóstico
            st.markdown("""
            <div style="background-color: #222; padding: 20px; border-radius: 10px; border: 1px solid #444;">
                <h3 style="color: #FFC107; margin-top: 0;">📝 VEREDITO DO MENTOR</h3>
                <p style="font-size: 16px;">{}</p>
            </div>
            """.format(texto_ia), unsafe_allow_html=True)
            
            # Botão Final (HTML Puro para garantir clique)
            st.markdown(f"""
            <br>
            <a href="https://wa.me/55999999999?text=Fiz+o+teste+e+deu+{quadrante}+Quero+ajuda" target="_blank" class="link-btn">
                <button style="
                    background-color: #FFC107; 
                    color: black; 
                    font-weight: bold; 
                    width: 100%; 
                    padding: 20px; 
                    font-size: 18px; 
                    border: none; 
                    border-radius: 8px; 
                    cursor: pointer;
                    text-transform: uppercase;">
                    SOLICITAR INTERVENÇÃO TÁTICA 🚀
                </button>
            </a>
            """, unsafe_allow_html=True)

# --- 8. RODAPÉ 2026 ---
st.markdown("""
    <div class="footer">
        <p><b style="color: #FFC107;">© 2026 MÉTODO ULTRA ®</b></p>
        <p>Engenharia de Lucidez Brutal • Desenvolvido para Mentes de Elite</p>
    </div>
""", unsafe_allow_html=True)
