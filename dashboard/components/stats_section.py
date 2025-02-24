from dash import dcc, html, dash_table

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