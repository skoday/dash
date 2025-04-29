from dash import dcc, html

def create_decade_distribution_section():
    """Crea una sección para mostrar la distribución de datos por decenas"""
    return html.Div([
        html.H2('Distribución por elemento', style={'text-align': 'center', 'color': '#f5f5f5', 'font-size': '24px'}),
        
        # Dropdown de columnas numéricas
        dcc.Dropdown(
            id='decade-column-dropdown',
            options=[],  # Se actualizará dinámicamente
            placeholder="Selecciona una columna numérica",
            className='dark-dropdown',
            style={
                'width': '100%',
                'font-size': '14px',
                'marginBottom': '20px',
                'background-color': '#2b2b2b',
                'color': '#f5f5f5'
            }
        ),

        # Gráfico de distribución
        dcc.Graph(id='decade-distribution-graph', style={'height': '350px'})
    ], style={
        'padding': '20px',
        'border': '1px solid #444',
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'background-color': '#1e1e1e',
        'margin': '10px 0'
    })
