import plotly.graph_objs as go
from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import requests
import pandas as pd
from datetime import datetime
from env_config import settings
from dash import callback_context

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
        
        # Controls section - AQUÍ ESTÁ TODO INTEGRADO
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
                ], style={'flex': '1'}),
                
                # ──────────── NUEVOS CAMPOS PARA PREDICCIÓN ────────────
                # Fecha de entrenamiento
                html.Div([
                    html.Label(
                        "Rango entrenamiento:",
                        style={
                            'color': '#f5f5f5',
                            'font-weight': 'bold',
                            'margin-bottom': '8px',
                            'display': 'block',
                            'font-size': '14px'
                        }
                    ),
                    dcc.DatePickerRange(
                        id='train-range',
                        min_date_allowed=datetime(1986, 1, 1),
                        max_date_allowed=datetime.now(),
                        start_date=datetime(2023, 1, 1),
                        end_date=datetime(2023, 1, 31),
                        display_format='YYYY-MM-DD',
                        style={
                            'background-color': '#1a1a1a',
                            'border': '1px solid #2c2c2c',
                            'border-radius': '5px',
                            'color': 'white'
                        }
                    )
                ], style={'flex': '2'}),
                
                # Ventana de predicción
                html.Div([
                    html.Label(
                        "Ventana (h):",
                        style={
                            'color': '#f5f5f5',
                            'font-weight': 'bold',
                            'margin-bottom': '8px',
                            'display': 'block',
                            'font-size': '14px'
                        }
                    ),
                    dcc.Input(
                        id='pred-window',
                        type='number',
                        min=1, max=720, step=1,
                        value=24,
                        style={
                            'width': '100%',
                            'background-color': '#1a1a1a',
                            'border': '1px solid #2c2c2c',
                            'border-radius': '5px',
                            'color': 'white',
                            'padding': '10px'
                        }
                    )
                ], style={'flex': '1'}),
                
                # Botón predecir
                html.Div([
                    html.Label(
                        "Acción predicción:",
                        style={
                            'color': '#f5f5f5',
                            'font-weight': 'bold',
                            'margin-bottom': '8px',
                            'display': 'block',
                            'font-size': '14px'
                        }
                    ),
                    html.Button(
                        "Predecir",
                        id="predecir-button",
                        style={
                            'background-color': '#e53935',
                            'color': 'white',
                            'border': 'none',
                            'padding': '10px 20px',
                            'border-radius': '5px',
                            'cursor': 'pointer',
                            'font-size': '16px',
                            'font-weight': 'bold',
                            'width': '100%',
                            'box-shadow': '0 2px 6px rgba(229, 57, 53, 0.3)'
                        }
                    )
                ], style={'flex': '1'}),
                # ──────────── FIN NUEVOS CAMPOS ────────────
                
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


@callback(
    [Output('time-series-graph', 'figure'),
     Output('status-alert', 'children')],
    [Input('mostrar-button', 'n_clicks'),
     Input('predecir-button', 'n_clicks')],
    [State('elemento-dropdown', 'value'),
     State('estacion-dropdown', 'value'),
     State('train-range', 'start_date'),
     State('train-range', 'end_date'),
     State('pred-window', 'value')]
)
def update_graph_and_alert(mostrar_clicks, predecir_clicks, elemento_id, estacion_id, 
                          start_date, end_date, ventana_horas):
    # Get which button triggered the callback
    ctx = callback_context
    
    # If no button has been clicked yet
    if not ctx.triggered:
        return create_empty_graph(), ""
    
    # Get the ID of the component that triggered the callback
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Route to appropriate function based on which button was clicked
    if button_id == 'mostrar-button':
        return handle_mostrar_button(mostrar_clicks, elemento_id, estacion_id)
    elif button_id == 'predecir-button':
        return handle_predecir_button(predecir_clicks, elemento_id, estacion_id, 
                                     start_date, end_date, ventana_horas)
    
    return create_empty_graph(), ""


