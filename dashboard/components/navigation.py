# navigation.py
from dash import html, dcc

def create_navigation_ribbon():
    """Create a thin navigation ribbon for all pages"""
    return html.Div([
        html.Div([
            # Logo/Title section
            html.Div([
                html.H3("Menu", 
                       style={
                           'margin': '0',
                           'color': '#f5f5f5',
                           'font-size': '16px',
                           'font-weight': 'bold',
                           'letter-spacing': '0.5px'
                       })
            ], style={'flex': '1'}),
            
            # Navigation buttons
            html.Div([
                dcc.Link(
                    html.Button("Dashboard", 
                               className="nav-button",
                               style={
                                   'background-color': '#1e88e5',
                                   'color': 'white',
                                   'border': 'none',
                                   'padding': '8px 16px',
                                   'margin': '0 5px',
                                   'border-radius': '4px',
                                   'cursor': 'pointer',
                                   'font-size': '14px',
                                   'font-weight': '500',
                                   'transition': 'background-color 0.2s ease',
                                   'text-decoration': 'none'
                               }),
                    href="/",
                    style={'text-decoration': 'none'}
                ),
                
                dcc.Link(
                    html.Button("RAMA", 
                               className="nav-button",
                               style={
                                   'background-color': '#4caf50',
                                   'color': 'white',
                                   'border': 'none',
                                   'padding': '8px 16px',
                                   'margin': '0 5px',
                                   'border-radius': '4px',
                                   'cursor': 'pointer',
                                   'font-size': '14px',
                                   'font-weight': '500',
                                   'transition': 'background-color 0.2s ease'
                               }),
                    href="/rama",
                    style={'text-decoration': 'none'}
                ),
                
                dcc.Link(
                    html.Button("Sensor Móvil DB", 
                               className="nav-button",
                               style={
                                   'background-color': '#ff9800',
                                   'color': 'white',
                                   'border': 'none',
                                   'padding': '8px 16px',
                                   'margin': '0 5px',
                                   'border-radius': '4px',
                                   'cursor': 'pointer',
                                   'font-size': '14px',
                                   'font-weight': '500',
                                   'transition': 'background-color 0.2s ease'
                               }),
                    href="/movil",
                    style={'text-decoration': 'none'}
                )
            ], style={'display': 'flex', 'align-items': 'center'})
        ], style={
            'display': 'flex',
            'justify-content': 'space-between',
            'align-items': 'center',
            'padding': '0 20px',
            'height': '50px'
        })
    ], style={
        'background-color': '#1e1e1e',
        'border-bottom': '2px solid #2c2c2c',
        'box-shadow': '0 2px 4px rgba(0,0,0,0.3)',
        'position': 'sticky',
        'top': '0',
        'z-index': '1000',
        'margin-bottom': '10px'
    })
