import plotly.graph_objs as go
from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import requests
import pandas as pd
from datetime import datetime
from env_config import settings

RAMA_URL = settings.rama_url  # This only provides an ip:port connection

def create_empty_graph():
    """Create empty graph for initial display"""
    fig = go.Figure()
    fig.update_layout(
        title='Selecciona un elemento y una estación para mostrar la serie de tiempo',
        xaxis_title='Fecha y Hora',
        yaxis_title='Medición',
        template='plotly_dark',
        height=500,
        showlegend=True
    )
    return fig

def integration_layout():
    return html.Div([
        # Title section
        html.Div([
            html.H2(
                "Visualización de componentes de las estaciones del sistema RAMA",
                style={
                    'text-align': 'center',
                    'color': '#f5f5f5',
                    'font-size': '24px',
                    'margin': '0 0 15px 0',
                    'line-height': '1.2',
                    'text-transform': 'uppercase',
                    'letter-spacing': '1px',
                    'font-weight': 'bold'
                }
            )
        ], style={
            'padding': '20px',
            'border': '1px solid #2c2c2c',
            'border-radius': '12px',
            'box-shadow': '0 0 12px rgba(0,0,0,0.3)',
            'background-color': '#1e1e1e',
            'margin': '10px 0'
        }),
        
        # Description section
        html.Div([
            html.P(
                "Se muestra la serie de tiempo de algún elemento específico en la estación elegida del sistema RAMA de la CDMX.",
                style={
                    'text-align': 'center',
                    'color': '#aaa',
                    'font-size': '14px',
                    'margin': '0',
                    'line-height': '1.4'
                }
            )
        ], style={
            'padding': '15px 20px',
            'border': '1px solid #2c2c2c',
            'border-radius': '12px',
            'box-shadow': '0 0 12px rgba(0,0,0,0.3)',
            'background-color': '#1a1a1a',
            'margin': '10px 0'
        }),
        
        # Controls section
        html.Div([
            html.Div([
                # Elemento dropdown
                html.Div([
                    html.Label(
                        "Elemento:",
                        style={
                            'color': '#f5f5f5',
                            'font-weight': 'bold',
                            'margin-bottom': '8px',
                            'display': 'block',
                            'font-size': '14px'
                        }
                    ),
                    dcc.Dropdown(
                        id='elemento-dropdown',
                        options=[],
                        placeholder="Cargando elementos...",
                        style={
                            'background-color': '#1a1a1a',
                            'border': '1px solid #2c2c2c',
                            'border-radius': '5px'
                        },
                        className='dark-dropdown'
                    )
                ], style={'flex': '1'}),
                
                # Estación dropdown
                html.Div([
                    html.Label(
                        "Estación:",
                        style={
                            'color': '#f5f5f5',
                            'font-weight': 'bold',
                            'margin-bottom': '8px',
                            'display': 'block',
                            'font-size': '14px'
                        }
                    ),
                    dcc.Dropdown(
                        id='estacion-dropdown',
                        options=[],
                        placeholder="Cargando estaciones...",
                        style={
                            'background-color': '#1a1a1a',
                            'border': '1px solid #2c2c2c',
                            'border-radius': '5px'
                        },
                        className='dark-dropdown'
                    )
                ], style={'flex': '1'}),
                
                # Mostrar button
                html.Div([
                    html.Label(
                        "Acción:",
                        style={
                            'color': '#f5f5f5',
                            'font-weight': 'bold',
                            'margin-bottom': '8px',
                            'display': 'block',
                            'font-size': '14px'
                        }
                    ),
                    html.Button(
                        "Mostrar",
                        id="mostrar-button",
                        style={
                            'background-color': '#1e88e5',
                            'color': 'white',
                            'border': 'none',
                            'padding': '10px 20px',
                            'border-radius': '5px',
                            'cursor': 'pointer',
                            'font-size': '16px',
                            'font-weight': 'bold',
                            'width': '100%',
                            'box-shadow': '0 2px 6px rgba(30, 136, 229, 0.3)'
                        }
                    )
                ], style={'flex': '1'})
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'gap': '20px',
                'align-items': 'end'
            })
        ], style={
            'padding': '20px',
            'border': '1px solid #2c2c2c',
            'border-radius': '12px',
            'box-shadow': '0 0 12px rgba(0,0,0,0.3)',
            'background-color': '#1e1e1e',
            'margin': '10px 0'
        }),
        
        # Graph section
        html.Div([
            html.H3(
                "Serie de Tiempo",
                style={
                    'text-align': 'center',
                    'color': '#f5f5f5',
                    'font-size': '18px',
                    'margin': '0 0 15px 0',
                    'text-transform': 'uppercase',
                    'letter-spacing': '1px'
                }
            ),
            dcc.Loading(
                id="loading",
                type="default",
                children=[
                    dcc.Graph(
                        id='time-series-graph',
                        figure=create_empty_graph(),
                        config={
                            'displayModeBar': False
                        },
                        style={
                            'height': '500px',
                            'border-radius': '10px',
                            'background-color': '#1a1a1a'
                        }
                    )
                ]
            )
        ], style={
            'padding': '20px',
            'border': '1px solid #2c2c2c',
            'border-radius': '12px',
            'box-shadow': '0 0 12px rgba(0,0,0,0.3)',
            'background-color': '#1e1e1e',
            'margin': '10px 0'
        }),
        
        # Status alert section
        html.Div([
            html.Div(id="status-alert")
        ], style={
            'margin': '10px 0'
        }),
        
        # Hidden div to trigger initial data loading
        html.Div(id="trigger-load", style={'display': 'none'})
    ])

