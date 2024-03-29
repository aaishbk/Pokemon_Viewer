import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import requests

st.title("Pokemon Explorer!")


def get_details(poke_number):
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
        response = requests.get(url)
        pokemon = response.json()
        name = pokemon['name']
        height = pokemon['height'] * 10 # Converts height into cm
        weight = pokemon['weight'] / 10 # Converts to kg
        front_default = pokemon['sprites']['other']['official-artwork']['front_default']
        audio_url = pokemon['cries']['latest']  # Access the correct key for audio URL
        types = [type_info['type']['name'] for type_info in pokemon['types']]
        moves = len(pokemon['moves'])
        return name, height, weight, front_default, audio_url, types, moves
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return 'Error', np.NaN, np.NaN, None, None, None, np.NaN

pokemon_num = st.slider("Pick a Pokemon ", min_value=1, max_value=1025)

name, height, weight, front_default, audio_url, types, moves = get_details(pokemon_num)

# Height dataframe
height_data = pd.DataFrame({'Pokemon': ['Weedle', name.title(), 'Victreebel'],
                            'Heights': [30, height, 170]})
# Weight dataframe
weight_data = pd.DataFrame({'Pokemon': ['Weedle', name.title(), 'Victreebel'],
                            'Weights': [32, weight, 155]})

# Bar Graph Configurations
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

h_colors = ['grey']
w_colors = ['grey']

h_graph = sns.barplot(data=height_data,
                      x='Pokemon',
                      y='Heights',
                      palette=h_colors,
                      ax=ax1)

w_graph = sns.barplot(data=weight_data, 
                      x='Pokemon',
                      y='Weights',
                      palette=w_colors,
                      ax=ax2)

for p in h_graph.patches:
    h_graph.annotate(f"{p.get_height()}cm",
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center',
                     va='center',
                     xytext=(0, 5),
                     textcoords='offset points')

for p in w_graph.patches:
    w_graph.annotate(f"{p.get_height()}kg",
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center',
                     va='center',
                     xytext=(0, 5),
                     textcoords='offset points')
    
#Change container color based on type
color_map = {'normal': 'grey', 
             'fire': 'orange', 
             'water': 'deepskyblue', 
             'electric': 'yellow',
             'grass': 'green', 
             'ice': 'lightcyan', 
             'fighting': 'red', 
             'poison': 'purple',
             'ground': 'darkgoldenrod', 
             'flying': 'mediumpurple', 
             'psychic': 'pink', 
             'bug': 'olive',
             'rock': 'brown', 
             'ghost': 'purple', 
             'dragon': 'indigo', 
             'dark': 'black',
             'steel': 'lightslategrey', 
             'fairy': 'pink'}

# Get the color of the first type
first_type = types[0] if types else None
type_color = color_map.get(first_type, 'blue')

# Apply color to the bars
h_graph.patches[1].set_facecolor(type_color)
w_graph.patches[1].set_facecolor(type_color)
    
# Sets x and y axis names as blank to not show Pokemon
ax1.set_title('Height')
ax2.set_title('Weight')
h_graph.set_xlabel('')
w_graph.set_xlabel('')

# Display Details
st.write(f'Name: {name.title()}')
st.write(f'Height: {height}cm')
st.write(f'Weight: {weight}kg')
st.write(f'Move Count: {moves}')
st.write(f'ID: {pokemon_num}')
st.write("Type:")
types_con = st.container()
with types_con:
    for pokemon_type in types:
        if pokemon_type in color_map:
            type_color = color_map[pokemon_type]
        else:
            type_color = 'grey'
        st.markdown(f'<div style="background-color:{type_color};padding:5px;border-radius:5px;">{pokemon_type.title()}</div>', unsafe_allow_html=True)
        

# Image display
st.markdown("<h1 style='text-align: center;'>Pokemon</h1>", unsafe_allow_html=True)
st.image(front_default, caption=f'Pokemon: {name}')

st.write(f'Pokemon Cry:')
st.audio(audio_url, format='audio/wav')

# Display graph
st.pyplot(fig)
