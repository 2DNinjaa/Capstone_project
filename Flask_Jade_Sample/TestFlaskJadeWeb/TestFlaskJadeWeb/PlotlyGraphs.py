#!/usr/bin/env python
# coding: utf-8

# In[3]:


import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import sqlite3
import csv
import xlrd
import matplotlib.pyplot as plt
import plotly.express as px
import chart_studio.tools as tls
import chart_studio.plotly as py
import plotly.io as pio
import plotly


# In[ ]:


def s():
    data = pd.read_csv('output.csv')

    #fig1 = px.line(data, x= 'location', y = 'jobType')
    
    fig2 = px.scatter(data, x = "salary", y = "salary", color = "jobCategory",
                     size = "salary", hover_data = ['Skills'], animation_frame = "location")
    fig2.update_layout(title = 'Salaries based on Location',
                      xaxis=dict(title='Cities', gridcolor='white',gridwidth=2),
                      yaxis=dict(title='Salaries ($)', gridcolor='white',gridwidth=2),
                      plot_bgcolor='rgb(243, 243, 246)')

    #fig3 = px.sunburst(data, path=['jobCategory', 'location', 'salary'], values = 'salary')

    fig4 = px.pie(data, values = 'salary', names = 'location', color_discrete_sequence
                  = px.colors.sequential.Greens, title = 'Salaries based on Location',
                  hover_data=['Skills'])
    fig4.update_traces(textposition = 'inside', textinfo = 'percent+label')



    #This puts it in your cloud for your Chart Studios Account
    #You can switch it to be your account/api_key from your account.
    tls.set_credentials_file(username = 'lbecker7', api_key = '3ztc7kdqWPHtPtkhusiy')

    #JUST fig2 (can make a list of embedded urls, but some of the figures above gave errors so i didnt do that)
    url = py.plot(fig2, filename = 'fig2', auto_open = True)
    url2 = py.plot(fig4, filename = 'fig4', auto_open = True)
    return [tls.get_embed(url), tls.get_embed(url2)]


# In[15]:


def s2():
    data = pd.read_csv('output.csv')

    fig1 = px.scatter(data, x = "location", y = "salary", color = "jobCategory",
                      size = "salary", hover_data = ['Skills'])
    
    fig2 = px.scatter(data, x = "salary", y = "salary", color = "jobCategory",
                     size = "salary", hover_data = ['Skills'], animation_frame = "location")
    fig2.update_layout(title = 'Salaries based on Location',
                      xaxis=dict(title='Cities', gridcolor='white',gridwidth=2),
                      yaxis=dict(title='Salaries ($)', gridcolor='white',gridwidth=2),
                      plot_bgcolor='rgb(243, 243, 246)')

    fig4 = px.pie(data, values = 'salary', names = 'location', color_discrete_sequence
                  = px.colors.sequential.Greens, title = 'Salaries based on Location',
                  hover_data=['Skills'])
    fig4.update_traces(textposition = 'inside', textinfo = 'percent+label')

    tls.set_credentials_file(username = 'kayleenvasil', api_key = 'J6eU4QmwoQIYA6CuZPvV')
    url1 = py.plot(fig1, filename = 'fig1', auto_open = True)
    url2 = py.plot(fig2, filename = 'fig2', auto_open = True)
    url3 = py.plot(fig4, filename = 'fig4', auto_open = True)
    print(tls.get_embed(url1))
    print(tls.get_embed(url2))
    print(tls.get_embed(url3))


# In[35]:


def s_modular(chartType = 'Scatter', animFrame = '', xAxis = 'Salary', yAxis = 'Location'):
    fig = None
    data = pd.read_csv('output.csv')
    if chartType == 'Scatter':
        if animFrame == '':
            fig = px.scatter(data, x = xAxis, y = yAxis, color = "category",
                              hover_data = ['skills'])
        else:
            fig = px.scatter(data, x = xAxis, y = yAxis, color = "category",
                              hover_data = ['skills'], animation_frame = animFrame)
        fig.update_layout(title = yAxis + ' based on '+ xAxis,
                           xaxis=dict(title=xAxis, gridcolor='white',gridwidth=2),
                           yaxis=dict(title=yAxis, gridcolor='white',gridwidth=2),
                           plot_bgcolor='rgb(243, 243, 246)')
            
    elif chartType == 'Pie':
        fig = px.pie(data, values = yAxis, names = xAxis, 
                      color_discrete_sequence = px.colors.sequential.Greens, title = yAxis + ' based on '+ xAxis,
                      hover_data=['skills'])
        fig.update_traces(textposition = 'inside', textinfo = 'percent+label')
    elif chartType == 'Bar':
        fig = px.bar(data, x = xAxis, y = yAxis, color = "category",
                              hover_data = ['skills'])
        fig.update_layout(title = yAxis + ' based on '+ xAxis,
                           xaxis=dict(title=xAxis, gridcolor='white',gridwidth=2),
                           yaxis=dict(title=yAxis, gridcolor='white',gridwidth=2),
                           plot_bgcolor='rgb(243, 243, 246)')
    else:
        return 'INVALID INPUTS'
        
    url = py.plot(fig, filename = 'fig', auto_open = False)
    embd = tls.get_embed(url).split(' ')
    src = ''
    for x in embd:
        if 'src' in x:
            src = x
    return src[5:-1]

import sqlite3
import unicodecsv as csv
def port_to_csv():
    inpsql3 = sqlite3.connect('Users.db')
    sql3_cursor = inpsql3.cursor()
    sql3_cursor.execute('SELECT * FROM JOBS')
    with open('output.csv','wb') as out_csv_file:
        csv_out = csv.writer(out_csv_file)
        # write header                        
        csv_out.writerow([d[0] for d in sql3_cursor.description])
        # write data                          
        for result in sql3_cursor:
            csv_out.writerow(result)
    inpsql3.close()


