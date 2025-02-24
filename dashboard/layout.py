from dash import html
from components.header import dashboard_header
from dash import dcc
from components.file_upload import create_upload_section
from components.table_section import create_table_section
from components.existing_data_graph import create_graph_section
from components.stats_section import create_stats_section
from components.corr_section import create_correlation_section
from components.map import create_map_section
from components.records_hours import create_table_section_for_days

def create_layout():
    return html.Div([
        dashboard_header(),
        create_upload_section(),
        dcc.Store(id='stored-clean-csv'),
        create_table_section('Días con Datos', 'tabla-dias'),
        create_table_section_for_days("Datos disponibles por día", "data-table", 'day-dropdown'),
        create_graph_section('Gráfico de Datos Nulos vs Existentes', 'grafico-columnas'),
        create_table_section('Detalles por Columna', 'tabla-columnas'),
        create_table_section('Tipos de Dato por Columna', 'tabla-tipos-dato'),
        create_stats_section(),
        create_correlation_section(),
        create_map_section()
    ])

