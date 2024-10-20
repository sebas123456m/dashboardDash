# -*- coding: utf-8 -*-
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Cargar los datos
url = "https://raw.githubusercontent.com/sebas123456m/dashboardDash/87adf606c7a615fcc002e99b8ffc0200297b490e/Encuesta%20Sobre%20Celular%20Xiomi%20Redmi%20(1-22)%20(1).xlsx"
encuesta = pd.read_excel(url)

# Procesar los datos
encuesta.columns = encuesta.columns.str.strip()
encuesta = encuesta.rename(columns={
    'Favor indicanos tu nombre': 'Nombre',
    '¿Cuentanos a qué te dedicas?': 'Ocupación',
    '¿Cuál es tu rango de edad?': 'Rango de Edad',
    '¿Cuál es tu género?': 'Género',
    '¿Tienes un celular Xiaomi Redmi  o has tenido experiencia con él?': 'Experiencia con Xiaomi',
    'En general, ¿cómo evaluaría su calidad?': 'Calidad',
    'En general, ¿cómo puntuaría la relación calidad-precio de este producto?': 'Calidad-Precio',
    'En comparación con otros productos de la competencia que ya estén en el mercado, diría que este producto es...': 'Innovación',
    '¿Cuál es la probabilidad de que recomiende este nuevo producto a amigos, compañeros de trabajo o familiares?': 'Probabilidad de Recomendación',
    '¿Qué es lo que más le gusta de este producto?': 'Aspecto Favorito',
    '¿Qué es lo que menos le gusta de este producto?': 'Aspecto Menos Favorito',
    'A continuación, te presento las características de dos celulares del mercado: uno corresponde a la marca Redmi y otro a Huawei ¿Cuál de ellos elegirías comprar? sin conocer su precio\n\n': 'Preferencia Sin Precio',
    'A continuación, te presento las características de dos celulares del mercado: uno corresponde a la marca Redmi y otro a Huawei con su precio actual  ¿Cuál de ellos elegirías comprar?': 'Preferencia Con Precio'
})

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Layout del dashboard
app.layout = html.Div([
    html.H1("Dashboard de Encuesta Xiaomi", style={'text-align': 'center'}),
    
    dcc.Slider(
        id='edad-slider',
        min=0,
        max=len(encuesta['Rango de Edad'].unique()) - 1,
        step=1,
        marks={i: rango for i, rango in enumerate(encuesta['Rango de Edad'].unique())},
        value=0,
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    
    dcc.Graph(id='calidad-graph'),
    dcc.Graph(id='calidad-precio-graph'),
    dcc.Graph(id='innovacion-graph'),

    html.Br(),

    dcc.Dropdown(
        id='ocupacion-dropdown',
        options=[{'label': ocupacion, 'value': ocupacion} for ocupacion in encuesta['Ocupación'].unique()],
        value=encuesta['Ocupación'].unique()[0],
        multi=False,
        style={"width": "50%"}
    ),
    dcc.Graph(id='ocupacion-calidad-graph')
])

# Callbacks para actualizar los gráficos
@app.callback(
    [Output('calidad-graph', 'figure'),
     Output('calidad-precio-graph', 'figure'),
     Output('innovacion-graph', 'figure')],
    [Input('edad-slider', 'value')]
)
def update_graphs(edad_value):
    rango_edad_seleccionado = encuesta['Rango de Edad'].unique()[edad_value]
    data_filtrada = encuesta[encuesta['Rango de Edad'] == rango_edad_seleccionado]

    # Gráficos
    fig_calidad = px.pie(names=data_filtrada['Calidad'].value_counts().index,
                          values=data_filtrada['Calidad'].value_counts(),
                          title="Evaluación de la Calidad")

    fig_calidad_precio = px.bar(x=data_filtrada['Calidad-Precio'].value_counts().index,
                                 y=data_filtrada['Calidad-Precio'].value_counts(),
                                 title="Relación Calidad-Precio")

    fig_innovacion = px.pie(names=data_filtrada['Innovación'].value_counts().index,
                             values=data_filtrada['Innovación'].value_counts(),
                             title="Percepción de Innovación")

    return fig_calidad, fig_calidad_precio, fig_innovacion

@app.callback(
    Output('ocupacion-calidad-graph', 'figure'),
    [Input('ocupacion-dropdown', 'value')]
)
def update_ocupacion_graph(ocupacion_value):
    data_filtrada = encuesta[encuesta['Ocupación'] == ocupacion_value]
    calidad_counts = data_filtrada['Calidad'].value_counts()
    fig_ocupacion_calidad = px.bar(x=calidad_counts.index, y=calidad_counts,
                                    title=f"Evaluación de la Calidad para {ocupacion_value}")
    return fig_ocupacion_calidad

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=int(os.environ.get("PORT", 8050)), debug=True)
