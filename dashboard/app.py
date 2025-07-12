import dash
from dash.dependencies import Input, Output, State
from layout import create_layout
from utils.process_file import process_file, find_timestamp, fix_timestamp, find_coordinates, remove_useless_gps_coordinates
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import plotly.express as px
from dash import dcc
from  utils.data_processing import DataProcessing
from dash import html
import io
from multiprocessing import Pool, cpu_count
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = dash.Dash(__name__, use_pages=True, pages_folder="")

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

# Upload file section
@app.callback(Output('output-datos', 'children'), Input('upload-data', 'contents'), State('upload-data', 'filename'))
def return_filename(contents, filename):
    if not contents:
        return "Sube un archivo csv. Aegurate que tenga headers.\nPara llenar todos los campos se necesitan las etiquetas timestamp, latitude y longituude"
    return filename

def helper(content_list):
    print("tipo: ", type(content_list))
    pipeline = DataProcessing(objects=[content_list], is_object=True)
    pipeline.read_files()
    pipeline.process_data()
    return pipeline.get_final_csv()
    

# THis part will format timestamp if it exists
@app.callback([Output('stored-clean-csv', 'data'),
               Output('gps-datapoints', 'data')], Input('upload-data', 'contents'))
def format_data(contents_list):
    if not contents_list:
        return [], []
    
    content_list = []

    for contents in contents_list:
        _, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        decoded = io.StringIO(decoded.decode('latin1'))
        content_list.append(decoded)
    print("tipogeneral: ", type(content_list), " type elements: ", type(content_list[0]))
    with Pool(cpu_count()) as pool:
        df_list = pool.map(helper, content_list)
    
    # Combine all the dataframes
    df = pd.concat(df_list, ignore_index=True)
    
    # Assuming find_coordinates is a function you've defined elsewhere
    # If not, you'll need to adapt this part
    coordinates = find_coordinates(df.columns)
    if coordinates:
        temp = df.dropna(subset=[coordinates[0], coordinates[1]])
        return df.to_dict('records'), temp.to_dict('records')

    return df.to_dict('records'), dash.no_update

# Show day with available data
@app.callback([Output('tabla-dias', 'data'),
               Output('day-dropdown', 'options')], 
              Input('stored-clean-csv', 'data'), 
              prevent_initial_call=True)
def days_table(contents):
    if not contents:
        return [{"Día": "No se encontró timestamp"}], []
    df =  pd.DataFrame(contents)
    timestamp_col = find_timestamp(df.columns)
    if timestamp_col:
        df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')
    if timestamp_col:
        df['Date'] = pd.to_datetime(df[timestamp_col]).dt.date
        dias = [{'Día': str(dia)} for dia in df['Date'].unique()]

        #drop down menu
        days = df[timestamp_col].dt.date.unique()


        return dias, [{'label': str(day), 'value': str(day)} for day in days]
    return [{"Día": "No se encontró timestamp"}], []


@app.callback(
    Output("hourly-graph", 'figure'),
    Input('day-dropdown', 'value'),
    State('stored-clean-csv', 'data')
)
def update_graph(selected_day, data):
    if not data or not selected_day:
        return create_empty_graph()

    df = pd.DataFrame(data)
    timestamp_col = find_timestamp(df.columns)
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])

    df_filtered = df[df[timestamp_col].dt.date.astype(str) == selected_day]
    hourly_counts = df_filtered.groupby(df_filtered[timestamp_col].dt.hour).size().reset_index(
        name='Cantidad de registros')
    hourly_counts.rename(columns={timestamp_col: 'Hora'}, inplace=True)

    # Crear el gráfico con tema oscuro
    fig = px.bar(
        hourly_counts,
        x='Hora',
        y='Cantidad de registros',
        labels={'Hora': 'Hora del día', 'Cantidad de registros': 'Cantidad'},
        template='plotly_dark'  # Usamos el tema oscuro
    )

    # Actualizamos el diseño del gráfico para que se vea bien en el modo oscuro
    fig.update_layout(
        margin=dict(t=40, b=20, l=10, r=10),
        plot_bgcolor='#2b2b2b',  # Fondo oscuro para el gráfico
        paper_bgcolor='#1e1e1e',  # Fondo oscuro para el área del gráfico
        font=dict(color='#f5f5f5'),  # Texto blanco
        xaxis=dict(tickangle=45, tickcolor='#f5f5f5'),  # Ticks y ejes en color blanco
        yaxis=dict(tickcolor='#f5f5f5'),  # Ticks del eje Y en color blanco
        title=dict(font=dict(color='#f5f5f5'))  # Título blanco
    )

    return fig



