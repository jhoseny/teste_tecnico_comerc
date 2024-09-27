"""
TESTE TÉCNICO COMERC - JHOSENY SOUZA SANTOS
"""
############################################# IMPORTANDO AS BIBLIOTECAS ############################################

from flask import Flask, jsonify
import os
import geopandas as gpd
from rasterstats import zonal_stats
import rasterio

################################################# ENTRADAS ######################################################

path_arquivos =  'C:/meu_projeto_docker/output' # caminho de onde estão os arquivos
os.chdir(path_arquivos) # entrar na pasta dos arquivos
bacia_gdf = gpd.read_file('jari.shp') # Carregue o shapefile da bacia desejada 
data = '20240103' # selecione a data desejada no formato yyyymmdd
bacia_nome = bacia_gdf['bacia'] # extraindo o nome da bacia do shapefile

################################################# HOME PAGE ######################################################
app = Flask(__name__)
@app.route('/')
def homepage():
    return 'A API do teste tecnico esta no ar. Use a rota /teste-tecnico/datas-limite para obter as datas limites e /teste-tecnico/media-bacia/obter para obter a media da precipitacao do dia e bacia escolhidos!'

############################################## PRIMEIRO ENDPOINT ##################################################

#lista com as datas disponíveis
datas_disponiveis = sorted([f.split('_')[-1].split('.')[0] for f in os.listdir(path_arquivos) if f.endswith('.nc')]) 

@app.route('/teste-tecnico/datas-limite', methods=['GET']) # Retorna o período de dados diários disponíveis
def get_datas_limite():
    if datas_disponiveis:
        data_inicial = datas_disponiveis[0] 
        data_final = datas_disponiveis[-1]
        return jsonify({'Data inicial': data_inicial, 'Data final': data_final})
    
############################################## SEGUNDO ENDPOINT ##################################################

@app.route('/teste-tecnico/media-bacia/obter', methods=['GET']) # Retorna a chuva média em uma bacia para uma data específica

def get_media_bacia():
    # Abrir o arquivo NetCDF
    with rasterio.open(f'acumulado_precip_{data}.nc') as src: #lendo o arquivo .nc da data escolhida
        precip_data = src.read(1)  # Lê a primeira banda
        transform = src.transform  # Obtém a transformação afim
    
    # Obtem a geometria da bacia 
    bacia_geom = bacia_gdf.geometry.values

    # Calcula a média de precipitação sobre a bacia
    stats = zonal_stats(bacia_geom, precip_data, affine=transform, stats="mean", geojson_out=True)

    # Extrai a precipitação média com duas casas decimais
    media_precip = round(stats[0]['properties']['mean'], 2) 

    return jsonify({'Bacia': bacia_nome[0], 'Data (yyyymmdd)': data, 'Precip. Media (mm/dia)': media_precip})

app.run(host='0.0.0.0')

##################################################### FIM #####################################################
