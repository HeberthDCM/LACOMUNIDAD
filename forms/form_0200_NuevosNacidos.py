import streamlit as st 
import sqlite3
import time as tm
from libraries.library_0200 import *

#cnx = sqlite3.connect(st.config["dataBase"], check_same_thread=False)
#cnx = sqlite3.connect("Datos.db", check_same_thread=False)
#cursor = cnx.cursor()

# Genera un identificador unico para cada formulario
def get_form_key():
    if 'form_key' not in st.session_state:
        st.session_state.form_key = 0
    return f"form_{st.session_state.form_key}"


# Formlario para insertar de forma individual los datos de un nuevo nacido
def frmRegistroNuevoNacido():

    with st.form(get_form_key()):

        nn_Nombres= st.text_input("Nombres y apellidos",value="")
        nn_Edad= st.text_input("Edad",value="")
        nn_Celular= st.text_input("Celular",value="")
        nn_Fecha = st.date_input("Fecha")  # Combina la fecha con la hora 00:00:00

        submit = st.form_submit_button('Ingresar',type='primary')
        if submit == True:
            #st.success("Nuevo Nacido registrado")
            add_NuevoNacido(nn_Fecha,nn_Nombres,nn_Edad,nn_Celular,1,1)
            tm.sleep(1)
            st.session_state.form_key += 1
            st.rerun()
    