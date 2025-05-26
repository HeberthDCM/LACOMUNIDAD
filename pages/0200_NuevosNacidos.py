import streamlit as st
import login
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px

from forms.form_0200_NuevosNacidos import *
from libraries.library_0200 import *

cnx = sqlite3.connect("Datos.db", check_same_thread=False)

def MostrarNN_Todos():
    pass



def MostrarNN_Semana():
    df=pd.read_sql("select FECHA from T_NuevosNacidos", cnx)
    df['FECHA'] = pd.to_datetime(df['FECHA'])

    # Agrupar por semana
    df['semana'] = df['FECHA'].dt.to_period('W').dt.start_time
    conteo_semanal = df.groupby('semana').size().reset_index(name='conteo')

    # Crear gráfico con Plotly
    fig = px.bar(conteo_semanal, x='semana', y='conteo', 
             title='Registros por semana',
             labels={'semana': 'Semana', 'conteo': 'Número de registros'})

    # Mostrar en Streamlit
    st.plotly_chart(fig)    

def MostrarNN_Sexo():
    df=pd.read_sql("select FECHA from T_NuevosNacidos", cnx)
    df['FECHA'] = pd.to_datetime(df['FECHA'])
    # Agrupar por semana
    df['semana'] = df['FECHA'].dt.to_period('W').dt.start_time
    conteo_semanal = df.groupby('semana').size().reset_index(name='conteo')
    # Crear gráfico con Plotly
    fig = px.line(conteo_semanal, x='semana', y='conteo', 
             title='Registros por semana',
             labels={'semana': 'Semana', 'conteo': 'Número de registros'},color_discrete_sequence=['#4CAA0A'])

    # Mostrar en Streamlit
    st.plotly_chart(fig,key="grafico_semanas_sexo")        

def MostrarNN_Edad():
    df=pd.read_sql("select FECHA from T_NuevosNacidos", cnx)
    df['FECHA'] = pd.to_datetime(df['FECHA'])
    # Agrupar por semana
    df['semana'] = df['FECHA'].dt.to_period('W').dt.start_time
    conteo_semanal = df.groupby('semana').size().reset_index(name='conteo')

    # Crear gráfico con Plotly
    fig = px.scatter(conteo_semanal, x='semana', y='conteo', 
             title='Registros por semana',
             labels={'semana': 'Semana', 'conteo': 'Número de registros'}, color_discrete_sequence=['#CCAF50'])

    # Mostrar en Streamlit
    st.plotly_chart(fig,key="grafico_semanas_edad")    






archivo=__file__.split("\\")[-1]
login.generarLogin(archivo)

if 'usuario' in st.session_state:
    st.header('Página :red[Nuevos Nacidos]')
    st.title("Estadisticas")
    MostrarNN_Semana()
    #sidebar_PaginaNuevosNacidos()

    with st.container():
        columna01 , columna02 = st.columns(2)
        with columna01:
            st.subheader("Graficos 02")
            MostrarNN_Sexo()
        with columna02:
            st.subheader("Graficos 03")
            MostrarNN_Edad()