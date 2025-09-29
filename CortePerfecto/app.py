import os, base64, streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
import math
from utils.calculator import CuttingCalculator
from utils.export_utils import ExportUtils
import streamlit.components.v1 as components

BASE_DIR = os.path.dirname(__file__)

# -------------------- CARGA DE RECURSOS --------------------
def load_image_base64(filename):
    # IMAGEN_LOGO #frambuesa - Lugar para cambiar logo
    svg_placeholder = """
    <svg width="80" height="80" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#FF69B4;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#FF1493;stop-opacity:1" />
            </linearGradient>
        </defs>
        <circle cx="40" cy="40" r="35" fill="url(#logoGrad)" opacity="0.9"/>
        <text x="40" y="45" text-anchor="middle" fill="white" font-size="12" font-weight="bold">LOGO</text>
    </svg>
    """
    return base64.b64encode(svg_placeholder.encode()).decode()

def show_floating_bar():
    img_b64 = load_image_base64("Imagen1.jpeg")
    st.markdown(f"""
    <div id="floatingBar" class="floating-bar" style="margin-bottom:10px;">
        <div class="floating-content">
            <img src="data:image/svg+xml;base64,{img_b64}" 
                 style="height:40px; border-radius: 50%; margin-right: 12px;"/>
            <span class="floating-text" style="white-space: normal; font-size: 18px; font-weight: bold;">¡ESTOY EN MI DESCANSO, EN UN MOMENTO SEGUIRÉ CON EL DESARROLLO!</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------- BARRA SOCIAL MEJORADA --------------------

def show_social_bar():
    """Muestra la barra social usando components.html - 100% funcional"""
    
    social_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            .social-bar {
                background: linear-gradient(135deg, #ff69b4, #ff1493);
                padding: 50px 35px;
                border-radius: 30px;
                margin: 40px 0 30px 0;
                box-shadow: 0 20px 45px rgba(255, 105, 180, 0.5);
                border: 4px solid rgba(255, 182, 193, 0.7);
                backdrop-filter: blur(15px);
                font-family: 'Poppins', sans-serif;
                min-height: 180px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            
            .social-container {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 35px;
                flex-wrap: wrap;
            }
            
            .social-button {
                background: rgba(255, 255, 255, 0.25);
                padding: 22px;
                border-radius: 50%;
                width: 85px;
                height: 85px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
                border: 4px solid rgba(255, 255, 255, 0.4);
                text-decoration: none;
                box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
                position: relative;
                overflow: hidden;
            }
            
            .social-button::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                transition: left 0.6s ease;
            }
            
            .social-button:hover::before {
                left: 100%;
            }
            
            .social-button:hover {
                transform: scale(1.2) rotate(8deg);
                background: rgba(255, 255, 255, 0.35);
                box-shadow: 0 20px 45px rgba(0, 0, 0, 0.3), 0 0 25px rgba(255, 255, 255, 0.4);
                border-color: rgba(255, 255, 255, 0.9);
            }
            
            .social-button i {
                font-size: 34px;
                color: white;
                position: relative;
                z-index: 2;
                text-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
            }
            
            .web-button {
                background: rgba(255, 255, 255, 0.25);
                padding: 22px 38px;
                border-radius: 45px;
                text-decoration: none;
                transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
                border: 4px solid rgba(255, 255, 255, 0.4);
                box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
                position: relative;
                overflow: hidden;
            }
            
            .web-button::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                transition: left 0.6s ease;
            }
            
            .web-button:hover::before {
                left: 100%;
            }
            
            .web-button:hover {
                transform: scale(1.15) translateY(-3px);
                background: rgba(255, 255, 255, 0.35);
                box-shadow: 0 20px 45px rgba(0, 0, 0, 0.3), 0 0 30px rgba(255, 255, 255, 0.5);
                border-color: rgba(255, 255, 255, 0.9);
            }
            
            .web-text {
                color: white;
                font-weight: 800;
                font-size: 24px;
                letter-spacing: 1.5px;
                text-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
                position: relative;
                z-index: 2;
                font-family: 'Poppins', sans-serif;
            }
            
            /* TEXTO OCULTO - Comentado para que no se muestre */
            .social-text {
                display: none; /* Oculta completamente el texto */
            }
            
            .social-subtext {
                display: none; /* Oculta completamente el subtítulo */
            }
            
            @media (max-width: 768px) {
                .social-bar {
                    padding: 40px 25px;
                    min-height: 160px;
                }
                
                .social-container {
                    gap: 25px;
                }
                
                .social-button {
                    width: 70px;
                    height: 70px;
                    padding: 20px;
                }
                
                .social-button i {
                    font-size: 28px;
                }
                
                .web-button {
                    padding: 20px 32px;
                }
                
                .web-text {
                    font-size: 20px;
                }
            }
        </style>
    </head>
    <body>
        <div class='social-bar'>
            <div class='social-container'>
                <!-- TikTok -->
                <a href="https://tiktok.com/@p.h.cajas" target="_blank" class='social-button' title="Síguenos en TikTok">
                    <i class='fab fa-tiktok'></i>
                </a>
                
                <!-- Facebook -->
                <a href="https://www.facebook.com/profile.php?id=61576728375462" target="_blank" class='social-button' title="Síguenos en Facebook">
                    <i class='fab fa-facebook-f'></i>
                </a>
                
                <!-- Instagram -->
                <a href="https://www.instagram.com/p.h.cajas/" target="_blank" class='social-button' title="Síguenos en Instagram">
                    <i class='fab fa-instagram'></i>
                </a>
                
                <!-- Web -->
                <a href="https://phcajasdelujo.taplink.mx/" target="_blank" class='web-button' title="Visita nuestra web">
                    <span class='web-text'>🌐 NUESTRA WEB</span>
                </a>
            </div>
            
            <!-- Texto oculto -->
            <div class='social-text' style="display: none;">
                📱 Síguenos en nuestras redes sociales
            </div>
            
            <div class='social-subtext' style="display: none;">
                ✨ PH Cajas de Lujo - Creando magia en cada detalle ✨
            </div>
        </div>
    </body>
    </html>
    """
    
    components.html(social_html, height=200)

# -------------------- ELEMENTOS ESTÉTICOS ADICIONALES --------------------
def show_decoration_elements():
    """Muestra elementos decorativos adicionales"""
    
    # Línea decorativa superior
    st.markdown("""
    <div style='
        height: 4px;
        background: linear-gradient(90deg, #FF69B4, #FF1493, #FF69B4);
        border-radius: 10px;
        margin: 10px 0 30px 0;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
    '></div>
    """, unsafe_allow_html=True)
    
    # Separador decorativo entre secciones
    st.markdown("""
    <div style='
        text-align: center;
        margin: 25px 0;
        color: #FF69B4;
        font-family: "Poppins", sans-serif;
        font-size: 14px;
        font-weight: 500;
    '>
        ✦ ✦ ✦
    </div>
    """, unsafe_allow_html=True)

def load_css():
    css_path = os.path.join(BASE_DIR, "static", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Determinar tema actual
    dark_mode = st.session_state.get('dark_mode', False)
    theme_mode = st.session_state.get('theme_mode', 'clasico')
    custom_colors = st.session_state.get('custom_colors', {'primary': '#FF69B4', 'secondary': '#FFB6C1'})
    
    # Convertir colores personalizados a RGB para uso en CSS
    primary_rgb = tuple(int(custom_colors['primary'][i:i+2], 16) for i in (1, 3, 5))
    secondary_rgb = tuple(int(custom_colors['secondary'][i:i+2], 16) for i in (1, 3, 5))
    
    # Colores según el tema y modo
    if theme_mode == 'rosa':
        # Tema Rosa (todo rosa)
        if dark_mode:
            bg_color = "linear-gradient(135deg, #2d1b2d 0%, #4a2d4a 50%, #6b396b 100%)"
            text_color = "#FFE4E1"
            input_bg = "#4a2d4a"
            card_bg = "rgba(75, 45, 75, 0.95)"
            card_border = "rgba(255, 182, 193, 0.6)"
            secondary_text = "#FFB6C1"
            hover_bg = "#5a3d5a"
        else:
            bg_color = "linear-gradient(135deg, #ffe4e1 0%, #ffc0cb 50%, #ffb6c1 100%)"
            text_color = "#8b0040"
            input_bg = "#ffe4e1"
            card_bg = "rgba(255, 228, 225, 0.95)"
            card_border = "rgba(255, 105, 180, 0.4)"
            secondary_text = "#c1486b"
            hover_bg = "#ffd0dc"
    elif theme_mode == 'minimalista':
        # Tema Minimalista (colores neutros)
        if dark_mode:
            bg_color = "linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #404040 100%)"
            text_color = "#f5f5f5"
            input_bg = "#2d2d2d"
            card_bg = "rgba(45, 45, 45, 0.95)"
            card_border = "rgba(200, 200, 200, 0.3)"
            secondary_text = "#cccccc"
            hover_bg = "#3d3d3d"
        else:
            bg_color = "linear-gradient(135deg, #fafafa 0%, #f5f5f5 50%, #eeeeee 100%)"
            text_color = "#333333"
            input_bg = "#ffffff"
            card_bg = "rgba(255, 255, 255, 0.95)"
            card_border = "rgba(150, 150, 150, 0.2)"
            secondary_text = "#666666"
            hover_bg = "#f8f8f8"
    else:
        # Tema Clásico (con colores personalizables)
        if dark_mode:
            bg_color = "#121212"
            text_color = "#FFFFFF"
            input_bg = "#2D2D2D"
            card_bg = "rgba(45, 45, 45, 0.95)"
            card_border = f"rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.6)"
            secondary_text = "#E0E0E0"
            hover_bg = "#383838"
        else:
            bg_color = "linear-gradient(135deg, #fef7f7 0%, #fce4ec 50%, #f8bbd9 100%)"
            text_color = "#2e2e2e"
            input_bg = "#ffffff"
            card_bg = "rgba(255, 255, 255, 0.95)"
            card_border = f"rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.3)"
            secondary_text = "#666666"
            hover_bg = "#fef7f7"

    # Estilos mejorados con modo oscuro/claro
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        /* Fondo principal mejorado */
        .stApp {{
            background: {bg_color} !important;
            font-family: 'Poppins', sans-serif !important;
        }}
        
        /* Títulos con mejor contraste */
        .main-title, h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
            font-weight: 600 !important;
            text-shadow: {'0 2px 4px rgba(0,0,0,0.3)' if dark_mode else '0 2px 4px rgba(255,105,180,0.2)'} !important;
        }}

        /* Texto secundario */
        .stMarkdown p, .stText, label {{
            color: {secondary_text} !important;
        }}

        /* Inputs mejorados */
        .stNumberInput div[data-baseweb="input"] input {{
            background-color: {input_bg} !important;
            color: {text_color} !important;
            border: 2px solid {'#444444' if dark_mode else '#FFB6C1'} !important;
            border-radius: 12px !important;
            padding: 12px !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
            box-shadow: {'0 4px 12px rgba(255,105,180,0.1)' if not dark_mode else '0 4px 12px rgba(0,0,0,0.3)'} !important;
        }}

        .stNumberInput div[data-baseweb="input"] input:focus {{
            border-color: #FF69B4 !important;
            box-shadow: 0 0 0 4px rgba(255, 105, 180, 0.2) !important;
            background: {hover_bg} !important;
        }}

        .stNumberInput label {{
            color: {text_color} !important;
            font-weight: 500 !important;
            font-size: 14px !important;
        }}

        /* Botones +/- usando colores personalizados */
        .stNumberInput div[data-baseweb="input"] button {{
            background: linear-gradient(135deg, {custom_colors['primary']}, {custom_colors['secondary']}) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }}

        .stNumberInput div[data-baseweb="input"] button:hover {{
            background: linear-gradient(135deg, {custom_colors['secondary']}, {custom_colors['primary']}) !important;
            transform: scale(1.1) !important;
            box-shadow: 0 4px 12px rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.4) !important;
        }}

        /* Botones principales con colores personalizados */
        .stButton>button {{
            background: linear-gradient(135deg, {custom_colors['primary']}, {custom_colors['secondary']}) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.3) !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }}

        .stButton>button:hover {{
            background: linear-gradient(135deg, {custom_colors['secondary']}, {custom_colors['primary']}) !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.5) !important;
        }}

        .stButton>button:active {{
            transform: translateY(-1px) !important;
        }}

        /* Cards/Secciones mejoradas */
        .section-card {{
            background: {card_bg} !important;
            border: 2px solid {card_border} !important;
            border-radius: 20px !important;
            padding: 24px !important;
            margin-bottom: 20px !important;
            box-shadow: {'0 8px 32px rgba(0,0,0,0.2)' if dark_mode else '0 8px 32px rgba(255,105,180,0.15)'} !important;
            backdrop-filter: blur(10px) !important;
            transition: all 0.3s ease !important;
        }}

        .section-card:hover {{
            transform: translateY(-5px) !important;
            box-shadow: {'0 12px 40px rgba(0,0,0,0.3)' if dark_mode else '0 12px 40px rgba(255,105,180,0.25)'} !important;
        }}

        /* Toggle del modo oscuro mejorado */
        .mode-toggle {{
            background: linear-gradient(135deg, #FF69B4, #FF1493) !important;
            border-radius: 25px !important;
            transition: all 0.3s ease !important;
        }}

        .mode-toggle:hover {{
            transform: translateY(-2px) scale(1.05) !important;
            box-shadow: 0 8px 25px rgba(255, 105, 180, 0.4) !important;
        }}

        /* Alertas mejoradas */
        .stAlert {{
            border-radius: 12px !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
            backdrop-filter: blur(10px) !important;
        }}

        .stSuccess {{
            background: linear-gradient(135deg, #d4edda, #c3e6cb) !important;
            color: #155724 !important;
            border-left: 4px solid #28a745 !important;
        }}

        .stError {{
            background: linear-gradient(135deg, #f8d7da, #f5c6cb) !important;
            color: #721c24 !important;
            border-left: 4px solid #dc3545 !important;
        }}

        .stInfo {{
            background: linear-gradient(135deg, {card_bg}, rgba(255, 105, 180, 0.1)) !important;
            color: {text_color} !important;
            border-left: 4px solid #FF69B4 !important;
        }}

        /* Floating bar mejorada */
        .floating-bar {{
            background: linear-gradient(135deg, #FF69B4, #FF1493) !important;
            color: white !important;
            padding: 20px 30px !important;
            border-radius: 50px !important;
            box-shadow: 0 12px 35px rgba(255, 105, 180, 0.5) !important;
            animation: float 3s ease-in-out infinite !important;
            backdrop-filter: blur(15px) !important;
            margin: 20px 0 !important;
            font-size: 18px !important;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) scale(1); }}
            50% {{ transform: translateY(-10px) scale(1.03); }}
        }}

        .floating-content {{
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 15px !important;
        }}

        .floating-text {{
            font-size: 18px !important;
            font-weight: bold !important;
            text-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
        }}

        /* Easter egg link */
        .easter-egg-link {{
            background: linear-gradient(135deg, #FFD700, #FFA500) !important;
            color: #8B4513 !important;
            padding: 12px 20px !important;
            border-radius: 25px !important;
            text-decoration: none !important;
            font-weight: bold !important;
            display: inline-block !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3) !important;
            animation: glow 2s ease-in-out infinite alternate !important;
        }}

        .easter-egg-link:hover {{
            transform: scale(1.05) !important;
            box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5) !important;
            text-decoration: none !important;
        }}

        @keyframes glow {{
            from {{ box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3); }}
            to {{ box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6); }}
        }}

        /* Responsividad mejorada */
        @media (max-width: 768px) {{
            .main-title {{
                font-size: 1.8rem !important;
            }}
            
            .section-card {{
                padding: 16px !important;
                margin-bottom: 16px !important;
            }}
            
            .stButton>button {{
                padding: 10px 20px !important;
                font-size: 14px !important;
            }}
            
            .floating-bar {{
                padding: 15px 20px !important;
            }}
            
            .floating-text {{
                font-size: 16px !important;
            }}
        }}

        /* Plotly charts mejorados */
        .js-plotly-plot {{
            border-radius: 15px !important;
            overflow: hidden !important;
            box-shadow: {'0 8px 32px rgba(0,0,0,0.2)' if dark_mode else '0 8px 32px rgba(255,105,180,0.15)'} !important;
        }}

        /* Sidebar mejorado si existe */
        .css-1d391kg {{
            background: {card_bg} !important;
            border-right: 2px solid {card_border} !important;
        }}

    </style>
    """, unsafe_allow_html=True)

def load_js():
    js_path = os.path.join(BASE_DIR, "static", "script.js")
    if os.path.exists(js_path):
        with open(js_path, "r") as f:
            st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)

# -------------------- INICIALIZACIÓN --------------------
def initialize_app():
    if 'calculator' not in st.session_state:
        st.session_state.calculator = CuttingCalculator()
    if 'export_utils' not in st.session_state:
        st.session_state.export_utils = ExportUtils()
    if 'calculation_result' not in st.session_state:
        st.session_state.calculation_result = None
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = 'clasico'
    if 'custom_colors' not in st.session_state:
        st.session_state.custom_colors = {
            'primary': '#FF69B4',
            'secondary': '#FFB6C1'
        }
    if 'calculator_mode' not in st.session_state:
        st.session_state.calculator_mode = 'normal'

# -------------------- CALCULADORAS ESPECIALIZADAS --------------------
class CalculadorasCajas:
    @staticmethod
    def calcular_cesta(espesor, largo, ancho, alto, acabado_virada=1.0, acabado_altura=1.5):
        """Calculadora Cesta - Basada en Excel 'Calculadora Cesta'"""
        resultados = {}
        
        # MEDIDAS CARTÓN - MÉTODO CORTE SEPARADO
        resultados['base'] = {
            'medida': f"{largo} x {ancho}",
            'descripcion': 'Base - 1 pieza'
        }
        
        resultados['lateral_largo'] = {
            'medida': f"{largo + ((espesor/10)*2):.1f} x {alto}",
            'descripcion': 'Lateral (largo) - 2 piezas'
        }
        
        resultados['lateral_ancho'] = {
            'medida': f"{ancho} x {alto}",
            'descripcion': 'Lateral (ancho) - 2 piezas'
        }
        
        # MEDIDAS CARTÓN - MÉTODO CORTE Y VINCO
        resultados['placa_vinco'] = {
            'medida': f"{largo + alto + alto:.1f} x {ancho + alto + alto:.1f}",
            'descripcion': 'Tamaño placa de cartón'
        }
        
        # MEDIDAS REVESTIMIENTO PAPEL
        resultados['parte_interna'] = {
            'medida': f"{largo + alto + alto:.1f} x {ancho + alto + alto:.1f}",
            'descripcion': 'Parte interna'
        }
        
        resultados['parte_externa_banda'] = {
            'medida': f"{largo + ancho + largo + ancho + acabado_virada + (espesor/10)*8:.1f} x {alto + acabado_altura + acabado_altura:.1f}",
            'descripcion': 'Parte externa - banda'
        }
        
        resultados['parte_externa_fondo'] = {
            'medida': f"{largo} x {ancho}",
            'descripcion': 'Parte externa - fondo'
        }
        
        return resultados

    @staticmethod
    def calcular_tapa_libro(espesor, largo, ancho, alto, acabado_virada=1.0, espacio_ranura=0.3):
        """Calculadora Tapa Libro - Basada en Excel 'Tampa Livro'"""
        resultados = {}
        
        # Variables específicas de tapa libro
        canaleta = ((espesor * 2) / 10) + 0.1
        
        # MEDIDAS CARTÓN - MÉTODO CORTE SEPARADO
        resultados['base'] = {
            'medida': f"{largo} x {ancho}",
            'descripcion': 'Base - 1 pieza'
        }
        
        resultados['lateral_largo'] = {
            'medida': f"{largo + ((espesor/10)*2):.1f} x {alto}",
            'descripcion': 'Lateral (largo) - 2 piezas'
        }
        
        resultados['lateral_ancho'] = {
            'medida': f"{ancho} x {alto}",
            'descripcion': 'Lateral (ancho) - 2 piezas'
        }
        
        # Cálculos para tapa
        tapa_largo = largo + canaleta + canaleta
        tapa_ancho = ancho + ((espesor * 2) / 10) + acabado_virada
        
        resultados['tapa'] = {
            'medida': f"{tapa_largo:.1f} x {tapa_ancho:.1f}",
            'descripcion': 'Tapa - 2 piezas'
        }
        
        resultados['lomo'] = {
            'medida': f"{tapa_largo:.1f} x {alto}",
            'descripcion': 'Lomo tapa'
        }
        
        # MEDIDAS CARTÓN - MÉTODO CORTE Y VINCO
        resultados['placa_base'] = {
            'medida': f"{largo + alto + alto:.1f} x {ancho + alto + alto:.1f}",
            'descripcion': 'Tamaño placa de cartón - BASE'
        }
        
        # MEDIDAS REVESTIMIENTO PAPEL
        resultados['parte_interna_base'] = {
            'medida': f"{largo + alto + alto:.1f} x {ancho + alto + alto + acabado_virada:.1f}",
            'descripcion': 'Parte interna base'
        }
        
        resultados['parte_externa_base_banda'] = {
            'medida': f"{(ancho + (espesor*2)/10) + largo + (ancho + (espesor*2)/10) + acabado_virada + acabado_virada:.1f} x {alto + acabado_virada + acabado_virada:.1f}",
            'descripcion': 'Parte externa base banda'
        }
        
        resultados['parte_externa_tapa'] = {
            'medida': f"{tapa_largo + acabado_virada + acabado_virada:.1f} x {tapa_ancho + alto + tapa_ancho + acabado_virada + acabado_virada + acabado_virada + acabado_virada:.1f}",
            'descripcion': 'Parte externa tapa'
        }
        
        resultados['parte_interna_tapa'] = {
            'medida': f"{largo + espesor*2/10:.1f} x {tapa_ancho + 2:.1f}",
            'descripcion': 'Parte interna tapa'
        }
        
        resultados['canaleta'] = {
            'medida': f"{canaleta:.1f}",
            'descripcion': 'Canaleta (cm)'
        }
        
        return resultados

    @staticmethod
    def calcular_tapa_suelta(espesor, largo, ancho, alto, altura_tapa=3.0, acabado_virada=1.5):
        """Calculadora Tapa Suelta - Basada en Excel 'Tampa de solta'"""
        resultados = {}
        
        # MEDIDAS CARTÓN - MÉTODO CORTE SEPARADO
        resultados['base'] = {
            'medida': f"{largo} x {ancho}",
            'descripcion': 'Base - 1 pieza'
        }
        
        resultados['lateral_largo'] = {
            'medida': f"{largo + ((espesor/10)*2):.1f} x {alto}",
            'descripcion': 'Lateral (largo) - 2 piezas'
        }
        
        resultados['lateral_ancho'] = {
            'medida': f"{ancho} x {alto}",
            'descripcion': 'Lateral (ancho) - 2 piezas'
        }
        
        # Tampa
        tapa_largo = largo + ((espesor * 3) / 10)
        tapa_ancho = ancho + ((espesor * 3) / 10)
        
        resultados['tapa'] = {
            'medida': f"{tapa_largo:.1f} x {tapa_ancho:.1f}",
            'descripcion': 'Tapa - 1 pieza'
        }
        
        resultados['tapa_lateral_largo'] = {
            'medida': f"{tapa_largo + ((espesor/10)*2):.1f} x {altura_tapa}",
            'descripcion': 'Tapa lateral (largo) - 2 piezas'
        }
        
        resultados['tapa_lateral_ancho'] = {
            'medida': f"{tapa_ancho} x {altura_tapa}",
            'descripcion': 'Tapa lateral (ancho) - 2 piezas'
        }
        
        # MEDIDAS CARTÓN - MÉTODO CORTE Y VINCO
        resultados['placa_base'] = {
            'medida': f"{largo + alto + alto:.1f} x {ancho + alto + alto:.1f}",
            'descripcion': 'Tamaño placa de cartón - BASE'
        }
        
        resultados['placa_tapa'] = {
            'medida': f"{tapa_largo + altura_tapa + altura_tapa:.1f} x {tapa_ancho + altura_tapa + altura_tapa:.1f}",
            'descripcion': 'Tamaño placa de cartón - TAPA'
        }
        
        # MEDIDAS REVESTIMIENTO PAPEL
        resultados['parte_interna_base'] = {
            'medida': f"{largo + alto + alto:.1f} x {ancho + alto + alto:.1f}",
            'descripcion': 'Parte interna base'
        }
        
        resultados['banda_externa_base'] = {
            'medida': f"{(largo + ((espesor/10)*2)) + (largo + ((espesor/10)*2)) + (ancho) + (ancho) + (espesor*4/10):.1f} x {alto + acabado_virada + acabado_virada:.1f}",
            'descripcion': 'Banda externa base'
        }
        
        resultados['fondo_base'] = {
            'medida': f"{largo} x {ancho}",
            'descripcion': 'Fondo base'
        }
        
        resultados['parte_interna_tapa'] = {
            'medida': f"{tapa_largo + altura_tapa + altura_tapa:.1f} x {tapa_ancho + altura_tapa + altura_tapa:.1f}",
            'descripcion': 'Parte interna tapa'
        }
        
        resultados['parte_externa_tapa'] = {
            'medida': f"{tapa_largo + acabado_virada + acabado_virada:.1f} x {tapa_ancho + acabado_virada + acabado_virada:.1f}",
            'descripcion': 'Parte externa tapa'
        }
        
        return resultados

    @staticmethod
    def calcular_redonda(espesor_banda, diametro_base, altura_banda_base, altura_banda_tapa):
        """Calculadora Redonda - Basada en Excel 'Caja Redonda'"""
        resultados = {}
        
        # MEDIDAS CARTÓN
        resultados['base'] = {
            'medida': f"{diametro_base}",
            'descripcion': 'Base circular (diámetro)'
        }
        
        resultados['banda_base'] = {
            'medida': f"{(diametro_base * 3.14) + 1:.1f} x {altura_banda_base}",
            'descripcion': 'Banda base'
        }
        
        resultados['tapa'] = {
            'medida': f"{diametro_base + espesor_banda*3/10 + 0.1:.1f}",
            'descripcion': 'Tapa circular (diámetro)'
        }
        
        diametro_tapa = diametro_base + espesor_banda*3/10 + 0.1
        resultados['banda_tapa'] = {
            'medida': f"{(diametro_tapa * 3.14) + 1:.1f} x {altura_banda_tapa}",
            'descripcion': 'Banda tapa'
        }
        
        return resultados

# -------------------- FUNCIONES DE CÁLCULO --------------------
def calculate_optimal(sheet_width, sheet_height, cut_width, cut_height):
    """Calcula el corte óptimo para modo normal"""
    try:
        result = st.session_state.calculator.calculate_optimal_cutting(
            sheet_width, sheet_height, cut_width, cut_height
        )
        st.session_state.calculation_result = result
        st.success("✅ Cálculo completado exitosamente")
    except Exception as e:
        st.error(f"Error en el cálculo: {str(e)}")

def calcular_caja_especializada():
    """Calcula medidas para calculadoras especializadas"""
    try:
        modo = st.session_state.calculator_mode
        calculadora = CalculadorasCajas()
        
        if modo == 'cesta':
            resultados = calculadora.calcular_cesta(
                st.session_state.espesor_caja,
                st.session_state.largo_caja,
                st.session_state.ancho_caja, 
                st.session_state.alto_caja,
                st.session_state.acabado_virada,
                st.session_state.acabado_altura
            )
        elif modo == 'tapa_libro':
            resultados = calculadora.calcular_tapa_libro(
                st.session_state.espesor_caja,
                st.session_state.largo_caja,
                st.session_state.ancho_caja,
                st.session_state.alto_caja,
                st.session_state.acabado_virada,
                st.session_state.espacio_ranura
            )
        elif modo == 'tapa_suelta':
            resultados = calculadora.calcular_tapa_suelta(
                st.session_state.espesor_caja,
                st.session_state.largo_caja,
                st.session_state.ancho_caja,
                st.session_state.alto_caja,
                st.session_state.altura_tapa,
                st.session_state.acabado_virada
            )
        elif modo == 'redonda':
            resultados = calculadora.calcular_redonda(
                st.session_state.espesor_banda,
                st.session_state.diametro_base,
                st.session_state.altura_banda_base,
                st.session_state.altura_banda_tapa
            )
        
        st.session_state.calculation_result = resultados
        st.success("✅ Cálculo de caja completado exitosamente")
        
    except Exception as e:
        st.error(f"Error en el cálculo de caja: {str(e)}")

def clear_all_fields():
    """Limpia todos los campos y resultados"""
    st.session_state.calculation_result = None
    st.success("🗑️ Campos limpiados")
    st.rerun()

def show_cutting_preview():
    """Muestra la vista previa del corte (solo para modo normal)"""
    if not st.session_state.calculation_result or st.session_state.calculator_mode != 'normal':
        return
        
    result = st.session_state.calculation_result
    
    # Crear gráfico con Plotly
    fig = go.Figure()
    
    # Añadir rectángulo de la hoja
    fig.add_shape(
        type="rect",
        x0=0, y0=0,
        x1=result['sheet_width'], y1=result['sheet_height'],
        line=dict(color="rgba(255, 105, 180, 0.8)", width=3),
        fillcolor="rgba(255, 182, 193, 0.2)"
    )
    
    # Añadir rectángulos de los cortes
    for i in range(result['cuts_horizontal']):
        for j in range(result['cuts_vertical']):
            x0 = i * result['cut_width']
            y0 = j * result['cut_height']
            x1 = x0 + result['cut_width']
            y1 = y0 + result['cut_height']
            
            fig.add_shape(
                type="rect",
                x0=x0, y0=y0, x1=x1, y1=y1,
                line=dict(color="rgba(255, 20, 147, 0.8)", width=2),
                fillcolor="rgba(255, 105, 180, 0.3)"
            )
    
    # Configurar el layout
    fig.update_layout(
        title="Vista Previa de Cortes",
        xaxis_title="Ancho (cm)",
        yaxis_title="Alto (cm)",
        showlegend=False,
        width=600,
        height=400,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_caja_report():
    """Muestra el reporte de medidas de caja"""
    if not st.session_state.calculation_result or st.session_state.calculator_mode == 'normal':
        return
        
    resultados = st.session_state.calculation_result
    
    # Crear DataFrame con los resultados
    data = {
        "Pieza": [resultados[key]['descripcion'] for key in resultados],
        "Medidas (cm)": [resultados[key]['medida'] for key in resultados]
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df, hide_index=True, use_container_width=True)

def show_cut_report():
    """Muestra el reporte de cortes (solo para modo normal)"""
    if not st.session_state.calculation_result or st.session_state.calculator_mode != 'normal':
        return
        
    result = st.session_state.calculation_result
    
    # Crear DataFrame con solo los datos requeridos
    data = {
        "Métrica": [
            "Cortes por hoja",
            "Cortes horizontales", 
            "Cortes verticales",
            "Hojas requeridas",
            "Cortes utilizables",
            "Utilización (%)"
        ],
        "Valor": [
            result.get('cuts_per_sheet', 0),
            result.get('cuts_horizontal', 0),
            result.get('cuts_vertical', 0),
            result.get('sheets_required', 1),
            result.get('usable_cuts', 0),
            f"{result.get('utilization_percentage', 0):.2f}"
        ]
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df, hide_index=True, use_container_width=True)

def export_excel():
    """Exporta los resultados a Excel"""
    if not st.session_state.calculation_result:
        st.error("No hay resultados para exportar")
        return
        
    try:
        if st.session_state.calculator_mode == 'normal':
            # Modo normal
            result = st.session_state.calculation_result
            filtered_data = {
                "Métrica": [
                    "Cortes por hoja",
                    "Cortes horizontales", 
                    "Cortes verticales",
                    "Hojas requeridas",
                    "Cortes utilizables",
                    "Utilización (%)"
                ],
                "Valor": [
                    result.get('cuts_per_sheet', 0),
                    result.get('cuts_horizontal', 0),
                    result.get('cuts_vertical', 0),
                    result.get('sheets_required', 1),
                    result.get('usable_cuts', 0),
                    f"{result.get('utilization_percentage', 0):.2f}"
                ]
            }
        else:
            # Modos especializados
            resultados = st.session_state.calculation_result
            filtered_data = {
                "Pieza": [resultados[key]['descripcion'] for key in resultados],
                "Medidas (cm)": [resultados[key]['medida'] for key in resultados]
            }
        
        excel_data = st.session_state.export_utils.export_to_excel(filtered_data)
        
        st.download_button(
            label="📊 Descargar Excel",
            data=excel_data,
            file_name=f"reporte_{st.session_state.calculator_mode}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        st.error(f"Error exportando a Excel: {str(e)}")

def export_pdf():
    """Exporta los resultados a PDF"""
    if not st.session_state.calculation_result:
        st.error("No hay resultados para exportar")
        return
        
    try:
        if st.session_state.calculator_mode == 'normal':
            # Modo normal
            result = st.session_state.calculation_result
            filtered_data = {
                "Métrica": [
                    "Cortes por hoja",
                    "Cortes horizontales", 
                    "Cortes verticales",
                    "Hojas requeridas",
                    "Cortes utilizables",
                    "Utilización (%)"
                ],
                "Valor": [
                    result.get('cuts_per_sheet', 0),
                    result.get('cuts_horizontal', 0),
                    result.get('cuts_vertical', 0),
                    result.get('sheets_required', 1),
                    result.get('usable_cuts', 0),
                    f"{result.get('utilization_percentage', 0):.2f}"
                ]
            }
        else:
            # Modos especializados
            resultados = st.session_state.calculation_result
            filtered_data = {
                "Pieza": [resultados[key]['descripcion'] for key in resultados],
                "Medidas (cm)": [resultados[key]['medida'] for key in resultados]
            }
        
        pdf_data = st.session_state.export_utils.export_to_pdf(filtered_data)
        
        st.download_button(
            label="📄 Descargar PDF",
            data=pdf_data,
            file_name=f"reporte_{st.session_state.calculator_mode}.pdf",
            mime="application/pdf"
        )
        
    except Exception as e:
        st.error(f"Error exportando a PDF: {str(e)}")

def generate_share_link():
    """Genera un link para compartir los resultados"""
    if not st.session_state.calculation_result:
        st.error("No hay resultados para compartir")
        return
        
    try:
        # ENLACE_COMPARTIR #frambuesa - Lugar para cambiar URL base
        base_url = "https://tu-app-url.com"  # Cambiar por la URL real de la app
        
        params = {
            'shared': 'true',
            'mode': st.session_state.calculator_mode
        }
        
        # Agregar parámetros según el modo
        if st.session_state.calculator_mode == 'normal':
            result = st.session_state.calculation_result
            params.update({
                'sheet_width': result.get('sheet_width', 100),
                'sheet_height': result.get('sheet_height', 70),
                'cut_width': result.get('cut_width', 10),
                'cut_height': result.get('cut_height', 7)
            })
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        share_url = f"{base_url}?{query_string}"
        
        st.code(share_url, language="text")
        st.success("🔗 Link generado para compartir")
        
    except Exception as e:
        st.error(f"Error generando link: {str(e)}")

def check_easter_eggs(sheet_width, sheet_height, cut_width, cut_height):
    """Verifica múltiples combinaciones de easter eggs"""
    values = [sheet_width, sheet_height, cut_width, cut_height]
    
    if all(v == 67.0 for v in values):
        return "magic_67"
    elif all(v == 42.0 for v in values):
        return "answer_universe"
    elif values == [1.0, 2.0, 3.0, 4.0]:
        return "sequential"
    elif all(v == 777.0 for v in values):
        return "lucky_777"
    elif all(v == 0.0 for v in values):
        return "zero_void"
    elif all(v == 100.0 for v in values):
        return "perfect_100"
    return None

def show_easter_egg(egg_type):
    """Muestra diferentes easter eggs según el tipo"""
    easter_eggs = {
        "magic_67": {
            "title": "🎉 ¡Easter Egg Desbloqueado! 🎉",
            "message": "¡Has encontrado el número mágico 67!",
            # ENLACE_EASTER_EGG #frambuesa - Lugar para cambiar enlace
            "link": "https://github.com/streamlit/streamlit",
            "link_text": "🔗 Enlace Secreto - Descubre Streamlit",
            "color": "linear-gradient(135deg, #FFD700, #FFA500)"
        },
        "answer_universe": {
            "title": "🌌 ¡La Respuesta Universal! 🌌",
            "message": "42 - La respuesta a la vida, el universo y todo",
            # ENLACE_EASTER_EGG #frambuesa - Lugar para cambiar enlace
            "link": "https://es.wikipedia.org/wiki/42_(n%C3%BAmero)",
            "link_text": "🌠 Descubre el Misterio del 42",
            "color": "linear-gradient(135deg, #4169E1, #1E90FF)"
        },
        "sequential": {
            "title": "🔢 ¡Secuencia Perfecta! 🔢",
            "message": "1, 2, 3, 4... ¡El orden perfecto!",
            # ENLACE_EASTER_EGG #frambuesa - Lugar para cambiar enlace
            "link": "https://oeis.org/A000027",
            "link_text": "📊 Números Naturales",
            "color": "linear-gradient(135deg, #32CD32, #00FF00)"
        },
        "lucky_777": {
            "title": "🍀 ¡Súper Suerte! 🍀",
            "message": "¡Triple 7! ¡La fortuna te sonríe!",
            # ENLACE_EASTER_EGG #frambuesa - Lugar para cambiar enlace
            "link": "https://es.wikipedia.org/wiki/777_(n%C3%BAmero)",
            "link_text": "🎰 Descubre la Suerte del 777",
            "color": "linear-gradient(135deg, #FFD700, #FF6347)"
        },
        "zero_void": {
            "title": "🌑 ¡El Vacío Absoluto! 🌑",
            "message": "Cero... el principio y el fin de todo",
            # ENLACE_EASTER_EGG #frambuesa - Lugar para cambiar enlace
            "link": "https://es.wikipedia.org/wiki/Cero",
            "link_text": "🔮 El Misterio del Cero",
            "color": "linear-gradient(135deg, #2F4F4F, #000000)"
        },
        "perfect_100": {
            "title": "💯 ¡Perfección Total! 💯",
            "message": "¡100% en todo! ¡Eres increíble!",
            # ENLACE_EASTER_EGG #frambuesa - Lugar para cambiar enlace
            "link": "https://es.wikipedia.org/wiki/100_(n%C3%BAmero)",
            "link_text": "⭐ La Perfección del 100",
            "color": "linear-gradient(135deg, #FF1493, #FF69B4)"
        }
    }
    
    egg = easter_eggs.get(egg_type)
    if egg:
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <h3>{egg['title']}</h3>
            <p>{egg['message']}</p>
            <a href="{egg['link']}" target="_blank" class="easter-egg-link" style="background: {egg['color']};">
                {egg['link_text']}
            </a>
        </div>
        """, unsafe_allow_html=True)

