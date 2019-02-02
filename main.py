import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
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
        ]) for i in range(len(dataframe))]
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='USAU Club Nationals - 2018'),
    html.Div([
        html.Label('Division'),
        # Division dropdown
        dcc.Dropdown(
            id='division-dropdown',
            options=[
                {'label': 'Open', 'value': 'Open'},
                {'label': 'Mixed', 'value': 'Mixed'},
                {'label': 'Women', 'value': 'Women'}
            ],
            value='Open'
        )], style={'width': '15%', 'float': 'left', 'display': 'inline-block', 'margin': '5px'}),
    html.Div([
        html.Label('Team'),
        # Team dropdown
        dcc.Dropdown(
            id='team-dropdown',
            options=[
                {'label': i, 'value': i} for i in df['Team'].unique()
            ],
        )], style={'width': '15%', 'float': 'left', 'margin': '5px'}),

    html.Div([
        html.Label('Player'),
        # Individual player dropdown
        dcc.Dropdown(
            id='player-dropdown',
            options=[
                {'label': i, 'value': i} for i in df['Player Name'].unique()
            ],
        )], style={'width': '15%', 'float': 'left', 'margin': '5px'}),

    html.Div([generate_table(df)], id='chart', style={'float': 'left'})
])

# Callback to update the chart based on the selected team
@app.callback(
    dash.dependencies.Output('chart', 'children'),
    [dash.dependencies.Input('team-dropdown', 'value')])
def update_data(selected_team):
    filtered_df = df[df.Team == selected_team]

    return generate_table(filtered_df)

# Callback to update the Team dropdown options based on selected Division
@app.callback(
    dash.dependencies.Output('team-dropdown', 'options'),
    [dash.dependencies.Input('division-dropdown', 'value')])
def update_dropdown(selected_division):
    return [{'label': i, 'value': i} for i in df['Team'][df.Division == selected_division].unique()]

# Callback to update the Player dropdown options based on selected Team
@app.callback(
    dash.dependencies.Output('player-dropdown', 'options'),
    [dash.dependencies.Input('team-dropdown', 'value')])
def update_player_dropdown(selected_team):
    return [{'label': i, 'value': i} for i in df['Player Name'][df.Team == selected_team]]


if __name__ == '__main__':
    app.run_server(debug=True)
