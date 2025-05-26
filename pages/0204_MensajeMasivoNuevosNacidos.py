import streamlit as st
import sqlite3
import pandas as pd
import pywhatkit as kit
from datetime import datetime
import time as tm
from streamlit_cookies_controller import CookieController
import login as login
from libraries.library_0200 import *

# Conexión a la base de datos
def get_db_connection():
    try:
        conn = sqlite3.connect("Datos.db", check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        st.error(f"Error al conectar a la base de datos: {e}")
        return None
    except Exception as e:
        st.error(f"Error inesperado: {e}")
        return None
    else:
        pass
        #st.success("Conexión a la base de datos exitosa.")
        #st.success(conn)
    #return conn

# Obtener comunicaciones pendientes
def get_comunicaciones_pendientes():
    conn = sqlite3.connect(st.secrets["baseDatos"], check_same_thread=False)
    #conn = get_db_connection()
    query = """
    SELECT c.Id, c.EmisorNombre, c.EmisorCelular, c.ReceptorNombre, c.ReceptorCelular, c.idMensaje, c.EnvioConfirmado, m.Mensaje FROM Comunicaciones c LEFT JOIN V_Mensajes m ON c.idMensaje = m.Id WHERE c.EnvioConfirmado = 0
    """
    comunicaciones = pd.read_sql(query, conn)
    cnx.close()
    return comunicaciones

# Actualizar estado de envío
def actualizar_envio(id_comunicacion):
    conn = sqlite3.connect("Datos.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Comunicaciones SET EnvioConfirmado = 1 WHERE Id = ?",
        (id_comunicacion,)
    )
    conn.commit()
    conn.close()

# Plantilla para mensaje al emisor
PLANTILLA_EMISOR = """
¡Hola {EmisorNombre}!

Recordatorio importante:
Por favor contacta a {ReceptorNombre} al número {ReceptorCelular}.

Gracias por tu atención.
"""

# Función para enviar mensajes
def enviar_mensaje_whatsapp(numero, mensaje):
    try:
        # Eliminar espacios y caracteres no numéricos excepto +
        numero = ''.join(c for c in numero if c.isdigit() or c == '+')
        
        if not numero.startswith('+'):
            numero = '+' + numero
            
        kit.sendwhatmsg_instantly(
            phone_no=numero,
            message=mensaje,
            wait_time=20,
            tab_close=True
        )
        return True
    except Exception as e:
        st.error(f"Error al enviar a {numero}: {str(e)}")
        return False

# Interfaz de la aplicación
st.title("📱 Sistema de Comunicaciones WhatsApp")



archivo=__file__.split("\\")[-1]
login.generarLogin(archivo)
if 'usuario' in st.session_state:
    st.header('Página :orange[PRUEBAS]')


    # Mostrar comunicaciones pendientes
    st.header("Comunicaciones Pendientes")
    comunicaciones = get_comunicaciones_pendientes()

    if comunicaciones.empty:
        st.success("No hay comunicaciones pendientes por enviar.")
        st.stop()

    st.dataframe(comunicaciones)

    # Dividir en dos pestañas
    tab1, tab2 = st.tabs(["Enviar Mensajes a Receptores", "Notificar a Emisores"])

    with tab1:
        st.header("Enviar Mensajes a Receptores")
    
        if st.button("📤 Enviar Todos los Mensajes a Receptores", key="btn_receptores"):
            progress_bar = st.progress(0)
            total = len(comunicaciones)
            exitosos = 0
        
            for index, row in comunicaciones.iterrows():
                mensaje = f"¡Hola {row['ReceptorNombre']}!\n\n{row['Mensaje']}"
            
                if enviar_mensaje_whatsapp(row['ReceptorCelular'], mensaje):
                    actualizar_envio(row['Id'])
                    exitosos += 1
            
                progress_bar.progress((index + 1) / total)
                tm.sleep(5)  # Espera para evitar bloqueos
        
            st.success(f"Proceso completado: {exitosos}/{total} mensajes enviados con éxito.")
            st.balloons()

    with tab2:
        st.header("Notificar a Emisores")
    
        if st.button("📢 Notificar a Todos los Emisores", key="btn_emisores"):
            progress_bar = st.progress(0)
            total = len(comunicaciones)
            exitosos = 0
        
            for index, row in comunicaciones.iterrows():
                mensaje = PLANTILLA_EMISOR.format(
                    EmisorNombre=row['EmisorNombre'],
                    ReceptorNombre=row['ReceptorNombre'],
                    ReceptorCelular=row['ReceptorCelular']
                )
            
                if enviar_mensaje_whatsapp(row['EmisorCelular'], mensaje):
                    exitosos += 1
            
                progress_bar.progress((index + 1) / total)
                tm.sleep(5)  # Espera para evitar bloqueos
        
            st.success(f"Proceso completado: {exitosos}/{total} notificaciones enviadas con éxito.")
            st.balloons()

    # Panel de control
    st.sidebar.header("Panel de Control")
    st.sidebar.info("""
    **Instrucciones:**
    1. Primero envía mensajes a receptores
    2. Luego notifica a emisores
    3. Los mensajes enviados se marcarán como confirmados
    """)

    st.sidebar.warning("""
    **Requisitos:**
    - Sesión activa en WhatsApp Web
    - Números en formato internacional
    - No cerrar la pestaña del navegador
    """)

    # Actualizar vista
    if st.sidebar.button("🔄 Actualizar Datos"):
        st.rerun()