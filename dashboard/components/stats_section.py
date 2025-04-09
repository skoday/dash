from dash import dcc, html, dash_table
'''
    def create_stats_section():
        """Crea la sección de estadísticas generales con checklist y botón mejorada con más estilo"""
        return html.Div([
            html.H2('Estadísticas Generales', style={'text-align': 'center', 'color': '#333', 'font-size': '24px'}),
            dcc.Checklist(
                id='numeric-columns-checklist',
                options=[],    # Se actualizará al cargar el archivo
                value=[],      # Valor inicial vacío
                labelStyle={'display': 'inline-block', 'margin-right': '10px', 'font-size': '16px'}
            ),
            html.Button('Mostrar Estadísticas', id='show-stats-button', style={
                'background-color': '#007BFF', 'color': 'white', 'border': 'none', 'border-radius': '5px',
                'padding': '10px 20px', 'cursor': 'pointer', 'font-size': '16px', 'margin-top': '15px'
            }),
            dash_table.DataTable(
                id='tabla-estadisticas',
                style_table={'height': '300px', 'overflowY': 'auto', 'border-radius': '8px', 'box-shadow': '0 4px 6px rgba(0,0,0,0.1)'},
                style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
                style_cell={'padding': '10px', 'textAlign': 'center'}
            )
        ], style={
            'padding': '20px',
            'border': '1px solid #ccc',
            'border-radius': '10px',
            'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
            'background-color': 'white',
            'margin': '10px 0'
    })
'''

from dash import dcc, html, dash_table

def create_stats_section():
    """Crea la sección de estadísticas generales con checklist y botón mejorada con más estilo"""
    return html.Div([
        html.H2('Estadísticas Generales', style={'text-align': 'center', 'color': '#333', 'font-size': '24px'}),
        html.Div([
            # Columna 1: Dropdown para el esquema de color
            html.Div([
                html.Label("Campo para escala de colores", style={'font-size': '14px', 'color': '#555'}),
                dcc.Dropdown(
                    id='numeric-columns-checklist',
                    options=[],  # se actualizará dinámicamente
                    multi=True,
                    placeholder="Selecciona un campo...",
                    style={'marginTop': '5px', 'font-size': '14px'}
                )
            ], style={'flex': '1', 'marginRight': '10px'}),
            # Columna 3: Botón para añadir filtro
            html.Div([
                html.Button('Añadir filtro', id='show-stats-button', style={
                    'background-color': '#007BFF',
                    'color': 'white',
                    'border': 'none',
                    'border-radius': '5px',
                    'padding': '10px 20px',
                    'cursor': 'pointer',
                    'font-size': '16px',
                    'width': '100%'  # El botón ocupa todo el ancho disponible
                })
            ], style={'flex': '1'}),

        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'gap': '10px',  # Espacio entre las columnas
            'marginBottom': '20px',  # Separación entre los filtros y el mapa
            'height': 'auto'
        }),
        dash_table.DataTable(
            id='tabla-estadisticas',
            style_table={'height': '300px', 'overflowY': 'auto', 'border-radius': '8px', 'box-shadow': '0 4px 6px rgba(0,0,0,0.1)'},
            style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
            style_cell={'padding': '10px', 'textAlign': 'center'}
        )
    ], style={
        'padding': '20px',
        'border': '1px solid #ccc',
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'background-color': 'white',
        'margin': '10px 0'
    })