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
from components.download_file import create_download_section

def create_layout():
    return html.Div([
        dashboard_header(),
        html.Div(
            children=[
                # CONTENEDOR QUE LIMITA EL ANCHO TOTAL
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                create_upload_section(),
                                create_download_section()
                            ],
                            style={"display": "flex", "flexDirection": "row", "gap": "20px"}  # opcional: gap para separar
                        )
                    ],
                    style={
                        "margin": "0 auto",   # centra horizontalmente
                        "padding": "20px"     # opcional: margen interno
                    }
                )
            ]
        ),

        dcc.Store(id='stored-clean-csv'),
        dcc.Store(id='gps-datapoints'),
        dcc.Store(id='general-statistics'),
        create_map_section(),
        create_table_section('Días con Datos', 'tabla-dias'),
        create_table_section_for_days("Datos disponibles por día", "data-table", 'day-dropdown'),
        create_graph_section('Gráfico de Datos Nulos vs Existentes', 'grafico-columnas'),
        
        html.Div(
                children=[
                    # Fila 1: 3 elementos en línea
                    html.Div(
                        children=[
                            create_table_section('Detalles por Columna', 'tabla-columnas'),
                            create_table_section('Tipos de Dato por Columna', 'tabla-tipos-dato'),
                        ],
                        style={"display": "flex", "flexDirection": "row"}
                    )
                ]
            ),
        create_stats_section(),
        create_correlation_section()
    ])