def load_shared_params():
    """Carga parámetros compartidos desde la URL si existen"""
    try:
        # Obtener parámetros de la URL
        query_params = st.query_params
        
        shared_params = {}
        
        # Verificar si es un link compartido
        if query_params.get('shared') == 'true':
            # Mostrar mensaje de link compartido
            st.success("📋 Se han cargado parámetros desde un enlace compartido")
            
            # Extraer parámetros numéricos
            for param in ['sheet_width', 'sheet_height', 'cut_width', 'cut_height']:
                if param in query_params:
                    try:
                        shared_params[param] = float(query_params[param])
                    except (ValueError, TypeError):
                        pass  # Ignorar parámetros inválidos
        
        return shared_params
        
    except Exception as e:
        st.error(f"Error cargando parámetros compartidos: {str(e)}")
        return {}

# -------------------- INTERFAZ DE USUARIO --------------------
def render_normal_mode(shared_params):
    """Renderiza la interfaz del modo normal"""
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📐 Tamaño del Pliego de Cartón")
    sheet_width = st.number_input("Ancho de la hoja (cm)", min_value=0.1, 
                                 value=shared_params.get('sheet_width', 100.0), step=0.1)
    sheet_height = st.number_input("Alto de la hoja (cm)", min_value=0.1, 
                                  value=shared_params.get('sheet_height', 70.0), step=0.1)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### ✂️ Tamaño del Corte")
    cut_width = st.number_input("Ancho del corte (cm)", min_value=0.1, 
                               value=shared_params.get('cut_width', 10.0), step=0.1)
    cut_height = st.number_input("Alto del corte (cm)", min_value=0.1, 
                                value=shared_params.get('cut_height', 7.0), step=0.1)
    
    # Validación en tiempo real
    validation_errors = []
    if cut_width > sheet_width:
        validation_errors.append(f"⚠️ El ancho del corte ({cut_width} cm) es mayor que el ancho de la hoja ({sheet_width} cm)")
    if cut_height > sheet_height:
        validation_errors.append(f"⚠️ El alto del corte ({cut_height} cm) es mayor que el alto de la hoja ({sheet_height} cm)")
    
    # Mostrar errores de validación
    if validation_errors:
        for error in validation_errors:
            st.error(error)
        st.info("💡 Ajusta las dimensiones del corte para que sean menores o iguales a las de la hoja.")
    else:
        # Mostrar mensaje de validación exitosa
        st.success("✅ Las dimensiones son válidas")
    
    # Verificar easter eggs
    easter_egg_type = check_easter_eggs(sheet_width, sheet_height, cut_width, cut_height)
    if easter_egg_type:
        show_easter_egg(easter_egg_type)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Botones
    col_opt, col_clear = st.columns([1, 1])
    with col_opt:
        if st.button("🎯 Calcular Óptimo", use_container_width=True):
            if not validation_errors:
                calculate_optimal(sheet_width, sheet_height, cut_width, cut_height)
            else:
                st.error("❌ Corrige los errores de validación antes de calcular")
    with col_clear:
        if st.button("🗑️ Limpiar Todo", use_container_width=True):
            clear_all_fields()
    
    return sheet_width, sheet_height, cut_width, cut_height

