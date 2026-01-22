import streamlit as st
import plotly.graph_objects as go
import google.generativeai as genai
import time
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Mapeamento Ultra",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- ESTILO VISUAL (GOLD ULTRA) ---
st.markdown("""
    <style>
    /* Slider Dourado */
    div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
        background-color: #FFC107 !important;
    }
    div.stSlider > div[data-baseweb="slider"] > div > div > div > div {
        background-color: #FFC107 !important;
    }
    /* Botão Vermelho Urgente */
    .stLinkButton > a {
        background-color: #791e1e !important;
        color: white !important;
        font-weight: bold !important;
        border: 1px solid #ff4b4b !important;
        text-align: center !important;
        display: block;
        width: 100%;
        padding: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO (PREENCHA DEPOIS AS CHAVES SE QUISER) ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    SHEET_URL = st.secrets["SHEET_URL"]
except:
    # Se der erro de chave, usa valores vazios para não travar o visual
    GOOGLE_API_KEY = "" 
    SHEET_URL = ""

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# --- FUNÇÕES INTERNAS ---
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
        return "⚠️ Sistema Operando em Modo Demonstração (Sem conexão IA). O resultado visual acima é preciso."
    
    if quadrante == "GIGANTE DE CRISTAL":
        tom = "Alerta Vermelho. Cirúrgico. Aponte a hipocrisia de vencer fora e perder dentro."
    elif quadrante == "LÍDER ANTIFRÁGIL":
        tom = "Respeito Máximo. Validação. Reconheça que ele é uma anomalia positiva. Fale de Legado."
    elif quadrante == "SONÂMBULO":
        tom = "Choque de Realidade. Ele está sobrevivendo, não vivendo."
    else: 
        tom = "Desafio à Ação. Ele tem paz mas não tem impacto. Chame para o jogo."

    prompt = f"""
    Atue como um Mentor Sênior (Método Ultra).
    Diagnóstico curto (máx 80 palavras) e impactante.
    DADOS: Palco {palco:.1f} | Bastidor {bastidor:.1f} | Arquétipo: {quadrante}
    PONTO FRACO: {pior_nota_nome} (Nota {pior_nota_valor})
    DIRETRIZES: {tom}
    REGRAS: NUNCA use "Eixo X/Y". Use "PALCO/IMPÉRIO" e "BASTIDOR/PAZ". Use Markdown e NEGRITO.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        return model.generate_content(prompt).text
    except:
        return "Diagnóstico indisponível no momento."

def feedback_visual(nota):
    if nota <= 4: return ":red[🔴 Nível Crítico]"
    elif nota <= 7: return ":orange[🟡 Atenção]"
    else: return ":green[🟢 Potência Ultra]"

# --- COMEÇO DO APP ---
st.markdown("<h1 style='text-align: center; color: white;'>MAPEAMENTO DE COERÊNCIA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ccc;'>Descubra a verdade por trás dos seus resultados.</p>", unsafe_allow_html=True)
st.divider()

st.markdown("Esqueça o personagem 'Líder'. Responda como o Ser Humano que carrega o peso.")
st.divider()

# PERGUNTAS PALCO
st.markdown("### 🏛️ O PALCO (O que o mundo vê)")
q1 = st.slider("1. Resultados e Entrega", 0, 10, 5)
st.caption(feedback_visual(q1))
q2 = st.slider("2. O Peso da Coroa", 0, 10, 5)
st.caption(feedback_visual(q2))
q3 = st.slider("3. Reconhecimento", 0, 10, 5)
st.caption(feedback_visual(q3))
q4 = st.slider("4. Fome de Conquista", 0, 10, 5)
st.caption(feedback_visual(q4))

# PERGUNTAS BASTIDOR
st.markdown("---")
st.markdown("### 🧱 O BASTIDOR (O que só você sente)")
q5 = st.slider("5. Nível de Bateria (Energia)", 0, 10, 5)
st.caption(feedback_visual(q5))
q6 = st.slider("6. Controle da Mente (Ansiedade)", 0, 10, 5)
st.caption(feedback_visual(q6))
q7 = st.slider("7. Presença Real (Família)", 0, 10, 5)
st.caption(feedback_visual(q7))
q8 = st.slider("8. Sentido de Vida (Propósito)", 0, 10, 5)
st.caption(feedback_visual(q8))
q9 = st.slider("9. A Prova do Silêncio", 0, 10, 5)
st.caption(feedback_visual(q9))

# CÁLCULOS
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

# LÓGICA PIOR NOTA
bastidor_labels = ["Energia", "Mente", "Presença", "Sentido", "Silêncio"]
bastidor_notas = [q5, q6, q7, q8, q9]
min_nota = min(bastidor_notas)
pior_area = bastidor_labels[bastidor_notas.index(min_nota)]

# --- BOTÃO E FORMULÁRIO (AQUI ESTÁ O E-MAIL) ---
st.divider()
if st.button("ANALISAR COERÊNCIA"):
    with st.form("lead_form"):
        st.write("🔒 **Relatório Confidencial Pronto.**")
        
        # CAMPOS DE CADASTRO
        nome = st.text_input("Seu Nome Completo")
        email = st.text_input("Seu E-mail Corporativo") # <--- O E-MAIL ESTÁ AQUI
        whatsapp = st.text_input("Seu WhatsApp (com DDD)")
        
        submitted = st.form_submit_button("REVELAR DIAGNÓSTICO ULTRA")
        
        if submitted:
            if not nome or not whatsapp or not email:
                st.error("⚠️ Preencha NOME, E-MAIL e WHATSAPP para liberar.")
            else:
                # Salva e Processa
                save_lead(nome, email, whatsapp, quadrante, media_palco, media_bastidor)
                
                placeholder = st.empty()
                placeholder.markdown("<br><h3 style='text-align: center; color: #FFC107;'>⚙️ O MENTOR ESTÁ ANALISANDO...</h3>", unsafe_allow_html=True)
                
                texto_ia = get_ai_diagnosis(media_palco, media_bastidor, quadrante, pior_area, min_nota)
                
                time.sleep(1.5)
                placeholder.empty()

                # MOSTRA RESULTADO
                st.markdown(f"<h2 style='text-align: center;'>RESULTADO: <span style='color: #FFC107;'>{quadrante}</span></h2>", unsafe_allow_html=True)
                
                # GRÁFICO
                fig = go.Figure()
                fig.add_shape(type="rect", x0=0, y0=5, x1=5, y1=10, fillcolor="red", opacity=0.15, line_width=0)
                fig.add_shape(type="rect", x0=5, y0=5, x1=10, y1=10, fillcolor="green", opacity=0.15, line_width=0)
                fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, fillcolor="gray", opacity=0.15, line_width=0)
                fig.add_shape(type="rect", x0=5, y0=0, x1=10, y1=5, fillcolor="blue", opacity=0.15, line_width=0)
                fig.add_trace(go.Scatter(x=[media_bastidor], y=[media_palco], mode='markers', marker=dict(size=25, color=cor_ponto, line=dict(width=3, color='white'))))
                fig.update_layout(xaxis=dict(range=[0, 10], title="BASTIDOR", showgrid=False), yaxis=dict(range=[0, 10], title="PALCO", showgrid=False, scaleanchor="x", scaleratio=1), width=500, height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("### 📝 VEREDITO")
                st.markdown(texto_ia)
                st.divider()
                st.link_button("SOLICITAR INTERVENÇÃO TÁTICA", "https://wa.me/55999999999?text=Sou+um+Gigante+de+Cristal")

# RODAPÉ
st.markdown("<br><br><br>---", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #666; font-size: 12px;'><p><b style='color: #FFC107;'>© 2026 MÉTODO ULTRA ®</b></p><p>Engenharia de Lucidez Brutal</p></div>", unsafe_allow_html=True)
