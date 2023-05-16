

from fastapi import FastAPI
import pandas as pd

data = pd.read_csv('data_movies.csv')
app = FastAPI()

@app.get("/pelicula_mes")
def peliculas_mes (mes):
    filtro_mes = data[data['month'] == mes]
    resultado = len(filtro_mes)
    return {'mes': mes, 'cantidad': resultado}

@app.get('/peliculas_dia')
def peliculas_dia (dia):
    filtro_dia = data[data['day'] == dia]
    resultado = len(filtro_dia)
    return {'dia': dia, 'cantidad': resultado}

@app.get('/franquicia')
def franquicia (franquicia):
    filtro_franquicia = data[data['belongs_to_collection'] == franquicia]
    resultado = len(filtro_franquicia)
    ganancia_total = filtro_franquicia['revenue'].sum()
    ganancia_promedio = ganancia_total / resultado
    return {'franquicia': franquicia, 'cantidad': resultado,'ganancia_total': ganancia_total, 'ganancia_promedio': ganancia_promedio}

@app.get('/peliculas_pais')
def peliculas_pais (pais):
    filtro_pais = data[data['production_countries'] == pais]
    resultado = len(filtro_pais)
    return {'pais': pais, 'cantidad': resultado}

@app.get('/productoras')
def productoras (productora):
    filtro_productora = data[data['production_companies'] == productora]
    resultado = len(filtro_productora)
    ganancia_total = filtro_productora['revenue'].sum()
    return {'productora': productora, 'ganacia_total': ganancia_total, 'cantidad': resultado}

@app.get('/retorno')
def retorno (pelicula):
    filtro_pelicula = data[data['title'] == pelicula]
    inversion = filtro_pelicula['budget'].item()
    ganancia_total = filtro_pelicula['revenue'].item()
    retorno = filtro_pelicula['return'].item()
    anio = filtro_pelicula['year'].item()
    return {'pelicula': pelicula, 'inversion': inversion, 'ganancia_total': ganancia_total, 'retorno': retorno, 'anio': anio}

movies = pd.read_csv('ml_movies.csv')
from sklearn.preprocessing import OrdinalEncoder
from sklearn.neighbors import NearestNeighbors

k = 6  
knn_model = NearestNeighbors(n_neighbors=k, metric='euclidean')
knn_model.fit(movies[['popularity_encoded']])

@app.get('/recomendaciones')
def get_recommendations(movie_title):
    idx = movies[movies['title'] == movie_title].index[0]
    distances, indices = knn_model.kneighbors(movies.loc[[idx], ['popularity_encoded']])
    top_indices = indices.flatten()[1:k+1]
    recommendations = movies.iloc[top_indices].sort_values('popularity', ascending=False)[['title', 'overview']]

    return recommendations