def render_cesta_mode():
    """Renderiza la interfaz del modo Cesta"""
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📦 Dimensiones de la Caja Cesta")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.espesor_caja = st.number_input("Espesor del cartón (mm)", min_value=0.1, value=2.0, step=0.1, key="espesor_cesta")
    with col2:
        st.session_state.largo_caja = st.number_input("Largo de la caja (cm)", min_value=0.1, value=15.0, step=0.1, key="largo_cesta")
    with col3:
        st.session_state.ancho_caja = st.number_input("Ancho de la caja (cm)", min_value=0.1, value=9.0, step=0.1, key="ancho_cesta")
    
    st.session_state.alto_caja = st.number_input("Alto de la caja (cm)", min_value=0.1, value=5.0, step=0.1, key="alto_cesta")
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🎨 Acabados para Revestimiento")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.acabado_virada = st.number_input("Acabado virada lateral (cm)", min_value=0.0, value=1.0, step=0.1, key="virada_cesta")
    with col2:
        st.session_state.acabado_altura = st.number_input("Acabado virada altura (cm)", min_value=0.0, value=1.5, step=0.1, key="altura_cesta")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Botones
    col_calc, col_clear = st.columns([1, 1])
    with col_calc:
        if st.button("🎯 Calcular Medidas", use_container_width=True):
            calcular_caja_especializada()
    with col_clear:
        if st.button("🗑️ Limpiar Todo", use_container_width=True):
            clear_all_fields()

