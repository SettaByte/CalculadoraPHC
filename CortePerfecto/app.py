```python
import os, base64, streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
from utils.calculator import CuttingCalculator
from utils.export_utils import ExportUtils

BASE_DIR = os.path.dirname(__file__)

# -------------------- CARGA DE RECURSOS --------------------
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

    # Estilos mínimos forzados
    st.markdown("""
    <style>
        /* Títulos siempre negros */
        .main-title, h1, h2, h3, h4, h5, h6 {
            color: black !important;
        }
    </style>
    """, unsafe_allow_html=True)

def show_cutting_preview(result):
    """ Gráfico del pliego con cortes """
    fig = go.Figure()

    # Rectángulo del pliego
    fig.add_shape(
        type="rect",
        x0=0, y0=0,
        x1=result['sheet_width'], y1=result['sheet_height'],
        line=dict(color="black"),
        fillcolor="rgba(255,182,193,0.2)"
    )

    # Rectángulos de cortes
    for cut in result['cuts']:
        fig.add_shape(
            type="rect",
            x0=cut['x'], y0=cut['y'],
            x1=cut['x'] + cut['width'], y1=cut['y'] + cut['height'],
            line=dict(color="deeppink"),
            fillcolor="rgba(255,105,180,0.4)"
        )

    fig.update_layout(
        title="Vista previa del corte",
        xaxis=dict(title="Ancho (cm)", range=[0, result['sheet_width'] + 5]),
        yaxis=dict(title="Alto (cm)", range=[0, result['sheet_height'] + 5]),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(page_title="Calculadora de Cortes", layout="wide")
    load_css()

    st.markdown('<h1 class="main-title">Calculadora de Cortes</h1>', unsafe_allow_html=True)

    # Inputs
    st.subheader("Tamaño del Pliego de Cartón")
    sheet_width = st.number_input("Ancho de hoja (cm)", min_value=1, value=100)
    sheet_height = st.number_input("Alto de hoja (cm)", min_value=1, value=70)

    st.subheader("Tamaño del Corte")
    cut_width = st.number_input("Ancho del corte (cm)", min_value=1, value=10)
    cut_height = st.number_input("Alto del corte (cm)", min_value=1, value=10)

    # Calcular cortes
    if st.button("Calcular"):
        calc = CuttingCalculator(sheet_width, sheet_height, cut_width, cut_height)
        result = calc.calculate()

        st.success("¡Cálculo completado!")

        # Mostrar preview
        show_cutting_preview(result)

        # Mostrar tabla
        df = pd.DataFrame([
            ["Ancho de hoja (cm)", sheet_width],
            ["Alto de hoja (cm)", sheet_height],
            ["Ancho del corte (cm)", cut_width],
            ["Alto del corte (cm)", cut_height],
            ["Cantidad de cortes", result['num_cuts']]
        ], columns=["Métrica", "Valor"])

        st.table(df)

        # Exportación
        export_utils = ExportUtils()

        pdf_bytes = export_utils.to_pdf(df)
        excel_bytes = export_utils.to_excel(df)

        st.markdown('<div class="export-buttons">', unsafe_allow_html=True)

        st.download_button(
            label="📄 Descargar PDF",
            data=pdf_bytes,
            file_name="reporte_cortes.pdf",
            mime="application/pdf"
        )

        st.download_button(
            label="📊 Descargar Excel",
            data=excel_bytes,
            file_name="reporte_cortes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.markdown('</div>', unsafe_allow_html=True)

    # Barra flotante
    show_floating_bar()

if __name__ == "__main__":
    main()
```
