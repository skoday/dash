from dash import dcc, html

def create_upload_section():
    """Sección para cargar archivos CSV compacta y alineada con la sección de descarga"""
    return html.Div([
        html.H2(
            'Cargar Archivo CSV',
            style={
                'text-align': 'center',
                'color': '#333',
                'font-size': '18px',
                'margin': '0 0 10px 0',
                'line-height': '1.2'
            }
        ),
        html.Div([
            dcc.Upload(
                id='upload-data',
                children=html.Button(
                    'Cargar archivo CSV',
                    style={
                        'background-color': '#007bff',
                        'color': 'white',
                        'border': 'none',
                        'padding': '8px 16px',
                        'border-radius': '5px',
                        'cursor': 'pointer',
                        'font-size': '14px'
                    }
                ),
                multiple=True,
                style={
                    'text-align': 'center',
                    'padding': '10px 20px',
                    'border': '2px dashed #007bff',
                    'border-radius': '10px',
                    'background-color': '#f9f9f9',
                    'cursor': 'pointer'
                }
            )
        ]),
        html.Div(
            id='output-datos',
            style={'marginTop': '10px', 'text-align': 'center', 'color': '#555', 'font-size': '14px'}
        )
    ], style={
        "flex": "1",
        'padding': '10px 20px',
        'border': '1px solid #ccc',
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'background-color': 'white',
        'margin': '5px 0'
    })
