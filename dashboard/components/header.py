from dash import html

def dashboard_header():
    return html.Div(
        html.H1(
                'Geo-Dashboard para microdatos moviles de medio ambiente',
                style={
                    'text-align': 'center',
                    'color': '#000000',
                    'font-size': '36px',
                    'font-weight': 'bold',
                    'text-transform': 'uppercase',
                    'letter-spacing': '2px',
                    'margin-top': '20px',
                    'margin-bottom': '20px',
                    'font-family': 'Arial, sans-serif',
                    'background': 'linear-gradient(45deg, #000000, #000000)',
                    'WebkitBackgroundClip': 'text',  # Esto aplica el gradiente solo al texto
                    'color': 'transparent'
                }
        )
    )