from dash import html
from dash import dcc
import dash
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output

data = pd.read_csv(r'C:\\data.csv') 

df = data['MAIN_PRODUCTION'].value_counts()

value = 5

df1 = df.nlargest(n=value, keep='all').sort_values(ascending=False)

trace = go.Bar(
    x=df1.values,
    y=df1.index,
    orientation='v',
    marker=dict(color=['goldenrod','hotpink','chocolate','lawngreen','dodgerblue','darkviolet','plum','forestgreen','crimson'])
)

data = [trace]

layout = go.Layout(
    title='Top {} countries that have the most TV shows in the period 1970 - 2020'.format(value),
    xaxis=dict(title='MAIN_PRODUCTION'),
    yaxis=dict(title="NUMBER OF TV SHOWS")
)

fig = go.Figure(data=data, layout=layout)

app = dash.Dash(__name__)
server=app.server()
app.layout = html.Div(
    children=[
        html.H1('Finding the top countries that produce the largest number of content titles', style={'text-align': 'center', 'color': 'black'}),
        html.P('Number of countries:'),
        dcc.Slider(id='slider', min=1, max=10, step=1, value=value),
        dcc.Graph(id='plot', figure=fig)
    ]
)

@app.callback(
    Output('plot', 'figure'),
    Input('slider', 'value')
)
def update_plot(value):
    df1 = df.nlargest(n=value, keep='all')
    fig.update_layout(title='Top {} countries that have the most TV shows in the period 1970 - 2020'.format(value))
    fig.update_traces(y=df1.values, x=df1.index)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
