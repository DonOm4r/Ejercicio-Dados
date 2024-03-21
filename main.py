import streamlit as st
import matplotlib.pyplot as plt

# Función para inicializar la tabla de probabilidades
def iniciar_tabla_prob(num_dados):
    max_sum = 6 * num_dados + 1
    tabla_prob = [[0] * max_sum for _ in range(num_dados + 1)]
    for i in range(1, 7):
        tabla_prob[1][i] = 1
    return tabla_prob

# Función para rellenar la tabla de probabilidades
def llenar_tabla_prob(tabla_prob, num_dados):
    for dado in range(2, num_dados + 1):
        for sum_val in range(dado, 6 * dado + 1):
            for dice_face in range(1, 7):
                if sum_val - dice_face >= dado - 1:
                    tabla_prob[dado][sum_val] += tabla_prob[dado - 1][sum_val - dice_face]

# Función para calcular las probabilidades
def calcular_probabilidades(tabla_prob, num_dados):
    total_combinations = 6 ** num_dados
    probabilities = dict()
    for sum_val in range(num_dados, 6 * num_dados + 1):
        probabilities[sum_val] = (tabla_prob[num_dados][sum_val] / total_combinations) * 100
    return probabilities

# Función que engloba todo el proceso
def probabilities(num_dados):
    tabla_prob = iniciar_tabla_prob(num_dados)
    llenar_tabla_prob(tabla_prob, num_dados)
    return calcular_probabilidades(tabla_prob, num_dados)


# Streamlit App
def main():
    
    background_image = f"""
        <style>
        .stApp {{
            background-image: url("https://downloadhdwallpapers.in/wp-content/uploads/2018/06/Rolling-Dice-Gif-Hot-Cute-Love.gif");
            background-size: cover;
        }}
        </style>
        """


    st.markdown(background_image, unsafe_allow_html=True)
    st.title('Probabilidades de Sumas de Dados')

    # Usuario puede ingresar el número de dados
    num_dados = st.number_input('Ingrese el número de dados', min_value=1, value=1, step=1)

    # Inicializar la 'num_dados' en st.session_state si aún no se ha hecho
    if 'num_dados' not in st.session_state:
        st.session_state['num_dados'] = num_dados

    # Comprobar si las probabilidades para el nuevo número de dados deben calcularse
    calculate_button = st.button('Calcular Probabilidades')
    if calculate_button or st.session_state['num_dados'] != num_dados:
        with st.spinner('Calculando...'):
            probs = probabilities(num_dados)
            st.session_state['probs'] = probs
            st.session_state['num_dados'] = num_dados
            st.session_state['calculate_pressed'] = True
            # Mostrar probabilidades en la aplicación
            st.sidebar.subheader('Probabilidades por suma de resultado:')
            for sum_val, prob in probs.items():
                st.sidebar.write(f"Suma {sum_val}: {prob:.4f}")

    # Mostrar el gráfico si se ha calculado la distribución de probabilidades.
    if 'probs' in st.session_state and st.session_state.get('calculate_pressed', False):
        st.subheader('Distribución de probabilidades:')
        fig, ax = plt.subplots()
        ax.bar(st.session_state['probs'].keys(), st.session_state['probs'].values())
        ax.set_xlabel('Suma de los dados')
        ax.set_ylabel('Probabilidad')
        ax.set_title('Lanzamiento de dados')
        st.pyplot(fig)

    # Sección para calcular la probabilidad de una suma específica.
    specific_sum_container = st.empty()
    specific_sum = specific_sum_container.number_input(
        'Ingrese una suma específica', 
        min_value=num_dados, 
        max_value=6*num_dados, 
        step=1, 
        key='specific_sum'
    )

    if st.button('Calcular Probabilidad para Suma Específica') and 'probs' in st.session_state:
        probability = st.session_state['probs'].get(specific_sum, 0)
        st.write(f"La probabilidad de obtener una suma de {specific_sum} es: {probability:.4f}")

# Correr la aplicación
if __name__ == "__main__":
    main()