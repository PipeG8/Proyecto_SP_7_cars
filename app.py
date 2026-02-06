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

#Organizar datos cronologicamente a partir de date posted

car_data_clean=car_data_clean.sort_values(by='date_posted',ascending=True)

#obtener mes de cada fecha el minimo y el maximo 
car_data_clean['date_posted']=pd.to_datetime(car_data_clean["date_posted"])
car_data_clean['month']=car_data_clean['date_posted'].dt.month



#-------------------------
#2.Titulo y descripción del proyecto 
#-------------------------

st.header('Información de carros')

st.write('Se obtiene la información de carros por modelo y año, así como la información de su odómetro.'
         ' Una vez tratados, se procede al análisis; se filtrará y mostrará gráficas de comportamiento del grupo de datos mostrado a continuación')


tabla_resumen = car_data_clean.head(10) # primeros 10 datos para tener una vista basica de que estamos analizando 

st.dataframe(tabla_resumen)


st.subheader("Resumen Estadístico de los Datos")

# ----------------------
#3. Crear un botón en la aplicación Streamlit para construir un historgrama de la columna odometer
#------------------------

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

#------------------------
#4.#crear un boton para apliación streamlit que haga un grafico de dispersion de datos que compare la distancia reccorrida con el precio del coche 
#------------------------

 
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

#-----------------------------
#5. Se crean las listas de los topics a analizar
#-----------------------------



car_data_clean['brand']=car_data_clean['model'].str.split(' ').str[0]


types=car_data_clean['type'].unique()

conditions=car_data_clean['condition'].unique()

brands=car_data_clean['brand'].unique()

variables=car_data_clean.columns.to_list()

st.write("## Analisis dinamico para la variables de interes a escoger ")

#------------------------
#6. se crean las ventanas desplegables 
#........................


st.write(
         "Haciendo uso de la lista de verificación y del slider se puede obtener difentes graficos de barras de acuerdo a lo que se necesite")

variable_1= st.selectbox(
    "Variable a analizar ",variables
)

st.write("Elegiste:", variable_1)


#---------------------
#7.se crea la tabla para de grupo a analizar 
#---------------------

minimo=car_data_clean['month'].min()
maximo=car_data_clean['month'].max()
#creación y configuración del slider con base en los meses 
dates= st.slider("month", minimo,maximo,(minimo,maximo),step=1)

date1=dates[0]

date2=dates[1]
#este es filtro del dataframe con base en el slider 
car_data_clean=car_data_clean[(car_data_clean['month']>=date1 )& 
                              (car_data_clean['month']<=date2)
                              ] 

try:
    
    df_var1_var2 = (
        car_data_clean
        .groupby([variable_1])
        .size()
        .reset_index(name='cantidad_carros')
    )
    
    st.write(f"Tabla obtenida para la variable {variable_1} ")
    
    st.dataframe(df_var1_var2,height=250)

  
except Exception as e:
    st.error(f" Error al cargar los datos: {st(e)}")
    st.error(f"Realiza un analisis con las dimensiones correctas")

    # Escribir un mensaje en la aplicación

st.write(f"Se analiza la cantidad de carros para la variable {variable_1} , entre los meses {date1} y el mes {date2}, obteniendo el siguiente grafico.")

#-------------------
#creación de grafico de barras
#..................


fig = go.Figure(
    data=[
        go.Bar(
            x=df_var1_var2[variable_1],
            y=df_var1_var2['cantidad_carros']
        )
    ]
)

fig.update_layout(
    title_text=f'Cantidad de carros por {variable_1}',
    xaxis_title=variable_1,
    yaxis_title='Cantidad de carros'
)

st.plotly_chart(fig, use_container_width=True)

