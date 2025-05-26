import streamlit as st
import login

from libraries.library_0200 import *
from forms.form_0200_NuevosNacidos import *


archivo=__file__.split("\\")[-1]
#archivo ="0200_NuevosNacidos.py"
login.generarLogin(archivo)

if 'usuario' in st.session_state:
    st.header('Página :orange[Registro de Nuevos Nacidos]')
    #sidebar_PaginaNuevosNacidos()
    
    st.write("Registre al nuevo nacido")
    frmRegistroNuevoNacido()
