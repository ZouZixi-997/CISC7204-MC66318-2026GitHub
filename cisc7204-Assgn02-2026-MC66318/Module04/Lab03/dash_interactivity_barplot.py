import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

airline_data = pd.read_csv(
    'airline_data.csv',
    encoding="ISO-8859-1",
    dtype={'Div1Airport': str, 'Div1TailNum': str,
           'Div2Airport': str, 'Div2TailNum': str})

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Total number of flights to the destination state split by reporting airline',
            style={'textAlign':'center','font-size':40}),

    html.Div([
        "Input Year: ",
        dcc.Input(id='input-year',
                  value='2010',
                  type='number',
                  style={'height':'50px','font-size':35})
    ], style={'font-size':40}),

    html.Br(),
    html.Br(),
    html.Div(dcc.Graph(id='bar-plot'))
])

@app.callback(
    Output(component_id='bar-plot', component_property='figure'),
    Input(component_id='input-year', component_property='value')
)

def get_bar_graph(entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)]
    bar_data = df.groupby(['DestState','Reporting_Airline'])['Flights'].sum().reset_index()

    fig = px.bar(
        bar_data,
        x="DestState",
        y="Flights",
        color="Reporting_Airline",
        title="Total number of flights to destination state split by reporting airline"
    )
    fig.update_layout(xaxis_title="Destination State", yaxis_title="Flights")
    return fig

if __name__ == '__main__':
    app.run()
