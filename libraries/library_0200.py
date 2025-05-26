import streamlit as st
import sqlite3
#import time
from datetime import datetime, time
from streamlit_cookies_controller import CookieController

#cnx = sqlite3.connect("Datos.db", check_same_thread=False)
cnx = sqlite3.connect(st.secrets["baseDatos"], check_same_thread=False)

cursor = cnx.cursor()



def sidebar_PaginaNuevosNacidos():
    st.sidebar.subheader("Tableros Nuevos Nacidos")
    with st.sidebar:
        #st.page_link("pages/0102_paginaInsertarNuevosNacidos.py", label="Registro de nuevo nacido", icon=":material/assignment_ind:")
        st.page_link("pages/0201_ImportarDatosNuevosNacidos.py", label="Importar Nuevos Nacidos", icon=":material/contact_page:")
        st.page_link("pages/0202_RegistrarNuevosNacidos.py", label="Registro de Nuevos Nacidos", icon=":material/person_add:")
        st.page_link("pages/0203_AsignacionNuevosNacidos.py", label="Asignar Resposabilidades", icon=":material/tenancy:")
        

def add_NuevoNacido (fecha,Nombre,Edad,Celular,idGrupo,idEstado):
    fecha2 =  datetime.combine(fecha, time(0, 0))
    cursor.execute(
        "insert into T_NuevosNacidos values (NULL,?,?,?,?,?,?)",
        (fecha2,Nombre,Edad,Celular,idGrupo,idEstado)     
    )
    cnx.commit()
    #cnx.close()
    st.success("Se agrego registro de Nuevo Nacido")
