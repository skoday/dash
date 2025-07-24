from dash import html, dcc
from db_main.db_connection import SessionLocal
from db_main.db_operations import DBOperations
from env_config import settings
import base64
import io
import pandas as pd
from dash import Input, Output, State, callback, html
from dash.exceptions import PreventUpdate


DB = DBOperations(SessionLocal())
PASSWORD = settings.password


def return_layout():
    return html.Div([
        # Title section
        html.Div([
            html.H2(
                "Gestión de Datos de Sensores Móviles",
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
                "Carga y descarga archivos CSV de datos de sensores ambientales. Gestiona campañas de medición y accede a datos históricos.",
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
        
        # CSV Upload section
        html.Div([
            html.H3(
                "Cargar Datos CSV",
                style={
                    'text-align': 'center',
                    'color': '#f5f5f5',
                    'font-size': '18px',
                    'margin': '0 0 20px 0',
                    'text-transform': 'uppercase',
                    'letter-spacing': '1px'
                }
            ),
            
            html.Div([
                # CSV Upload component
                html.Div([
                    html.Label(
                        "Archivo CSV:",
                        style={
                            'color': '#f5f5f5',
                            'font-weight': 'bold',
                            'margin-bottom': '8px',
                            'display': 'block',
                            'font-size': '14px'
                        }
                    ),
                    dcc.Upload(
                        id='csv-upload',
                        children=html.Div([
                            'Arrastra o ',
                            html.A('selecciona un archivo', style={'color': '#1e88e5', 'text-decoration': 'underline'})
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '2px',
                            'borderStyle': 'dashed',
                            'borderColor': '#2c2c2c',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'background-color': '#1a1a1a',
                            'color': '#aaa',
                            'cursor': 'pointer',
                            'transition': 'border-color 0.3s ease'
                        },
                        multiple=False
                    )
                ], style={'flex': '1'}),
                
                # Campaign Name input
                html.Div([
                    html.Label(
                        "Nombre de Campaña:",
                        style={
                            'color': '#f5f5f5',
                            'font-weight': 'bold',
                            'margin-bottom': '8px',
                            'display': 'block',
                            'font-size': '14px'
                        }
                    ),
                    dcc.Input(
                        id='campaign-name-input',
                        type='text',
                        placeholder='ej: Centro_CDMX_Julio2025',
                        style={
                            'width': '100%',
                            'height': '40px',
                            'background-color': '#1a1a1a',
                            'border': '1px solid #2c2c2c',
                            'border-radius': '5px',
                            'color': '#f5f5f5',
                            'padding': '10px',
                            'font-size': '14px'
                        }
                    )
                ], style={'flex': '1'}),
                
                # Password input for upload
                html.Div([
                    html.Label(
                        "Contraseña:",
                        style={
                            'color': '#f5f5f5',
                            'font-weight': 'bold',
                            'margin-bottom': '8px',
                            'display': 'block',
                            'font-size': '14px'
                        }
                    ),
                    dcc.Input(
                        id='upload-password-input',
                        type='password',
                        placeholder='Ingresa la contraseña',
                        style={
                            'width': '100%',
                            'height': '40px',
                            'background-color': '#1a1a1a',
                            'border': '1px solid #2c2c2c',
                            'border-radius': '5px',
                            'color': '#f5f5f5',
                            'padding': '10px',
                            'font-size': '14px'
                        }
                    )
                ], style={'flex': '1'}),
                
                # Upload button
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
                        "Cargar a BD",
                        id="upload-button",
                        style={
                            'background-color': '#4caf50',
                            'color': 'white',
                            'border': 'none',
                            'padding': '10px 20px',
                            'border-radius': '5px',
                            'cursor': 'pointer',
                            'font-size': '16px',
                            'font-weight': 'bold',
                            'width': '100%',
                            'box-shadow': '0 2px 6px rgba(76, 175, 80, 0.3)',
                            'transition': 'background-color 0.3s ease'
                        }
                    )
                ], style={'flex': '1'})
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'gap': '20px',
                'align-items': 'end'
            }),
            
            # Space for additional text
            html.Div([
                html.Div(
                    id='additional-text-space',
                    children=[
                        html.P(
                            "Se espera que los archivos cargados se hayan unificado > pasado por el dashboard y descagado, y que tengan las siguientes columnas:" \
                            """columnas = [
                                "Timestamp", "Unix Time", "RTC Temp", "GPS UTC Time", "GPS Date", "GPS_Latitude",
                                "GPS_Longitude", "GPS Altitude", "GPS Satellites", "GPS HDOP", "GPS Speed (Knots)",
                                "GPS Speed (Km/h)", "GPS Track Degrees", "CycleID", "Hash", "SPS30 mc 1.0", "SPS30 mc 2.5",
                                "SPS30 mc 4.0", "SPS30 mc 10.0", "SPS30 nc 0.5", "SPS30 nc 1.0", "SPS30 nc 2.5",
                                "SPS30 nc 4.0", "SPS30 nc 10.0", "SPS30 Particle Size", "AHT20 Temperature", "AHT20 Humidity",
                                "BMP280 Temperature", "BMP280 Pressure","BMP280 Altitude", "co_level"
                            ]""",
                            style={
                                'color': '#666',
                                'font-style': 'italic',
                                'text-align': 'center',
                                'margin': '0',
                                'font-size': '12px'
                            }
                        )
                    ],
                    style={
                        'background-color': '#1a1a1a',
                        'border': '1px dashed #2c2c2c',
                        'border-radius': '5px',
                        'padding': '15px',
                        'margin-top': '15px'
                    }
                )
            ])
        ], style={
            'padding': '20px',
            'border': '1px solid #2c2c2c',
            'border-radius': '12px',
            'box-shadow': '0 0 12px rgba(0,0,0,0.3)',
            'background-color': '#1e1e1e',
            'margin': '10px 0'
        }),
        
        # CSV Download section
        html.Div([
            html.H3(
                "Descargar Datos por Campaña",
                style={
                    'text-align': 'center',
                    'color': '#f5f5f5',
                    'font-size': '18px',
                    'margin': '0 0 20px 0',
                    'text-transform': 'uppercase',
                    'letter-spacing': '1px'
                }
            ),
            
            html.Div([
                # Campaign dropdown
                html.Div([
                    html.Label(
                        "Seleccionar Campaña:",
                        style={
                            'color': '#f5f5f5',
                            'font-weight': 'bold',
                            'margin-bottom': '8px',
                            'display': 'block',
                            'font-size': '14px'
                        }
                    ),
                    dcc.Dropdown(
                        id='campaign-dropdown',
                        options=[],
                        placeholder="Cargando campañas...",
                        style={
                            'background-color': '#1a1a1a',
                            'border': '1px solid #2c2c2c',
                            'border-radius': '5px'
                        },
                        className='dark-dropdown'
                    )
                ], style={'flex': '2'}),
                
                # Password input for download
                html.Div([
                    html.Label(
                        "Contraseña:",
                        style={
                            'color': '#f5f5f5',
                            'font-weight': 'bold',
                            'margin-bottom': '8px',
                            'display': 'block',
                            'font-size': '14px'
                        }
                    ),
                    dcc.Input(
                        id='download-password-input',
                        type='password',
                        placeholder='Ingresa la contraseña',
                        style={
                            'width': '100%',
                            'height': '40px',
                            'background-color': '#1a1a1a',
                            'border': '1px solid #2c2c2c',
                            'border-radius': '5px',
                            'color': '#f5f5f5',
                            'padding': '10px',
                            'font-size': '14px'
                        }
                    )
                ], style={'flex': '1'}),
                
                # Refresh campaigns button
                html.Div([
                    html.Label(
                        "Actualizar:",
                        style={
                            'color': '#f5f5f5',
                            'font-weight': 'bold',
                            'margin-bottom': '8px',
                            'display': 'block',
                            'font-size': '14px'
                        }
                    ),
                    html.Button(
                        "Refrescar",
                        id="refresh-campaigns-button",
                        style={
                            'background-color': '#ff9800',
                            'color': 'white',
                            'border': 'none',
                            'padding': '10px 20px',
                            'border-radius': '5px',
                            'cursor': 'pointer',
                            'font-size': '16px',
                            'font-weight': 'bold',
                            'width': '100%',
                            'box-shadow': '0 2px 6px rgba(255, 152, 0, 0.3)'
                        }
                    )
                ], style={'flex': '1'}),
                
                # Download button
                html.Div([
                    html.Label(
                        "Descargar:",
                        style={
                            'color': '#f5f5f5',
                            'font-weight': 'bold',
                            'margin-bottom': '8px',
                            'display': 'block',
                            'font-size': '14px'
                        }
                    ),
                    html.Button(
                        "Descargar CSV",
                        id="download-button",
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
        
        # Status messages section
        html.Div([
            html.Div(id="upload-status-alert"),
            html.Div(id="download-status-alert")
        ], style={
            'margin': '10px 0'
        }),
        
        # Hidden divs for data storage and downloads
        html.Div(id="csv-data-store", style={'display': 'none'}),
        html.Div(id="trigger-campaigns-load", style={'display': 'none'}),
        dcc.Download(id="download-csv-file")
    ])



@callback(
    Output('campaign-dropdown', 'options'),
    Output('trigger-campaigns-load', 'children'),
    Input('trigger-campaigns-load', 'children'),
    Input('refresh-campaigns-button', 'n_clicks')
)
def load_campaigns(trigger, refresh_clicks):
    """Load all available campaigns into dropdown"""
    try:
        session = SessionLocal()
        db_ops = DBOperations(session)
        
        campaigns = db_ops.get_all_campaigns()
        session.close()
        
        options = [{'label': campaign, 'value': campaign} for campaign in campaigns]
        
        if not options:
            options = [{'label': 'No hay campañas disponibles', 'value': '', 'disabled': True}]
            
        return options, "loaded"
        
    except Exception as e:
        return [{'label': f'Error cargando campañas: {str(e)}', 'value': '', 'disabled': True}], "error"


# Callback for CSV upload and database insertion
@callback(
    Output('upload-status-alert', 'children'),
    Input('upload-button', 'n_clicks'),
    State('csv-upload', 'contents'),
    State('csv-upload', 'filename'),
    State('campaign-name-input', 'value'),
    State('upload-password-input', 'value')
)
def upload_csv_to_database(n_clicks, contents, filename, campaign_name, password):
    """Handle CSV upload with password validation"""
    if not n_clicks:
        raise PreventUpdate
    
    # Validation checks
    if not password:
        return html.Div([
            html.Div("❌ Debes ingresar la contraseña", 
                    style={'color': '#f44336', 'padding': '10px', 'background-color': '#1a1a1a', 
                           'border': '1px solid #f44336', 'border-radius': '5px', 'margin': '5px 0'})
        ])
    
    if password != PASSWORD:
        return html.Div([
            html.Div("❌ Contraseña incorrecta", 
                    style={'color': '#f44336', 'padding': '10px', 'background-color': '#1a1a1a', 
                           'border': '1px solid #f44336', 'border-radius': '5px', 'margin': '5px 0'})
        ])
    
    if not contents:
        return html.Div([
            html.Div("❌ Debes seleccionar un archivo CSV", 
                    style={'color': '#f44336', 'padding': '10px', 'background-color': '#1a1a1a', 
                           'border': '1px solid #f44336', 'border-radius': '5px', 'margin': '5px 0'})
        ])
    
    if not campaign_name:
        return html.Div([
            html.Div("❌ Debes ingresar un nombre de campaña", 
                    style={'color': '#f44336', 'padding': '10px', 'background-color': '#1a1a1a', 
                           'border': '1px solid #f44336', 'border-radius': '5px', 'margin': '5px 0'})
        ])
    
    try:
        # Parse uploaded CSV
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Read CSV into DataFrame
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        # Insert into database
        session = SessionLocal()
        db_ops = DBOperations(session)
        
        result = db_ops.insert_df_to_db(df, campaign_name)
        session.close()
        
        return html.Div([
            html.Div(f"✅ {result}", 
                    style={'color': '#4caf50', 'padding': '10px', 'background-color': '#1a1a1a', 
                           'border': '1px solid #4caf50', 'border-radius': '5px', 'margin': '5px 0'})
        ])
        
    except Exception as e:
        return html.Div([
            html.Div(f"❌ Error procesando archivo: {str(e)}", 
                    style={'color': '#f44336', 'padding': '10px', 'background-color': '#1a1a1a', 
                           'border': '1px solid #f44336', 'border-radius': '5px', 'margin': '5px 0'})
        ])


# Callback for CSV download with password verification
@callback(
    Output('download-csv-file', 'data'),
    Output('download-status-alert', 'children'),
    Input('download-button', 'n_clicks'),
    State('campaign-dropdown', 'value'),
    State('download-password-input', 'value')
)
def download_campaign_csv(n_clicks, selected_campaign, password):
    """Download selected campaign data as CSV with password verification"""
    if not n_clicks:
        raise PreventUpdate
    
    # Password validation for downloads
    if not password:
        return None, html.Div([
            html.Div("❌ Debes ingresar la contraseña para descargar", 
                    style={'color': '#f44336', 'padding': '10px', 'background-color': '#1a1a1a', 
                           'border': '1px solid #f44336', 'border-radius': '5px', 'margin': '5px 0'})
        ])
    
    if password != PASSWORD:
        return None, html.Div([
            html.Div("❌ Contraseña incorrecta", 
                    style={'color': '#f44336', 'padding': '10px', 'background-color': '#1a1a1a', 
                           'border': '1px solid #f44336', 'border-radius': '5px', 'margin': '5px 0'})
        ])
    
    if not selected_campaign:
        return None, html.Div([
            html.Div("❌ Debes seleccionar una campaña", 
                    style={'color': '#f44336', 'padding': '10px', 'background-color': '#1a1a1a', 
                           'border': '1px solid #f44336', 'border-radius': '5px', 'margin': '5px 0'})
        ])
    
    try:
        # Get data from database
        session = SessionLocal()
        db_ops = DBOperations(session)
        
        df = db_ops.get_data_by_campaign(selected_campaign)
        session.close()
        
        if df.empty:
            return None, html.Div([
                html.Div(f"❌ No hay datos para la campaña '{selected_campaign}'", 
                        style={'color': '#f44336', 'padding': '10px', 'background-color': '#1a1a1a', 
                               'border': '1px solid #f44336', 'border-radius': '5px', 'margin': '5px 0'})
            ])
        
        # Prepare download
        filename = f"{selected_campaign}_datos.csv"
        
        success_message = html.Div([
            html.Div(f"✅ Descargando {len(df)} registros de '{selected_campaign}'", 
                    style={'color': '#4caf50', 'padding': '10px', 'background-color': '#1a1a1a', 
                           'border': '1px solid #4caf50', 'border-radius': '5px', 'margin': '5px 0'})
        ])
        
        return {
            'content': df.to_csv(index=False),
            'filename': filename,
            'type': 'text/csv'
        }, success_message
        
    except Exception as e:
        return None, html.Div([
            html.Div(f"❌ Error descargando datos: {str(e)}", 
                    style={'color': '#f44336', 'padding': '10px', 'background-color': '#1a1a1a', 
                           'border': '1px solid #f44336', 'border-radius': '5px', 'margin': '5px 0'})
        ])


# Callback to clear password fields after successful operations
@callback(
    Output('upload-password-input', 'value'),
    Output('download-password-input', 'value'),
    Input('upload-status-alert', 'children'),
    Input('download-status-alert', 'children'),
    State('upload-password-input', 'value'),
    State('download-password-input', 'value')
)
def clear_passwords_on_success(upload_status, download_status, upload_password, download_password):
    """Clear password fields after successful operations for security"""
    upload_clear = ""
    download_clear = ""
    
    # Clear upload password on success
    if upload_status and upload_password:
        if hasattr(upload_status, 'children') and any('✅' in str(child) for child in upload_status['children']):
            upload_clear = ""
        else:
            upload_clear = upload_password
    
    # Clear download password on success
    if download_status and download_password:
        if hasattr(download_status, 'children') and any('✅' in str(child) for child in download_status['children']):
            download_clear = ""
        else:
            download_clear = download_password
    
    return upload_clear, download_clear


# Callback to update campaign dropdown after successful upload
@callback(
    Output('campaign-dropdown', 'options', allow_duplicate=True),
    Input('upload-status-alert', 'children'),
    prevent_initial_call=True
)
def refresh_campaigns_after_upload(status_alert):
    """Refresh campaign list after successful upload"""
    if status_alert:
        # Check if upload was successful
        if hasattr(status_alert, 'children') and any('✅' in str(child) for child in status_alert['children']):
            try:
                session = SessionLocal()
                db_ops = DBOperations(session)
                campaigns = db_ops.get_all_campaigns()
                session.close()
                
                return [{'label': campaign, 'value': campaign} for campaign in campaigns]
            except:
                pass
    raise PreventUpdate
