import os, base64, streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.calculator import CuttingCalculator
from utils.export_utils import ExportUtils
# from utils.database import DatabaseManager  # Opcional: solo si tienes DB
from datetime import datetime

# Ruta base
BASE_DIR = os.path.dirname(__file__)

# ---------- UTILIDADES ----------
def load_image_base64(filename):
    img_path = os.path.join(BASE_DIR, "assets", filename)
    if not os.path.exists(img_path):
        st.error(f"No se encontró la imagen: {img_path}")
        return ""
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def show_floating_bar():
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

def load_css():
    css_path = os.path.join(BASE_DIR, "static", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_js():
    js_path = os.path.join(BASE_DIR, "static", "script.js")
    if os.path.exists(js_path):
        with open(js_path, "r") as f:
            st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)

# ---------- INICIALIZACIÓN ----------
def initialize_app():
    if 'calculator' not in st.session_state:
        st.session_state.calculator = CuttingCalculator()
    if 'export_utils' not in st.session_state:
        st.session_state.export_utils = ExportUtils()
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = None  # Para que funcione aunque no haya DB
    if 'special_code_check' not in st.session_state:
        st.session_state.special_code_check = {"width": "", "height": "", "quantity": ""}
    if 'comparison_mode' not in st.session_state:
        st.session_state.comparison_mode = False
    if 'comparison_configs' not in st.session_state:
        st.session_state.comparison_configs = []

# ---------- EASTER EGG ----------
def check_special_code(sheet_width, sheet_height, grammage, cost_per_sheet, cut_width, cut_height):
    try:
        w = int(sheet_width)
        h = int(sheet_height)
        g = int(grammage)
        c = int(cost_per_sheet)
        cw = int(cut_width)
        ch = int(cut_height)

        if all(x == 67 for x in [w, h, g, c, cw, ch]):
            secret_url = (
                "https://imgs.search.brave.com/"
                "GlSKdEx-RwYTPm6AW96H8dw2SILz2VcKAoT7gTada4g/"
                "rs:fit:860:0:0:0/g:ce/"
                "aHR0cHM6Ly9wcmV2aWV3LnJlZGQuaXQv/dGhpcy1tZW1lLWJy/"
                "b3VnaHQtdG8teW91LWJ5LXRoZS11bmNzLW9mLWFtZXJpY2Et/"
                "NjctaXNudC12MC1t/N3JndTVlbmU1bmYx/LmpwZWc_d2lkdGg9/"
                "MjI0JmF1dG89d2Vi/cCZzPTIxMjcyZjMz/MWRmZGExOGI2OTQ3/"
                "MGQ3NmExNDVkOTQ5/NWYwODBjMDM"
            )
            st.success("¡MANGO MANGO MANGO!")
            st.markdown(f"🔗[ABRIR EASTER EGG]({secret_url})", unsafe_allow_html=True)
    except ValueError:
        pass

# ---------- FUNCIONES DE CÁLCULO ----------
def calculate_optimal(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet=0):
    result = st.session_state.calculator.calculate_optimal(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage)
    result['cost_per_sheet'] = cost_per_sheet
    result['total_cost'] = result['sheets_required'] * cost_per_sheet
    st.session_state.calculation_result = result
    st.session_state.calculation_type = "optimal"

def calculate_inline(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet=0):
    result = st.session_state.calculator.calculate_inline(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage)
    result['cost_per_sheet'] = cost_per_sheet
    result['total_cost'] = result['sheets_required'] * cost_per_sheet
    st.session_state.calculation_result = result
    st.session_state.calculation_type = "inline"

def clear_all_fields():
    keys_to_keep = ['calculator', 'export_utils', 'db_manager', 'comparison_mode', 'comparison_configs']
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]

