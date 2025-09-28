import os, base64, streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.calculator import CuttingCalculator
from utils.export_utils import ExportUtils
from utils.database import DatabaseManager
from datetime import datetime
from pathlib import Path

# Ruta base donde está este script
BASE_DIR = os.path.dirname(__file__)

def load_image_base64(filename):
    """Convierte una imagen en base64 para usarla en HTML."""
    img_path = os.path.join(BASE_DIR, "assets", filename)
    if not os.path.exists(img_path):
        st.error(f"No se encontró la imagen: {img_path}")
        return ""
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def show_floating_bar():
    """Muestra la barra flotante con imagen en base64"""
    img_b64 = load_image_base64("Imagen1.jpeg")
    if img_b64:
        st.markdown(f"""
        <div id="floatingBar" class="floating-bar">
            <div class="floating-content">
                <img src="data:image/jpeg;base64,{img_b64}" 
                     style="height:40px; border-radius: 50%; margin-right: 10px;"/>
                <span class="floating-text" style="white-space: normal;">¡Calculadora de Cortes Profesional!</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Cortes",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cargar CSS personalizado
def load_css():
    css_path = os.path.join(BASE_DIR, "static", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ No se encontró styles.css")

# Cargar JavaScript personalizado
def load_js():
    js_path = os.path.join(BASE_DIR, "static", "script.js")
    if os.path.exists(js_path):
        with open(js_path, "r") as f:
            st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ No se encontró script.js")

# Inicializar la aplicación
def initialize_app():
    if 'calculator' not in st.session_state:
        st.session_state.calculator = CuttingCalculator()
    if 'export_utils' not in st.session_state:
        st.session_state.export_utils = ExportUtils()
    if 'db_manager' not in st.session_state:
        try:
            st.session_state.db_manager = DatabaseManager()
        except Exception as e:
            st.warning(f"No se pudo conectar a la base de datos: {e}")
            st.session_state.db_manager = None
    if 'special_code_check' not in st.session_state:
        st.session_state.special_code_check = {"width": "", "height": "", "quantity": ""}
    if 'comparison_mode' not in st.session_state:
        st.session_state.comparison_mode = False
    if 'comparison_configs' not in st.session_state:
        st.session_state.comparison_configs = []

def main():
    load_css()
    load_js()
    initialize_app()
    
    # Logo en la parte superior izquierda
    logo_b64 = load_image_base64("Imagen2.jpeg")
    st.markdown(f"""
    <div class="header-container">
        <div class="logo-container">
            <img src="data:image/jpeg;base64,{logo_b64}" class="logo" style="border-radius: 50%; width: 80px; height: 80px;">
        </div>
        <h1 class="main-title">Calculadora de Cortes</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar con nuevas funcionalidades
    with st.sidebar:
        st.markdown("## 🔧 Herramientas")
        show_templates_section()
        show_favorites_section()
        show_history_section()
        show_comparison_section()
        show_statistics_section()
    
    # Layout principal
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📐 Tamaño de la Hoja")
        
        sheet_width = st.number_input(
            "Ancho (cm)",
            min_value=0.1,
            value=100.0,
            step=0.1,
            help="Ingrese el ancho de la hoja en centímetros"
        )
        
        sheet_height = st.number_input(
            "Alto (cm)",
            min_value=0.1,
            value=70.0,
            step=0.1,
            help="Ingrese el alto de la hoja en centímetros"
        )
        
        grammage = st.number_input(
            "Gramaje (g/m²)",
            min_value=1,
            value=80,
            step=1,
            help="Ingrese el gramaje del papel en gramos por metro cuadrado"
        )

        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botón limpiar
        if st.button("🗑️ Limpiar", use_container_width=True):
            clear_all_fields()
        
        st.markdown("### ✂️ Tamaño del Corte")
        
        cut_width = st.number_input(
            "Ancho del corte (cm)",
            min_value=0.1,
            value=10.0,
            step=0.1,
            help="Ingrese el ancho del corte deseado",
            key="cut_width"
        )
        
        cut_height = st.number_input(
            "Alto del corte (cm)",
            min_value=0.1,
            value=7.0,
            step=0.1,
            help="Ingrese el alto del corte deseado",
            key="cut_height"
        )
        
        # Campo de cantidad oculto con valor fijo
        quantity = 100  # Valor por defecto fijo
        
        # Verificar código especial "67"
        cost_per_sheet = 0  # Inicializar para check_special_code
        check_special_code(
            sheet_width,
            sheet_height,
            grammage,
            cost_per_sheet,
            cut_width,
            cut_height
        )
        
        # Botones de acción
        st.markdown('<div class="button-row">', unsafe_allow_html=True)
        col_opt, col_inline, col_clear = st.columns(3)
        
        with col_opt:
            if st.button("🎯 Óptimo", use_container_width=True, type="primary"):
                calculate_optimal(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet)
        
        with col_inline:
            if st.button("📏 En Línea", use_container_width=True):
                calculate_inline(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet)
        
        with col_clear:
            if st.button("🗑️ Limpiar", use_container_width=True):
                clear_all_fields()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Vista previa del área de corte
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 👁️ Vista Previa del Área de Corte")
        
        if 'calculation_result' in st.session_state:
            show_cutting_preview()
        else:
            st.info("Haga clic en 'Óptimo' o 'En Línea' para ver la vista previa")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Reporte de cortes
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Reporte de Cortes")
        
        if 'calculation_result' in st.session_state:
            show_cut_report()
            
            # Botones de exportación
            st.markdown('<div class="export-buttons">', unsafe_allow_html=True)
            col_print, col_email, col_excel, col_pdf = st.columns(4)
            
            with col_print:
                if st.button("🖨️ Imprimir", use_container_width=True):
                    print_report()
            
            with col_email:
                if st.button("📧 Enviar", use_container_width=True):
                    send_email()
            
            with col_excel:
                if st.button("📑 Excel", use_container_width=True):
                    export_excel()
            
            with col_pdf:
                if st.button("📄 PDF", use_container_width=True):
                    export_pdf()
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Los resultados aparecerán aquí después del cálculo")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer con redes sociales
    show_footer()
    
    # Barra flotante
    show_floating_bar()

# --- Resto de funciones (calculate_optimal, calculate_inline, clear_all_fields, show_cutting_preview, etc.) ---
# Se mantienen igual que tu código original, solo revisando que db_manager se use con get() para evitar errores
# y la indentación esté correcta.

if __name__ == "__main__":
    main()
