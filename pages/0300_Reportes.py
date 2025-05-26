import streamlit as st
import login
import streamlit as st
import pandas as pd
import sqlite3
from sqlite3 import Connection
from libraries.library_0200 import *
from streamlit_cookies_controller import CookieController


#archivo=__file__.split("\\")[-1]
archivo=__file__.split("//")[-1]
login.generarLogin(archivo)
if 'usuario' in st.session_state:
    st.header('Página :orange[Asistencia GP]')

