import streamlit as st
import login as login
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px

from forms.form_0200_NuevosNacidos import *
from libraries.library_0200 import *

cnx = sqlite3.connect(st.secrets["baseDatos"], check_same_thread=False)

#tab01, tab02, tab03 = st.tabs(["Nuevos Nacidos", "Seguimiento Nuevos Nacidos", "Asistencia"])
#st.set_page_config(page_title="Pagina de Inicio", page_icon="🖇️", layout="wide")


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

def MostrarNN_Semana2():
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
    st.plotly_chart(fig,key="grafico_semanas_edad3")    

def MostrarNN_Sexo2():
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
    st.plotly_chart(fig,key="grafico_semanas_sexo1")        

def MostrarNN_Edad2():
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
    st.plotly_chart(fig,key="grafico_semanas_edad1")    








archivo=__file__.split("\\")[-1]
login.generarLogin(archivo)
#st.set_page_config(page_title="Pagina de Inicio", page_icon="🖇️", layout="wide")
#tab01, tab02, tab03 = st.tabs(["Nuevos Nacidos", "Seguimiento Nuevos Nacidos", "Asistencia"])
if 'usuario' in st.session_state:
    st.header('Página :orange[Inicio]')
    st.markdown("Bienvenido a la página de inicio, aquí podrás ver las estadísticas de los nuevos nacidos.")
    tab01, tab02, tab03 = st.tabs(["Nuevos Nacidos", "Seguimiento Nuevos Nacidos", "Asistencia"])
    with tab01:
        st.header("Estadisticas de Nuevos Nacidos")
        col01tab01, col02tab01 = st.columns(2)
        with col01tab01:
            st.subheader("Graficos 01")
            MostrarNN_Semana()
        with col02tab01:
            st.subheader("Graficos 02")
            MostrarNN_Semana2()
    with tab02:
        st.header("Seguimiento de Nuevos Nacidos")
        st.markdown("En esta sección podrás ver el seguimiento de los nuevos nacidos.")
        col01tab02, col02tab02 = st.columns(2)
    
        with col01tab02:
            st.subheader("Graficos 01")
            MostrarNN_Sexo()
        with col02tab02:
            st.subheader("Graficos 02")
            MostrarNN_Sexo2()

    with tab03:
       st.header("Seguimiento de Nuevos Nacidos")
       st.markdown("En esta sección podrás ver el seguimiento de los nuevos nacidos.")
       col01tab03, col02tab03 = st.columns(2)
   
       with col01tab03:
          st.subheader("Graficos 01")
          MostrarNN_Edad()
       with col02tab03:
          st.subheader("Graficos 02")
          MostrarNN_Edad2()











