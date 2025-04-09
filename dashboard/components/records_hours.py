from dash import dcc, html

def create_hourly_graph_section(title, graph_id, dropdown_id):
    return html.Div([
        html.H2(title, style={'text-align': 'center', 'color': '#f5f5f5'}),  # Título blanco para el tema oscuro
        dcc.Dropdown(
            id=dropdown_id,
            placeholder='Selecciona un día',
            className='dark-dropdown',
            style={
                'width': '50%',
                'margin': 'auto',
                'background-color': '#333',  # Fondo oscuro para el dropdown
                'color': '#f5f5f5',  # Texto blanco para el dropdown
                'border': '1px solid #444',  # Borde oscuro
                'border-radius': '5px',
                'font-size': '14px'
            }
        ),
        dcc.Graph(id=graph_id, style={'height': '300px', 'marginTop': '20px'})
    ], style={
        'padding': '20px',
        'border': '1px solid #444',  # Bordes oscuros
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'background-color': '#1e1e1e',  # Fondo oscuro para la sección
        'margin': '10px 0'
    })
