import streamlit as st
import login
import sqlite3 
import pandas as pd
from sqlite3 import Connection
from libraries.library_0200 import *
from streamlit_cookies_controller import CookieController
import time as tm


def dataframeEditableNuevosNacidos():

    # Conexión a la base de datos
    conn = sqlite3.connect("Datos.db", check_same_thread=False)
    cursor = conn.cursor()

    st.title("Listado de Nuevos Nacidos sin Grupo Asignado")

    # Cargar datos de referencia
    grupos_df = pd.read_sql_query("SELECT * FROM T_Grupos", conn)
    estados_df = pd.read_sql_query("SELECT * FROM T_Estado", conn)

    # Cargar datos principales con joins para mostrar nombres
    query = """
    SELECT nn.id, nn.Fecha, nn.Nombre, nn.edad, nn.celular, 
       nn.idGRUPO, g.Grupo, nn.idEstado, e.estado
    FROM T_NuevosNacidos nn
    LEFT JOIN T_Grupos g ON nn.idGRUPO = g.id
    LEFT JOIN T_Estado e ON nn.idEstado = e.id
    where nn.idGRUPO = 1
    """
    nacidos_df = pd.read_sql_query(query, conn)

    # Mapeos para los selectboxes
    grupo_map = dict(zip(grupos_df['Grupo'], grupos_df['Id']))
    estado_map = dict(zip(estados_df['Estado'], estados_df['Id']))
    grupo_reverse_map = {v: k for k, v in grupo_map.items()}
    estado_reverse_map = {v: k for k, v in estado_map.items()}

    # Agregar columnas editables visibles con valores legibles
    nacidos_df['Grupo_editable'] = nacidos_df['idGRUPO'].map(grupo_reverse_map)
    nacidos_df['Estado_editable'] = nacidos_df['idESTADO'].map(estado_reverse_map)

    # Mostrar editor
    edited_df = st.data_editor(
        nacidos_df[['id','FECHA', 'NOMBRE', 'EDAD', 'CELULAR', 'Grupo_editable', 'Estado_editable']],
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Grupo_editable": st.column_config.SelectboxColumn(
                label="Grupo",
                options=list(grupo_map.keys())
            ),
            "Estado_editable": st.column_config.SelectboxColumn(
                label="Estado",
                options=list(estado_map.keys())
            )
        },
        key="editable_table"
    )

    if st.button("Guardar cambios"):
        cambios = 0
        for idx, row in edited_df.iterrows():
            grupo_id = grupo_map[row['Grupo_editable']]
            estado_id = estado_map[row['Estado_editable']]
            cursor.execute("""
                UPDATE T_NuevosNacidos
                SET idGrupo = ?, idEstado = ?
                WHERE id = ?
            """, (grupo_id, estado_id, row['id']))
            cambios += 1
        conn.commit()
        st.success(f"Se actualizaron {cambios} registros correctamente.")
        tm.sleep(1)
        st.rerun()  



archivo=__file__.split("/")[-1]
#archivo=__file__.split("\\")[-1]
#archivo ="0200_NuevosNacidos.py"
login.generarLogin(archivo)
if 'usuario' in st.session_state:
    st.header('Página :orange[ Asignar de responsabilidad Nuevos Nacidos]')
    #sidebar_PaginaNuevosNacidos()
    dataframeEditableNuevosNacidos()



