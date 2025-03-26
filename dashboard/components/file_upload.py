from dash import dcc, html

def create_upload_section():
    """Sección para cargar archivos CSV con más estilos"""
    return html.Div([
        html.H2('Cargar Archivo CSV', style={'text-align': 'center', 'color': '#333'}),
        dcc.Upload(
            id='upload-data',
            children=html.Button(
                'Cargar archivo CSV',
                style={
                    'background-color': '#007bff',  # Azul moderno
                    'color': 'white',
                    'border': 'none',
                    'padding': '10px 20px',
                    'border-radius': '5px',
                    'cursor': 'pointer',
                    'font-size': '16px'
                }
            ),
            multiple=True,
            style={
                'text-align': 'center',
                'padding': '20px',
                'border': '2px dashed #007bff',  # Línea punteada azul
                'border-radius': '10px',
                'background-color': '#f9f9f9',
                'cursor': 'pointer'
            }
        ),
        html.Div(id='output-datos', style={'marginTop': '20px', 'text-align': 'center', 'color': '#555'})
    ], style={
        'padding': '20px',
        'border': '1px solid #ccc',
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'background-color': 'white',
        'margin': '10px 0'
    })