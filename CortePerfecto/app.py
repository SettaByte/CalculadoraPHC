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
            st.error(f"Error conectando a la base de datos: {e}")
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
        
        # Plantillas predefinidas
        show_templates_section()
        
        # Configuraciones favoritas
        show_favorites_section()
        
        # Historial de cálculos
        show_history_section()
        
        # Modo comparación
        show_comparison_section()
        
        # Estadísticas
        show_statistics_section()
    
    # Layout principal
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📐 Tamaño de la Hoja")
        
        sheet_width = st.number_input(
            "Ancho de la hoja (cm)",
            min_value=0.1,
            value=100.0,
            step=0.1,
            help="Ingrese el ancho de la hoja en centímetros"
        )
        
        sheet_height = st.number_input(
            "Alto de la hoja (cm)",
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
        
        # Cálculo de costos
        st.markdown("### 💰 Cálculo de Costos")
        cost_per_sheet = st.number_input(
            "Costo por hoja ($)",
            min_value=0.0,
            value=0.0,
            step=0.01,
            help="Ingrese el costo unitario por hoja para calcular el costo total"
        )
        
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
        check_special_code(cut_width, cut_height, quantity)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
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

def check_special_code(width, height, quantity):
    """Verifica si se ingresó el código especial '67' en ancho y alto y muestra el URL"""
    try:
        # Convertir a int para comparar
        w = int(width)
        h = int(height)
        
        if w == 67 and h == 67:
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
            st.markdown(f"🔗 URL Secreto: [Abrir Easter Egg]({secret_url})", unsafe_allow_html=True)
    except ValueError:
        pass





def calculate_optimal(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet=0):
    """Calcula el corte óptimo"""
    result = st.session_state.calculator.calculate_optimal(
        sheet_width, sheet_height, cut_width, cut_height, quantity, grammage
    )
    
    # Agregar cálculo de costos
    result['cost_per_sheet'] = cost_per_sheet
    result['total_cost'] = result['sheets_required'] * cost_per_sheet
    
    st.session_state.calculation_result = result
    st.session_state.calculation_type = "optimal"
    
    # Guardar en historial si la base de datos está disponible
    if st.session_state.db_manager:
        try:
            st.session_state.db_manager.save_calculation_to_history(result, cost_per_sheet)
        except Exception as e:
            st.warning(f"No se pudo guardar en el historial: {e}")
    
    # Agregar a comparación si está habilitado
    if st.session_state.comparison_mode:
        if len(st.session_state.comparison_configs) < 5:  # Límite de 5 configuraciones
            st.session_state.comparison_configs.append(result.copy())
            st.success(f"Configuración agregada a comparación ({len(st.session_state.comparison_configs)}/5)")
        else:
            st.warning("Máximo 5 configuraciones en comparación. Elimine algunas para agregar nuevas.")
    
    st.rerun()

def calculate_inline(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage, cost_per_sheet=0):
    """Calcula el corte en línea"""
    result = st.session_state.calculator.calculate_inline(
        sheet_width, sheet_height, cut_width, cut_height, quantity, grammage
    )
    
    # Agregar cálculo de costos
    result['cost_per_sheet'] = cost_per_sheet
    result['total_cost'] = result['sheets_required'] * cost_per_sheet
    
    st.session_state.calculation_result = result
    st.session_state.calculation_type = "inline"
    
    # Guardar en historial si la base de datos está disponible
    if st.session_state.db_manager:
        try:
            st.session_state.db_manager.save_calculation_to_history(result, cost_per_sheet)
        except Exception as e:
            st.warning(f"No se pudo guardar en el historial: {e}")
    
    # Agregar a comparación si está habilitado
    if st.session_state.comparison_mode:
        if len(st.session_state.comparison_configs) < 5:  # Límite de 5 configuraciones
            st.session_state.comparison_configs.append(result.copy())
            st.success(f"Configuración agregada a comparación ({len(st.session_state.comparison_configs)}/5)")
        else:
            st.warning("Máximo 5 configuraciones en comparación. Elimine algunas para agregar nuevas.")
    
    st.rerun()

def clear_all_fields():
    """Limpia todos los campos y resultados"""
    for key in list(st.session_state.keys()):
        if key not in ['calculator', 'export_utils']:
            del st.session_state[key]
    st.rerun()

def show_cutting_preview():
    """Muestra la vista previa del área de corte"""
    result = st.session_state.calculation_result
    
    # Crear gráfico de utilización
    fig = go.Figure()
    
    # Área total de la hoja
    fig.add_shape(
        type="rect",
        x0=0, y0=0,
        x1=result['sheet_width'], y1=result['sheet_height'],
        fillcolor="rgba(255, 182, 193, 0.3)",
        line=dict(color="rgba(255, 182, 193, 1)", width=2)
    )
    
    # Áreas de corte
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
        height=400,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar estadísticas de utilización
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Área Utilizada", f"{result['utilization_percentage']:.1f}%")
    with col2:
        st.metric("Área Desperdiciada", f"{100 - result['utilization_percentage']:.1f}%")

def show_cut_report():
    """Muestra el reporte detallado de cortes"""
    result = st.session_state.calculation_result
    
    # Crear DataFrame para mostrar los resultados
    report_data = {
        "Métrica": [
            "Cortes por hoja",
            "Cortes utilizables",
            "Cortes horizontales",
            "Cortes verticales",
            "Hojas requeridas",
            "Total de cortes",
            "Peso final (g)",
            "Costo por hoja ($)",
            "Costo total ($)"
        ],
        "Valor": [
            result['cuts_per_sheet'],
            result['usable_cuts'],
            result['cuts_horizontal'],
            result['cuts_vertical'],
            result['sheets_required'],
            result['total_cuts'],
            f"{result['final_weight']:.2f}",
            f"{result.get('cost_per_sheet', 0):.2f}",
            f"{result.get('total_cost', 0):.2f}"
        ]
    }
    
    df = pd.DataFrame(report_data)
    st.table(df)

def print_report():
    """Simula la impresión del reporte"""
    st.success("Reporte enviado a la impresora")
    
def send_email():
    """Simula el envío por email"""
    st.success("Reporte enviado por correo electrónico")

def export_excel():
    """Exporta los resultados a Excel"""
    if 'calculation_result' in st.session_state:
        excel_data = st.session_state.export_utils.to_excel(st.session_state.calculation_result)
        st.download_button(
            label="Descargar Excel",
            data=excel_data,
            file_name="reporte_cortes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

def export_pdf():
    """Exporta los resultados a PDF"""
    if 'calculation_result' in st.session_state:
        pdf_data = st.session_state.export_utils.to_pdf(st.session_state.calculation_result)
        st.download_button(
            label="Descargar PDF",
            data=pdf_data,
            file_name="reporte_cortes.pdf",
            mime="application/pdf"
        )

def show_footer():
    """Muestra el footer con redes sociales"""
    st.markdown("""
    <div class="footer">
        <div class="social-media">
            <a href="https://www.instagram.com/p.h.cajas/" target="_blank" class="social-link">
                <i class="fab fa-instagram"></i>
            </a>
            <a href="https://tiktok.com" target="_blank" class="social-link">
                <i class="fab fa-tiktok"></i>
            </a>
            <a href="https://facebook.com" target="_blank" class="social-link">
                <i class="fab fa-facebook"></i>
            </a>
            <a href="https://phcajasdelujo.taplink.mx/" target="_blank" class="social-link">
                <span>Web</span>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_templates_section():
    """Muestra la sección de plantillas predefinidas"""
    if not st.session_state.db_manager:
        return
    
    st.markdown("### 📋 Plantillas")
    
    try:
        templates = st.session_state.db_manager.get_templates()
        
        if templates:
            template_names = [f"{t['name']} ({t['sheet_width']}x{t['sheet_height']}cm)" for t in templates]
            selected_template = st.selectbox(
                "Seleccionar plantilla:",
                ["Ninguna"] + template_names,
                key="template_selector"
            )
            
            if selected_template != "Ninguna":
                idx = template_names.index(selected_template)
                template = templates[idx]
                
                if st.button("🔄 Cargar Plantilla", use_container_width=True):
                    st.session_state.template_loaded = {
                        'sheet_width': float(template['sheet_width']),
                        'sheet_height': float(template['sheet_height']),
                        'grammage': int(template['grammage'])
                    }
                    st.success(f"Plantilla '{template['name']}' cargada")
                    st.rerun()
        else:
            st.info("No hay plantillas disponibles")
    
    except Exception as e:
        st.error(f"Error cargando plantillas: {e}")

def show_favorites_section():
    """Muestra la sección de configuraciones favoritas"""
    if not st.session_state.db_manager:
        return
    
    st.markdown("### ⭐ Favoritos")
    
    # Guardar configuración actual como favorita
    with st.expander("💾 Guardar Actual"):
        favorite_name = st.text_input("Nombre de la configuración:", key="fav_name")
        if st.button("💾 Guardar Favorito", use_container_width=True):
            if favorite_name and hasattr(st.session_state, 'calculation_result'):
                config = {
                    'sheet_width': st.session_state.calculation_result['sheet_width'],
                    'sheet_height': st.session_state.calculation_result['sheet_height'],
                    'cut_width': st.session_state.calculation_result['cut_width'],
                    'cut_height': st.session_state.calculation_result['cut_height'],
                    'grammage': st.session_state.calculation_result['grammage'],
                    'quantity': st.session_state.calculation_result['quantity_requested'],
                    'cost_per_sheet': st.session_state.calculation_result.get('cost_per_sheet', 0)
                }
                try:
                    st.session_state.db_manager.save_favorite_configuration(favorite_name, config)
                    st.success("Configuración guardada")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error guardando: {e}")
            else:
                st.warning("Ingrese un nombre y realice un cálculo primero")
    
    # Mostrar favoritos existentes
    try:
        favorites = st.session_state.db_manager.get_favorite_configurations()
        
        if favorites:
            for fav in favorites[:5]:
                with st.expander(f"⭐ {fav['name']}"):
                    st.write(f"**Hoja:** {fav['sheet_width']}x{fav['sheet_height']}cm")
                    st.write(f"**Corte:** {fav['cut_width']}x{fav['cut_height']}cm")
                    st.write(f"**Cantidad:** {fav['quantity']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Cargar", key=f"load_fav_{fav['id']}", use_container_width=True):
                            st.session_state.favorite_loaded = fav
                            st.success("Favorito cargado")
                            st.rerun()
                    with col2:
                        if st.button("🗑️ Eliminar", key=f"del_fav_{fav['id']}", use_container_width=True):
                            st.session_state.db_manager.delete_favorite_configuration(fav['id'])
                            st.success("Favorito eliminado")
                            st.rerun()
        else:
            st.info("No hay favoritos guardados")
    
    except Exception as e:
        st.error(f"Error cargando favoritos: {e}")

def show_history_section():
    """Muestra la sección de historial de cálculos"""
    if not st.session_state.db_manager:
        return
    
    st.markdown("### 📊 Historial")
    
    try:
        history = st.session_state.db_manager.get_calculation_history(10)
        
        if history:
            for calc in history[:3]:
                with st.expander(f"📅 {calc['created_at'].strftime('%d/%m %H:%M')}"):
                    st.write(f"**Tipo:** {calc['calculation_type']}")
                    st.write(f"**Utilización:** {calc['utilization_percentage']:.1f}%")
                    st.write(f"**Hojas:** {calc['sheets_required']}")
                    if calc['total_cost'] > 0:
                        st.write(f"**Costo:** ${calc['total_cost']:.2f}")
            
            if st.button("🗑️ Limpiar Historial", use_container_width=True):
                st.session_state.db_manager.clear_calculation_history()
                st.success("Historial limpiado")
                st.rerun()
        else:
            st.info("No hay historial disponible")
    
    except Exception as e:
        st.error(f"Error cargando historial: {e}")

def show_comparison_section():
    """Muestra la sección de modo comparación"""
    st.markdown("### 🔄 Comparación")
    
    comparison_mode = st.toggle("Modo Comparación", value=st.session_state.comparison_mode)
    st.session_state.comparison_mode = comparison_mode
    
    if comparison_mode:
        st.info("Realice cálculos para agregar a la comparación")
        
        if st.session_state.comparison_configs:
            for i, config in enumerate(st.session_state.comparison_configs[:3]):
                with st.expander(f"Config {i+1}: {config['utilization_percentage']:.1f}% util."):
                    st.write(f"**Tipo:** {config.get('orientation', 'unknown')}")
                    st.write(f"**Hojas:** {config['sheets_required']}")
                    st.write(f"**Cortes:** {config['total_cuts']}")
                    if st.button("🗑️ Quitar", key=f"remove_comp_{i}"):
                        st.session_state.comparison_configs.pop(i)
                        st.rerun()
        
        if len(st.session_state.comparison_configs) > 1:
            if st.button("📊 Ver Comparación Detallada", use_container_width=True):
                show_comparison_results()
        
        if st.button("🗑️ Limpiar Comparaciones", use_container_width=True):
            st.session_state.comparison_configs = []
            st.rerun()

def show_statistics_section():
    """Muestra estadísticas generales"""
    if not st.session_state.db_manager:
        return
    
    st.markdown("### 📈 Estadísticas")
    
    try:
        stats = st.session_state.db_manager.get_statistics()
        
        st.metric("Cálculos Realizados", stats['total_calculations'])
        st.metric("Favoritos Guardados", stats['favorite_configurations'])
        if stats['average_utilization'] > 0:
            st.metric("Utilización Promedio", f"{stats['average_utilization']:.1f}%")
        if stats['total_sheets_calculated'] > 0:
            st.metric("Total Hojas Calculadas", stats['total_sheets_calculated'])
    
    except Exception as e:
        st.error(f"Error cargando estadísticas: {e}")

def show_comparison_results():
    """Muestra los resultados de comparación detallada"""
    if len(st.session_state.comparison_configs) < 2:
        st.warning("Se necesitan al menos 2 configuraciones para comparar")
        return
    
    st.markdown("## 🔄 Comparación de Configuraciones")
    
    comparison_data = []
    for i, config in enumerate(st.session_state.comparison_configs):
        comparison_data.append({
            'Configuración': f"Config {i+1}",
            'Tipo': config.get('orientation', 'unknown'),
            'Utilización (%)': f"{config['utilization_percentage']:.1f}",
            'Hojas Requeridas': config['sheets_required'],
            'Total Cortes': config['total_cuts'],
            'Peso Final (g)': f"{config['final_weight']:.2f}",
            'Costo Total ($)': f"{config.get('total_cost', 0):.2f}"
        })
    
    df_comparison = pd.DataFrame(comparison_data)
    st.table(df_comparison)
    
    fig = go.Figure()
    
    configs = [f"Config {i+1}" for i in range(len(st.session_state.comparison_configs))]
    utilizations = [config['utilization_percentage'] for config in st.session_state.comparison_configs]
    
    fig.add_trace(go.Bar(
        x=configs,
        y=utilizations,
        name='Utilización (%)',
        marker_color='rgba(255, 105, 180, 0.7)'
    ))
    
    fig.update_layout(
        title="Comparación de Utilización",
        xaxis_title="Configuraciones",
        yaxis_title="Utilización (%)",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
