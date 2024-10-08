# -*- coding: utf-8 -*-
"""programacion ciencia de datos.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vpUSTNJ-JBEMDmb_YPWoABF0XddmFF-s
"""
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from base64 import b64encode
import plotly.graph_objects as go
import io
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
df = pd.read_csv("https://raw.githubusercontent.com/sebas123456m/dashboardDash/d0d727180942145d1c167626c5930abb957199ac/adult.csv", sep=",")  
df = df.rename(columns={'marital.status': 'marital_status'})
min_age = df['age'].min()
max_age = df['age'].max()
dropdown_sex = dcc.Dropdown(
    id="dropdown",
    options=[
        {'label': 'Ambos', 'value': 'Both'},
        {'label': 'Female', 'value': 'Female'},
        {'label': 'Male', 'value': 'Male'}
    ],
    value="Both",
    clearable=False,
    style={'fontSize': '16px', 'width': '100%'}
)
age_slider = dcc.RangeSlider(
    id='age_slider',
    min=min_age,
    max=max_age,
    value=[min_age, max_age],
    marks={str(age): str(age) for age in range(min_age, max_age + 1, 5)},
    step=1,
    tooltip={"placement": "bottom", "always_visible": True}
)
app.layout = dbc.Container(
    [
        html.H2("Análisis de Datos de Ingresos Por genero", style={'textAlign': 'center', 'color': '#003366'}),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col([
                    html.Label("Selecciona el Sexo:", style={'fontSize': '18px'}),
                    dropdown_sex,
                    html.Label("Rango de Edad:", style={'fontSize': '18px'}),
                    age_slider,
                ], md=4, sm=12, className="mb-4"),
            ],
            justify="center"
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="income_graph"), md=6, sm=12),
                dbc.Col(dcc.Graph(id="education_graph"), md=6, sm=12),
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="marital_status"), md=6, sm=12),
                dbc.Col(dcc.Graph(id="relationship_bubble_chart"), md=6, sm=12),
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graficoRaza"), md=6, sm=12),
                dbc.Col(dcc.Graph(id="graficoOcupacion"), md=6, sm=12),
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="graficoWorkClass",
                        style={'height': '70vh', 'width': '100%'}
                    ),
                    md=6, sm=12,
                    className="mx-auto"
                ),
            ],
            justify="center"
        )
    ],
    fluid=True,
    style={'backgroundColor': '#f8f9fa'}
)
@app.callback(
    Output("income_graph", "figure"),
    Input("dropdown", "value"),
    Input("age_slider", "value"),
)
def update_income_bar_chart(selected_sex, age_range):
    if selected_sex == "Both":
        dff = df
    else:
        dff = df[df['sex'] == selected_sex]

    dff = dff[(dff['age'] >= age_range[0]) & (dff['age'] <= age_range[1])]
    dff_grouped = dff.groupby(['sex', 'income']).size().reset_index(name='count')
    fig = px.bar(dff_grouped,
                 x="sex",
                 y="count",
                 color="income",
                 text="count",
                 labels={"income": "Ingreso", "count": "Cantidad"},
                 title="Distribución de Ingresos por Sexo",
                 barmode='stack')
    fig.update_traces(texttemplate='%{text}', textposition='inside', hovertemplate='Sexo: %{x}<br>Ingreso: %{color}<br>Cantidad: %{y}')
    buffer = io.StringIO()
    fig.write_html(buffer)
    html_bytes = buffer.getvalue().encode()
    encoded = b64encode(html_bytes).decode()
    href = "data:text/html;base64," + encoded

    return fig
@app.callback(
    Output("education_graph", "figure"),
    Input("dropdown", "value"),
    Input("age_slider", "value"),
)
def update_education_bar_chart(selected_sex, age_range):
    if selected_sex == "Both":
        dff = df
    else:
        dff = df[df['sex'] == selected_sex]

    dff = dff[(dff['age'] >= age_range[0]) & (dff['age'] <= age_range[1])]
    dff_grouped = dff.groupby(['sex', 'education']).size().reset_index(name='count')
    fig = px.bar(dff_grouped,
                 x="sex",
                 y="count",
                 color="education",
                 text="count",
                 labels={"education": "Educación", "count": "Cantidad"},
                 title="Distribución de Educación por Sexo",
                 barmode='group')
    fig.update_traces(texttemplate='%{text}', textposition='inside', hovertemplate='Sexo: %{x}<br>Educación: %{color}<br>Cantidad: %{y}')

    return fig