def handle_mostrar_button(n_clicks, elemento_id, estacion_id):
    """Handle the 'Mostrar' button logic"""
    if n_clicks is None or elemento_id is None or estacion_id is None:
        return create_empty_graph(), ""
    
    try:
        # Your existing mostrar logic here
        response = requests.get(
            f"{RAMA_URL}/mediciones/time-series",
            params={'id_estacion': estacion_id, 'id_elemento': elemento_id},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if not data:
                alert = dbc.Alert("No se encontraron datos para la combinación seleccionada.", 
                                color="warning", className="mt-3")
                return create_empty_graph(), alert
            
            # Convert to DataFrame and process (your existing logic)
            df = pd.DataFrame(data)
            df['datetime'] = pd.to_datetime(df['datetime'])
            df_filtered = df[df['medicion'] != -99.0]
            
            if df_filtered.empty:
                alert = dbc.Alert("No se encontraron mediciones válidas para la selección.", 
                                color="warning", className="mt-3")
                return create_empty_graph(), alert
            
            # Create the figure (your existing plotting logic)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_filtered['datetime'],
                y=df_filtered['medicion'],
                mode='lines',
                name='Datos Históricos',
                line=dict(color='#2E86AB', width=2),
                hovertemplate='<b>Fecha:</b> %{x}<br><b>Medición:</b> %{y}<extra></extra>'
            ))
            
            fig.update_layout(
                title="Serie de Tiempo - Datos Históricos",
                xaxis_title='Fecha y Hora',
                yaxis_title='Medición',
                template='plotly_dark',
                height=500,
                showlegend=True,
                hovermode='x unified'
            )
            
            alert = dbc.Alert("", color="success", className="mt-3")
            return fig, alert
            
        else:
            alert = dbc.Alert(f"Error al obtener datos: {response.status_code}", 
                            color="danger", className="mt-3")
            return create_empty_graph(), alert
            
    except Exception as e:
        alert = dbc.Alert(f"Error: {str(e)}", color="danger", className="mt-3")
        return create_empty_graph(), alert


def handle_predecir_button(n_clicks, elemento_id, estacion_id, start_date, end_date, ventana_horas):
    """Handle the 'Predecir' button logic"""
    if n_clicks is None:
        return create_empty_graph(), ""
    
    if None in (elemento_id, estacion_id, start_date, end_date, ventana_horas):
        alerta = dbc.Alert("Completa todos los campos antes de predecir.", 
                           color="warning", className="mt-3")
        return create_empty_graph(), alerta
    
    try:
        # Your existing prediction logic here
        params = {
            'id_estacion': estacion_id,
            'id_elemento': elemento_id,
            'start_date': f"{start_date} 00:00:00",
            'end_date': f"{end_date} 23:59:59",
            'prediction_window': ventana_horas
        }
        
        resp = requests.get(f"{RAMA_URL}/mediciones/predict", 
                            params=params, timeout=600)
        
        if resp.status_code != 200:
            alerta = dbc.Alert(f"Error {resp.status_code} al predecir.", 
                               color="danger", className="mt-3")
            return create_empty_graph(), alerta
        
        data = resp.json()
        
        # Create DataFrames and plot (your existing logic)
        hist_df = pd.DataFrame(data['historical_data'])
        hist_df['timestamp'] = pd.to_datetime(hist_df['timestamp'])
        
        pred_df = pd.DataFrame(data['predictions'])
        pred_df['timestamp'] = pd.to_datetime(pred_df['timestamp'])
        
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=hist_df['timestamp'], 
            y=hist_df['actual_value'],
            mode='lines', 
            name='Histórico',
            line=dict(color='#2E86AB', width=2),
            hovertemplate='<b>Fecha:</b> %{x}<br><b>Histórico:</b> %{y}<extra></extra>'
        ))
        
        # Predictions
        fig.add_trace(go.Scatter(
            x=pred_df['timestamp'], 
            y=pred_df['predicted_value'],
            mode='lines', 
            name='Predicción',
            line=dict(color='#e53935', width=2, dash='dash'),
            hovertemplate='<b>Fecha:</b> %{x}<br><b>Predicción:</b> %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Histórico + Predicción LSTM",
            xaxis_title='Fecha y Hora',
            yaxis_title='Medición',
            template='plotly_dark',
            height=500,
            showlegend=True,
            hovermode='x unified'
        )
        
        alerta = dbc.Alert(
            f"Predicción generada: {len(pred_df)} puntos con ventana de {ventana_horas} horas.",
            color="success", className="mt-3"
        )
        return fig, alerta
        
    except Exception as e:
        alerta = dbc.Alert(f"Error: {e}", color="danger", className="mt-3")
        return create_empty_graph(), alerta