@app.callback([Output('grafico-columnas', 'figure'),
               Output('tabla-columnas', 'data'),
               Output('tabla-tipos-dato', 'data'),
               Output('numeric-columns-checklist', 'options'),
               Output('numeric-columns-checklist-corr', 'options'),
               Output('color-schemna', 'options'),
               Output('tags-in-map', 'options')],
               Input('stored-clean-csv', 'data'),
               prevent_initial_call=True)
def day_graph_existing_values_data_type(data):
    if not data:
        return create_empty_graph(), [], [], [], [], [], []
    df =  pd.DataFrame(data)
    columns = df.columns
    null_data = df.isnull().sum()
    available_data = df.notnull().sum()
    
    fig = {
        'data': [
            {
                'x': list(columns),
                'y': list(null_data),
                'type': 'bar',
                'name': 'Datos Nulos',
                'marker': {'color': 'red'}
            },
            {
                'x': list(columns),
                'y': list(available_data),
                'type': 'bar',
                'name': 'Datos Existentes',
                'marker': {'color': 'blue'}
            }
        ],
        'layout': {
            'barmode': 'group',
            'title': "Datos Nulos vs Datos Existentes por Columna",
            'xaxis': {'title': 'Columnas'},
            'yaxis': {'title': 'Cantidad de Datos'},
            'plot_bgcolor': '#1e1e1e',
            'paper_bgcolor': '#1e1e1e',
            'font': {'color': '#f5f5f5'}
        }
    }

    
    table = [{'Columna': col, 'Datos Nulos': null_data[col], 'Datos Existentes': available_data[col]} for col in columns]

    data_type_table = [{'Columna': col, 'Tipo de Dato': str(df[col].dtype)} for col in columns]

    numeric_cols = df.select_dtypes(include=['number']).columns
    checklist_options = [{'label': col, 'value': col} for col in numeric_cols]
    
    timestamp_col = find_timestamp(df.columns)
    if timestamp_col:
        tags_options = checklist_options.copy()
        temp = {
                    "label": timestamp_col,
                    "value": timestamp_col
                }
        tags_options.append(temp)
        return fig, table, data_type_table, checklist_options, checklist_options, checklist_options, tags_options

    return fig, table, data_type_table, checklist_options, checklist_options, checklist_options, checklist_options

