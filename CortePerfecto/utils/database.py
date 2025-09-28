import os
import psycopg2
import psycopg2.extras
from datetime import datetime
from typing import List, Dict, Optional
import json

class DatabaseManager:
    """Gestor de base de datos para la calculadora de cortes"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            # Fallback to individual parameters
            self.connection_params = {
                'host': os.getenv('PGHOST'),
                'port': int(os.getenv('PGPORT', 5432)),
                'database': os.getenv('PGDATABASE'),
                'user': os.getenv('PGUSER'),
                'password': os.getenv('PGPASSWORD')
            }
        self.init_tables()
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        if self.database_url:
            return psycopg2.connect(self.database_url)
        else:
            return psycopg2.connect(**self.connection_params)
    
    def init_tables(self):
        """Inicializa las tablas de la base de datos"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # Tabla de plantillas predefinidas
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS templates (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        description TEXT,
                        sheet_width DECIMAL(10,2) NOT NULL,
                        sheet_height DECIMAL(10,2) NOT NULL,
                        grammage INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # Tabla de configuraciones favoritas
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS favorite_configurations (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        sheet_width DECIMAL(10,2) NOT NULL,
                        sheet_height DECIMAL(10,2) NOT NULL,
                        cut_width DECIMAL(10,2) NOT NULL,
                        cut_height DECIMAL(10,2) NOT NULL,
                        grammage INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        cost_per_sheet DECIMAL(10,2) DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # Tabla de historial de cálculos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS calculation_history (
                        id SERIAL PRIMARY KEY,
                        calculation_type VARCHAR(20) NOT NULL,
                        sheet_width DECIMAL(10,2) NOT NULL,
                        sheet_height DECIMAL(10,2) NOT NULL,
                        cut_width DECIMAL(10,2) NOT NULL,
                        cut_height DECIMAL(10,2) NOT NULL,
                        grammage INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        cost_per_sheet DECIMAL(10,2) DEFAULT 0,
                        cuts_per_sheet INTEGER NOT NULL,
                        sheets_required INTEGER NOT NULL,
                        total_cuts INTEGER NOT NULL,
                        utilization_percentage DECIMAL(5,2) NOT NULL,
                        final_weight DECIMAL(10,2) NOT NULL,
                        total_cost DECIMAL(10,2) DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                conn.commit()
                
                # Insertar plantillas predefinidas si no existen
                self._insert_default_templates(cursor)
                conn.commit()
    
    def _insert_default_templates(self, cursor):
        """Inserta plantillas predefinidas si no existen"""
        cursor.execute("SELECT COUNT(*) FROM templates")
        if cursor.fetchone()[0] == 0:
            templates = [
                ('A4', 'Papel A4 estándar', 21.0, 29.7, 80),
                ('A3', 'Papel A3 grande', 29.7, 42.0, 80),
                ('Carta', 'Papel Carta US', 21.6, 27.9, 80),
                ('Legal', 'Papel Legal US', 21.6, 35.6, 80),
                ('Tabloid', 'Papel Tabloid/A3+', 27.9, 43.2, 80),
                ('A5', 'Papel A5 pequeño', 14.8, 21.0, 80),
                ('A2', 'Papel A2 extra grande', 42.0, 59.4, 80),
                ('Oficio', 'Papel Oficio', 21.6, 33.0, 80)
            ]
            
            for name, description, width, height, grammage in templates:
                cursor.execute("""
                    INSERT INTO templates (name, description, sheet_width, sheet_height, grammage)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, description, width, height, grammage))
    
    def get_templates(self) -> List[Dict]:
        """Obtiene todas las plantillas disponibles"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM templates ORDER BY name
                """)
                return [dict(row) for row in cursor.fetchall()]
    
    def save_favorite_configuration(self, name: str, config: Dict) -> int:
        """Guarda una configuración favorita"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO favorite_configurations 
                    (name, sheet_width, sheet_height, cut_width, cut_height, grammage, quantity, cost_per_sheet)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    name,
                    config['sheet_width'],
                    config['sheet_height'],
                    config['cut_width'],
                    config['cut_height'],
                    config['grammage'],
                    config['quantity'],
                    config.get('cost_per_sheet', 0)
                ))
                return cursor.fetchone()[0]
    
    def get_favorite_configurations(self) -> List[Dict]:
        """Obtiene todas las configuraciones favoritas"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM favorite_configurations ORDER BY created_at DESC
                """)
                return [dict(row) for row in cursor.fetchall()]
    
    def delete_favorite_configuration(self, config_id: int) -> bool:
        """Elimina una configuración favorita"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM favorite_configurations WHERE id = %s", (config_id,))
                return cursor.rowcount > 0
    
    def save_calculation_to_history(self, calculation_result: Dict, cost_per_sheet: float = 0) -> int:
        """Guarda un cálculo en el historial"""
        total_cost = calculation_result['sheets_required'] * cost_per_sheet
        
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO calculation_history 
                    (calculation_type, sheet_width, sheet_height, cut_width, cut_height, 
                     grammage, quantity, cost_per_sheet, cuts_per_sheet, sheets_required, 
                     total_cuts, utilization_percentage, final_weight, total_cost)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    calculation_result.get('orientation', 'unknown'),
                    calculation_result['sheet_width'],
                    calculation_result['sheet_height'],
                    calculation_result['cut_width'],
                    calculation_result['cut_height'],
                    calculation_result['grammage'],
                    calculation_result['quantity_requested'],
                    cost_per_sheet,
                    calculation_result['cuts_per_sheet'],
                    calculation_result['sheets_required'],
                    calculation_result['total_cuts'],
                    calculation_result['utilization_percentage'],
                    calculation_result['final_weight'],
                    total_cost
                ))
                return cursor.fetchone()[0]
    
    def get_calculation_history(self, limit: int = 50) -> List[Dict]:
        """Obtiene el historial de cálculos"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM calculation_history 
                    ORDER BY created_at DESC 
                    LIMIT %s
                """, (limit,))
                return [dict(row) for row in cursor.fetchall()]
    
    def clear_calculation_history(self) -> bool:
        """Limpia el historial de cálculos"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM calculation_history")
                return cursor.rowcount > 0
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas generales"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                stats = {}
                
                # Total de cálculos realizados
                cursor.execute("SELECT COUNT(*) FROM calculation_history")
                stats['total_calculations'] = cursor.fetchone()[0]
                
                # Configuraciones favoritas guardadas
                cursor.execute("SELECT COUNT(*) FROM favorite_configurations")
                stats['favorite_configurations'] = cursor.fetchone()[0]
                
                # Promedio de utilización
                cursor.execute("SELECT AVG(utilization_percentage) FROM calculation_history")
                result = cursor.fetchone()[0]
                stats['average_utilization'] = float(result) if result else 0
                
                # Total de hojas calculadas
                cursor.execute("SELECT SUM(sheets_required) FROM calculation_history")
                result = cursor.fetchone()[0]
                stats['total_sheets_calculated'] = int(result) if result else 0
                
                return stats