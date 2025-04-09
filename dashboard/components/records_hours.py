from dash import dcc, html

def create_hourly_graph_section(title, graph_id, dropdown_id):
    return html.Div([
        html.H2(title, style={'text-align': 'center', 'color': '#333'}),
        dcc.Dropdown(id=dropdown_id, placeholder='Selecciona un día', style={'width': '50%', 'margin': 'auto'}),
        dcc.Graph(id=graph_id, style={'height': '300px', 'marginTop': '20px'})
    ], style={
        'padding': '20px',
        'border': '1px solid #ccc',
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'background-color': 'white',
        'margin': '10px 0'
    })
