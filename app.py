import streamlit as st 
#import matplotlib.pyplot as plt
import plotly.express as px
import jinja2
import pandas as pd
import numpy as np
import math
import re
import io

pd.options.future.infer_string = True

columnas=["id","perc_premium_paid_by_cash_credit","age_in_days","Income","Count_3-6_months_late",
          "Count_6-12_months_late","Count_more_than_12_months_late","application_underwriting_score",
          "no_of_premiums_paid","sourcing_channel,residence_area_type","premium","renewal"]

if 'df_res' not in st.session_state:
    st.session_state.df_res = pd.DataFrame(columns=columnas)


# Inicialización de estado en Streamlit
st.title("📊 Proyecto - Streamlit")

# Menú de navegación
opcion = st.sidebar.selectbox("Selecciona una acción", ["Home", "Carga del Dataset"])

# Agregar nueva actividad
if opcion == "Home":
    #st.subheader("➕ Agregar Nueva Actividad")
    titulo = "Analisis Exploratorio de Datos (EDA)"
    
    st.image("logo_aos.png", width =150)
    st.subheader(titulo)
    st.markdown("**Nombre: Alex Arturo Ortega Soto**")
    st.write("    ")
    st.markdown(":blue[Este proyecto realizar un analisis profundo de dataset de TelcoCustomerChurn]")
    st.markdown("""
                **Curso: Esp. Python ed.57**: 
                - Año: 2026
                
                - El dataset contiene información de una TELCO con la finalidad de realizar un analisis
                  profundo para entender la fuga de clientes y mejorar la retención de los mismos
                  
                  Tecnologias usadas:
                  - Python, Streamlit, Pandas, NumPy
                """)
    
elif opcion == "Carga del Dataset":
    st.markdown(":blue[Ejercicio 1]")
    st.markdown("""
                **Aplicar y demostrar el uso de dataframe y captura de datos
                  
                """)    

    uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.df_res = df
        #st.rerun()
        #st.write(df)
        st.write("Archivo Cargado correctamente")
        filas, columnas = st.session_state.df_res.shape

        # Opción 1: Texto simple con st.write
        st.write(f"El dataset tiene {filas} filas y {columnas} columnas.")
        #df['TotalCharges'] = df['TotalCharges'].astype(float)
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df['SeniorCitizen'] = df['SeniorCitizen'].astype(str)

        limites0 = [0, 35.5, 70.35, 89.85, np.inf]        
        etiquetas0 = ["Renta Baja", "Renta Media", "Renta Alta", "Renta Muy Alta"]
        #df["Rango_renta"] = pd.qcut(df["MonthlyCharges"], q=4, 
        #    labels=["Renta Baja (Q1)", "Renta Media (Q2)", "Renta Alta (Q3)", "Renta Muy Alta (Q4)"]
        #        )
        df["Rango_renta"] = pd.cut(
            df["MonthlyCharges"], 
            bins=limites0, 
            labels=etiquetas0, 
            right=False  # Incluye el límite inferior y excluye el superior (ej: [0, 50) )
        )        
        limites = [0, 401.45, 3795, np.inf]
        # 2. Definir las etiquetas correspondientes
        etiquetas = ["Factura Baja", "Factura Media", "Factura Alta"]
        df["Rango_facturacion"] = pd.cut(
            df["TotalCharges"], 
            bins=limites, 
            labels=etiquetas, 
            right=False  # Incluye el límite inferior y excluye el superior (ej: [0, 50) )
        )
        st.session_state.df_res = df        
        #df["Rango_facturacion"] = pd.qcut(df["TotalCharges"], q=3, 
        #    labels=["Factura Baja (T1)", "Factura Media (T2)", "Factura Alta (T3)"]
        #        )


        # Mostrar los datos debajo
        st.dataframe(st.session_state.df_res.head())    
        
        # Opción 2: Tarjetas visuales interactivas (Recomendado)
        col1, col2 = st.columns(2)
        col1.metric(label="Número de Filas", value=filas)
        col2.metric(label="Número de Columnas", value=columnas)
        st.markdown("""
            <style>
            /* Permite que el contenedor de pestañas envuelva los elementos en varias filas */
            div[data-testid="stTabs"] button {
                flex-wrap: wrap !important;
            }
            div[data-testid="stTabs"] [role="tablist"] {
                flex-wrap: wrap !important;
                gap: 4px; /* Espacio opcional entre filas de pestañas */
            }
            </style>
        """, unsafe_allow_html=True)
                
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10  = st.tabs(["🎉 Información del Dataset", 
            "📁 Clasificación variables", 
            "📊 Estadistica Descriptiva", 
            "🎉 Análisis de valores faltantes", 
            "🔢 Distribución de variables numéricas", 
            "🔤 Analisis de variables categóricas", 
            "⚙️ Análisis (numérico vs categórico)", 
            "⚙️ Análisis (categórico vs categórico)",
            "📊 Análisis basado en parámetros seleccionados", 
            "🔍 Hallazgos claves"])
        
        with tab1:
          st.header("Vista de información general del dataset")
          st.write("")
          st.write("Información del dataframe :")
          buffer = io.StringIO()
          df.info(buf=buffer)
          s = buffer.getvalue()
          lineas = s.split("\n")
          datos_filas = []
          for linea in lineas:
            match = re.match(r"^\s*(\d+)\s+(.+?)\s+(\d+)\s+non-null\s+(.+)$", linea.strip()
                             )
            if match:
              
                datos_filas.append(
                    {"Id": match.group(1).strip(), 
                        "Columna": match.group(2).strip(),
                        "No Nulos": int(match.group(3)),
                        "Tipo": match.group(4).strip(),
                    })

