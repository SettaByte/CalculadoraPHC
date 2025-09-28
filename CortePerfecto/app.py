import os, base64, streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.calculator import CuttingCalculator
from utils.export_utils import ExportUtils

# Ruta base
BASE_DIR = os.path.dirname(__file__)

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

def initialize_app():
    if 'calculator' not in st.session_state:
        st.session_state.calculator = CuttingCalculator()
    if 'export_utils' not in st.session_state:
        st.session_state.export_utils = ExportUtils()
    if 'calculation_result' not in st.session_state:
        st.session_state.calculation_result = None

def main():
    load_css()
    load_js()
    initialize_app()

    # Header
    logo_b64 = load_image_base64("Imagen2.jpeg")
    st.markdown(f"""
    <div class="header-container">
        <div class="logo-container">
            <img src="data:image/jpeg;base64,{logo_b64}" class="logo" style="border-radius: 50%; width: 80px; height: 80px;">
        </div>
        <h1 class="main-title">Calculadora de Cortes</h1>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    # Column 1: Inputs y botones
    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📐 Tamaño de la Hoja")
        sheet_width = st.number_input("Ancho de la hoja (cm)", min_value=0.1, value=100.0, step=0.1)
        sheet_height = st.number_input("Alto de la hoja (cm)", min_value=0.1, value=70.0, step=0.1)
        grammage = st.number_input("Gramaje (g/m²)", min_value=1, value=80, step=1)

        st.markdown("### ✂️ Tamaño del Corte")
        cut_width = st.number_input("Ancho del corte (cm)", min_value=0.1, value=10.0, step=0.1)
        cut_height = st.number_input("Alto del corte (cm)", min_value=0.1, value=7.0, step=0.1)

        quantity = st.number_input("Cantidad deseada", min_value=1, value=100, step=1)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="button-row">', unsafe_allow_html=True)
        col_opt, col_clear = st.columns(2)
        with col_opt:
            if st.button("🎯 Óptimo", use_container_width=True):
                calculate_optimal(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage)
        with col_clear:
            if st.button("🗑️ Limpiar Todo", use_container_width=True):
                clear_all_fields()
        st.markdown('</div>', unsafe_allow_html=True)

    # Column 2: Gráfica y tabla
    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 👁️ Vista Previa del Área de Corte")
        if st.session_state.calculation_result:
            show_cutting_preview()
        else:
            st.info("Haga clic en 'Óptimo' para ver la vista previa")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Reporte de Cortes")
        if st.session_state.calculation_result:
            show_cut_report()
        else:
            st.info("Los resultados aparecerán aquí después del cálculo")
        st.markdown('</div>', unsafe_allow_html=True)

    show_footer()
    show_floating_bar()

def calculate_optimal(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage):
    result = st.session_state.calculator.calculate_optimal(
        sheet_width, sheet_height, cut_width, cut_height, quantity, grammage
    )

    # Total de cortes limitado a la cantidad pedida
    possible_cuts = result['cuts_horizontal'] * result['cuts_vertical'] * result['sheets_required']
    result['total_cuts'] = min(possible_cuts, quantity)

    st.session_state.calculation_result = result
    st.rerun()

def clear_all_fields():
    for key in list(st.session_state.keys()):
        if key != 'calculator' and key != 'export_utils':
            del st.session_state[key]
    st.rerun()

def show_cutting_preview():
    result = st.session_state.calculation_result
    fig = go.Figure()

    fig.add_shape(
        type="rect",
        x0=0, y0=0,
        x1=result['sheet_width'], y1=result['sheet_height'],
        fillcolor="rgba(255, 182, 193, 0.3)",
        line=dict(color="rgba(255, 182, 193, 1)", width=2)
    )

    for i in range(result['cuts_horizontal']):
        for j in range(result['cuts_vertical']):
            x = i * result['cut_width']
            y = j * result['cut_height']
            if x + result['cut_width'] <= result['sheet_width'] and y + result['cut_height'] <= result['sheet_height']:
                fig.add_shape(
                    type="rect",
                    x0=x, y0=y,
                    x1=x + result['cut_width'], y1=y + result['cut_height'],
                    fillcolor="rgba(255, 105, 180, 0.7)",
                    line=dict(color="rgba(255, 105, 180, 1)", width=1)
                )

    fig.update_layout(
        title=f"Utilización: {result['utilization_percentage']:.1f}%",
        xaxis_title="Ancho (cm)",
        yaxis_title="Alto (cm)",
        showlegend=False,
        height=500,
        width=900,
        plot_bgcolor="white",
        paper_bgcolor="white",
        dragmode="pan",
        updatemenus=[
            dict(
                type="buttons",
                y=1.05,
                x=1.05,
                xanchor="right",
                yanchor="top",
                buttons=[
                    dict(label="Zoom In", method="relayout",
                         args=[{"xaxis.range": [0, result['sheet_width']/2], "yaxis.range": [0, result['sheet_height']/2]}]),
                    dict(label="Zoom Out", method="relayout",
                         args=[{"xaxis.range": [0, result['sheet_width']], "yaxis.range": [0, result['sheet_height']]}]),
                    dict(label="Mover", method="relayout",
                         args=[{"dragmode": "pan"}])
                ]
            )
        ]
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Área Utilizada", f"{result['utilization_percentage']:.1f}%")
    with col2:
        st.metric("Área Desperdiciada", f"{100 - result['utilization_percentage']:.1f}%")

def show_cut_report():
    result = st.session_state.calculation_result
    report_data = {
        "Métrica": [
            "📐 Ancho de la hoja (cm)",
            "📐 Alto de la hoja (cm)",
            "📐 Gramaje (g/m²)",
            "✂️ Ancho del corte (cm)",
            "✂️ Alto del corte (cm)",
            "Total de cortes",
            "Peso final (g)"
        ],
        "Valor": [
            f"{result['sheet_width']:.2f}",
            f"{result['sheet_height']:.2f}",
            f"{result['grammage']}",
            f"{result['cut_width']:.2f}",
            f"{result['cut_height']:.2f}",
            result['total_cuts'],
            f"{result['final_weight']:.2f}"
        ]
    }
    df = pd.DataFrame(report_data)
    st.info("💡 Esta tabla muestra los resultados y los datos de entrada. Usa el scroll si es necesario.")
    st.dataframe(df, height=250)

def show_footer():
    st.markdown("""
    <div class="footer">
        <div class="social-media">
            <a href="https://www.instagram.com/p.h.cajas/" target="_blank" class="social-link">
                <i class="fab fa-instagram"></i>
            </a>
            <a href="https://tiktok.com" target="_blank" class="social-link">
                <i class="fab fa-tiktok"></i>
            </a>
            <a href="https://www.facebook.com/profile.php?id=61576728375462&mibextid=
