import math

class CuttingCalculator:
    """Calculadora para optimizar cortes en hojas de papel"""
    
    def __init__(self):
        pass
    
    def calculate_optimal(self, sheet_width, sheet_height, cut_width, cut_height, quantity, grammage):
        """Calcula el corte óptimo considerando las dos orientaciones posibles"""
        
        # Calcular cortes en orientación normal
        normal_result = self._calculate_cuts(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage)
        
        # Calcular cortes en orientación rotada (90 grados)
        rotated_result = self._calculate_cuts(sheet_width, sheet_height, cut_height, cut_width, quantity, grammage)
        
        # Elegir la mejor opción (mayor utilización)
        if normal_result['utilization_percentage'] >= rotated_result['utilization_percentage']:
            result = normal_result
            result['orientation'] = 'normal'
        else:
            result = rotated_result
            result['orientation'] = 'rotated'
            result['cut_width'], result['cut_height'] = result['cut_height'], result['cut_width']
        
        return result
    
    def calculate_inline(self, sheet_width, sheet_height, cut_width, cut_height, quantity, grammage):
        """Calcula cortes en línea (sin rotación)"""
        result = self._calculate_cuts(sheet_width, sheet_height, cut_width, cut_height, quantity, grammage)
        result['orientation'] = 'inline'
        return result
    
    def _calculate_cuts(self, sheet_width, sheet_height, cut_width, cut_height, quantity, grammage):
        """Realiza los cálculos básicos de corte"""
        
        # Calcular cuántos cortes caben por dimensión
        cuts_horizontal = int(sheet_width // cut_width)
        cuts_vertical = int(sheet_height // cut_height)
        
        # Cortes por hoja
        cuts_per_sheet = cuts_horizontal * cuts_vertical
        
        # Hojas requeridas
        sheets_required = math.ceil(quantity / cuts_per_sheet) if cuts_per_sheet > 0 else 0
        
        # Cortes totales que se pueden hacer
        total_cuts = sheets_required * cuts_per_sheet
        
        # Cortes utilizables (los que realmente se necesitan)
        usable_cuts = min(quantity, total_cuts)
        
        # Cálculo del área utilizada
        area_per_cut = cut_width * cut_height
        total_used_area = usable_cuts * area_per_cut
        sheet_area = sheet_width * sheet_height
        total_sheet_area = sheets_required * sheet_area
        
        utilization_percentage = (total_used_area / total_sheet_area * 100) if total_sheet_area > 0 else 0
        
        # Cálculo del peso final
        # Gramaje es g/m², necesitamos convertir cm² a m²
        total_used_area_m2 = total_used_area / 10000  # cm² a m²
        final_weight = total_used_area_m2 * grammage
        
        return {
            'sheet_width': sheet_width,
            'sheet_height': sheet_height,
            'cut_width': cut_width,
            'cut_height': cut_height,
            'cuts_horizontal': cuts_horizontal,
            'cuts_vertical': cuts_vertical,
            'cuts_per_sheet': cuts_per_sheet,
            'sheets_required': sheets_required,
            'total_cuts': total_cuts,
            'usable_cuts': usable_cuts,
            'utilization_percentage': utilization_percentage,
            'final_weight': final_weight,
            'grammage': grammage,
            'quantity_requested': quantity
        }