@app.callback(
    Output('tabla-estadisticas', 'data'),
    [Input('show-stats-button', 'n_clicks'),
     Input('stored-clean-csv', 'data')],
    [State('stored-clean-csv', 'data'),
     State('numeric-columns-checklist', 'value')]
)
def mostrar_estadisticas(n_clicks,stored_data1, stored_data, selected_columns):
    if not stored_data1:
        return []
    if stored_data1 and not selected_columns:
        df = pd.DataFrame(stored_data)
        columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
        columnas_filtradas = [
            col for col in columnas_numericas
            if not any(substring in col.lower() for substring in ["lat", "lon", "time"])
            ]
        stats = df[columnas_filtradas].describe().transpose()
        tabla_estadisticas = [{
            'Columna': index,
            'No de registros': stats.loc[index, 'count'],
            'Promedio': stats.loc[index, 'mean'],
            'Desviación Estándar': stats.loc[index, 'std'],
            'Mínimo': stats.loc[index, 'min'],
            '25%': stats.loc[index, '25%'],
            'Mediana (50%)': stats.loc[index, '50%'],
            '75%': stats.loc[index, '75%'],
            'Máximo': stats.loc[index, 'max']
        } for index in stats.index]
        return tabla_estadisticas
    else:
        df = pd.DataFrame(stored_data)
        stats = df[selected_columns].describe().transpose()
        tabla_estadisticas = [{
            'Columna': index,
            'No de registros': stats.loc[index, 'count'],
            'Promedio': stats.loc[index, 'mean'],
            'Desviación Estándar': stats.loc[index, 'std'],
            'Mínimo': stats.loc[index, 'min'],
            '25%': stats.loc[index, '25%'],
            'Mediana (50%)': stats.loc[index, '50%'],
            '75%': stats.loc[index, '75%'],
            'Máximo': stats.loc[index, 'max']
        } for index in stats.index]
        return tabla_estadisticas