# Callback to load elementos dropdown
@callback(
    Output('elemento-dropdown', 'options'),
    Output('elemento-dropdown', 'placeholder'),
    Input('trigger-load', 'children')
)
def load_elementos(_):
    try:
        response = requests.get(f"{RAMA_URL}/elementos", timeout=10)
        if response.status_code == 200:
            elementos = response.json()
            options = [{'label': f"{elem['elemento']} - {elem['nombre_elemento']}", 
                       'value': elem['id_elemento']} for elem in elementos]
            return options, "Selecciona un elemento..."
        else:
            return [], f"Error al cargar elementos (Código: {response.status_code})"
    except requests.exceptions.RequestException as e:
        return [], f"Error de conexión: {str(e)}"
    except Exception as e:
        return [], f"Error: {str(e)}"

# Callback to load estaciones dropdown
@callback(
    Output('estacion-dropdown', 'options'),
    Output('estacion-dropdown', 'placeholder'),
    Input('trigger-load', 'children')
)
def load_estaciones(_):
    try:
        response = requests.get(f"{RAMA_URL}/estaciones", timeout=10)
        if response.status_code == 200:
            estaciones = response.json()
            options = [{'label': f"{est['clave_estacion']} - {est['nombre_estacion']}", 
                       'value': est['id_estacion']} for est in estaciones]
            return options, "Selecciona una estación..."
        else:
            return [], f"Error al cargar estaciones (Código: {response.status_code})"
    except requests.exceptions.RequestException as e:
        return [], f"Error de conexión: {str(e)}"
    except Exception as e:
        return [], f"Error: {str(e)}"

# Callback to update the time series graph
@callback(
    [Output('time-series-graph', 'figure'),
     Output('status-alert', 'children')],
    [Input('mostrar-button', 'n_clicks')],
    [State('elemento-dropdown', 'value'),
     State('estacion-dropdown', 'value')]
)
def update_time_series(n_clicks, elemento_id, estacion_id):
    if n_clicks is None or elemento_id is None or estacion_id is None:
        return create_empty_graph(), ""
    
    try:
        # Fetch time series data
        response = requests.get(
            f"{RAMA_URL}/mediciones/time-series",
            params={'id_estacion': estacion_id, 'id_elemento': elemento_id},
            timeout=30  # Longer timeout for potentially large datasets
        )
        
        if response.status_code == 200:
            data = response.json()
            #print(data)
            if not data:
                alert = dbc.Alert("No se encontraron datos para la combinación seleccionada.", 
                                color="warning", className="mt-3")
                return create_empty_graph(), alert
            
            # Convert to DataFrame for easier handling
            df = pd.DataFrame(data)
            df['datetime'] = pd.to_datetime(df['datetime'])
            
            # Filter out invalid measurements (assuming -99.0 means no data)
            df_filtered = df[df['medicion'] != -99.0]
            
            if df_filtered.empty:
                alert = dbc.Alert("No se encontraron mediciones válidas para la selección.", 
                                color="warning", className="mt-3")
                return create_empty_graph(), alert
            
            # Get elemento and estacion info for labels
            elemento_info = None
            estacion_info = None
            
            try:
                elementos_response = requests.get(f"{RAMA_URL}/elementos", timeout=10)
                if elementos_response.status_code == 200:
                    elementos = elementos_response.json()
                    elemento_info = next((e for e in elementos if e['id_elemento'] == elemento_id), None)
            except:
                pass
                
            try:
                estaciones_response = requests.get(f"{RAMA_URL}/estaciones", timeout=10)
                if estaciones_response.status_code == 200:
                    estaciones = estaciones_response.json()
                    estacion_info = next((e for e in estaciones if e['id_estacion'] == estacion_id), None)
            except:
                pass
            
            # Create the figure
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df_filtered['datetime'],
                y=df_filtered['medicion'],
                mode='lines',
                name=f"{elemento_info['elemento'] if elemento_info else 'Elemento'} - {estacion_info['clave_estacion'] if estacion_info else 'Estación'}",
                line=dict(color='#2E86AB', width=2),
                hovertemplate='<b>Fecha:</b> %{x}<br><b>Medición:</b> %{y}<extra></extra>'
            ))
            
            # Update layout
            title = f"Serie de Tiempo - {elemento_info['nombre_elemento'] if elemento_info else 'Elemento'}"
            if estacion_info:
                title += f" en {estacion_info['nombre_estacion']}"
                
            y_title = f"Medición ({elemento_info['unidad_medicion'] if elemento_info else 'Unidad'})"
            
            fig.update_layout(
                title=title,
                xaxis_title='Fecha y Hora',
                yaxis_title=y_title,
                template='plotly_dark',
                height=500,
                showlegend=True,
                hovermode='x unified'
            )
            
            # Success alert
            total_points = len(df_filtered)
            date_range = f"{df_filtered['datetime'].min().strftime('%Y-%m-%d')} a {df_filtered['datetime'].max().strftime('%Y-%m-%d')}"
            alert = dbc.Alert(""
                #f"Datos cargados exitosamente. {total_points:,} mediciones desde {date_range}.", 
                #color="success", className="mt-3"
            )
            
            return fig, alert
            
        else:
            alert = dbc.Alert(f"Error al obtener datos de la serie de tiempo: {response.status_code}", 
                            color="danger", className="mt-3")
            return create_empty_graph(), alert
            
    except requests.exceptions.RequestException as e:
        alert = dbc.Alert(f"Error de conexión con la API: {str(e)}", 
                        color="danger", className="mt-3")
        return create_empty_graph(), alert
    except Exception as e:
        alert = dbc.Alert(f"Error al procesar los datos: {str(e)}", 
                        color="danger", className="mt-3")
        return create_empty_graph(), alert
