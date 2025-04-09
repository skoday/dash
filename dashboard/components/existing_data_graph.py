import dash
from dash import html, dcc

def create_graph_section(title, graph_id):
    """Genera una sección con un gráfico Dash adaptado a dark mode"""
    return html.Div([
        html.H2(
            title,
            style={
                'text-align': 'center',
                'color': '#f5f5f5',
                'font-size': '20px',
                'margin': '0 0 15px 0',
                'text-transform': 'uppercase',
                'letter-spacing': '1px'
            }
        ),
        dcc.Graph(
            id=graph_id,
            config={
                'displayModeBar': False  # más limpio, pero lo puedes cambiar
            },
            style={
                'height': '400px',
                'border-radius': '10px',
                'background-color': '#1a1a1a'
            }
        )
    ], style={
        'padding': '20px',
        'border': '1px solid #2c2c2c',
        'border-radius': '12px',
        'box-shadow': '0 0 12px rgba(0,0,0,0.3)',
        'background-color': '#1e1e1e',
        'margin': '10px 0'
    })
