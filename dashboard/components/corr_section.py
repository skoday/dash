from dash import dcc, html

def create_correlation_section():
    """Crea la sección para la matriz de correlación con checklist y botón mejorada con más estilo"""
    return html.Div([
        html.H2('Matriz de Correlación', style={'text-align': 'center', 'color': '#f5f5f5', 'font-size': '24px'}),
        
        # Checklist para seleccionar las columnas numéricas
        dcc.Checklist(
            id='numeric-columns-checklist-corr',
            options=[],    # Se actualizará al cargar el archivo
            value=[],      # Valor inicial vacío
            labelStyle={'display': 'inline-block', 'margin-right': '10px', 'font-size': '16px', 'color': '#f5f5f5'}
        ),
        
        # Botón para mostrar la matriz de correlación
        html.Button('Mostrar Matriz de Correlación', id='show-corr-button', style={
            'background-color': '#007BFF', 
            'color': 'white', 
            'border': 'none', 
            'border-radius': '5px',
            'padding': '10px 20px', 
            'cursor': 'pointer', 
            'font-size': '16px', 
            'margin-top': '15px',
            'width': '100%'  # El botón ocupa todo el ancho disponible
        }),
        
        # Imagen de la matriz de correlación
        html.Img(id='matriz-correlacion', style={
            'width': '100%', 
            'max-height': '1300px', 
            'margin-top': '20px', 
            'border-radius': '8px', 
            'box-shadow': '0 4px 6px rgba(0,0,0,0.1)'
        })
    ], style={
        'padding': '20px',
        'border': '1px solid #444',  # Borde oscuro
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'background-color': '#1e1e1e',  # Fondo oscuro para la sección
        'margin': '10px 0'
    })
