import os
import base64
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.calculator import CuttingCalculator
from utils.export_utils import ExportUtils

# --- Configuración inicial ---
BASE_DIR = os.path.dirname(__file__)

st.set_page_config(
    page_title="Calculadora de Cortes",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Funciones auxiliares ---
def load_image_base64(filename):
    if filename not in st.session_state:
        img_path = os.path.join(BASE_DIR, "assets", filename)
        if not os.path.exists(img_path):
            st.error(f"No se encontró la imagen: {img_path}")
            return ""
        with open(img_path, "rb") as f:
            st.session_state[filename] = base64.b64encode(f.read()).decode("utf-8")
    return st.session_state[filename]

def load_css_js():
    if 'css_loaded' not in st.session_state:
        css_path = os.path.join(BASE_DIR, "static", "styles.css")
        if os.path.exists(css_path):
            with open(css_path, "r") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        js_path = os.path.join(BASE_DIR, "static", "script.js")
        if os.path.exists(js_path):
            with open(js_path, "r") as f:
                st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)
        st.session_state.css_loaded = True

def show_floating_bar():
    img_b64 = load_image_base64("Imagen1.jpeg")
    if img_b64:
        st.markdown(f"""
        <div id="floatingBar" class="floating-bar">
            <div class="floating-content">
                <img src="data:image/jpeg;base64,{img_b64}" 
                     style="height:40px; border-radius: 50%; margin-right: 10px;"/>
                <span class="floating-text">¡Calculadora de Cortes Profesional!</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def initialize_app():
    if 'calculator' not in st.session_state:
        st.session_state.calculator = CuttingCalculator()
    if 'export_utils' not in st.session_state:
        st.session_state.export_utils = ExportUtils()
    defaults = {
        'special_code_check': {"sheet_width":0, "sheet_height":0, "grammage":0, "cost":0, "cut_width":0, "cut_height":0},
        'calculation_result': None,
        'comparison_mode': False,
        'comparison_configs': []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# --- Funciones de cálculo ---
def check_special_code(sheet_width, sheet_height, grammage, cost_per_sheet, cut_width, cut_height):
    try:
        values = [int(sheet_width), int(sheet_height), int(grammage),
                  int(cost_per_sheet), int(cut_width), int(cut_height)]
        if all(v == 67 for v in values):
            secret_url = "https://imgs.search.brave.com/GlSKdEx-RwYTPm6AW96H8dw2SILz2VcKAoT7gTada4g/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9wcmV2aWV3LnJlZGQuaXQv/dGhpcy1tZW1lLWJy/b3VnaHQtdG8teW91/LWJ5LXRoZS11bmNzLW9mLWFtZXJpY2Et/NjctaXNudC12MC1t/N3JndTVlbmU1bmYx/LmpwZWc_d2lkdGg9/MjI0JmF1dG89d2Vi/cCZzPTIxMjcyZjMz/MWRmZGExOGI2OTQ3/MGQ3NmExNDVkOTQ5/NWYwODBjMDM"
            st.success("¡MANGO MANGO MANGO! 🎉")
            st.markdown(f"🔗[ABRIR EASTER EGG]({secret_url})", unsafe_allow_html=True)
    except ValueError:
        pass

def calculate(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet=0, mode='optimal'):
    calc_func = st.session_state.calculator.calculate_optimal if mode=='optimal' else st.session_state.calculator.calculate_inline
    result = calc_func(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage)
    result['cost_per_sheet'] = cost_per_sheet
    result['total_cost'] = result['sheets_required'] * cost_per_sheet
    st.session_state.calculation_result = result
    st.success(f"Cálculo {'Óptimo' if mode=='optimal' else 'En Línea'} Realizado ✅")
    st.info("⚠️ Anote estos resultados en una hoja si desea conservarlos")
    if st.session_state.comparison_mode:
        st.session_state.comparison_configs.append(result.copy())

def clear_all_fields():
    keys_to_clear = [k for k in st.session_state.keys() if k not in ['calculator','export_utils']]
    for key in keys_to_clear:
        del st.session_state[key]
    st.experimental_rerun()

# --- Visualización ---
def show_cutting_preview(max_cuts=500):
    result = st.session_state.calculation_result
    if not result:
        st.info("Realice un cálculo para ver la vista previa")
        return
    
    fig = go.Figure()
    fig.add_shape(type="rect", x0=0, y0=0, x1=result['sheet_width'], y1=result['sheet_height'],
                  fillcolor="rgba(200,200,200,0.2)", line=dict(color="gray", width=2))
    
    total_cuts = result['cuts_horizontal'] * result['cuts_vertical']
    skip = max(1, int(total_cuts / max_cuts))  # Limita rectángulos si hay demasiados
    
    for i in range(result['cuts_horizontal']):
        for j in range(result['cuts_vertical']):
            if (i*j) % skip != 0:
                continue
            x0, y0 = i*result['cut_width'], j*result['cut_height']
            x1, y1 = x0+result['cut_width'], y0+result['cut_height']
            if x1 <= result['sheet_width'] and y1 <= result['sheet_height']:
                fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
                              fillcolor="rgba(255,105,180,0.7)", line=dict(color="rgba(255,105,180,1)", width=1))
    
    fig.update_layout(title=f"Utilización: {result['utilization_percentage']:.1f}%",
                      xaxis_title="Ancho (cm)", yaxis_title="Alto (cm)",
                      height=400, plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1: st.metric("Área Utilizada", f"{result['utilization_percentage']:.1f}%")
    with col2: st.metric("Área Desperdiciada", f"{100 - result['utilization_percentage']:.1f}%")

def show_cut_report():
    result = st.session_state.calculation_result
    if not result:
        st.info("Realice un cálculo para ver el reporte")
        return
    
    report_data = {
        "Métrica": ["Cortes por hoja","Cortes utilizables","Cortes horizontales",
                    "Cortes verticales","Hojas requeridas","Total de cortes",
                    "Peso final (g)","Costo por hoja ($)","Costo total ($)"],
        "Valor": [result['cuts_per_sheet'], result['usable_cuts'], result['cuts_horizontal'],
                  result['cuts_vertical'], result['sheets_required'], result['total_cuts'],
                  f"{result['final_weight']:.2f}", f"{result.get('cost_per_sheet',0):.2f}",
                  f"{result.get('total_cost',0):.2f}"]
    }
    df = pd.DataFrame(report_data)
    st.table(df)

# --- Main ---
def main():
    load_css_js()
    initialize_app()
    
    logo_b64 = load_image_base64("Imagen2.jpeg")
    st.markdown(f"""
    <div style="display:flex; align-items:center;">
        <img src="data:image/jpeg;base64,{logo_b64}" style="border-radius:50%; width:80px; height:80px; margin-right:10px;">
        <h1>Calculadora de Cortes</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("### 📐 Tamaño de la Hoja")
        sheet_width = st.number_input("Ancho de la hoja (cm)", min_value=0.1, value=100.0, step=0.1)
        sheet_height = st.number_input("Alto de la hoja (cm)", min_value=0.1, value=70.0, step=0.1)
        grammage = st.number_input("Gramaje (g/m²)", min_value=1, value=80, step=1)
        st.markdown("### 💰 Cálculo de Costos")
        cost_per_sheet = st.number_input("Costo por hoja ($)", min_value=0.0, value=0.0, step=0.01)
        st.markdown("### ✂️ Tamaño del Corte")
        cut_width = st.number_input("Ancho del corte (cm)", min_value=0.1, value=10.0, step=0.1)
        cut_height = st.number_input("Alto del corte (cm)", min_value=0.1, value=7.0, step=0.1)
        quantity = 100

        check_special_code(sheet_width, sheet_height, grammage, cost_per_sheet, cut_width, cut_height)

        col_opt, col_inline, col_clear = st.columns(3)
        with col_opt:
            if st.button("🎯 Óptimo"):
                calculate(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet, mode='optimal')
        with col_inline:
            if st.button("📏 En Línea"):
                calculate(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet, mode='inline')
        with col_clear:
            if st.button("🗑️ Limpiar"):
                clear_all_fields()
    
    with col2:
        show_cutting_preview()
        show_cut_report()
    
    show_floating_bar()

if __name__ == "__main__":
    main()
