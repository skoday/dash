import plotly.graph_objs as go
from dash import dcc, html
import dash_bootstrap_components as dbc
import numpy as np

def create_test_graph():
    # Generate some random data for testing
    np.random.seed(42)  # For reproducible "random" data
    x_values = list(range(1, 21))
    y_values = np.random.randint(5, 50, 20).tolist()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        name='Random Test Data',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=8, color='#A23B72')
    ))
    
    fig.update_layout(
        title='Test Graph for Second Layout',
        xaxis_title='Time Points',
        yaxis_title='Random Values',
        template='plotly_white',
        height=400
    )
    
    return fig

# Your integration page layout
def integration_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Integration View", className="text-center mb-4"),
                html.P("This is your second layout with a test graph below:", 
                       className="text-muted text-center")
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='test-graph',
                    figure=create_test_graph()
                )
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Alert("Graph loaded successfully! Your second layout is working.", 
                         color="success", className="mt-3")
            ])
        ])
    ])