def render_tapa_libro_mode():
    """Renderiza la interfaz del modo Tapa Libro"""
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📚 Dimensiones de la Caja Tapa Libro")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.espesor_caja = st.number_input("Espesor del cartón (mm)", min_value=0.1, value=2.0, step=0.1, key="espesor_libro")
    with col2:
        st.session_state.largo_caja = st.number_input("Largo de la caja (cm)", min_value=0.1, value=25.0, step=0.1, key="largo_libro")
    with col3:
        st.session_state.ancho_caja = st.number_input("Ancho de la caja (cm)", min_value=0.1, value=30.0, step=0.1, key="ancho_libro")
    
    st.session_state.alto_caja = st.number_input("Alto de la caja (cm)", min_value=0.1, value=7.0, step=0.1, key="alto_libro")
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Configuración Tapa Libro")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.acabado_virada = st.number_input("Acabado virada (cm)", min_value=0.0, value=1.0, step=0.1, key="virada_libro")
    with col2:
        st.session_state.espacio_ranura = st.number_input("Espacio ranura (cm)", min_value=0.0, value=0.3, step=0.1, key="ranura_libro")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Botones
    col_calc, col_clear = st.columns([1, 1])
    with col_calc:
        if st.button("🎯 Calcular Medidas", use_container_width=True):
            calcular_caja_especializada()
    with col_clear:
        if st.button("🗑️ Limpiar Todo", use_container_width=True):
            clear_all_fields()

