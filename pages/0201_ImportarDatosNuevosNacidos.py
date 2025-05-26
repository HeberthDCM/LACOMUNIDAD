import streamlit as st
import login
import pandas as pd 

from libraries.library_0200 import *

def get_db_connection():
    conn = sqlite3.connect(st.secrets["baseDatos"])  # Nombre de tu base de datos
    conn.row_factory = sqlite3.Row
    return conn


def insert_data(df):
    conn = get_db_connection()
    try:
        # Validar que el DataFrame tenga las columnas correctas
        required_columns = {'FECHA','NOMBRE', 'EDAD', 'CELULAR'}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            st.error(f"Faltan columnas obligatorias: {', '.join(missing)}")
            return False
        
        # Convertir fechas si es necesario
        if not pd.api.types.is_datetime64_any_dtype(df['FECHA']):
            df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce')
            #df['FECHA'] = df['FECHA'].dt.strftime('%Y-%m-%d')
            if df['FECHA'].isnull().any():
                st.error("Algunas fechas no tienen formato válido")
                return False
        
        df['idGRUPO'] = 1
        df['idESTADO'] = 1

        # Insertar datos
        #df.to_sql('personas', conn, if_exists='append', index=False)
        df.to_sql('T_NuevosNacidos', conn, if_exists='append', index=False,dtype={'FECHA': 'DATE'})
        st.success(f"✅ Se insertaron {len(df)} registros correctamente!")
        return True
        
    except Exception as e:
        st.error(f"❌ Error al insertar datos: {str(e)}")
        return False
    finally:
        conn.close()


archivo=__file__.split("\\")[-1]
#archivo ="0200_NuevosNacidos.py"
login.generarLogin(archivo)
if 'usuario' in st.session_state:
    st.header('Página :orange[Importar Excel de Nuevos Nacidos]')
    #sidebar_PaginaNuevosNacidos()
    archivo =st.file_uploader("Cargue el archivo con los datos de los Nuevos Nacidos", type=["xlsx","xls","csv"], accept_multiple_files= False)
    
    if archivo is not None:
        df=pd.read_excel(archivo)
        st.dataframe(df) 
        if st.button("Insertar datos del archivo"):
            if insert_data(df):
                st.session_state.file_uploaded = None
                st.rerun()