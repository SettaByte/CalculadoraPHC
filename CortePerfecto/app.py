import os, json, base64, streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ----------------- Utilidades JSON -----------------
def load_json(file):
    path = os.path.join(DATA_DIR, file)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_json(file, data):
    path = os.path.join(DATA_DIR, file)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ----------------- Imágenes -----------------
def load_image_base64(filename):
    path = os.path.join(BASE_DIR, "assets", filename)
    if not os.path.exists(path):
        st.error(f"No se encontró la imagen: {path}")
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ----------------- CSS y JS -----------------
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

# ----------------- Inicialización -----------------
def initialize_app():
    if 'calculation_result' not in st.session_state:
        st.session_state.calculation_result = None
    if 'comparison_configs' not in st.session_state:
        st.session_state.comparison_configs = []
    if 'comparison_mode' not in st.session_state:
        st.session_state.comparison_mode = False

# ----------------- Código secreto -----------------
def check_special_code(sheet_width, sheet_height, grammage, cost_per_sheet, cut_width, cut_height):
    try:
        values = [int(sheet_width), int(sheet_height), int(grammage), int(cost_per_sheet), int(cut_width), int(cut_height)]
        if all(v == 67 for v in values):
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
    except:
        pass

# ----------------- Cálculos -----------------
def calculate_optimal(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet=0):
    # Simulación de cálculo simple
    cuts_horizontal = int(sheet_width // cut_width)
    cuts_vertical = int(sheet_height // cut_height)
    cuts_per_sheet = cuts_horizontal * cuts_vertical
    total_cuts = cuts_per_sheet * quantity
    sheets_required = (total_cuts // cuts_per_sheet) + (1 if total_cuts % cuts_per_sheet else 0)
    utilization_percentage = (cuts_per_sheet * cut_width * cut_height) / (sheet_width * sheet_height) * 100
    final_weight = grammage * sheet_width * sheet_height / 10000  # g
    
    result = {
        'sheet_width': sheet_width,
        'sheet_height': sheet_height,
        'cut_width': cut_width,
        'cut_height': cut_height,
        'grammage': grammage,
        'quantity_requested': quantity,
        'cuts_horizontal': cuts_horizontal,
        'cuts_vertical': cuts_vertical,
        'cuts_per_sheet': cuts_per_sheet,
        'total_cuts': total_cuts,
        'sheets_required': sheets_required,
        'utilization_percentage': utilization_percentage,
        'final_weight': final_weight,
        'cost_per_sheet': cost_per_sheet,
        'total_cost': sheets_required * cost_per_sheet,
        'calculation_type': 'optimal',
        'created_at': datetime.now().isoformat()
    }
    st.session_state.calculation_result = result
    
    # Guardar en historial local
    history = load_json("history.json")
    history.append(result)
    save_json("history.json", history)
    st.success("Cálculo completado. Recuerde anotar los resultados en su hoja.")

def calculate_inline(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet=0):
    # Misma simulación
    calculate_optimal(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet)

# ----------------- Funciones de UI -----------------
def show_cutting_preview():
    if not st.session_state.calculation_result:
        st.info("Haga un cálculo primero")
        return
    result = st.session_state.calculation_result
    fig = go.Figure()
    fig.add_shape(
        type="rect",
        x0=0, y0=0,
        x1=result['sheet_width'], y1=result['sheet_height'],
        fillcolor="rgba(255,182,193,0.3)",
        line=dict(color="rgba(255,182,193,1)", width=2)
    )
    for i in range(result['cuts_horizontal']):
        for j in range(result['cuts_vertical']):
            x = i * result['cut_width']
            y = j * result['cut_height']
            fig.add_shape(
                type="rect",
                x0=x, y0=y,
                x1=x + result['cut_width'], y1=y + result['cut_height'],
                fillcolor="rgba(255,105,180,0.7)",
                line=dict(color="rgba(255,105,180,1)", width=1)
            )
    fig.update_layout(
        title=f"Utilización: {result['utilization_percentage']:.1f}%",
        xaxis_title="Ancho (cm)",
        yaxis_title="Alto (cm)",
        showlegend=False,
        height=400,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_cut_report():
    if not st.session_state.calculation_result:
        st.info("Haga un cálculo primero")
        return
    result = st.session_state.calculation_result
    df = pd.DataFrame({
        "Métrica": ["Cortes por hoja","Cortes utilizables","Cortes horizontales",
                    "Cortes verticales","Hojas requeridas","Total de cortes","Peso final (g)",
                    "Costo por hoja ($)","Costo total ($)"],
        "Valor": [result['cuts_per_sheet'], result['cuts_per_sheet'], result['cuts_horizontal'],
                  result['cuts_vertical'], result['sheets_required'], result['total_cuts'],
                  f"{result['final_weight']:.2f}", f"{result['cost_per_sheet']:.2f}",
                  f"{result['total_cost']:.2f}"]
    })
    st.table(df)

def show_footer():
    st.markdown("""
    <div class="footer">
        <span>📌 Esta app funciona 100% local, recuerde anotar resultados en su hoja.</span>
    </div>
    """, unsafe_allow_html=True)

# ----------------- Main -----------------
def main():
    st.set_page_config(page_title="Calculadora de Cortes", page_icon="✂️", layout="wide")
    load_css()
    load_js()
    initialize_app()
    
    logo_b64 = load_image_base64("Imagen2.jpeg")
    st.markdown(f"""
    <div class="header-container">
        <img src="data:image/jpeg;base64,{logo_b64}" style="width:80px;height:80px;border-radius:50%;"/>
        <h1>Calculadora de Cortes</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("### 📐 Tamaño de la Hoja")
        sheet_width = st.number_input("Ancho de la hoja (cm)", value=100.0, step=0.1)
        sheet_height = st.number_input("Alto de la hoja (cm)", value=70.0, step=0.1)
        grammage = st.number_input("Gramaje (g/m²)", value=80, step=1)
        st.markdown("### 💰 Cálculo de Costos")
        cost_per_sheet = st.number_input("Costo por hoja ($)", value=0.0, step=0.01)
        st.markdown("### ✂️ Tamaño del Corte")
        cut_width = st.number_input("Ancho del corte (cm)", value=10.0, step=0.1)
        cut_height = st.number_input("Alto del corte (cm)", value=7.0, step=0.1)
        quantity = 100
        
        check_special_code(sheet_width, sheet_height, grammage, cost_per_sheet, cut_width, cut_height)
        
        st.markdown('<div class="button-row">', unsafe_allow_html=True)
        col_opt, col_inline = st.columns(2)
        with col_opt:
            if st.button("🎯 Óptimo"):
                calculate_optimal(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet)
        with col_inline:
            if st.button("📏 En Línea"):
                calculate_inline(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 👁️ Vista Previa del Área de Corte")
        show_cutting_preview()
        st.markdown("### 📊 Reporte de Cortes")
        show_cut_report()
    
    show_footer()

if __name__ == "__main__":
    main()