def render_tapa_suelta_mode():
    """Renderiza la interfaz del modo Tapa Suelta"""
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🧩 Dimensiones de la Caja Tapa Suelta")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.espesor_caja = st.number_input("Espesor del cartón (mm)", min_value=0.1, value=2.0, step=0.1, key="espesor_suelta")
    with col2:
        st.session_state.largo_caja = st.number_input("Largo de la caja (cm)", min_value=0.1, value=25.0, step=0.1, key="largo_suelta")
    with col3:
        st.session_state.ancho_caja = st.number_input("Ancho de la caja (cm)", min_value=0.1, value=25.0, step=0.1, key="ancho_suelta")
    
    st.session_state.alto_caja = st.number_input("Alto de la caja (cm)", min_value=0.1, value=25.0, step=0.1, key="alto_suelta")
    st.session_state.altura_tapa = st.number_input("Altura de la tapa (cm)", min_value=0.1, value=3.0, step=0.1, key="altura_tapa_suelta")
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🎨 Acabados para Revestimiento")
    
    st.session_state.acabado_virada = st.number_input("Acabado virada (cm)", min_value=0.0, value=1.5, step=0.1, key="virada_suelta")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Botones
    col_calc, col_clear = st.columns([1, 1])
    with col_calc:
        if st.button("🎯 Calcular Medidas", use_container_width=True):
            calcular_caja_especializada()
    with col_clear:
        if st.button("🗑️ Limpiar Todo", use_container_width=True):
            clear_all_fields()

