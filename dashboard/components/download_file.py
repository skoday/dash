from dash import dcc, html

def create_download_section():
    """Sección para descargar archivos CSV con estilos chidos"""
    return html.Div([
        html.H2('Descargar Archivo CSV', style={'text-align': 'center', 'color': '#333'}),

        html.Div([
            html.Button(
                'Descargar archivo CSV',
                id='download-btn',
                style={
                    'background-color': '#007bff',
                    'color': 'white',
                    'border': 'none',
                    'padding': '8px 16px',
                    'border-radius': '5px',
                    'cursor': 'pointer',
                    'font-size': '14px'
                }
            )
        ], style={
            'text-align': 'center',
            'padding': '10px 20px',
            'border': '2px dashed #007bff',
            'border-radius': '10px',
            'background-color': '#f9f9f9',
            'cursor': 'pointer'
        }),

        dcc.Download(id='download-data')  # Sin hijos
    ], style={
        "flex": "1",
        'padding': '10px 20px',
        'border': '1px solid #ccc',
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'background-color': 'white',
        'margin': '5px 0'
    })
