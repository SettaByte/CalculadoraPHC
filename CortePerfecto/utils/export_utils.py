import pandas as pd
from io import BytesIO
import xlsxwriter
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

class ExportUtils:
    """Utilidades para exportar reportes a diferentes formatos"""
    
    def __init__(self):
        pass
    
    def to_excel(self, calculation_result):
        """Exporta los resultados a formato Excel"""
        output = BytesIO()
        
        # Crear workbook y worksheet
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Reporte de Cortes')
        
        # Formatos
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#FFB6C1'
        })
        
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#FFC0CB',
            'border': 1
        })
        
        data_format = workbook.add_format({
            'border': 1,
            'align': 'right'
        })
        
        # Escribir título
        worksheet.merge_range(0, 0, 0, 1, 'Reporte de Cortes', title_format)
        worksheet.write(1, 0, f'Fecha: {datetime.now().strftime("%d/%m/%Y %H:%M")}')
        
        # Datos de entrada
        row = 4
        worksheet.write(row, 0, 'DATOS DE ENTRADA', header_format)
        row += 1
        
        input_data = [
            ('Ancho de hoja (cm)', calculation_result['sheet_width']),
            ('Alto de hoja (cm)', calculation_result['sheet_height']),
            ('Ancho de corte (cm)', calculation_result['cut_width']),
            ('Alto de corte (cm)', calculation_result['cut_height']),
            ('Gramaje (g/m²)', calculation_result['grammage']),
            ('Cantidad requerida', calculation_result['quantity_requested'])
        ]
        
        for label, value in input_data:
            worksheet.write(row, 0, label, header_format)
            worksheet.write(row, 1, value, data_format)
            row += 1
        
        # Resultados
        row += 1
        worksheet.write(row, 0, 'RESULTADOS', header_format)
        row += 1
        
        results_data = [
            ('Cortes por hoja', calculation_result['cuts_per_sheet']),
            ('Cortes horizontales', calculation_result['cuts_horizontal']),
            ('Cortes verticales', calculation_result['cuts_vertical']),
            ('Hojas requeridas', calculation_result['sheets_required']),
            ('Total de cortes', calculation_result['total_cuts']),
            ('Cortes utilizables', calculation_result['usable_cuts']),
            ('Utilización (%)', f"{calculation_result['utilization_percentage']:.2f}"),
            ('Peso final (g)', f"{calculation_result['final_weight']:.2f}")
        ]
        
        for label, value in results_data:
            worksheet.write(row, 0, label, header_format)
            worksheet.write(row, 1, value, data_format)
            row += 1
        
        # Ajustar ancho de columnas
        worksheet.set_column(0, 0, 25)
        worksheet.set_column(1, 1, 15)
        
        workbook.close()
        output.seek(0)
        
        return output.getvalue()
    
    def to_pdf(self, calculation_result):
        """Exporta los resultados a formato PDF"""
        buffer = BytesIO()
        
        # Crear documento PDF
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#FF69B4'),
            alignment=1,
            spaceAfter=30
        )
        
        # Título
        title = Paragraph("Reporte de Cortes", title_style)
        elements.append(title)
        
        # Fecha
        date_para = Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal'])
        elements.append(date_para)
        elements.append(Spacer(1, 20))
        
        # Datos de entrada
        input_data = [
            ['DATOS DE ENTRADA', ''],
            ['Ancho de hoja (cm)', str(calculation_result['sheet_width'])],
            ['Alto de hoja (cm)', str(calculation_result['sheet_height'])],
            ['Ancho de corte (cm)', str(calculation_result['cut_width'])],
            ['Alto de corte (cm)', str(calculation_result['cut_height'])],
            ['Gramaje (g/m²)', str(calculation_result['grammage'])],
            ['Cantidad requerida', str(calculation_result['quantity_requested'])]
        ]
        
        input_table = Table(input_data)
        input_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFB6C1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(input_table)
        elements.append(Spacer(1, 20))
        
        # Resultados
        results_data = [
            ['RESULTADOS', ''],
            ['Cortes por hoja', str(calculation_result['cuts_per_sheet'])],
            ['Cortes horizontales', str(calculation_result['cuts_horizontal'])],
            ['Cortes verticales', str(calculation_result['cuts_vertical'])],
            ['Hojas requeridas', str(calculation_result['sheets_required'])],
            ['Total de cortes', str(calculation_result['total_cuts'])],
            ['Cortes utilizables', str(calculation_result['usable_cuts'])],
            ['Utilización (%)', f"{calculation_result['utilization_percentage']:.2f}"],
            ['Peso final (g)', f"{calculation_result['final_weight']:.2f}"]
        ]
        
        results_table = Table(results_data)
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFB6C1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(results_table)
        
        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        
        return buffer.getvalue()
