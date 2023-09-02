import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
from dash import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import os
from dash import dash_table
from flask import send_from_directory
data = pd.read_excel('C:/Users/alex1/Desktop/FSDS.xlsx')

# инициализация Dash

app = dash.Dash(__name__, external_stylesheets=['style.css'])
# переменные с жанрами и рейтингами для фильтрации


# определение внешнего вида приложения dash

app.layout = html.Div(children=[
        html.Div([
            

            html.P(
                "Динамическая веб-диаграмма подробно анализирует все источники дохода"
                
            )
        ], style = {'font-size': '32px',
            'font-weight': 'bold',
            'text-align': 'center',
            'backgroundColor': '#1b1b32',
            'padding': '5px 5px',
            'color':'white'
        }),

        # фильтр по жанрам 
        html.Div([
            html.Div([
                
                dcc.Dropdown(
                    id = 'crossfilter-years',
                    options = [ {'label': i, 'value': i} for i in data['Year'].unique() ],   value='2022'
                    # значения жанров по умолчанию
                    
                    # множественный выбор
                   
                )
            ],
            style = {'width': '25%', 'display': 'inline-block','font-size': '18px',
            'font-weight': 'bold',
            'text-align': 'left',
            'backgroundColor': '#1b1b32',
            'borderRadius': '15px',
            
            'color':'black'}),

           
        ], style = {'font-size': '18px',
            'font-weight': 'bold',
            'text-align': 'left',
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': '#000000',
            'padding': '10px 50px',
            
            'color':'black'
        }),

        # заготовка для интерактивного текста - результата фильтрации
    
    html.Div([
    html.Div(id='output',style = {'font-size': '36px',
                                  'width': '40%',
            'font-weight': 'bold',
            'text-align': 'left',
            'backgroundColor': '#1b1b32',
            'display': 'inline-block',
            'padding': '25px 25px',
            'color':'white'
        }),
    
    html.Div(id='output1',style = {'font-size': '36px',
                                   'width': '40%',
            'font-weight': 'bold',
            'text-align': 'left',
            'backgroundColor': '#1b1b32',
            'display': 'inline-block',
            'padding': '25px 25px',
            'color':'white'
        }),
   
    html.Table(id='my-table',  
                   style = {'font-size': '24px',
                                   'width': '50%',
            'font-weight': 'bold',
            'text-align': 'right',
            'vertical-align': 'top',
            'display': 'inline-block',
            'backgroundColor': '#000000',
            'padding': '25px 25px',
            'color':'white'
        }
                   ),
    html.Table(id='my-table1',  
                   style = {'font-size': '24px',
                                   'width': '50%',
            'font-weight': 'bold',
            'text-align': 'right',
            'backgroundColor': '#000000',
            'vertical-align': 'top',
            'display': 'inline-block',
            'padding': '25px 25px',
            'color':'white'
        }
                   )], style  ={'display': 'inline-block'}),
     
    html.Div([
        html.Div(
            dcc.Graph(id = 'mounsts1'),
            style = {'width': '25%', 'display': 'inline-block','font-size': '18px',
            'font-weight': 'bold',
            'borderRadius': '15px',
            'text-align': 'left'}
        ),
        html.Div(
            dcc.Graph(id = 'mounsts2'),
            style = {'width': '25%',
                     'font-size': '18px',
            'font-weight': 'bold',
            'text-align': 'right',
            'borderRadius': '15px',
                     'display': 'inline-block'}
        ),
        html.Div(
            dcc.Graph(id = 'archived'),
            style = {'width': '22%', 'display': 'inline-block','font-size': '18px',
            'font-weight': 'bold',
            'borderRadius': '15px',
            'text-align': 'left'}
        ),
    html.Div(
            dcc.Graph(id = 'scatter-plot',style = {
            'borderRadius': '15px'
            }),
            
            style = {'width': '28%', 'float': 'right', 'display': 'inline-block','font-size': '18px',
            'font-weight': 'bold',
            'borderRadius': '15px',
            'text-align': 'center'}
        )
      ]),
        # гистограмма
        
        # диаграмма рассеяния (scatter plot)
        
        # фильтр по годам
        
 ],style = {'backgroundColor': '#000000'} )

# обратный вызов результата фильтрации



# обратный вызов histogram
@app.callback(
    Output('my-table', 'children'), 
    [
    Input('crossfilter-years', 'value')])
def update_stacked_area(year):
    if type(year) != int:
        year = 2022
    filtered_data = data[data['Year'] == year]
    filtered_data = filtered_data.groupby(pd.Grouper(key='Income sources'))['Counts'].sum().reset_index()
    summ = filtered_data['Counts'].values.sum()

    filtered_data['Quantity'] = filtered_data.apply(lambda row: str(round(row.Counts/summ*100))+'%',axis = 1)

    filtered_data = filtered_data[['Income sources','Quantity','Counts']]
    filtered_data = filtered_data.rename(columns = {'Income sources':'Sources','Quantity':'Quantity',"Counts":'Counts'})
    table_data = filtered_data[['Sources', 'Quantity', 'Counts']].to_dict('records')
    
    return [html.Tr([html.Th(col) for col in filtered_data.columns])] +\
           [html.Tr([html.Td(data[col]) for col in filtered_data.columns]) for data in table_data]
@app.callback(
    Output('my-table1', 'children'), 
    [
    Input('crossfilter-years', 'value')])
