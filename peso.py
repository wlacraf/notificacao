import streamlit as st
import pandas as pd
import pydeck as pdk

# Carrega o DataFrame a partir de um arquivo CSV
def carregar_dados(nome_arquivo):
    return pd.read_csv(nome_arquivo, encoding='latin1',engine='python')

# Titulo do aplicativo
st.title("Mapa de Localização das Notificações")
col1, col2, col3, col4 = st.columns(4)
with col2:
 st.write("by Eng Wagner Cunha")
with col3:
 st.write("PMAC")

# Carrega os dados
nome_arquivo = 'notificacao.csv'
df = carregar_dados(nome_arquivo)

# Assegura que LAT e LON são numéricos
df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
df['LON'] = pd.to_numeric(df['LON'], errors='coerce')

# Converte 'Peso' para um valor numérico (ajuste conforme necessário)
df['Peso'] = pd.to_numeric(df['Peso'], errors='coerce').fillna(0)

# Normaliza o Peso para o tamanho do raio (ajuste a fórmula conforme necessário)
df['radius'] = df['Peso'] * 50  # Exemplo de ajuste de tamanho

# Gera uma coluna de cor baseada no Peso
# Exemplo: varia de azul (menor peso) para vermelho (maior peso)
max_peso = df['Peso'].max()
df['color'] = df['Peso'].apply(lambda x: [int(x/max_peso * 255), 20, 150, 140])

# Define a camada para o mapa
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position=["LON", "LAT"],
    get_color="color",  # Usa a coluna 'color' para a cor do ponto
    get_radius="radius",  # Usa a coluna 'radius' ajustada para o tamanho do ponto
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
)

# Define as configurações do mapa
view_state = pdk.ViewState(latitude=-22.973356, longitude=-42.025602, zoom=13.5)

# Configuração do tooltip
tooltip = {
    "html": "{Name}",  # Exibe o valor do Peso no tooltip
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
    }
}

# Renderiza o mapa com a camada definida e o tooltip configurado
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/satellite-streets-v11",
    tooltip=tooltip
))