def render_redonda_mode():
    """Renderiza la interfaz del modo Redonda"""
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🔵 Dimensiones de la Caja Redonda")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.espesor_banda = st.number_input("Espesor de la banda (mm)", min_value=0.1, value=1.3, step=0.1, key="espesor_redonda")
    with col2:
        st.session_state.diametro_base = st.number_input("Diámetro de la base (cm)", min_value=0.1, value=20.0, step=0.1, key="diametro_redonda")
    
    st.session_state.altura_banda_base = st.number_input("Altura de la banda base (cm)", min_value=0.1, value=20.0, step=0.1, key="altura_base_redonda")
    st.session_state.altura_banda_tapa = st.number_input("Altura de la banda tapa (cm)", min_value=0.1, value=3.0, step=0.1, key="altura_tapa_redonda")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Botones
    col_calc, col_clear = st.columns([1, 1])
    with col_calc:
        if st.button("🎯 Calcular Medidas", use_container_width=True):
            calcular_caja_especializada()
    with col_clear:
        if st.button("🗑️ Limpiar Todo", use_container_width=True):
            clear_all_fields()

# -------------------- MAIN --------------------
def main():
    st.set_page_config(
        page_title="Calculadora de Cortes y Cajas",
        page_icon="✂️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    load_css()
    load_js()
    initialize_app()

    # IMAGEN_LOGO #frambuesa - Lugar para cambiar logo
    logo_b64 = load_image_base64("/assets/Imagen2.jpeg")
    
    # Header con controles de tema y modo calculadora
    col_header, col_mode, col_theme, col_toggle = st.columns([3, 2, 1, 1])
    
    with col_header:
        st.markdown(f"""
        <div class="header-container" style="margin-bottom:30px;">
            <div class="logo-container">
                <img src="data:image/svg+xml;base64,{logo_b64}" class="logo" style="border-radius: 50%; width: 80px; height: 80px;">
            </div>
            <h1 class="main-title">✂️ Calculadora Profesional de Cortes y Cajas</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col_mode:
        st.markdown("### 🧮 Modo Calculadora")
        modos_calculadora = {
            'normal': '✂️ Corte Normal',
            'cesta': '🧺 Caja Cesta',
            'tapa_libro': '📚 Tapa Libro', 
            'tapa_suelta': '🧩 Tapa Suelta',
            'redonda': '🔵 Caja Redonda'
        }
        
        selected_mode = st.selectbox(
            "Seleccionar modo",
            options=list(modos_calculadora.keys()),
            format_func=lambda x: modos_calculadora[x],
            index=list(modos_calculadora.keys()).index(st.session_state.calculator_mode),
            label_visibility="collapsed"
        )
        
        if selected_mode != st.session_state.calculator_mode:
            st.session_state.calculator_mode = selected_mode
            st.session_state.calculation_result = None
            st.rerun()
    
    with col_theme:
        st.markdown("### 🎨 Tema")
        theme_options = {
            'clasico': '🌸 Clásico',
            'rosa': '🌹 Rosa',
            'minimalista': '⚪ Minimalista'
        }
        
        selected_theme = st.selectbox(
            "Seleccionar tema",
            options=list(theme_options.keys()),
            format_func=lambda x: theme_options[x],
            index=list(theme_options.keys()).index(st.session_state.theme_mode),
            label_visibility="collapsed"
        )
        
        if selected_theme != st.session_state.theme_mode:
            st.session_state.theme_mode = selected_theme
            st.rerun()
    
    with col_toggle:
        st.markdown("### 🌓 Modo")
        dark_mode_icon = "🌙" if st.session_state.dark_mode else "☀️"
        mode_text = "Oscuro" if st.session_state.dark_mode else "Claro"
        
        if st.button(f"{dark_mode_icon} {mode_text}", key="mode_toggle", help="Cambiar tema"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    # Elementos decorativos
    show_decoration_elements()

    # Floating bar
    show_floating_bar()

    # Cargar parámetros compartidos si existen
    shared_params = load_shared_params()
    
    col1, col2 = st.columns([1, 1])

    # -------------------- COLUMNA 1: INPUTS --------------------
    with col1:
        # Renderizar interfaz según el modo seleccionado
        if st.session_state.calculator_mode == 'normal':
            render_normal_mode(shared_params)
        elif st.session_state.calculator_mode == 'cesta':
            render_cesta_mode()
        elif st.session_state.calculator_mode == 'tapa_libro':
            render_tapa_libro_mode()
        elif st.session_state.calculator_mode == 'tapa_suelta':
            render_tapa_suelta_mode()
        elif st.session_state.calculator_mode == 'redonda':
            render_redonda_mode()

    # -------------------- COLUMNA 2: RESULTADOS --------------------
    with col2:
        if st.session_state.calculator_mode == 'normal':
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Vista Previa de Cortes")
            st.markdown("<p style='font-size: 14px; opacity: 0.8;'>La gráfica es interactiva - puedes hacer zoom y arrastrar</p>", unsafe_allow_html=True)
            if st.session_state.calculation_result:
                show_cutting_preview()
            else:
                st.info("Haz clic en 'Calcular Óptimo' para ver la vista previa")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### 📈 Reporte de Cortes")
            if st.session_state.calculation_result:
                show_cut_report()
            else:
                st.info("Los resultados aparecerán aquí después del cálculo")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### 📋 Medidas de la Caja")
            st.markdown("<p style='font-size: 14px; opacity: 0.8;'>Todas las medidas necesarias para construir la caja</p>", unsafe_allow_html=True)
            if st.session_state.calculation_result:
                show_caja_report()
            else:
                st.info("Haz clic en 'Calcular Medidas' para ver los resultados")
            st.markdown('</div>', unsafe_allow_html=True)

        # Botones de descarga y compartir (siempre visibles)
        if st.session_state.calculation_result:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### 💾 Exportar Resultados")
            
            col_excel, col_pdf, col_share = st.columns([1, 1, 1])
            with col_excel:
                if st.button("📊 Excel", key="excel_btn", help="Descargar resultados como Excel", use_container_width=True):
                    export_excel()
            with col_pdf:
                if st.button("📄 PDF", key="pdf_btn", help="Descargar resultados como PDF", use_container_width=True):
                    export_pdf()
            with col_share:
                if st.button("🔗 Compartir", key="share_btn", help="Generar enlace para compartir", use_container_width=True):
                    generate_share_link()
            st.markdown('</div>', unsafe_allow_html=True)

        # Controles de personalización de colores (siempre visibles)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        with st.expander("🎨 Personalizar Colores", expanded=False):
            col_primary, col_secondary = st.columns(2)
            
            with col_primary:
                new_primary = st.color_picker(
                    "Color Primario",
                    value=st.session_state.custom_colors['primary'],
                    key="primary_color"
                )
            
            with col_secondary:
                new_secondary = st.color_picker(
                    "Color Secundario", 
                    value=st.session_state.custom_colors['secondary'],
                    key="secondary_color"
                )
            
            if (new_primary != st.session_state.custom_colors['primary'] or 
                new_secondary != st.session_state.custom_colors['secondary']):
                st.session_state.custom_colors = {
                    'primary': new_primary,
                    'secondary': new_secondary
                }
                st.rerun()
            
            if st.button("🔄 Restablecer Colores", key="reset_colors"):
                st.session_state.custom_colors = {
                    'primary': '#FF69B4',
                    'secondary': '#FFB6C1'
                }
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Barra social al final
    show_social_bar()

if __name__ == "__main__":
    main()