def update_stacked_area(year):
    if type(year) != int:
        year = 2022
    filtered_data = data[data['Year'] == year]
    filtered_data = filtered_data.groupby(pd.Grouper(key='Income sources'))['Income'].sum().reset_index()
    summ = filtered_data['Income'].values.sum()
    
    filtered_data['Income Archived'] = filtered_data.apply(lambda row: str(round(row.Income/summ*100))+'%',axis = 1)

    filtered_data = filtered_data[['Income sources','Income Archived','Income']]
    filtered_data = filtered_data.rename(columns = {'Income sources':'Sources','Income Archived':'Archived',"Income":'Income'})
    table_data = filtered_data[['Sources', 'Archived', 'Income']].to_dict('records')
    
    return [html.Tr([html.Th(col) for col in filtered_data.columns])] +\
           [html.Tr([html.Td(data[col]) for col in filtered_data.columns]) for data in table_data]


# Здесь можно реализовать логику изменения данных для отображения
@app.callback(Output('output', 'children'),
              [Input('crossfilter-years', 'value')])
def update_output(year):
    if type(year) != int:
        year = 2022
    filtered_data = data[data['Year'] == year]
    
    
    sums_TI = round(filtered_data['Target Income'].values.sum())
    
    return 'Target Income - '+str(sums_TI) 
@app.callback(Output('output1', 'children'),
              [Input('crossfilter-years', 'value')])
def update_output(year):
    if type(year) != int:
        year = 2022
    filtered_data = data[data['Year'] == year]
    
    sums_IN = round(filtered_data['Income'].values.sum())
    return 'Income - ' + str(sums_IN)




#R2-D2 srarwars
@app.callback(
    Output('scatter-plot', 'figure'), 
    [
    Input('crossfilter-years', 'value')])
def update_stacked_right(year):
    if type(year) != int:
        year = 2022
    filtered_data = data[data['Year'] == year]
    B2B = round(filtered_data[filtered_data['Marketing Strategies'] == 'B2B']['Income'].values.sum())
    B2C = round(filtered_data[filtered_data['Marketing Strategies'] == 'B2C']['Income'].values.sum())
    figure = px.pie(
         filtered_data,
         values = 'operating profit',
         names =  "Marketing Strategies",
         
        
        title = 'B2B-' + str(B2B)+ '-' + str(round(B2B/(B2B+B2C)*100,2)) + '% | ' + 'B2C-' + str(B2C) + '-' + str(round(B2C/(B2B+B2C)*100,2))+'%'
    )
    figure.update_layout(
    plot_bgcolor='#000000',
    paper_bgcolor='#000000',
    
    font_color='white'
)
    return figure

@app.callback(
    Output('archived', 'figure'), 
    [
    Input('crossfilter-years', 'value')])

def update_stacked_right(year):
    if type(year) != int:
        year = 2022
    filtered_data = data[data['Year'] == year]
    income_arch = round(filtered_data['Income'].values.sum()/filtered_data['Target Income'].values.sum()*100)
    filtered_data = filtered_data.groupby(pd.Grouper(key='Income sources'))['Income'].sum().reset_index()
    # Создаем список значений оси X (названия источников дохода)
    categories = list(filtered_data['Income sources'])

    # Создаем список значений оси Y (данные об источниках дохода)
    values = list(map(round,filtered_data['Income']))

    # Создаем диаграмму-паутинку
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        fill="toself",
        theta=categories,
        
    ))

    fig.update_layout(
        title='Income archived  - ' + str(income_arch) + '%',
        polar=dict(
        bgcolor="#000000",
        radialaxis=dict(
            visible=False
        ),
        angularaxis=dict(
            tickfont=dict(
                color="white"
            ))),
        plot_bgcolor='#000000',
    paper_bgcolor='#000000',
  
    font_color='white',
   
    showlegend=False
    )
    return fig   

# обратный вызов mounsts
@app.callback(
    Output('mounsts1', 'figure'), 
    [
    Input('crossfilter-years', 'value')])
def update_stacked_area(year):
    if type(year) != int:
        year = 2022
    filtered_data = data[data['Year'] ==year]
   
    filtered_data = filtered_data.groupby(pd.Grouper(key='Month'))['Income'].sum().reset_index()
    prof = round(filtered_data['Income'].values.mean(),0)
    figure = px.line(
        filtered_data,
         x =  "Month",
         y = 'Income',
         
         title = 'Average Monthly Income - ' + str(prof)
        
         
    )
    figure.update_layout(
    plot_bgcolor='#000000',
    paper_bgcolor='#000000',
   
    font_color='white'
)
    return figure

@app.callback(
    Output('mounsts2', 'figure'), 
    [
    Input('crossfilter-years', 'value')])

def update_stacked_area(year):
    if type(year) != int:
        year = 2022
    filtered_data = data[data['Year'] ==year]
    prof = round(filtered_data['operating profit'].values.sum())
    filtered_data = filtered_data.groupby(pd.Grouper(key='Month'))['operating profit'].sum().reset_index()
    
    figure = px.histogram(
        filtered_data,
         
         y =  "Month",
         x = 'operating profit',
        
         title = "Operating Profits - " + str(prof)
    )
    figure.update_layout(
    plot_bgcolor='#000000',
    paper_bgcolor='#000000',
  
    font_color='white'
)
    return figure



if __name__ == '__main__':
    app.run_server(debug=True)