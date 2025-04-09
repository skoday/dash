from dash import html

def dashboard_header():
    return html.Div([
        html.H1(
            'Geo-Dashboard para microdatos móviles de medio ambiente',
            style={
                'text-align': 'center',
                'font-size': '40px',
                'font-weight': '900',
                'text-transform': 'uppercase',
                'letter-spacing': '2px',
                'margin': '0',
                'padding': '20px',
                'font-family': 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
                'color': 'white',
                'background': 'linear-gradient(135deg, #007bff, #00c6ff)',  # Degradado moderno
                'border-radius': '15px',
                'box-shadow': '0px 4px 12px rgba(0, 0, 0, 0.2)'
            }
        )
    ], style={
        'max-width': '1000px',
        'margin': '30px auto',
        'text-align': 'center'
    })
