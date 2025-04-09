from dash import dcc, html, dash_table

def create_table_section(title, table_id):
    """Genera una sección con una tabla Dash con estilos mejorados"""
    return html.Div([
        html.H2(title, style={
            'text-align': 'center',
            'color': '#f5f5f5',  # Título en blanco para el tema oscuro
            'font-size': '24px'
        }),

        dash_table.DataTable(
            id=table_id,
            style_table={
                'height': '300px',
                'overflowY': 'auto',
                'border-radius': '10px',
                'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
                'background-color': '#2a2a2a'  # Fondo oscuro para la tabla
            },
            style_header={
                'backgroundColor': '#007bff',  # Azul brillante para el encabezado
                'color': 'white',  # Color de texto blanco para el encabezado
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_cell={
                'textAlign': 'center',
                'padding': '10px',
                'border': '1px solid #444',  # Bordes más oscuros
                'color': '#f5f5f5',  # Texto blanco para las celdas
                'backgroundColor': '#2a2a2a'  # Fondo oscuro para las celdas
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#3c3c3c'  # Fondo ligeramente más claro para las filas impares
                },
                {
                    'if': {'state': 'active'},
                    'backgroundColor': '#0056b3',  # Color al hacer clic (azul)
                    'border': '1px solid #007bff'
                }
            ]
        )
    ], style={
        "flex": "1",
        'padding': '20px',
        'border': '1px solid #444',  # Bordes más oscuros alrededor de la sección
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'background-color': '#1e1e1e',  # Fondo oscuro para la sección
        'margin': '10px 0'
    })
