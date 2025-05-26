import streamlit as st
import login
import sqlite3 
import pandas as pd
from sqlite3 import Connection
from libraries.library_0200 import *
from streamlit_cookies_controller import CookieController
# Conexión a la base de datosconn = sqlite3.connect(st.secrets["baseDatos"], check_same_thread=False)cursor = conn.cursor()st.title("Gestión de Nuevos Nacidos")# Cargar datos de referenciagrupos_df = pd.read_sql_query("SELECT * FROM T_Grupos", conn)estados_df = pd.read_sql_query("SELECT * FROM T_Estado", conn)# Cargar datos principales con joins para mostrar nombresquery = """SELECT nn.id, nn.Nombre, nn.edad, nn.celular,        nn.idGRUPO, g.Grupo, nn.idEstado, e.estadoFROM T_NuevosNacidos nnLEFT JOIN T_Grupos g ON nn.idGRUPO = g.idLEFT JOIN T_Estado e ON nn.idEstado = e.id"""nacidos_df = pd.read_sql_query(query, conn)# Mapeos para los selectboxesgrupo_map = dict(zip(grupos_df['Grupo'], grupos_df['Id']))estado_map = dict(zip(estados_df['Estado'], estados_df['Id']))grupo_reverse_map = {v: k for k, v in grupo_map.items()}estado_reverse_map = {v: k for k, v in estado_map.items()}# Agregar columnas editables visibles con valores legiblesnacidos_df['Grupo_editable'] = nacidos_df['idGRUPO'].map(grupo_reverse_map)nacidos_df['Estado_editable'] = nacidos_df['idESTADO'].map(estado_reverse_map)# Mostrar editoredited_df = st.data_editor(    nacidos_df[['id', 'NOMBRE', 'EDAD', 'CELULAR', 'Grupo_editable', 'Estado_editable']],    num_rows="dynamic",    use_container_width=True,    column_config={        "Grupo_editable": st.column_config.SelectboxColumn(            label="Grupo",            options=list(grupo_map.keys())        ),        "Estado_editable": st.column_config.SelectboxColumn(            label="Estado",            options=list(estado_map.keys())        )    },    key="editable_table")# Botón para guardar cambiosif st.button("Guardar cambios"):    cambios = 0    for idx, row in edited_df.iterrows():        grupo_id = grupo_map[row['Grupo_editable']]        estado_id = estado_map[row['Estado_editable']]        cursor.execute("""            UPDATE T_NuevosNacidos            SET idGrupo = ?, idEstado = ?            WHERE id = ?        """, (grupo_id, estado_id, row['id']))        cambios += 1    conn.commit()    st.success(f"Se actualizaron {cambios} registros correctamente.")

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