# ---------- VISTA PREVIA ----------
def show_cutting_preview():
    result = st.session_state.calculation_result
    fig = go.Figure()
    # Hoja
    fig.add_shape(type="rect", x0=0, y0=0, x1=result['sheet_width'], y1=result['sheet_height'],
                  fillcolor="rgba(200,200,200,0.3)", line=dict(color="black", width=2))
    # Cortes
    for i in range(result['cuts_horizontal']):
        for j in range(result['cuts_vertical']):
            x = i * result['cut_width']
            y = j * result['cut_height']
            if x + result['cut_width'] <= result['sheet_width'] and y + result['cut_height'] <= result['sheet_height']:
                fig.add_shape(type="rect", x0=x, y0=y, x1=x+result['cut_width'], y1=y+result['cut_height'],
                              fillcolor="rgba(255,105,180,0.7)", line=dict(color="rgba(255,105,180,1)", width=1))
    fig.update_layout(title=f"Utilización: {result['utilization_percentage']:.1f}%",
                      xaxis_title="Ancho (cm)", yaxis_title="Alto (cm)",
                      height=400, plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns(2)
    col1.metric("Área Utilizada", f"{result['utilization_percentage']:.1f}%")
    col2.metric("Área Desperdiciada", f"{100 - result['utilization_percentage']:.1f}%")

# ---------- REPORTE ----------
def show_cut_report():
    result = st.session_state.calculation_result
    report_data = {
        "Métrica": ["Cortes por hoja", "Cortes utilizables", "Cortes horizontales", "Cortes verticales",
                    "Hojas requeridas", "Total de cortes", "Peso final (g)", "Costo por hoja ($)", "Costo total ($)"],
        "Valor": [result['cuts_per_sheet'], result['usable_cuts'], result['cuts_horizontal'], result['cuts_vertical'],
                  result['sheets_required'], result['total_cuts'], f"{result['final_weight']:.2f}",
                  f"{result.get('cost_per_sheet',0):.2f}", f"{result.get('total_cost',0):.2f}"]
    }
    df = pd.DataFrame(report_data)
    st.table(df)

# ---------- EXPORTACIÓN SIMULADA ----------
def export_excel(): 
    st.info("Función de exportar a Excel simulada")

def export_pdf(): 
    st.info("Función de exportar a PDF simulada")

def print_report():
    st.info("Función de impresión simulada")

def send_email():
    st.info("Función de envío de email simulada")

# ---------- MAIN ----------
def main():
    st.set_page_config(page_title="Calculadora de Cortes", page_icon="✂️", layout="wide")
    load_css()
    load_js()
    initialize_app()

    logo_b64 = load_image_base64("Imagen2.jpeg")
    st.markdown(f"<img src='data:image/jpeg;base64,{logo_b64}' width=80 style='border-radius:50%'>", unsafe_allow_html=True)

    # Inputs
    col1, col2 = st.columns([1,1])
    with col1:
        sheet_width = st.number_input("Ancho de la hoja (cm)", min_value=0.1, value=100.0, step=0.1)
        sheet_height = st.number_input("Alto de la hoja (cm)", min_value=0.1, value=70.0, step=0.1)
        grammage = st.number_input("Gramaje (g/m²)", min_value=1, value=80, step=1)
        cost_per_sheet = st.number_input("Costo por hoja ($)", min_value=0.0, value=0.0, step=0.01)
        cut_width = st.number_input("Ancho del corte (cm)", min_value=0.1, value=10.0, step=0.1)
        cut_height = st.number_input("Alto del corte (cm)", min_value=0.1, value=7.0, step=0.1)
        quantity = 100

        check_special_code(sheet_width, sheet_height, grammage, cost_per_sheet, cut_width, cut_height)

        col_opt, col_inline, col_clear = st.columns(3)
        with col_opt:
            if st.button("🎯 Óptimo"):
                calculate_optimal(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet)
        with col_inline:
            if st.button("📏 En Línea"):
                calculate_inline(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet)
        with col_clear:
            if st.button("🗑️ Limpiar"):
                clear_all_fields()

    with col2:
        if 'calculation_result' in st.session_state:
            show_cutting_preview()
            show_cut_report()
        else:
            st.info("Realice un cálculo para ver resultados")

    show_floating_bar()

if __name__ == "__main__":
    main()
