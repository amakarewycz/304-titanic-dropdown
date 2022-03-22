######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Titanic!'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
color4='#37C300'

sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/amakarewycz/304-titanic-dropdown'


###### Import a dataframe #######
df = pd.read_csv("https://raw.githubusercontent.com/austinlasseter/plotly_dash_tutorial/master/00%20resources/titanic.csv")
df['Female']=df['Sex'].map({'male':0, 'female':1})
df['Male']=df['Sex'].map({'male':1, 'female':0})
df['Cabin Class'] = df['Pclass'].map({1:'first', 2: 'second', 3:'third'})
variables_list=['Survived', 'Female', 'Male', 'Fare', 'Age']

# Create a list with those 5 values as cut points. (props if you can do this without hard-coding them!)
mybins=[0,18,30,60,80]

# Create some labels for the new variable. NOTE: There are 5 cut points but only four labels. Why is that?
mylabels=['1 children', '2 young adult', '3 middle-aged', '4 elderly']
# Use the .cut method to create a new variable using those cut points and labels.
df['Age Groups']= pd.cut(df['Age'], bins=mybins, labels=mylabels)

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H1('The Titanic:'),
    html.H3('Choose a continuous variable for summary statistics:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_mean=df.groupby(['Age Groups', 'Embarked'])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['1 children'].index,
        y=results.loc['1 children'][continuous_var],
        name='Children',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['2 young adult'].index,
        y=results.loc['2 young adult'][continuous_var],
        name='Young Adult',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=results.loc['3 middle-aged'].index,
        y=results.loc['3 middle-aged'][continuous_var],
        name='Middle Aged',
        marker=dict(color=color3)
    )

    mydata4 = go.Bar(
        x=results.loc['4 elderly'].index,
        y=results.loc['4 elderly'][continuous_var],
        name='Elderly',
        marker=dict(color=color4)
    )

    mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'Port of Embarkation'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3, mydata4], layout=mylayout)

    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
