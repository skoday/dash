from dash import dcc, html

def create_upload_section():
    """Sección para cargar archivos CSV con estilo dark moderno"""
    return html.Div([
        html.H2(
            'Cargar Archivo CSV',
            style={
                'text-align': 'center',
                'color': '#f5f5f5',
                'font-size': '20px',
                'margin': '0 0 10px 0',
                'line-height': '1.2',
                'text-transform': 'uppercase',
                'letter-spacing': '1px'
            }
        ),
        html.Div([
            dcc.Upload(
                id='upload-data',
                children=html.Button(
                    '📁 Subir archivo',
                    style={
                        'background-color': '#1e88e5',
                        'color': 'white',
                        'border': 'none',
                        'padding': '8px 20px',
                        'border-radius': '5px',
                        'cursor': 'pointer',
                        'font-size': '14px',
                        'box-shadow': '0 2px 6px rgba(30, 136, 229, 0.3)'
                    }
                ),
                multiple=True,
                style={
                    'text-align': 'center',
                    'padding': '15px',
                    'border': '2px dashed #1e88e5',
                    'border-radius': '10px',
                    'background-color': '#1e1e1e',
                    'cursor': 'pointer'
                }
            )
        ]),
        html.Div(
            id='output-datos',
            style={
                'marginTop': '12px',
                'text-align': 'center',
                'color': '#aaa',
                'font-size': '13px'
            }
        )
    ], style={
        "flex": "1",
        'padding': '15px 20px',
        'border': '1px solid #2c2c2c',
        'border-radius': '12px',
        'box-shadow': '0 0 12px rgba(0,0,0,0.3)',
        'background-color': '#1a1a1a',
        'margin': '10px 0'
    })
