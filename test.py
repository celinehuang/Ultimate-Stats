import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv(
    './USAU_Nationals_Player_Stats.csv')


def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='USAU Club Nationals - 2018'),
    html.Div([
        html.Label('Division'),
        dcc.Dropdown(
        options=[
            {'label': 'Open', 'value': 'OPEN'},
            {'label': 'Mixed', 'value': 'MIXED'},
            {'label': 'Women', 'value': 'WOMEN'}
        ],
        value='OPEN'
    )], style={'width': '15%', 'float': 'left', 'display': 'inline-block', 'margin': '5px'}),
    html.Div([
        html.Label('Team'),
        dcc.Dropdown(
        options=[
            {'label': i, 'value': i} for i in df['Team'].unique()
        ],
        value='MTL'
    )], style={'width': '15%', 'float': 'left', 'margin': '5px'}),
    html.Div([
        html.Label('Position'),
        dcc.Dropdown(
        options=[
            {'label': i, 'value': i} for i in df['Position'].unique()
        ],
        value='MTL'
    )], style={'width': '15%', 'float': 'left', 'margin': '5px'}),

    html.Div([generate_table(df)], style={'float': 'left'}) 
])

if __name__ == '__main__':
    app.run_server(debug=True)