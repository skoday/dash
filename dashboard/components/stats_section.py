from dash import dcc, html, dash_table

def create_stats_section():
    """Crea la sección de estadísticas generales con checklist y botón mejorada con más estilo"""
    return html.Div([
        html.H2('Estadísticas Generales', style={'text-align': 'center', 'color': '#f5f5f5', 'font-size': '24px'}),
        
        # Contenedor para los controles
        html.Div([
            # Columna 1: Dropdown para el esquema de color
            html.Div([
                html.Label("Campo para escala de colores", style={'font-size': '14px', 'color': '#f5f5f5'}),
                dcc.Dropdown(
                    id='numeric-columns-checklist',
                    options=[],  # Se actualizará dinámicamente
                    multi=True,
                    placeholder="Selecciona un campo...",
                    className='dark-dropdown',
                    style={'marginTop': '5px', 'font-size': '14px', 'backgroundColor': '#333', 'color': '#f5f5f5'}
                )
            ], style={'flex': '1', 'marginRight': '10px'}),

            # Columna 2: Botón para añadir filtro
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
            'marginBottom': '20px',  # Separación entre los filtros y la tabla
            'height': 'auto'
        }),

        # Tabla de estadísticas
        dash_table.DataTable(
            id='tabla-estadisticas',
            style_table={
                'height': '300px', 
                'overflowY': 'auto', 
                'border-radius': '8px', 
                'box-shadow': '0 4px 6px rgba(0,0,0,0.1)',
                'backgroundColor': '#2b2b2b'  # Fondo oscuro para la tabla
            },
            style_header={
                'backgroundColor': '#444',  # Fondo oscuro para la cabecera
                'fontWeight': 'bold',
                'color': '#f5f5f5'  # Texto blanco
            },
            style_cell={
                'padding': '10px', 
                'textAlign': 'center',
                'color': '#f5f5f5',  # Texto blanco para las celdas
                'backgroundColor': '#333',  # Fondo oscuro para las celdas
                'border': '1px solid #555'  # Bordes sutiles
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#444'  # Alterna el color de las filas impares
                },
                {
                    'if': {'state': 'active'},
                    'backgroundColor': '#007BFF',  # Color cuando la fila está activa
                    'border': '1px solid #007BFF'
                }
            ]
        )
    ], style={
        'padding': '20px',
        'border': '1px solid #444',
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'background-color': '#1e1e1e',  # Fondo oscuro para la sección
        'margin': '10px 0'
    })
