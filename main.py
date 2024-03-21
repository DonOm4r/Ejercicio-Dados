import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.sidebar.title("Predicción con Modelos de Regresión")
# Sidebar para la carga del archivo CSV
uploaded_file = st.sidebar.file_uploader("Elige un archivo CSV", type="csv")

# Inicialización de variables
Misdatos = None
predictions = []
RMSE_array = []

def Cal_error(Y_prediction, Y):
    MSE = np.mean(np.square(Y_prediction - Y))
    RMSE = np.sqrt(MSE)
    return (MSE, RMSE)

def create_polynomial_matrices(X, Y, X_sums, XY_products):
    predictions = []  # Inicializamos la lista de predicciones
    for n in range(1, 21):
        # Construimos la matriz
        matrix = np.array([[X_sums[j + i] for j in range(n+1)] for i in range(n+1)])
        vector = np.array([XY_products[z] for z in range(n+1)])
        SL = np.dot(np.linalg.inv(matrix), vector)

        Y_prediction = np.zeros_like(X)  # Inicializamos Y_prediction con la misma forma que X
        for i in range(len(SL)):
            Y_prediction += SL[i] * X**i

        predictions.append((Y_prediction, f"Orden {n}"))

    return predictions

# Verifica si se ha subido un archivo
if uploaded_file is not None:
    Misdatos = pd.read_csv(uploaded_file)
    Misdatos_Array = np.array(Misdatos)
    X = Misdatos_Array[:, 0]
    Y = Misdatos_Array[:, 1]
    X_sums = [sum(X**i) for i in range(0, 41)]
    XY_products = [sum((X**i) * Y) for i in range(21)]

    predictions = create_polynomial_matrices(X, Y, X_sums, XY_products)

    # Sidebar para visualizar la tabla completa
    if st.sidebar.checkbox('Ver tabla completa'):
        # Crear dos columnas
        col1, col2 = st.columns(2)
    
        # Columna para la tabla
        with col1:
          st.title("Tabla")
          st.write(Misdatos)
    
        # Columna para la gráfica
        with col2:
          st.title("Gráfica")
          fig1, ax1 = plt.subplots()
          ax1.plot(X, Y, '*r', label='Datos')
          plt.xlabel('Tiempo')
          plt.ylabel('Temperatura')
          plt.title('Ebullicion de el Agua')
          plt.grid()
          st.pyplot(fig1)

    # Sidebar para ingresar el orden deseado
    orden_deseado = st.sidebar.number_input('Ingresa el orden deseado', min_value=1, max_value=20, value=1, step=1)

    # Función para mostrar la gráfica y el error del orden deseado
    def mostrar_grafica_y_error(orden_deseado, calcular_optimo=False):
        if not predictions:
            st.error("No hay predicciones disponibles. Asegúrate de haber cargado los datos y calculado las predicciones.")
            return

        Y_pred, title = predictions[orden_deseado - 1]
        fig, ax = plt.subplots()
        ax.scatter(X, Y, label='Datos')
        ax.plot(X, Y_pred, '*k', label='Predicción Modelo')
        ax.set_title(f"Modelo de Regresión - Orden {orden_deseado}")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Temperatura")
        st.pyplot(fig)

        # Calcula y muestra el error
        _, RMSE = Cal_error(Y_pred, Y)
        st.write(f'El valor de error RMSE para el orden {orden_deseado} es: ', RMSE)

         # Construir y mostrar la ecuación del modelo
        equation = " + ".join([f"K{i+1}*X^{i}" if i > 0 else f"K{i+1}" for i in range(orden_deseado + 1)])
        st.write(f"La ecuación del modelo de orden {orden_deseado} es: y = {equation}")

        if calcular_optimo:
            RMSE_array.append(RMSE)

    # Si se ingresa un orden, mostrar solo la gráfica de ese orden
    if orden_deseado:
        mostrar_grafica_y_error(orden_deseado)

    # Sidebar para mostrar todos los órdenes
    if st.sidebar.checkbox('Mostrar todos los órdenes'):
        RMSE_array.clear()
        for i in range(1, 21):
            mostrar_grafica_y_error(i, calcular_optimo=True)

        if RMSE_array:
            orden_optimo = np.argmin(RMSE_array) + 1
            st.sidebar.success(
                f'El orden óptimo recomendado es: {orden_optimo} ya que su valor de error RMSE es de: '
                f'{RMSE_array[orden_optimo - 1]} siendo este el más bajo de los modelos calculados.'
            )
        else:
            st.sidebar.error('No se han calculado los valores de RMSE.')