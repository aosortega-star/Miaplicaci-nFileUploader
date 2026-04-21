import streamlit as st
import pandas as pd


st.title("Manejo de Dataframes")
st.sidebar.title("Herramientas")

archivo = st.sidebar.file_uploader("Seleccione su archivo")

if archivo is not None:

    st.write("Su archivo ha sido cargado")
    

    if archivo.name.endswith(".csv"):
        datos = pd.read_csv(archivo)
    elif archivo.name.endswith(".xlsx"):
        datos = pd.read_excel(archivo)
      
    st.write(datos)
  
else:
    
    st.write("Cargue el archivo ")
