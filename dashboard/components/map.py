from dash import html, dcc

def create_map_section():
    return html.Div([
        html.H2(
            'Mapa de puntos',
            style={
                'text-align': 'center',
                'color': '#f5f5f5',
                'font-size': '24px',
                'margin-bottom': '20px'
            }
        ),

        # Contenedor de filtros (dropdowns y botón)
        html.Div([
            # Dropdown de escala de colores
            html.Div([
                html.Label(
                    "Campo para escala de colores",
                    style={'font-size': '14px', 'color': '#ccc'}
                ),
                dcc.Dropdown(
                    id='color-schemna',
                    options=[],
                    placeholder="Selecciona un campo...",
                    className='dark-dropdown',
                    style={
                        'marginTop': '5px',
                        'font-size': '14px',
                        'background-color': '#2c2c2c',
                        'color': '#f5f5f5',
                        'border': '1px solid #444',
                        'border-radius': '5px'
                    }
                )
            ], style={'flex': '1', 'marginRight': '10px'}),

            # Dropdown de etiquetas
            html.Div([
                html.Label(
                    "Etiquetas para los puntos",
                    style={'font-size': '14px', 'color': '#ccc'}
                ),
                dcc.Dropdown(
                    id='tags-in-map',
                    options=[],
                    multi=True,
                    placeholder="Selecciona etiquetas...",
                    className='dark-dropdown',
                    style={
                        'marginTop': '5px',
                        'font-size': '14px',
                        'background-color': '#2c2c2c',
                        'color': '#f5f5f5',
                        'border': '1px solid #444',
                        'border-radius': '5px'
                    }
                )
            ], style={'flex': '1', 'marginRight': '10px'}),

            # Botón de filtro
            html.Div([
                html.Button(
                    'Añadir filtro',
                    id='map-filter-button',
                    style={
                        'background-color': '#007BFF',
                        'color': 'white',
                        'border': 'none',
                        'border-radius': '5px',
                        'padding': '10px 20px',
                        'cursor': 'pointer',
                        'font-size': '16px',
                        'width': '100%'
                    }
                )
            ], style={'flex': '1'})
        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'gap': '10px',
            'marginBottom': '20px'
        }),

        # Imagen o mapa renderizado
        html.Div(
            id='map-image',
            style={
                'marginBottom': '20px',
                'border-radius': '10px',
                'overflow': 'hidden',
                'background-color': '#1e1e1e',
                'padding': '10px'
            }
        )

    ], style={
        'width': '100%',
        'padding': '20px',
        'border': '1px solid #444',
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.3)',
        'background-color': '#222',
        'margin': '10px 0',
        'box-sizing': 'border-box'
    })
