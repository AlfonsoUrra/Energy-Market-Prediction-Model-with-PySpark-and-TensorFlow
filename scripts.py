import keras
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras import layers




st.title("Price predictor")
st.header("Predicting the price of a energy in Spain")


# Ruta relativa del archivo CSV
archivo_csv = "Data/df_scripts.csv"  # Usamos "/" en lugar de "\" para las rutas en sistemas Unix

# Intenta cargar el archivo CSV
try:
    df = pd.read_csv(archivo_csv)
    # Selector de fechas
    df['datetime'] = pd.to_datetime(df['datetime'])
    fecha_minima = df['datetime'].min()
    fecha_maxima = df['datetime'].max()

    # Valor predeterminado dentro del rango de fechas permitido
    fecha_inicio_predeterminada = fecha_minima  # Puedes establecer el valor predeterminado como la fecha mínima
    fecha_fin_predeterminada = fecha_maxima  # Puedes establecer el valor predeterminado como la fecha máxima

    fecha_inicio = st.date_input("Fecha de inicio", min_value=fecha_minima.date(), max_value=fecha_maxima.date(), value=fecha_inicio_predeterminada.date())
    fecha_fin = st.date_input("Fecha de fin", min_value=fecha_minima.date(), max_value=fecha_maxima.date(), value=fecha_fin_predeterminada.date())

    # Convertir las fechas seleccionadas a objetos datetime64[ns]
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    # Filtrar el DataFrame por el rango de fechas seleccionado
    df_filtrado = df[(df['datetime'] >= fecha_inicio) & (df['datetime'] <= fecha_fin)]

    # X_train, X_test, y_tain, y_test = train_test_split(df_filtrado['value'], df_filtrado['value'], train_size=0.8, test_size=0.2, random_state=42)
    model = keras.Sequential([layers.Input(shape=(1,)),
                              layers.Dense(50, activation = 'relu'),
                              layers.Dense(1)])
    model.compile(optimizer='adam', loss='mse', metrics = ['mae'])
    model.fit(df_filtrado['value'], df_filtrado['value'], epochs=100, batch_size=32, verbose=0)


    y_pred = model.predict(df_filtrado['value'])

    df_predicciones = pd.DataFrame({'Fecha': df_filtrado['datetime'], 'Valor Predicho': y_pred.flatten()})

    # Mostrar los datos filtrados
    st.subheader("Precios para 2023:")
    st.write(df_predicciones)

    # Crear el gráfico de dispersión de los datos filtrados
    fig, ax = plt.subplots()
    ax.scatter(df_filtrado["datetime"], df_filtrado['value'])
    ax.set_xlabel('Fecha y Hora')
    ax.set_ylabel('Precio')
    ax.set_title('Gráfico de Dispersión de DataFrame Filtrado')

except FileNotFoundError:
    st.write("El archivo CSV no se encuentra en la ruta especificada:", archivo_csv)
except Exception as e:
    st.write("Ocurrió un error al cargar el archivo CSV:", str(e))


try:
    st.write("Gráfica de los datos 2:")

    monthly_avg = df.groupby('Month')['value'].mean().reset_index()

    # Crear el gráfico de dispersión
    fig, ax = plt.subplots()
    ax.bar(monthly_avg['Month'], monthly_avg['value'])

    # Configurar etiquetas y título
    ax.set_xlabel('Mes')
    ax.set_ylabel('Precio Promedio')
    ax.set_title('Precio Promedio Mensual')

    # Rotar las etiquetas del eje X para mejorar la legibilidad
    plt.xticks(rotation=45)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

except FileNotFoundError:
    st.write("El archivo CSV no se encuentra en la ruta especificada:", archivo_csv)
except Exception as e:
    st.write("Ocurrió un error al cargar el archivo CSV:", str(e))