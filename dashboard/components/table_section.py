from dash import dcc, html, dash_table

def create_table_section(title, table_id):
    """Genera una sección con una tabla Dash con estilos mejorados"""
    return html.Div([
        html.H2(title, style={'text-align': 'center', 'color': '#333'}),
        dash_table.DataTable(
            id=table_id,
            style_table={
                'height': '300px', 
                'overflowY': 'auto', 
                'border-radius': '10px',
                'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)'
            },
            style_header={
                'backgroundColor': '#007bff',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_cell={
                'textAlign': 'center',
                'padding': '10px',
                'border': '1px solid #ddd'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f9f9f9'
                },
                {
                    'if': {'state': 'active'},
                    'backgroundColor': '#d3e3fc',
                    'border': '1px solid #007bff'
                }
            ]
        )
    ], style={
        'padding': '20px',
        'border': '1px solid #ccc',
        'border-radius': '10px',
        'box-shadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'background-color': 'white',
        'margin': '10px 0'
    })