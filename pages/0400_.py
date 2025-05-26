import streamlit as st
import login

import streamlit as st
import pandas as pd



#archivo=__file__.split("\\")[-1]
archivo=__file__.split("/")[-1]
login.generarLogin(archivo)
if 'usuario' in st.session_state:
    st.header('Página :orange[Asistencia GP]')