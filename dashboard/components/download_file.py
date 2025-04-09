from dash import dcc, html

def create_download_section():
    """Sección para descargar archivos CSV con estilos dark bien pro"""
    return html.Div([
        html.H2(
            'Descargar Archivo CSV',
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
            html.Button(
                '⬇️ Descargar archivo CSV',
                id='download-btn',
                style={
                    'background-color': '#43a047',  # Verde elegante
                    'color': 'white',
                    'border': 'none',
                    'padding': '8px 20px',
                    'border-radius': '5px',
                    'cursor': 'pointer',
                    'font-size': '14px',
                    'box-shadow': '0 2px 6px rgba(67, 160, 71, 0.3)'
                }
            )
        ], style={
            'text-align': 'center',
            'padding': '15px',
            'border': '2px dashed #43a047',
            'border-radius': '10px',
            'background-color': '#1e1e1e',
            'cursor': 'pointer'
        }),
        dcc.Download(id='download-data')
    ], style={
        "flex": "1",
        'padding': '15px 20px',
        'border': '1px solid #2c2c2c',
        'border-radius': '12px',
        'box-shadow': '0 0 12px rgba(0,0,0,0.3)',
        'background-color': '#1a1a1a',
        'margin': '10px 0'
    })
