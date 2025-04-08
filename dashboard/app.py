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
import io

app = dash.Dash(__name__)

# Upload file section
@app.callback(Output('output-datos', 'children'), Input('upload-data', 'contents'), State('upload-data', 'filename'))
def return_filename(contents, filename):
    if not contents:
        return "Sube un archivo csv. Aegurate que tenga headers.\nPara llenar todos los campos se necesitan las etiquetas timestamp, latitude y longituude"
    return filename

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

    pipeline = DataProcessing(objects=content_list, is_object=True)
    pipeline.read_files()
    pipeline.process_data()
    df = pipeline.get_final_csv()


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
"""
# this section will display available data per days
@app.callback(
    Output('day-dropdown', 'options'),
    Input('stored-clean-csv', 'data')
)
def update_dropdown(data):
    if not data:
        return []
    df = pd.DataFrame(data)
    timestamp_col = find_timestamp(df.columns)
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    days = df[timestamp_col].dt.date.unique()
    return [{'label': str(day), 'value': str(day)} for day in days]
"""
@app.callback(
    Output('data-table', 'data'),
    Input('day-dropdown', 'value'),
    State('stored-clean-csv', 'data')
)
def update_table(selected_day, data):
    if not data or not selected_day:
        return []
    df = pd.DataFrame(data)
    timestamp_col = find_timestamp(df.columns)
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    df_filtered = df[df[timestamp_col].dt.date.astype(str) == selected_day]
    hourly_counts = df_filtered.groupby(df_filtered[timestamp_col].dt.hour).size().reset_index(name='Cantidad de registros')
    hourly_counts.rename(columns={timestamp_col: 'Hora'}, inplace=True)
    return hourly_counts.to_dict('records')


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
        return {}, [], [], [], [], [], []
    df =  pd.DataFrame(data)
    columns = df.columns
    null_data = df.isnull().sum()
    available_data = df.notnull().sum()
    
    fig = {
        'data': [
            {'x': list(columns), 'y': list(null_data), 'type': 'bar', 'name': 'Datos Nulos', 'marker': {'color': 'red'}},
            {'x': list(columns), 'y': list(available_data), 'type': 'bar', 'name': 'Datos Existentes', 'marker': {'color': 'blue'}}
        ],
        'layout': {
            'barmode': 'group',
            'title': "Datos Nulos vs Datos Existentes por Columna",
            'xaxis': {'title': 'Columnas'},
            'yaxis': {'title': 'Cantidad de Datos'}
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
    [Input('show-stats-button', 'n_clicks')],
    [State('stored-clean-csv', 'data'),
     State('numeric-columns-checklist', 'value')]
)
def mostrar_estadisticas(n_clicks, stored_data, selected_columns):
    if not n_clicks or stored_data is None or not selected_columns:
        return []
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
        return "Sube un archivo CSV para ver el mapa."
    
    df = pd.DataFrame(contents)
    
    # Buscar las columnas de latitud y longitud (considerando variantes)
    lon_col, lat_col = None, None
    temp = find_coordinates(df.columns)
    lon_col, lat_col = temp[0], temp[1]
    fig = None

    if not colors and not tags:
        fig = px.scatter_map(
            df,
            lat=lat_col,
            lon=lon_col,
            zoom=3,
            height=800,
            size_max=15
        )

    # Condición de 'colors' no vacío
    if colors and not tags:
        fig = px.scatter_map(
            df,
            lat=lat_col,
            lon=lon_col,
            color=colors,
            #size = colors,
            color_continuous_scale=px.colors.sequential.Bluered,
            zoom=3,
            size_max=10,
            height=800
        )

    if tags and not colors:
        fig = px.scatter_map(
                df,
                lat=lat_col,
                lon=lon_col,
                hover_data=tags,
                zoom=3,
                height=800,
                size_max=15
            )
    
    # Condición de 'tags' no vacío
    if tags and colors:
        fig = px.scatter_map(
            df,
            lat=lat_col,
            lon=lon_col,
            color=colors,
            #size = colors,
            color_continuous_scale=px.colors.sequential.Bluered,
            hover_data=tags,
            size_max=10,
            zoom=3,
            height=800
        )

    
    return dcc.Graph(figure=fig)

app.layout = create_layout()


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug=True, threaded=True)
