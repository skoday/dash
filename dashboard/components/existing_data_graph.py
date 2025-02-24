import dash
from dash import html, dcc

def create_graph_section(title, graph_id):
    """Genera una sección con un gráfico Dash con estilos mejorados"""
    return html.Div([
        html.H2(title, style={'text-align': 'center', 'color': '#333'}),
        dcc.Graph(id=graph_id, style={'height': '400px'})
    ], style={
        'padding': '20px',
        'border': '1px solid #ccc',
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'background-color': 'white',
        'margin': '10px 0'
    })