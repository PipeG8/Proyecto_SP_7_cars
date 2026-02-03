import pandas as pd
import plotly.graph_objects as go  # Importación de plotly.graph_objects como go
import streamlit as st
#liberias para llamar funciones uicacdas en utils 
from src.utils.data_processing import clean_data 


#-------------------------
#1. Cargar los datos y limpiar los datos con base en la columna model 
#-------------------------

URL='https://raw.githubusercontent.com/PipeG8/Proyecto_SP_7_cars/refs/heads/main/vehicles_us.csv'

car_data = pd.read_csv(URL)

car_data_clean=clean_data(car_data)

#obtener la lista de tipos de carro 

types=car_data_clean['type'].unique()

#-------------------------
#2.Titulo y descripción del proyecto 
#-------------------------

st.header('Información de carros')

st.write('Se obtiene la información de carros por modelo y año asi como la información de su odometro,'
         'mendiante analisis se filtara y mostrara graficas de comportamiento del grupo de datos mostrado a continuación ')



tabla_resumen = car_data_clean.head(10) # nos da una breve descripción estadistica del grupo de datos 

st.dataframe(tabla_resumen)


st.subheader("Resumen Estadístico de los Datos")

# Crear un botón en la aplicación Streamlit
hist_button = st.checkbox('Construir un histograma')

# Lógica a ejecutar cuando se hace clic en el botón
if hist_button:
    # Escribir un mensaje en la aplicación
    st.write('Creación de un histograma para el conjunto de datos de anuncios de venta de coches')

    # Crear un histograma utilizando plotly.graph_objects
    # Se crea una figura vacía y luego se añade un rastro de histograma
    fig = go.Figure(data=[go.Histogram(x=car_data_clean['odometer'])])

    # Opcional: Puedes añadir un título al gráfico si lo deseas
    fig.update_layout(title_text='Distribución del Odómetro')

    # Mostrar el gráfico Plotly interactivo en la aplicación Streamlit
    # 'use_container_width=True' ajusta el ancho del gráfico al contenedor
    st.plotly_chart(fig, use_container_width=True)

#crear un boton para apliación streamlit que haga un grafico de dispersion de datos 
dispertion_button = st.button('Construir dispersion')

if dispertion_button:
    # Escribir un mensaje en la aplicación
    st.write('Creación de un grafico de dispersión para el conjunto de datos de anuncios de venta de coches')

    # Crear un scatter plot utilizando plotly.graph_objects
    # Se crea una figura vacía y luego se añade un rastro de scatter
    fig = go.Figure(data=[go.Scatter(x=car_data_clean['odometer'], y=car_data_clean['price'], mode='markers')])

    # Opcional: Puedes añadir un título al gráfico si lo deseas
    fig.update_layout(title_text='Relación entre Odómetro y Precio')

    # Mostrar el gráfico Plotly
    st.plotly_chart(fig, use_container_width=True)