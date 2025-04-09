from dash import html, dcc

def create_map_section():
    return html.Div([
        html.H2('Mapa de puntos', style={'text-align': 'center', 'color': '#333', 'font-size': '24px'}),

        # Contenedor con 3 columnas para los dropdowns y el botón
        html.Div([
            # Columna 1: Dropdown para el esquema de color
            html.Div([
                html.Label("Campo para escala de colores", style={'font-size': '14px', 'color': '#555'}),
                dcc.Dropdown(
                    id='color-schemna',
                    options=[],  # se actualizará dinámicamente
                    placeholder="Selecciona un campo...",
                    style={'marginTop': '5px', 'font-size': '14px'}
                )
            ], style={'flex': '1', 'marginRight': '10px'}),

            # Columna 2: Dropdown para etiquetas
            html.Div([
                html.Label("Etiquetas para los puntos", style={'font-size': '14px', 'color': '#555'}),
                dcc.Dropdown(
                    id='tags-in-map',
                    options=[],  # se actualizará dinámicamente
                    multi=True,
                    placeholder="Selecciona etiquetas...",
                    style={'marginTop': '5px', 'font-size': '14px'}
                )
            ], style={'flex': '1', 'marginRight': '10px'}),

            # Columna 3: Botón para añadir filtro
            html.Div([
                html.Button('Añadir filtro', id='map-filter-button', style={
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

        # Aquí renderizas la imagen o gráfico del mapa
        html.Div(id='map-image', style={'marginBottom': '20px'}),

    ], style={
        'width': '100%',
        'padding': '20px',
        'border': '1px solid #ccc',
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'background-color': 'white',
        'margin': '10px 0',
        'box-sizing': 'border-box'
    })