def generate_correlation_matrix(df):
    """Genera una imagen de la matriz de correlación y devuelve la URL en base64"""
    df_numerico = df.select_dtypes(include=['number'])
    matriz_correlacion = df_numerico.corr()
    plt.figure(figsize=(15, 15))
    sns.heatmap(matriz_correlacion, annot=True, cmap='RdBu', center=0, fmt='.2f', linewidths=0.5)
    plt.title('Matriz de Correlación de datos numéricos')
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()  # Cierra la figura para liberar memoria
    img.seek(0)
    img_str = base64.b64encode(img.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"

@app.callback(
    Output('matriz-correlacion', 'src'),
    [Input('show-corr-button', 'n_clicks')],
    [State('stored-clean-csv', 'data'),
     State('numeric-columns-checklist-corr', 'value')]
)
def update_correlation_matrix(n_clicks, stored_data, selected_columns):
    if not n_clicks or stored_data is None or not selected_columns:
        return ''
    df = pd.DataFrame(stored_data)
    df_subset = df[selected_columns]
    img_url = generate_correlation_matrix(df_subset)
    return img_url

@app.callback(Output('map-image', 'children'),
              [Input('gps-datapoints', 'data'),
               Input('map-filter-button', 'n_clicks')],
               [State('color-schemna', 'value'),
                State('tags-in-map', 'value')]
               )
def update_map(contents, n_clicks, colors, tags):
    if not contents:
        return html.Div(
            "Sube un archivo CSV para ver el mapa.",
            style={
                'text-align': 'center',
                'color': '#ccc',
                'font-size': '16px',
                'padding': '20px',
                'background-color': '#333',
                'border-radius': '10px',
                'box-shadow': '2px 2px 10px rgba(0,0,0,0.3)',
            }
        )
    
    df = pd.DataFrame(contents)
    
    # Buscar las columnas de latitud y longitud (considerando variantes)
    lon_col, lat_col = None, None
    temp = find_coordinates(df.columns)
    lon_col, lat_col = temp[0], temp[1]
    fig = None

    # Generación de gráficos según condiciones
    if not colors and not tags:
        fig = px.scatter_map(
            df,
            lat=lat_col,
            lon=lon_col,
            zoom=3,
            height=800,
            size_max=15,
            map_style='streets'
        )

    # Condición de 'colors' no vacío
    if colors and not tags:
        fig = px.scatter_map(
            df,
            lat=lat_col,
            lon=lon_col,
            color=colors,
            color_continuous_scale=px.colors.sequential.Bluered,
            zoom=3,
            size_max=10,
            height=800,
            map_style='streets'
        )

    if tags and not colors:
        fig = px.scatter_map(
                df,
                lat=lat_col,
                lon=lon_col,
                hover_data=tags,
                zoom=3,
                height=800,
                size_max=15,
                map_style='streets'
            )
    
    # Condición de 'tags' y 'colors' no vacío
    if tags and colors:
        fig = px.scatter_map(
            df,
            lat=lat_col,
            lon=lon_col,
            color=colors,
            color_continuous_scale=px.colors.sequential.Bluered,
            hover_data=tags,
            size_max=10,
            zoom=3,
            height=800,
            map_style='streets'
        )

    # Aquí agregamos estilos para el gráfico
    fig.update_layout(
        plot_bgcolor="#121212",  # Fondo oscuro
        paper_bgcolor="#121212",  # Fondo de la zona del gráfico
        font=dict(color="#f5f5f5"),  # Texto en blanco
        geo=dict(bgcolor="#121212", lakecolor="#121212"),  # Fondo del mapa en oscuro
        margin=dict(l=10, r=10, t=10, b=10),  # Márgenes pequeños para no perder espacio
    )
    return dcc.Graph(
        figure=fig,
        style={
            'border-radius': '10px',
            'box-shadow': '2px 2px 10px rgba(0,0,0,0.3)',  # Sombra discreta para mantenerlo elegante
            'height': '800px',  # Altura para que no quede comprimido
            'background-color': '#1e1e1e',  # Fondo suave oscuro
        }
    )


@app.callback(
    Output('download-data', 'data'),
    Input('download-btn', 'n_clicks'),
    State('stored-clean-csv', 'data')
)
def trigger_download(n_clicks, data):
    if not data:
        return dash.no_update
    df = pd.DataFrame(data)
    
    return dcc.send_data_frame(df.to_csv, filename="mis_datos.csv", index=False)

@app.callback(
        Output('timeseries-dropdown', 'options'),
        Input('stored-clean-csv', 'data')
    )
def fill_dropdown_options(data):
    if not data:
        return []
    df = pd.DataFrame(data)
    columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    columnas_filtradas = [
            col for col in columnas_numericas
            if not any(substring in col.lower() for substring in ["lat", "lon", "time"])
            ]
    return [{'label': col, 'value': col} for col in columnas_filtradas]

@app.callback(
    Output('timeseries-plot', 'figure'),
    Input('timeseries-dropdown', 'value'),
    State('stored-clean-csv', 'data')
)
def update_plot(selected_column, data):
    if not selected_column or not data:
        return create_empty_graph()

    df = pd.DataFrame(data)

    # Buscar timestamp si existe
    timestamp_col = find_timestamp(df.columns)
    if timestamp_col:
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
        x = df[timestamp_col]
    else:
        x = df.index

    # Crear figura
    fig = px.scatter(
        df, x=x, y=selected_column,
        labels={'x': 'Tiempo', selected_column: 'Valor'},
        title=f'Serie de tiempo: {selected_column}'
    )

    # Estilo del gráfico
    fig.update_traces(marker=dict(color="#007bff", size=7))  # Ajustar tamaño de los puntos
    fig.update_layout(
        margin={"l": 40, "r": 20, "t": 40, "b": 40},  # Ajustar márgenes
        plot_bgcolor="#1e1e1e",  # Fondo oscuro
        paper_bgcolor="#1e1e1e",  # Fondo del papel oscuro
        font=dict(family="Segoe UI, sans-serif", color="#f5f5f5"),  # Fuente blanca y legible
        title_font=dict(family="Segoe UI, sans-serif", size=18, color="#f5f5f5"),  # Título en blanco
        xaxis=dict(
            title="Tiempo",
            showgrid=True,  # Mostrar las líneas de la cuadrícula
            gridcolor="#444",  # Color gris oscuro de la cuadrícula
            zeroline=False  # No mostrar la línea en cero
        ),
        yaxis=dict(
            title="Valor",
            showgrid=True,  # Mostrar las líneas de la cuadrícula
            gridcolor="#444",  # Color gris oscuro de la cuadrícula
            zeroline=False  # No mostrar la línea en cero
        ),
    )
    return fig


#app.layout = create_layout()

# Callback 1: llenar dropdown con columnas numéricas
@app.callback(
    Output('decade-column-dropdown', 'options'),
    Input('stored-clean-csv', 'data')
)
def update_numeric_column_options(data):
    if not data:
        return []
    df = pd.DataFrame(data)
    numeric_columns = df.select_dtypes(include='number').columns
    return [{'label': col, 'value': col} for col in numeric_columns]

# Callback 2: graficar distribución por decenas
@app.callback(
    Output('decade-distribution-graph', 'figure'),
    Input('decade-column-dropdown', 'value'),
    State('stored-clean-csv', 'data')
)
def update_distribution_visualization(selected_column, data):
    if not data or not selected_column:
        return create_empty_graph()

    df = pd.DataFrame(data)
    df = df[[selected_column]].dropna()
    
    # Convertimos a numérico
    df[selected_column] = pd.to_numeric(df[selected_column], errors='coerce')
    df = df.dropna()
    
    # Calculamos estadísticas básicas para determinar rangos apropiados
    min_val = df[selected_column].min()
    max_val = df[selected_column].max()
    
    # Elegir número de bins apropiado basado en la regla de Sturges
    n_bins = int(np.ceil(np.log2(len(df))) + 1)
    
    # Crear histograma con bins adaptados y mejor visualización
    fig = px.histogram(
        df, 
        x=selected_column,
        nbins=n_bins,  # Bins adaptados a los datos
        labels={selected_column: 'Valor', 'count': 'Frecuencia'},
        template='plotly_dark',
        marginal='box',  # Añade un box plot en el margen para ver la distribución
        opacity=0.7,
        color_discrete_sequence=['#2EA5D1']  # Color más atractivo
    )
    
    # Mejoramos la presentación
    fig.update_layout(
        margin=dict(t=50, b=30, l=40, r=40),
        title=f"Distribución de {selected_column}",
        xaxis_title=f"Valores de {selected_column}",
        yaxis_title="Frecuencia",
        bargap=0.1  # Espacio entre barras
    )
    
    # Añadimos líneas para valor medio y mediana
    mean_val = df[selected_column].mean()
    median_val = df[selected_column].median()
    
    fig.add_shape(
        type="line", line=dict(dash="dash", color="#FF4B4B", width=2),
        x0=mean_val, x1=mean_val, y0=0, y1=1, 
        yref="paper"
    )
    fig.add_shape(
        type="line", line=dict(dash="solid", color="#FFD700", width=2),
        x0=median_val, x1=median_val, y0=0, y1=1, 
        yref="paper"
    )
    
    # Añadimos anotaciones para explicar las líneas
    fig.add_annotation(
        x=mean_val, y=0.98, yref="paper",
        text=f"Media: {mean_val:.2f}",
        showarrow=True, arrowhead=1, ax=60, ay=-30,
        font=dict(color="#FF4B4B")
    )
    fig.add_annotation(
        x=median_val, y=0.90, yref="paper",
        text=f"Mediana: {median_val:.2f}",
        showarrow=True, arrowhead=1, ax=-60, ay=-30,
        font=dict(color="#FFD700")
    )
    
    return fig

final_layout = html.Div(
                        children=[
                            create_layout(),
                            html.Div(
                                [
                                    # tus secciones y componentes aquí
                                ]
                            )
                        ],
                        style={
                            'backgroundColor': '#121212',
                            'minHeight': '100vh',
                            'padding': '0',
                            'margin': '0',
                            'color': '#f5f5f5',
                            'font-family': 'Segoe UI, sans-serif'
                        }
                    )

dash.register_page("main_dashboard",
                   path='/',
                   layout=final_layout)
from layoutsecondview import integration_layout

dash.register_page("forecast",
                   path='/forecast',
                   layout=integration_layout)

from layout_db import return_layout
dash.register_page("Dashboard db operations",
                   path='/db',
                   layout=return_layout())



app.layout = html.Div([
    dash.page_container
])



if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug=False, threaded=True)
