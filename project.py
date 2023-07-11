import dash

import dash_bootstrap_components as dbc

from dash import html

from dash import dcc

from dash.dependencies import Input, Output

import pandas as pd

import plotly.express as px

import plotly.graph_objects as go


# Read the CSV data
data = pd.read_csv('https://raw.githubusercontent.com/ngocanhjs/1031/main/data.csv')

# Define color list
colors = ['goldenrod', 'hotpink', 'chocolate', 'lawngreen', 'dodgerblue']

# Create the bar chart
df_bar = data['MAIN_PRODUCTION'].value_counts().nlargest(n=5, keep='all').sort_values(ascending=False)
trace_bar = go.Bar(
    y=df_bar.values,
    x=df_bar.index,
    orientation='v',
    marker=dict(
        color=colors
    )
)
data_bar = [trace_bar]
layout_bar = go.Layout(
    title='Top 5 countries with the most TV shows (1970-2020)',
    xaxis=dict(title='Main Production'),
    yaxis=dict(title='Number of TV shows'),
    height=500
)
fig_bar = go.Figure(data=data_bar, layout=layout_bar)

# Create the box chart
fig_box = px.box(data, x="MAIN_GENRE", y="SCORE", color="MAIN_GENRE",
                title="the distribution of range score of TV shows according to main_genres",
                color_discrete_map={genre: color for genre, color in zip(data['MAIN_GENRE'].unique(), colors)})
med_score = data.groupby('MAIN_GENRE')['SCORE'].median().sort_values()
sorted_genre = med_score.index.tolist()
fig_box.update_layout(xaxis=dict(categoryorder='array', categoryarray=sorted_genre))

# Create the pie chart
country_df = data['MAIN_PRODUCTION'].value_counts().reset_index()
country_df = country_df[country_df['MAIN_PRODUCTION'] / country_df['MAIN_PRODUCTION'].sum() > 0.01]
fig_pie = px.pie(country_df, values='MAIN_PRODUCTION', names='index', color_discrete_sequence=colors,title="The scatter plot shows the scores of TV shows by genre",)
fig_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='white', width=1)))
fig_pie.update_layout(height=500)

# Create the scatter plot
fig_scatter = px.scatter(
    data,
    x="RELEASE_YEAR",
    y="SCORE",
    color="MAIN_GENRE",
    title="The scatter plot shows the scores of TV shows by genre",
    color_discrete_map={genre: color for genre, color in zip(data['MAIN_GENRE'].unique(), colors)},
    height = 800
)
fig_scatter.update_layout(height=800)
# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = dbc.Container([
    html.H1('NETFLIX TV SHOW DATA VISUALIZATION', style={'text-align': 'center'}),
        html.H6("This interactive web application includes a bar chart visualizing the top 5 countries with the highest Netflix TV show production, as well as a box chart displaying the distribution of scores within different genres. Users can interact with the slider and dropdown menu to explore the data.",
                style={'text-align': 'center', 'color': 'lightblack', 'font-style': 'italic'}),
        html.A('Click here for more information', href='https://www.netflix.com/',
               style={'text-align': 'center', 'color': 'blue','font-style': 'italic','font-size': '14px'}),
    html.Hr(),
    dbc.Row([html.H2('The Distribution of Main Genre', style={'text-align': 'center', 'color': 'black'}),
             html.Hr(),
        dbc.Col([
            html.Hr(),
            html.H5('THE BAR CHART'),
            html.P('Number of countries:'),
            dcc.Slider(id='slider', min=1, max=5, step=1, value=5),
            dcc.Graph(id='plot-bar', figure=fig_bar)
        ], md=6),
        dbc.Col([
            html.Hr(),
            html.H5('THE PIE CHART'),
            html.P('Number of countries:'),
            html.H6('nfj'),
            dcc.Graph(id='plot-pie', figure=fig_pie)
        ], md=6)
    ]),
    html.Hr(),
    dbc.Row([
        html.H2('The Distribution of Main Genre', style={'text-align': 'center', 'color': 'black'}),
        dbc.Col([
            html.Hr(),
            html.H5('THE MAIN BOX CHART'),
            dcc.Graph(id='plot-box', figure=fig_box, style={'height': 950}),
        ], width=6),
        dbc.Col([
            html.Hr(),
            html.H5('THE SCATTER PLOT', className='text-center'),
            html.Hr(),
            html.H6('Select genre that you want to see:', className='text-center'),
            dcc.Dropdown(
                id='dropdown',
                options=[{"label": option, "value": option} for option in data["MAIN_GENRE"].unique()],
                value="drama"
            ),
            dcc.Graph(id="plot-sub-box"),
        ], width=5)
    ]),
], fluid=True)

# Callback to update the bar chart based on the slider value
@app.callback(Output('plot-bar', 'figure'), [Input('slider', 'value')])
def update_bar_chart(value):
    df1 = df_bar.nlargest(n=value, keep='all').sort_values(ascending=False)
    fig_bar.update_layout(title='Top {} countries that have the most TV shows in the period 1970 - 2020'.format(value))
    fig_bar.update_traces(y=df1.values, x=df1.index)
    return fig_bar

# Callback to update the scatter plot based on the dropdown selection
@app.callback(Output('plot-sub-box', 'figure'), [Input('dropdown', 'value')])
def update_scatter_plot(genre_selection):
    data_subset = data.loc[data['MAIN_GENRE'] == genre_selection]
    fig = px.scatter(
        data_subset,
        x="RELEASE_YEAR",
        y="SCORE",
        color="MAIN_GENRE",
        title=f"The scatter plot for {genre_selection} genre",
        color_discrete_map={genre: color for genre, color in zip(data['MAIN_GENRE'].unique(), colors)}
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
