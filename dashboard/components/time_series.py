from dash import html, dcc

def create_timeseries_section():
    return html.Div([
        html.H2('Comportamiento de variables en el tiempo', style={
            'text-align': 'center',
            'color': '#f5f5f5',  # Texto en blanco para contrastar
            'margin-bottom': '10px',
            'font-size': '24px',
        }),

        # Dropdown para elegir la columna numérica
        dcc.Dropdown(
            id='timeseries-dropdown',
            options=[],  # Se llena dinámicamente
            value=None,
            placeholder='Selecciona una columna numérica',
            className='dark-dropdown',
            style={
                'width': '60%',
                'margin': '0 auto 20px auto',
                'font-size': '16px',
                'background-color': '#333',
                'color': '#f5f5f5',  # Texto claro
                'border': '1px solid #444',
                'border-radius': '5px',
                'padding': '8px',
                'box-shadow': '2px 2px 8px rgba(0,0,0,0.3)',
            }
        ),

        # Gráfico de la serie de tiempo
        dcc.Graph(id='timeseries-plot', style={
            'height': '400px',
            'border-radius': '10px',
            'box-shadow': '2px 2px 10px rgba(0,0,0,0.3)',  # Agrega sombra
            'background-color': '#1e1e1e',  # Fondo oscuro del gráfico
        })
        
    ], style={
        'padding': '20px',
        'border': '1px solid #444',
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.2)',
        'background-color': '#1e1e1e',  # Fondo oscuro para todo el contenedor
        'margin': '10px 0',
    })