@app.callback(
    Output("marital_status", "figure"),
    Input("dropdown", "value"),
    Input("age_slider", "value"),
)
def update_marital_status_bar_chart(selected_sex, age_range):
    if selected_sex == "Both":
        dff = df
    else:
        dff = df[df['sex'] == selected_sex]
    dff = dff[(dff['age'] >= age_range[0]) & (dff['age'] <= age_range[1])]

    dff_grouped = dff.groupby(['marital_status']).size().reset_index(name='count')
    fig = px.bar(dff_grouped,
                 x="count",
                 y="marital_status",
                 color="marital_status",
                 text="count",
                 labels={"marital_status": "Estado Civil", "count": "Cantidad"},
                 title="Distribución del Estado Civil",
                 orientation='h')
    fig.update_traces(texttemplate='%{text}', textposition='inside', hovertemplate='Estado Civil: %{y}<br>Cantidad: %{x}')

    return fig
@app.callback(
    Output("relationship_bubble_chart", "figure"),
    Input("dropdown", "value"),
    Input("age_slider", "value"),
)
def update_relationship_bubble_chart(selected_sex, age_range):
    if selected_sex == "Both":
        dff = df
    else:
        dff = df[df['sex'] == selected_sex]

    dff = dff[(dff['age'] >= age_range[0]) & (dff['age'] <= age_range[1])]
    dff_grouped = dff.groupby(['relationship', 'sex']).size().reset_index(name='count')
    fig = px.scatter(dff_grouped,
                     x='relationship',
                     y='count',
                     color='sex',
                     size='count',
                     hover_name='relationship',
                     labels={"relationship": "Relación", "count": "Cantidad"},
                     title="Distribución de Relaciones por Sexo")

    return fig
@app.callback(
    Output("graficoRaza", "figure"),
    Input("dropdown", "value"),
    Input("age_slider", "value"),
)
def update_race_pie_chart(selected_sex, age_range):
    if selected_sex == "Both":
        dff = df
    else:
        dff = df[df['sex'] == selected_sex]
    dff = dff[(dff['age'] >= age_range[0]) & (dff['age'] <= age_range[1])]
    dff_grouped = dff.groupby(['race']).size().reset_index(name='count')
    fig = px.pie(
        dff_grouped,
        names='race',
        values='count',
        labels={"race": "Raza", "count": "Cantidad"},
        title="Distribución de Razas",
        hole=0.4
    )
    fig.update_traces(hovertemplate='Raza: %{label}<br>Cantidad: %{value}<br>Porcentaje: %{percent}', textposition='inside')
    return fig

@app.callback(
    Output("graficoOcupacion", "figure"),
    Input("dropdown", "value"),
    Input("age_slider", "value"),
)
def update_occupation_bubble_chart(selected_sex, age_range):
    if selected_sex == "Both":
        dff = df
    else:
        dff = df[df['sex'] == selected_sex]

    dff = dff[(dff['age'] >= age_range[0]) & (dff['age'] <= age_range[1])]
    dff_grouped = dff.groupby(['occupation']).size().reset_index(name='count')
    fig = px.scatter(
        dff_grouped,
        x='occupation',
        y='count',
        size='count',
        color='occupation',
        labels={"occupation": "Ocupación", "count": "Cantidad"},
        title="Distribución de Ocupaciones",
        hover_name='occupation',
        size_max=60
    )

    fig.update_traces(textposition='top center', hovertemplate='Ocupación: %{x}<br>Cantidad: %{y}')
    fig.update_layout(
        xaxis_title="Ocupación",
        yaxis_title="Cantidad",
        showlegend=False
    )

    return fig

@app.callback(
    Output("graficoWorkClass", "figure"),
    Input("dropdown", "value"),
    Input("age_slider", "value"),
)
def update_workclass_bar_chart(selected_sex, age_range):
    if selected_sex == "Both":
        dff = df
    else:
        dff = df[df['sex'] == selected_sex]

    dff = dff[(dff['age'] >= age_range[0]) & (dff['age'] <= age_range[1])]
    dff_grouped = dff.groupby(['workclass']).size().reset_index(name='count')
    fig = px.bar(dff_grouped,
                 x="workclass",
                 y="count",
                 color="workclass",
                 text="count",
                 labels={"workclass": "Clase de Trabajo", "count": "Cantidad"},
                 title="Distribución de Clases de Trabajo")
    fig.update_traces(texttemplate='%{text}', textposition='inside', hovertemplate='Clase de Trabajo: %{x}<br>Cantidad: %{y}')

    return fig
if __name__ == '__main__':
    app.run_server(debug=True)
