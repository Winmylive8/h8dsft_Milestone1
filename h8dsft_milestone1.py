import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

import plotly.express as px
from plotly.subplots import make_subplots

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Data Preprocessing
pokedex = pd.read_csv('Pokemon.csv', error_bad_lines=False)
variables = ["Type 1", "Type 2", "Generation", "Legendary"]

for i in variables:
    pokedex[i] = pokedex[i].astype('category')

# How many Legendary Pokemons are there?

legendary_count = pokedex[['Legendary']].groupby('Legendary').size().reset_index(name="Total")
legendary_count['% Total'] = (legendary_count['Total'] / sum(legendary_count['Total'])) * 100
dfT = legendary_count.T

colors = ['#0d1137', '#e52165']

fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}]])


fig.add_trace(go.Bar(x=legendary_count['Legendary'],
                     y=legendary_count['Total'],
                     marker_color=colors,
                     ),
              row=1, col=1)

fig.add_trace(go.Pie(labels=legendary_count['Legendary'], values=legendary_count['Total'],
                     marker_colors=colors,
                     name='Percentage Count'),
              row=1, col=2)

fig.update_layout(title_text='Non-Legendary and Legendary Pokemons',
                  template='plotly_white')
fig.update_xaxes(title_text='Legendary')
fig.update_yaxes(title_text='Total Pokemons')

fig.layout.xaxis.fixedrange = True
fig.layout.yaxis.fixedrange = True

# Attack vs Defense

X = pokedex['Defense'].values.reshape(-1, 1)

model = LinearRegression()
model.fit(X, pokedex['Attack'])

x_range = np.linspace(X.min(), X.max(), 100)
y_range = model.predict(x_range.reshape(-1, 1))

colors = ['#aed6dc', '#ff9a8d']

fig2 = px.scatter(pokedex, x='Defense', y='Attack', color='Legendary',
                 color_discrete_sequence=colors,
                 hover_name="Name",
                 template='plotly_white',
                 title="Attack Vs Defense")
fig2.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Fit',
                          marker=dict(color='#4a536b')))

fig2.layout.xaxis.fixedrange = True
fig2.layout.yaxis.fixedrange = True

# Legendary Pokémon by type

legend_by_type = pokedex[['Type 1', 'Legendary']]
legend_by_type['Legendary'] = legend_by_type['Legendary'].astype('int64')
legend_by_type = legend_by_type.groupby('Type 1').sum().reset_index().sort_values(['Legendary'])


legend_by_type2 = pokedex[['Type 2', 'Legendary']]
legend_by_type2['Legendary'] = legend_by_type2['Legendary'].astype('int64')
legend_by_type2 = legend_by_type2.groupby('Type 2').sum().reset_index().sort_values(['Legendary'])


# Plotting Bar plots
fig3 = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "bar"}]],
                    subplot_titles=("Primary Type", "Secondary Type"))

fig3.add_trace(go.Bar(x=legend_by_type['Legendary'],
                     y=legend_by_type['Type 1'],
                     name='Type 1',
                     orientation='h',
                     marker_color="#408ec6",
                     ),
              row=1, col=1)

fig3.add_trace(go.Bar(x=legend_by_type2['Legendary'],
                     y=legend_by_type2['Type 2'],
                     name='Type 2',
                     orientation='h',
                     marker_color="#7a2048"
                     ),
              row=1, col=2)

fig3.update_layout(title_text='Legendary Pokemon by Type',
                  template='plotly_white')
fig3.update_xaxes(title_text='Total Legendaries')
fig3.update_yaxes(title_text='Types')

fig3.layout.xaxis.fixedrange = True
fig3.layout.yaxis.fixedrange = True

fig3.update_layout(showlegend=False)


app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.H1("Welcome to the Hacktiv8 Milestone dashboard",
                className="text-center"),
                className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(
                html.H5(children='My name is Winwin! This is my milestone dash dashboard!'),
                className="mb-4")
        ]),
 
        dbc.Row([
            dbc.Col(
                html.H5(children='It consists of two main pages: Pokemon, This data set includes 721 Pokemon, including their number, name, first and second type, and basic stats: HP, Attack, Defense, Special Attack, Special Defense, and Speed, '
                'Home, you get the original dataset and visit my Github page from here'),
                className="mb-5")
        ]),
        dbc.Row([
            dbc.Col(
                html.H1("The Hypothesis",
                className="text-center"),
                className="mb-5 mt-5")               
        ]),
        dbc.Row([
            dbc.Col(
                html.H5(children='The Pokemon dataset is analyzed to determine the type of pokemon (legendary or normal), to determine the attack and defense of the pokemon and to find out the most types of legendary pokemon'),
                className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(
                html.H1("The Summary",
                className="text-center"),
                className="mb-5 mt-5")               
        ]),
        dbc.Row([
            dbc.Col(
                html.H5(children='1. From the graph of a total of 791 pokemon, legendary pokemon only amount to 8.13% pokemons 2. From the attack vs defense graph, almost all legendary pokemon have above average attack and defense 3. From the graph of pokemon types, psychic and flying pokemon types have the highest number'),
                className="mb-4")
        ]),

        dbc.Row([
            dbc.Col(
                html.H1("How many Legendary Pokemons are there?"),
                className="mb-2 mt-2"
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.H6(children='Non-Legendary and Legendary Pokemons'),
                className="mb-4"
            )

        ]),        
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id='Non-Legendary and Legendary Pokemons',
                    figure=fig
                )
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.H1(children='Legendary Pokemon by Attack and Defense'),
                className="mb-4"
            )
        ]),
                dbc.Row([
            dbc.Col(
                html.H6(children='Attack Vs Defense'),
                className="mb-4"
            )
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id='Attack Vs Defense',
                    figure=fig2
                )
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.H1(children='Legendary Pokemon by Type'),
                className="mb-4"
            )
        ]),
                dbc.Row([
            dbc.Col(
                html.H6(children='Legendary Pokemon by Type'),
                className="mb-4"
            )
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id='Legendary Pokemon by Type',
                    figure=fig3
                )
            )
        ]),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    children=[
                        html.H3(children='Get the original dataset here',
                        className="text-center"),
                        dbc.Button("Pokemon Dataset",
                        href="https://www.kaggle.com/abcsds/pokemon",
                        color="primary",
                        className="mt-3"),
                    ],
                    body=True, color="dark", outline=True
                ),
                width=6, className="mb-6"
            ),
 
            dbc.Col(
                dbc.Card(
                    children=[
                        html.H3(children='Visit my Github Page',
                        className="text-center"),
                        dbc.Button("GitHub",
                        href="https://github.com/Winmylive8",
                        color="primary",
                        className="mt-3"),
                    ],
                    body=True, color="dark", outline=True
                ),
                width=6, className="mb-6"
            ),
        ], className="mb-5"),                              
    ])
])



if __name__ == '__main__':
    app.run_server(debug=True)