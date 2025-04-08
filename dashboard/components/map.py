from dash import html, dcc

def create_map_section():
    return html.Div([
        html.H2('Mapa de puntos', style={'text-align': 'center', 'color': '#333', 'font-size': '24px'}),
        html.Div(id='map-image'),
        html.Div(children="Selecciona campo a usar como referencia para la escala de colores", style={'marginTop': '20px', 'text-align': 'center', 'color': '#555'}),
        dcc.RadioItems(
            id='color-schemna',
            options=[],    # Se actualizará al cargar el archivo
            value=None,      # Valor inicial vacío
            labelStyle={'display': 'inline-block', 'margin-right': '10px', 'font-size': '16px'}
        ),
        html.Div(children='Selecciona etiquetas para cada punto', style={'marginTop': '20px', 'text-align': 'center', 'color': '#555'}),
        dcc.Checklist(
            id='tags-in-map',
            options=[],    # Se actualizará al cargar el archivo
            value=[],      # Valor inicial vacío
            labelStyle={'display': 'inline-block', 'margin-right': '10px', 'font-size': '16px'}
        ),
        html.Button('Añadir filtro', id='map-filter-button', style={
            'background-color': '#007BFF', 'color': 'white', 'border': 'none', 'border-radius': '5px',
            'padding': '10px 20px', 'cursor': 'pointer', 'font-size': '16px', 'margin-top': '15px'
        })
    ], style={
        'padding': '20px',
        'border': '1px solid #ccc',
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'background-color': 'white',
        'margin': '10px 0'
    })