# 3. Crear un DataFrame limpio con los resultados del buffer
          df_info_tabulado = pd.DataFrame(datos_filas)
          st.dataframe(df_info_tabulado)
          st.write("Información del dataframe de Telecom")
          st.write(s)
          st.write(" ")
          st.write("Cantidad de Valores Nulos:")
          st.dataframe(st.session_state.df_res.isnull().sum())
          st.write(df)
          
        with tab2:
          st.header("Clasificación de variables")
          st.write("Esta sección permite identificar los tipos de variables que tenemos en el dataset")
          st.write("asi como tambien un analisis de cada variable del dataset")
          st.write("Identificación de variables:")
          df = st.session_state.df_res
          columnas_numericas = df.select_dtypes(include=["number"]).columns.tolist()
          columnas_categoricas = df.select_dtypes(include=["object", "category","bool"]).columns.tolist()
          #columnas_categoricas = df.select_dtypes(include=["category", "bool"]).columns.tolist()
          col1, col2 = st.columns(2)
          with col1:
            st.subheader(f"🔢 Numéricas ({len(columnas_numericas)})")
            if columnas_numericas:
                for col in columnas_numericas:
                    st.write(f"- **{col}** (`{df[col].dtype}`)")
            else:
                st.info("No se encontraron variables numéricas.")

          with col2:
            st.subheader(f"🔤 Categóricas ({len(columnas_categoricas)})")
            if columnas_categoricas:
              for col in columnas_categoricas:
                  st.write(f"- **{col}** (`{df[col].dtype}`)")
            else:
                  st.info("No se encontraron variables categóricas.")

          df = st.session_state.df_res

          todas_columnas = df.columns.tolist()
          if st.checkbox("Mostrar conteo de columnas"):
            col_a_cambiar = st.selectbox(
                "Selecciona la columna:", ["Ninguna"] + todas_columnas
            )
            if col_a_cambiar != "Ninguna":
              if col_a_cambiar in columnas_categoricas:
                st.write("**Frecuencia de categorías (conteo):**")
                st.dataframe(df[col_a_cambiar].value_counts())
              else:
                  st.write("**Resumen estadístico numérico:**")
                  st.dataframe(df[col_a_cambiar].describe())
            else:
                st.info("Por favor, selecciona una columna")
              

        with tab3:
          st.header("Estadistica Descriptiva")
          st.write("Nos permite tener un detalle estadistico completo de cada variable del dataset")
          st.write("con información del tipo cantidad, media, desviación estandar de cada atributo")
          if st.checkbox("Mostrar resumen estadístico"):
            if columnas_numericas:
                st.write("**Resumen Numérico:**")
                st.dataframe(df[columnas_numericas].describe())
            if columnas_categoricas:
                st.write("**Resumen Categórico:**")
                st.dataframe(df[columnas_categoricas].describe(include="all")) 
            
            st.write("La Media nos indica el valor medio central de una variable numérica es el promedio de valores")
            st.write("")
            st.write("La Mediana es el valor central de una conjunto de datos, es muy util cuando tienes valores atipicos ")
            st.write("En el trabajo la media de Tenure es 32.37 y la mediana 29 lo que indica que los valores centrales son muy similares")
            st.write("lo que indica que no existe un mucha diferencia en el punto central. Sin embargo la desviación estandar")            
            st.write("es 24 lo que es un valor muy alto e indica una alta dispersion de valores respecto al centro")            

        with tab4:
          st.header("Análisis de valores faltantes")
          st.write("")
                    
          df_nulos = df.isna().sum().reset_index()
          df_nulos.columns = ["Variable", "Cantidad de Nulos"]

          df_con_nulos = df_nulos[df_nulos["Cantidad de Nulos"] > 0]

          st.subheader("🔍 Reporte de Valores Faltantes")

          if not df_con_nulos.empty:
              st.dataframe(df_con_nulos, use_container_width=True, width='stretch')
          else:
              st.success("🎉 ¡Excelente! No se encontraron valores nulos en el dataset.")          
          
          st.write("")
          st.write("Mostrando valores atipicos en columnas numéricas")
            # 1. Filtrar el DataFrame con las columnas numéricas
          df_num = df.select_dtypes(include="number")

          # 2. Crear el boxplot interactivo usando Plotly
          fig = px.box(df_num, template="plotly_white")

          # 3. Rotar los nombres de las columnas para que se lean perfectamente
          fig.update_xaxes(tickangle=90)

          # 4. Renderizar en Streamlit ocupando todo el ancho disponible
          st.plotly_chart(fig, use_container_width=True,width='stretch')
          
          #st.dataframe(df.select_dtypes(include='number').boxplot(figsize=(20,10), rot=90)) #todas las columnas numericas y muestra los valores atipicos mto_lim_cre_sf
          
          st.write("En el caso de Telecom, no se encuentran valores nulos en el dataset, por lo que no")
          st.write("seria necesario hacer algun tratamiento para eliminarlos o completarlos")
          
        with tab5:
          st.header("Distribución de variables numéricas")
          st.write("")
          columnas_numericas = df.select_dtypes(include=["number"]).columns.tolist()          

          if st.checkbox("Mostrar columnas numéricas"):
            col_a_cambiar = st.selectbox(
                "Selecciona la columna:", ["Ninguna"] + columnas_numericas
            )
            if col_a_cambiar != "Ninguna":
              if col_a_cambiar in columnas_numericas:
                fig = px.histogram(
                        df,
                        x=col_a_cambiar,
                        nbins=30,  # Número de barras
                        title=f"Distribución de {col_a_cambiar}",
                        template="plotly_white",
                    )
                st.plotly_chart(fig, use_container_width=True, width='stretch')
            else:
                st.info("Por favor, selecciona una columna")
          
            st.write("En el caso de la variable Tenure, esta no sigue una distribución normal")
            st.write("lo que se muestra es una campana invertida con picos en los dos extremos puestos")
            st.write("esto demuestra que tenemos un churn temprano bastante importante. Pero tambien ")
            st.write("un grupo de clientes importantes que se mantienen en el tiempo")
            
        with tab6:
          st.header("Análisis de variables categóricas")
          st.write("")
          
          # 1. Identificar y clasificar los tipos de variables
          num_cols = df.select_dtypes(include=["number"]).columns.tolist()
          cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
          bool_cols = df.select_dtypes(include=["bool"]).columns.tolist()
          date_cols = df.select_dtypes(include=["datetime"]).columns.tolist()

          # 2. Construir un DataFrame con los conteos agrupados
          resumen_tipos = pd.DataFrame(
              {
                  "Tipo de Variable": [
                      "Numéricas",
                      "Categorícas/Texto",
                      "Booleanas",
                      "Fechas/Tiempo",
                  ],
                  "Cantidad": [len(num_cols), len(cat_cols), len(bool_cols), len(date_cols)],
              }
          )

          # Filtrar tipos que no tengan ninguna variable para no ensuciar el gráfico
          resumen_tipos = resumen_tipos[resumen_tipos["Cantidad"] > 0]

          # 3. Mostrar métricas rápidas en la parte superior
          st.subheader("📋 Resumen Total")
          st.write(
              f"El dataset contiene un total de **{df.shape[1]}** columnas analizadas."
          )

          # 4. Crear los gráficos interactivos en paralelo (Dos Columnas)
          col_graf1, col_graf2 = st.columns(2)

          with col_graf1:
              st.markdown("### 🔢 Conteo Absoluto")
              fig_bar = px.bar(
                  resumen_tipos,
                  x="Tipo de Variable",
                  y="Cantidad",
                  color="Tipo de Variable",
                  text="Cantidad",
                  template="plotly_white",
                  title="Cantidad de columnas por tipo",
              )
              fig_bar.update_traces(textposition="outside")
              fig_bar.update_layout(showlegend=False)  # Ocultar leyenda redundante en barras
              st.plotly_chart(fig_bar, use_container_width=True,width='stretch')

          with col_graf2:
              st.markdown("### 🍕 Proporción Relativa")
              fig_pie = px.pie(
                  resumen_tipos,
                  names="Tipo de Variable",
                  values="Cantidad",
                  color="Tipo de Variable",
                  hole=0.4,  # Estilo dona para mejor visualización
                  template="plotly_white",
                  title="Distribución porcentual del dataset",
              )
              fig_pie.update_traces(textinfo="percent+label")
              st.plotly_chart(fig_pie, use_container_width=True,width='stretch')
        
        with tab7:
          st.header("Análisis de variables numéricos vs categorico")
          st.write("")          
          columnas_numericas = df.select_dtypes(include=["number"]).columns.tolist()
          columnas_categoricas = df.select_dtypes(
              include=["object", "category", "bool"]
          ).columns.tolist()

          if columnas_numericas and columnas_categoricas:
              # 2. Selectores en la sección central para el cruce de datos
              col_sel1, col_sel2 = st.columns(2)

              with col_sel1:
                  var_num = st.selectbox(
                      "1. Selecciona la Variable Numérica (Eje Y):", columnas_numericas, key='selectbox_t7.1'
                  )

              with col_sel2:
                  var_cat = st.selectbox(
                      "2. Selecciona la Variable Categórica (Eje X):",
                      columnas_categoricas, key='selectbox_t7.2'
                  )

              # 3. Generar el gráfico interactivo bivariado
              st.subheader(f"🔍 Distribución de {var_num} por {var_cat}")

              fig_bivariado = px.box(
                  df,
                  x=var_cat,
                  y=var_num,
                  color=var_cat,  # Diferencia cada categoría con un color único
                  template="plotly_white",
                  points="outliers",  # Muestra los puntos atípicos fuera de las cajas
                  title=f"Gráfico de Cajas: {var_num} según {var_cat}",
              )

              # Mejorar estética de las etiquetas del eje X si son muy largas
              fig_bivariado.update_xaxes(tickangle=45)

              # Mostrar en Streamlit ocupando todo el ancho
              st.plotly_chart(fig_bivariado, use_container_width=True, width='stretch')

              # 4. Tabla de Resumen Estadístico Agrupado (El complemento numérico ideal)
              st.markdown("### 📈 Resumen Estadístico Agrupado")
              st.write(
                  f"Métricas detalladas de la variable **{var_num}** para cada grupo de **{var_cat}**:"
              )

              # Calcular estadísticas agrupadas usando Pandas
              tabla_agrupada = (
                  df.groupby(var_cat)[var_num]
                  .describe()
                  .rename(
                      columns={
                          "count": "Conteo",
                          "mean": "Promedio",
                          "std": "Desv. Estándar",
                          "min": "Mínimo",
                          "25%": "25% (Q1)",
                          "50%": "Mediana (Q2)",
                          "75%": "75% (Q3)",
                          "max": "Máximo",
                      }
                  )
              )

              st.dataframe(tabla_agrupada, use_container_width=True, width='stretch')

          else:
              st.warning(
                  "⚠️ Para realizar un análisis bivariado necesitas tener al menos una columna numérica y una columna categórica en tu dataset."
              )
        with tab8:
          st.header("Análisis de variables categorico vs categorico")
          st.write("")          
          columnas_categoricas = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

          if len(columnas_categoricas) >= 2:
              # 2. Selectores de variables
              col_sel1, col_sel2 = st.columns(2)

              with col_sel1:
                  var_cat1 = st.selectbox(
                      "1. Selecciona la Variable Principal (Eje X):",
                      columnas_categoricas, key='selectbox_t80',
                      index=0,
                  )

              with col_sel2:
                  # Evitamos seleccionar la misma variable en ambos ejes por defecto
                  var_cat2 = st.selectbox(
                      "2. Selecciona la Variable de Agrupación (Color):",
                      columnas_categoricas,key='selectbox_t81',
                      index=1 if len(columnas_categoricas) > 1 else 0,
                  )

              # 3. Gráfico de Barras Cruzadas con Plotly
              st.subheader(f"🔍 Distribución de {var_cat1} según {var_cat2}")

              # Selector para que el usuario elija cómo ver las barras
              tipo_barra = st.radio(
                  "Estilo de gráfico:",
                  ["Barras Agrupadas (Comparar totales)", "Barras Apiladas al 100% (Comparar proporciones)"],
                  horizontal=True,
              )

              if "100%" in tipo_barra:
                  # Crear gráfico apilado al 100%
                  # Primero agrupamos y calculamos porcentajes para que Plotly lo dibuje correctamente
                  df_counts = df.groupby([var_cat1, var_cat2]).size().reset_index(name="Cantidad")
                  fig_cat = px.histogram(
                              df,
                              x=var_cat1,
                              color=var_cat2,
                              barnorm="percent",  # Ahora sí funcionará perfectamente
                              template="plotly_white",
                              title=f"Proporción de {var_cat1} por {var_cat2}",
                          )
                  fig_cat.update_layout(yaxis_title="Porcentaje (%)")
              else:
                  # Crear gráfico tradicional de barras una al lado de la otra
                  fig_cat = px.histogram(
                      df,
                      x=var_cat1,
                      color=var_cat2,
                      barmode="group",
                      template="plotly_white",
                      title=f"Conteo de {var_cat1} agrupado por {var_cat2}",
                  )

              st.plotly_chart(fig_cat, use_container_width=True,width='stretch')

              # 4. Tabla de Contingencia (Crosstab)
              st.markdown("### 📈 Tabla de Contingencia (Frecuencias)")
              st.write("Conteo cruzado exacto entre ambas variables:")

              # Creamos la tabulación cruzada incluyendo los totales (margins=True)
              tabla_contingencia = pd.crosstab(
                  df[var_cat1], df[var_cat2], margins=True, margins_name="Total General"
              )

              st.dataframe(tabla_contingencia, use_container_width=True,width='stretch')

              # 5. Opcional: Tabla de Contingencia en Porcentajes
              if st.checkbox("Ver tabla en porcentajes relativos"):
                  tabla_porcentaje = (
                      pd.crosstab(df[var_cat1], df[var_cat2], normalize="index") * 100
                  ).round(2)
                  tabla_formateada = tabla_porcentaje.astype(str) + "%"
                  st.write("**Porcentaje por cada fila (Base 100% horizontal):**")
                  st.dataframe(tabla_formateada, use_container_width=True)

          else:
              st.warning(
                  "⚠️ Necesitas al menos dos columnas categóricas o de texto en tu dataset para realizar este análisis cruzado."
              )

        with tab9:
          st.header("Análisis basado en parámetros seleccionados")
          st.write("")          
          columnas_numericas = df.select_dtypes(include=["number"]).columns.tolist()
          columnas_categoricas = df.select_dtypes(
              include=["object", "category", "bool"]
          ).columns.tolist()

          if columnas_numericas and columnas_categoricas:
            # 2. Selectores en la sección central para el cruce de datos
            col_sel1, col_sel2 = st.columns(2)

            with col_sel1:
                vars_num = st.multiselect("1. Selecciona las Variables Numéricas:", 
                columnas_numericas, default=[columnas_numericas[0]], key='multiselect_t90')


            with col_sel2:
                var_cat = st.selectbox(
                    "2. Selecciona la Variable Categórica (Eje X):", 
                    columnas_categoricas, key='selectbox_t91'
                )

            # Controlar que el usuario haya seleccionado al menos una variable numérica
            if vars_num:
                # 3. Generar el gráfico interactivo bivariado
                # Convertimos la lista de variables en un texto para el título
                texto_vars = ", ".join(vars_num)
                st.subheader(f"🔍 Distribución de {texto_vars} por {var_cat}")

                # Melt del DataFrame: reestructuramos los datos para que Plotly pinte múltiples cajas
                df_melted = df.melt(id_vars=[var_cat], value_vars=vars_num, var_name="Variable Numérica", value_name="Valor")

                fig_bivariado = px.box(
                    df_melted,
                    x=var_cat,
                    y="Valor",
                    color="Variable Numérica",  # Colorea por el tipo de variable numérica seleccionada
                    template="plotly_white",
                    points="outliers",  
                    title=f"Gráfico de Cajas Múltiple según {var_cat}",
                )

                # Mejorar estética de las etiquetas del eje X si son muy largas
                fig_bivariado.update_xaxes(tickangle=45)

                # Mostrar en Streamlit ocupando todo el ancho
                st.plotly_chart(fig_bivariado, use_container_width=True)

                # 4. Tabla de Resumen Estadístico Agrupado
                st.markdown("### 📈 Resumen Estadístico Agrupado")
                st.write(
                    f"Métricas detalladas para cada grupo de **{var_cat}**:"
                )

                # Calcular estadísticas agrupadas agrupando por Categoría y por cada Variable Numérica
                tabla_agrupada = (
                    df.groupby(var_cat)[vars_num]
                    .describe()
                    .rename(
                        columns={
                            "count": "Conteo",
                            "mean": "Promedio",
                            "std": "Desv. Estándar",
                            "min": "Mínimo",
                            "25%": "25% (Q1)",
                            "50%": "Mediana (Q2)",
                            "75%": "75% (Q3)",
                            "max": "Máximo",
                        }
                    )
                )

                st.dataframe(tabla_agrupada, use_container_width=True)

            else:
                st.warning(
                  "⚠️ Para realizar un análisis bivariado necesitas tener al menos una columna numérica y una columna categórica en tu dataset."
              )              
        with tab10:
          st.header("Hallazgos Clave")
          st.write("Para profundizar en este punto se ha agregado los comentarios en el PDF del trabajo")

  #
  # Contenido de tu requirements.txt
#pandas
#streamlit
#plotly
#jinja2
