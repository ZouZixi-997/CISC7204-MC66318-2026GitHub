import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px

data = pd.read_csv("historical_automobile_sales.csv")
app = dash.Dash(__name__)

year_list = [i for i in range(1980, 2024, 1)]

app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard",
            style={'textAlign':'center', 'color':'#503D36', 'font-size':24}),
    html.Div([
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label':'Yearly Statistics', 'value':'Yearly Statistics'},
                {'label':'Recession Period Statistics', 'value':'Recession Period Statistics'}
            ],
            value='Select Statistics',
            placeholder='Select a report type',
            style={'width':'80%','padding':'3px','fontSize':'20px','textAlignLast':'center'}
        )
    ]),
    html.Br(),
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label':i, 'value':i} for i in year_list],
            value='Select-year',
            placeholder='Select-year',
            style={'width':'80%','padding':'3px','fontSize':'20px','textAlignLast':'center'}
        )
    ]),
    html.Div(id='output-container', className='chart-grid', style={'display':'flex','flexWrap':'wrap'})
])

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics':
        return False
    else:
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [
        Input(component_id='dropdown-statistics', component_property='value'),
        Input(component_id='select-year', component_property='value')
    ]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
                           x='Year',
                           y='Automobile_Sales',
                           title="Average Automobile Sales fluctuation over Recession Period"))

        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
                          x='Vehicle_Type',
                          y='Automobile_Sales',
                          title="Average number of vehicles sold by vehicle type"))

        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                          values='Advertising_Expenditure',
                          names='Vehicle_Type',
                          title="Total Expenditure Share by Vehicle Type During Recessions"))

        unemp_data = recession_data.groupby(['unemployment_rate','Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                          x='unemployment_rate',
                          y='Automobile_Sales',
                          color='Vehicle_Type',
                          labels={'unemployment_rate':'Unemployment Rate','Automobile_Sales':'Average Automobile Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div(className='chart-item',
                     children=[html.Div(children=R_chart1,style={'width':'50%'}),
                               html.Div(children=R_chart2,style={'width':'50%'})],
                     style={'display':'flex','width':'100%'}),
            html.Div(className='chart-item',
                     children=[html.Div(children=R_chart3,style={'width':'50%'}),
                               html.Div(children=R_chart4,style={'width':'50%'})],
                     style={'display':'flex','width':'100%'})
        ]

    elif (input_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == input_year]

        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales',
                                            title='Yearly Automobile Sales Using Line Chart for the Whole Period'))

        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas,
                                            x='Month',
                                            y='Automobile_Sales',
                                            title='Total Monthly Automobile Sales'))

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata,
                                           x='Vehicle_Type',
                                           y='Automobile_Sales',
                                           title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data,
                                          values='Advertising_Expenditure',
                                          names='Vehicle_Type',
                                          title='Total Advertisement Expenditure for Each Vehicle'))

        return [
            html.Div(className='chart-item',
                     children=[html.Div(children=Y_chart1,style={'width':'50%'}),
                               html.Div(children=Y_chart2,style={'width':'50%'})],
                     style={'display':'flex','width':'100%'}),
            html.Div(className='chart-item',
                     children=[html.Div(children=Y_chart3,style={'width':'50%'}),
                               html.Div(children=Y_chart4,style={'width':'50%'})],
                     style={'display':'flex','width':'100%'})
        ]
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
