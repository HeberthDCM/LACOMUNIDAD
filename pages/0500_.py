import streamlit as st
import login
import sqlite3 
import pandas as pd
from sqlite3 import Connection
from libraries.library_0200 import *
from streamlit_cookies_controller import CookieController# 

import pywhatkit as kit
from datetime import datetime
import time


# Función para enviar
def enviar_mensaje_whatsapp(numero, mensaje, enviar_ahora):
    try:
        if enviar_ahora:
            st.info("Enviando mensaje inmediatamente...")
            kit.sendwhatmsg_instantly(
                phone_no=numero,
                message=mensaje,
                wait_time=15,
                tab_close=True
            )
        else:
            # Programar para el minuto siguiente
            ahora = datetime.now()
            hora = ahora.hour
            minuto = ahora.minute + 1
            
            st.info(f"Programando envío para {hora}:{minuto:02d}...")
            kit.sendwhatmsg(
                phone_no=numero,
                message=mensaje,
                time_hour=hora,
                time_min=minuto,
                wait_time=15,
                tab_close=True
            )
        
        st.success("¡Mensaje enviado con éxito!")
        st.balloons()
        
    except Exception as e:
        st.error(f"Error al enviar: {str(e)}")
        st.error("""
        Posibles soluciones:
        1. Verifica que WhatsApp Web esté abierto en tu navegador
        2. Asegúrate que el número tenga formato internacional
        3. Espera unos segundos y vuelve a intentar
        """)






# Configuración de la página

archivo=__file__.split("\\")[-1]
login.generarLogin(archivo)
if 'usuario' in st.session_state:
    st.header('Página :orange[Comunicacion masiva]')

    st.title("🔍 Prueba Rápida de Envío por WhatsApp")

    # Advertencia importante

    # Entrada de datos
    with st.form("form_prueba"):
        numero = st.text_input("Número de teléfono (formato internacional):", placeholder="+51987654321")
        mensaje = st.text_area("Mensaje:", value="Hola, esto es una prueba desde Streamlit 🚀")
        enviar_ahora = st.checkbox("Enviar inmediatamente", value=True)
    
        submit_button = st.form_submit_button("📤 Enviar Mensaje")


    # Al enviar el formulario
    if submit_button:
        if not numero.startswith("+"):
            st.error("El número debe comenzar con '+' (formato internacional)")
        elif len(mensaje) == 0:
            st.error("El mensaje no puede estar vacío")
        else:
            with st.spinner("Enviando mensaje..."):
                time.sleep(2)  # Pequeña pausa para que el usuario vea el spinner
                enviar_mensaje_whatsapp(numero, mensaje, enviar_ahora)

    # Información adicional
    st.markdown("---")












