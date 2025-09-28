import os, base64, streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.calculator import CuttingCalculator
from utils.export_utils import ExportUtils

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
        <div id="floatingBar" class="floating-bar" style="margin-bottom:20px;">
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

    # Forzar inputs en negro y botones centrados
    st.markdown("""
    <style>
    .stNumberInput label, .stTextInput label {
        color: black !important;
    }
    .stButton>button {
        white-space: nowrap;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

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

    logo_b64 = load_image_base64("Imagen2.jpeg")
    st.markdown(f"""
    <div class="header-container" style="margin-bottom:30px;">
        <div class="logo-container">
            <img src="data:image/jpeg;base64,{logo_b64}" class="logo" style="border-radius: 50%; width: 80px; height: 80px;">
        </div>
        <h1 class="main-title">Calculadora de Cortes</h1>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])  # Inputs a la izquierda, gráfica a la derecha

    with col1:
        st.markdown("### 📐 Tamaño de la Hoja")
        sheet_width = st.number_input("Ancho de la hoja (cm)", min_value=0.1, value=100.0, step=0.1)
        sheet_height = st.number_input("Alto de la hoja (cm)", min_value=0.1, value=70.0, step=0.1)

        st.markdown("### ✂️ Tamaño del Corte")
        cut_width = st.number_input("Ancho del corte (cm)", min_value=0.1, value=10.0, step=0.1)
        cut_height = st.number_input("Alto del corte (cm)", min_value=0.1, value=7.0, step=0.1)

        # Botones alineados
        col_opt, col_clear = st.columns([1, 1])
        with col_opt:
            if st.button("🎯 Óptimo", use_container_width=True):
                calculate_optimal(sheet_width, sheet_height, cut_width, cut_height)
                check_special_code(sheet_width, sheet_height, cut_width, cut_height)
        with col_clear:
            if st.button("🗑️ Limpiar Todo", use_container_width=True):
                clear_all_fields()

    with col2:
        st.markdown("### 👁️ Vista Previa del Área de Corte")
        st.markdown("<p style='font-size:14px;'>Arrastre la esquina superior del eje Y para modificarla</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px;'>Arrastre la esquina derecha del eje X para modificarlo</p>", unsafe_allow_html=True)
        st.info("ℹ️ La gráfica cuenta con barra de herramientas interactiva (zoom in/out, mover, guardar imagen).")

        if st.session_state.calculation_result:
            show_cutting_preview()
        else:
            st.info("Haga clic en 'Óptimo' para ver la vista previa")

        st.markdown("### 📊 Reporte de Cortes")
        if st.session_state.calculation_result:
            show_cut_report()
        else:
            st.info("Los resultados aparecerán aquí después del cálculo")

    show_footer()
    show_floating_bar()

def calculate_optimal(sheet_width, sheet_height, cut_width, cut_height):
    result = st.session_state.calculator.calculate_optimal(
        sheet_width, sheet_height, cut_width, cut_height, 1, 1
    )

    total_cuts_width = int(sheet_width // cut_width)
    total_cuts_height = int(sheet_height // cut_height)
    used_area = total_cuts_width * cut_width * total_cuts_height * cut_height
    total_area = sheet_width * sheet_height
    utilization_percentage = (used_area / total_area) * 100

    result['cuts_horizontal'] = total_cuts_width
    result['cuts_vertical'] = total_cuts_height
    result['utilization_percentage'] = utilization_percentage

    st.session_state.calculation_result = result
    st.rerun()

def clear_all_fields():
    for key in list(st.session_state.keys()):
        if key not in ['calculator', 'export_utils']:
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
        title="",
        xaxis_title="Ancho (cm)",
        yaxis_title="Alto (cm)",
        showlegend=False,
        height=550,
        width=950,
        plot_bgcolor="white",
        paper_bgcolor="white",
        dragmode="pan"
    )

    st.plotly_chart(fig, use_container_width=True, config={
        'modeBarButtonsToRemove': ['zoom2d']
    })

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
            "✂️ Ancho del corte (cm)",
            "✂️ Alto del corte (cm)"
        ],
        "Valor": [
            f"{result['sheet_width']:.2f}",
            f"{result['sheet_height']:.2f}",
            f"{result['cut_width']:.2f}",
            f"{result['cut_height']:.2f}"
        ]
    }
    df = pd.DataFrame(report_data)
    st.info("💡 Esta tabla muestra los resultados y los datos de entrada. Usa el scroll si es necesario.")
    st.dataframe(df, height=250)

    # Descargar PDF
    if st.button("📥 Descargar como PDF", use_container_width=True):
        pdf_path = st.session_state.export_utils.export_to_pdf(df)
        with open(pdf_path, "rb") as f:
            st.download_button("Descargar PDF", f, file_name="reporte_cortes.pdf")

def check_special_code(sheet_width, sheet_height, cut_width, cut_height):
    try:
        w = int(sheet_width)
        h = int(sheet_height)
        cw = int(cut_width)
        ch = int(cut_height)
        if all(x == 67 for x in [w, h, cw, ch]):
            secret_url = "https://www.youtube.com/watch?v=3tQHBUP1tcI"
            st.success("¡MANGO MANGO MANGO!")
            st.markdown(f"🔗[ABRIR EASTER EGG]({secret_url})", unsafe_allow_html=True)
    except ValueError:
        pass

def show_footer():
    st.markdown("""
    <div class="footer" style="margin-top:30px;">
        <div class="social-media">
            <a href="https://www.instagram.com/p.h.cajas/" target="_blank" class="social-link">
                <i class="fab fa-instagram"></i>
            </a>
            <a href="https://tiktok.com" target="_blank" class="social-link">
                <i class="fab fa-tiktok"></i>
            </a>
            <a href="https://www.facebook.com/profile.php?id=61576728375462&mibextid=ZbWKwL" target="_blank" class="social-link">
                <i class="fab fa-facebook"></i>
            </a>
            <a href="https://phcajasdelujo.taplink.mx/" target="_blank" class="social-link">
                <span>Web</span>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
