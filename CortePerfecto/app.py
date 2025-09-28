import os, base64, streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
from utils.calculator import CuttingCalculator
from utils.export_utils import ExportUtils

BASE_DIR = os.path.dirname(__file__)

# -------------------- CARGA DE RECURSOS --------------------
def load_image_base64(filename):
    # Since we can't generate actual image files, we'll create a placeholder SVG
    svg_placeholder = """
    <svg width="80" height="80" xmlns="http://www.w3.org/2000/svg">
        <circle cx="40" cy="40" r="35" fill="#FF69B4" opacity="0.3"/>
        <text x="40" y="45" text-anchor="middle" fill="#FF1493" font-size="12" font-weight="bold">LOGO</text>
    </svg>
    """
    return base64.b64encode(svg_placeholder.encode()).decode()

def show_floating_bar():
    img_b64 = load_image_base64("Imagen1.jpeg")
    st.markdown(f"""
    <div id="floatingBar" class="floating-bar" style="margin-bottom:20px;">
        <div class="floating-content">
            <img src="data:image/svg+xml;base64,{img_b64}" 
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

    # Determinar si estamos en modo oscuro
    dark_mode = st.session_state.get('dark_mode', False)
    
    # Colores según el modo
    if dark_mode:
        bg_color = "#1e1e1e"
        text_color = "white"
        input_bg = "#333333"
        card_bg = "rgba(50, 50, 50, 0.8)"
        card_border = "rgba(255, 105, 180, 0.4)"
    else:
        bg_color = "#ffffff"
        text_color = "black"
        input_bg = "#ffffff"
        card_bg = "rgba(255, 255, 255, 0.9)"
        card_border = "rgba(255, 105, 180, 0.2)"

    # Estilos mejorados con modo oscuro/claro
    st.markdown(f"""
    <style>
        /* Fondo principal */
        .stApp {{
            background-color: {bg_color} !important;
        }}
        
        /* Títulos */
        .main-title, h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
        }}

        /* Inputs */
        .stNumberInput div[data-baseweb="input"] input {{
            background-color: {input_bg} !important;
            color: {text_color} !important;
            border: 1px solid #ccc !important;
            border-radius: 6px !important;
        }}

        .stNumberInput label {{
            color: {text_color} !important;
        }}

        /* Botones +/- rosa en inputs numéricos */
        .stNumberInput div[data-baseweb="input"] button {{
            background-color: #FF69B4 !important;
            color: white !important;
            border: 1px solid #FF1493 !important;
            border-radius: 4px !important;
        }}

        .stNumberInput div[data-baseweb="input"] button:hover {{
            background-color: #FF1493 !important;
            transform: scale(1.05);
        }}

        /* Botones principales */
        .stButton>button {{
            background-color: {input_bg if not dark_mode else '#444444'} !important;
            color: {text_color} !important;
            border: 1px solid #ccc !important;
            border-radius: 8px !important;
        }}

        /* Cards/Secciones */
        .section-card {{
            background: {card_bg} !important;
            border: 2px solid {card_border} !important;
        }}

        /* Toggle del modo oscuro */
        .mode-toggle {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: linear-gradient(135deg, #FF69B4, #FF1493);
            padding: 8px 15px;
            border-radius: 25px;
            color: white;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
        }}

        .mode-toggle:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 105, 180, 0.4);
        }}

        /* Responsividad mejorada */
        @media (max-width: 768px) {{
            .main-title {{
                font-size: 1.5rem !important;
            }}
            
            .stPlotlyChart {{
                height: 400px !important;
            }}
            
            .logo {{
                width: 60px !important;
                height: 60px !important;
            }}
        }}

        /* Floating bar mejorada */
        .floating-bar {{
            background: linear-gradient(135deg, #FF69B4, #FF1493);
            color: white;
            padding: 10px 20px;
            border-radius: 50px;
            box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
            animation: float 3s ease-in-out infinite;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-5px); }}
        }}

        .floating-content {{
            display: flex;
            align-items: center;
            justify-content: center;
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

def load_shared_params():
    """Carga parámetros compartidos desde la URL si existen"""
    try:
        # Obtener parámetros de la URL
        query_params = st.query_params
        
        shared_params = {}
        
        # Verificar si es un link compartido
        if query_params.get('shared') == 'true':
            # Mostrar mensaje de link compartido
            st.success("📋 Se han cargado parámetros desde un link compartido")
            
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

# -------------------- MAIN --------------------
def main():
    load_css()
    load_js()
    initialize_app()

    logo_b64 = load_image_base64("Imagen2.jpeg")
    # Toggle del modo oscuro en la parte superior
    col_header, col_toggle = st.columns([4, 1])
    
    with col_header:
        st.markdown(f"""
        <div class="header-container" style="margin-bottom:30px;">
            <div class="logo-container">
                <img src="data:image/svg+xml;base64,{logo_b64}" class="logo" style="border-radius: 50%; width: 80px; height: 80px;">
            </div>
            <h1 class="main-title">Calculadora de Cortes</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col_toggle:
        st.markdown("### 🌓 Modo")
        dark_mode_icon = "🌙" if st.session_state.dark_mode else "☀️"
        mode_text = "Oscuro" if st.session_state.dark_mode else "Claro"
        
        if st.button(f"{dark_mode_icon} {mode_text}", key="mode_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    # Cargar parámetros compartidos si existen
    shared_params = load_shared_params()
    
    col1, col2 = st.columns([1, 1])

    # -------------------- COLUMNA 1: INPUTS --------------------
    with col1:
        st.markdown('<div class="section-card" style="margin-bottom:20px;">', unsafe_allow_html=True)
        st.markdown("### 📐 Tamaño del Pliego de Cartón")
        sheet_width = st.number_input("Ancho de la hoja (cm)", min_value=0.1, 
                                     value=shared_params.get('sheet_width', 100.0), step=0.1)
        sheet_height = st.number_input("Alto de la hoja (cm)", min_value=0.1, 
                                      value=shared_params.get('sheet_height', 70.0), step=0.1)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card" style="margin-bottom:20px;">', unsafe_allow_html=True)
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
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Botones
        st.markdown('<div class="button-row" style="display:flex; gap:10px; margin-bottom:20px;">', unsafe_allow_html=True)
        col_opt, col_clear = st.columns([1, 1], gap="small")
        with col_opt:
            if st.button("🎯 Óptimo", use_container_width=True):
                calculate_optimal(sheet_width, sheet_height, cut_width, cut_height)
        with col_clear:
            if st.button("🗑️ Limpiar Todo", use_container_width=True):
                clear_all_fields()
        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------- COLUMNA 2: GRAFICA Y REPORTE --------------------
    with col2:
        st.markdown('<div class="section-card" style="margin-bottom:20px;">', unsafe_allow_html=True)
        st.markdown("<p>Arrastre la esquina superior del eje Y para modificarla</p>", unsafe_allow_html=True)
        st.markdown("<p>Arrastre la esquina derecha del eje X para modificarlo</p>", unsafe_allow_html=True)
        st.info("La gráfica cuenta con barra de herramientas.")
        if st.session_state.calculation_result:
            show_cutting_preview()
        else:
            st.info("Haga clic en 'Óptimo' para ver la vista previa")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card" style="margin-bottom:20px;">', unsafe_allow_html=True)
        st.markdown("### 📊 Reporte de Cortes")
        if st.session_state.calculation_result:
            show_cut_report()
            # Botones de descarga y compartir
            col_excel, col_pdf, col_share = st.columns([1, 1, 1])
            with col_excel:
                if st.button("📊 Descargar Excel", key="excel_btn", help="Descargar tabla como Excel"):
                    export_excel()
            with col_pdf:
                if st.button("📄 Descargar PDF", key="pdf_btn", help="Descargar tabla y gráfico como PDF"):
                    export_pdf()
            with col_share:
                if st.button("🔗 Compartir", key="share_btn", help="Generar link para compartir resultado"):
                    generate_share_link()
        else:
            st.info("Los resultados aparecerán aquí después del cálculo")
        st.markdown('</div>', unsafe_allow_html=True)

    show_footer()
    show_floating_bar()

# -------------------- CALCULOS --------------------
def calculate_optimal(sheet_width, sheet_height, cut_width, cut_height):
    result = st.session_state.calculator.calculate_optimal(
        sheet_width, sheet_height, cut_width, cut_height, 1, 80
    )

    # Calcular área utilizada
    total_cuts_width = int(sheet_width // cut_width)
    total_cuts_height = int(sheet_height // cut_height)
    used_area = total_cuts_width * cut_width * total_cuts_height * cut_height
    total_area = sheet_width * sheet_height
    utilization_percentage = (used_area / total_area) * 100

    result['cuts_horizontal'] = total_cuts_width
    result['cuts_vertical'] = total_cuts_height
    result['utilization_percentage'] = utilization_percentage
    st.session_state.calculation_result = result

    # Easter egg 67
    check_special_code(sheet_width, sheet_height, cut_width, cut_height)

    st.rerun()

def clear_all_fields():
    for key in list(st.session_state.keys()):
        if key not in ['calculator', 'export_utils']:
            del st.session_state[key]
    st.rerun()

# -------------------- GRAFICA MEJORADA --------------------
def show_cutting_preview():
    result = st.session_state.calculation_result
    dark_mode = st.session_state.get('dark_mode', False)
    fig = go.Figure()

    # Colores según el modo
    if dark_mode:
        bg_color = "#2e2e2e"
        paper_color = "#1e1e1e"
        grid_color = "rgba(255, 105, 180, 0.3)"
        text_color = "white"
    else:
        bg_color = "white"
        paper_color = "white"
        grid_color = "rgba(255, 105, 180, 0.2)"
        text_color = "black"

    # Área de hoja con colores rosa adaptados
    fig.add_shape(
        type="rect",
        x0=0, y0=0,
        x1=result['sheet_width'], y1=result['sheet_height'],
        fillcolor="rgba(255, 182, 193, 0.2)" if not dark_mode else "rgba(255, 182, 193, 0.4)",
        line=dict(color="rgba(255, 105, 180, 0.8)", width=3)
    )

    # Dibujar cortes con tema rosa
    for i in range(result['cuts_horizontal']):
        for j in range(result['cuts_vertical']):
            x = i * result['cut_width']
            y = j * result['cut_height']
            if x + result['cut_width'] <= result['sheet_width'] and y + result['cut_height'] <= result['sheet_height']:
                fig.add_shape(
                    type="rect",
                    x0=x, y0=y,
                    x1=x + result['cut_width'], y1=y + result['cut_height'],
                    fillcolor="rgba(255, 105, 180, 0.6)" if not dark_mode else "rgba(255, 105, 180, 0.8)",
                    line=dict(color="rgba(255, 20, 147, 0.8)", width=1.5)
                )

    # Configuración mejorada para responsividad y modo oscuro
    fig.update_layout(
        title="",
        xaxis_title="Ancho (cm)",
        yaxis_title="Alto (cm)",
        showlegend=False,
        height=450,  # Altura fija más manejable
        plot_bgcolor=bg_color,
        paper_bgcolor=paper_color,
        dragmode="pan",
        # Configuración responsiva mejorada
        autosize=True,
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(color=text_color),
        xaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            zeroline=True,
            zerolinecolor="rgba(255, 105, 180, 0.4)",
            color=text_color
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            zeroline=True,
            zerolinecolor="rgba(255, 105, 180, 0.4)",
            color=text_color
        )
    )

    # Indicadores discretos
    fig.add_annotation(
        x=0, y=result['sheet_height'], text="↕",
        showarrow=False, font=dict(size=14, color="#FF1493"),
        xanchor="left", yanchor="bottom"
    )
    fig.add_annotation(
        x=result['sheet_width'], y=0, text="↔",
        showarrow=False, font=dict(size=14, color="#FF1493"),
        xanchor="right", yanchor="top"
    )

    # Configuración para dispositivos móviles
    config = {
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['zoom2d', 'lasso2d', 'select2d'],
        'responsive': True,
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'cutting_layout',
            'height': 500,
            'width': 700,
            'scale': 1
        }
    }

    st.plotly_chart(fig, use_container_width=True, config=config)

    # Métricas con colores rosa
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Área Utilizada", f"{result['utilization_percentage']:.1f}%", delta=None)
    with col2:
        st.metric("Área Desperdiciada", f"{100 - result['utilization_percentage']:.1f}%", delta=None)

# -------------------- TABLA DE DATOS MEJORADA --------------------
def show_cut_report():
    result = st.session_state.calculation_result
    report_data = {
        "Métrica": [
            "📐 Ancho de la hoja (cm)",
            "📐 Alto de la hoja (cm)",
            "✂️ Ancho del corte (cm)",
            "✂️ Alto del corte (cm)",
            "🔢 Cortes horizontales",
            "🔢 Cortes verticales",
            "📊 Utilización (%)",
            "📉 Desperdicio (%)"
        ],
        "Valor": [
            f"{result['sheet_width']:.2f}",
            f"{result['sheet_height']:.2f}",
            f"{result['cut_width']:.2f}",
            f"{result['cut_height']:.2f}",
            f"{result['cuts_horizontal']}",
            f"{result['cuts_vertical']}",
            f"{result['utilization_percentage']:.1f}%",
            f"{100 - result['utilization_percentage']:.1f}%"
        ]
    }
    df = pd.DataFrame(report_data)
    st.info("💡 Esta tabla muestra los resultados y los datos de entrada. Usa el scroll si es necesario.")

    # Aplicar estilo rosa a la tabla
    styled_df = df.style.apply(lambda x: ['background-color: rgba(255, 182, 193, 0.3); color: black; font-weight: bold'] * len(x), axis=1)
    st.dataframe(styled_df, height=300, use_container_width=True)

# -------------------- FUNCIONES DE EXPORTACIÓN --------------------
def export_excel():
    """Exporta los resultados a Excel con estilo rosa"""
    if 'calculation_result' in st.session_state and st.session_state.calculation_result is not None:
        try:
            # Verificar que no hay errores en los resultados
            result = st.session_state.calculation_result
            if 'error' in result:
                st.error(f"No se puede exportar: {result['error']}")
                return
                
            excel_data = st.session_state.export_utils.to_excel(result)
            st.download_button(
                label="📊 Descargar Excel",
                data=excel_data,
                file_name="reporte_cortes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_excel"
            )
            st.success("¡Excel generado exitosamente!")
        except Exception as e:
            st.error(f"Error al generar Excel: {str(e)}")
    else:
        st.error("No hay resultados para exportar")

def export_pdf():
    """Exporta los resultados a PDF con gráfico y tabla"""
    if 'calculation_result' in st.session_state and st.session_state.calculation_result is not None:
        try:
            # Verificar que no hay errores en los resultados
            result = st.session_state.calculation_result
            if 'error' in result:
                st.error(f"No se puede exportar: {result['error']}")
                return
                
            pdf_data = st.session_state.export_utils.to_pdf(result)
            st.download_button(
                label="📄 Descargar PDF",
                data=pdf_data,
                file_name="reporte_cortes.pdf",
                mime="application/pdf",
                key="download_pdf"
            )
            st.success("¡PDF generado exitosamente!")
        except Exception as e:
            st.error(f"Error al generar PDF: {str(e)}")
    else:
        st.error("No hay resultados para exportar")

def generate_share_link():
    """Genera un link para compartir los resultados actuales"""
    if 'calculation_result' in st.session_state:
        try:
            import urllib.parse as urlparse
            result = st.session_state.calculation_result
            
            # Crear URL relativa para mayor portabilidad
            params = {
                'sheet_width': result['sheet_width'],
                'sheet_height': result['sheet_height'],
                'cut_width': result['cut_width'], 
                'cut_height': result['cut_height'],
                'shared': 'true'
            }
            
            query_string = urlparse.urlencode(params)
            # Usar URL relativa que funcionará en cualquier despliegue
            share_url = f"/?{query_string}"
            
            # Mostrar el link generado
            st.success("🎉 ¡Link generado exitosamente!")
            st.text_area(
                "Link para compartir:",
                share_url,
                height=80,
                help="Copia este link para compartir tus resultados"
            )
            
            # Información adicional
            st.info(f"""
            📋 **Compartir resultados:**
            • Hoja: {result['sheet_width']}×{result['sheet_height']} cm  
            • Corte: {result['cut_width']}×{result['cut_height']} cm
            • Utilización: {result['utilization_percentage']:.1f}%
            """)
            
        except Exception as e:
            st.error(f"Error al generar link: {str(e)}")

# -------------------- FOOTER --------------------
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

# -------------------- EASTER EGG --------------------
def check_special_code(sheet_width, sheet_height, cut_width, cut_height):
    try:
        vals = [int(sheet_width), int(sheet_height), int(cut_width), int(cut_height)]
        if all(x == 67 for x in vals):
            secret_url = "https://www.youtube.com/watch?v=3tQHBUP1tcI"
            st.success("¡MANGO MANGO MANGO!")
            st.balloons()
    except:
        pass

if __name__ == "__main__":
    main()
