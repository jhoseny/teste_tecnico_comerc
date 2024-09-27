"""
TESTE TÉCNICO COMERC - JHOSENY SOUZA SANTOS
"""
############################# IMPORTANDO AS BIBLIOTECAS ##############################
import requests as req
from bs4 import BeautifulSoup
import numpy as np
import xarray as xr
import cfgrib
import os

################################################# ENTRADAS ######################################################

output_dir = '/output' # caminho de onde os arquivos devem ser salvos
yy = 2024  # ano de download desejado
mm = 1  # mês de download desejado
dd_ini = 1  # dia inicial de download desejado
dd_end = 5  # dia final de download desejado

############################# DECLARANDO A FUNÇÃO PRINCIPAL ##########################
def main(output_dir):

    ############## DOWNLOAD DOS DADOS ###########
    url_base = 'https://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/HOURLY/' # url da "raiz" dos dados horários

    # Criando a lista de dias no formato 'YYYY/MM/DD'
    dias = [f'{yy}/{str(mm).zfill(2)}/{str(dia).zfill(2)}' for dia in range(dd_ini, dd_end + 1)]

    print(f'Dias escolhidos para download {dias}')

    hora = np.arange(0, 24, 1)  # vetor com as horas do dia

    for i in range(0, len(dias)):  # loop para acessar as pastas dos dias escolhidos para download
        url_full = url_base + dias[i] + '/'  # URL completa da pasta do dia
        page = req.get(url_full)  # Acessando a página
        # acessando o conteudo da página
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.find_all('a')  # pegando os links dos arquivos da página

        for link in links:  # loop dos links
            file_name = link.get('href')
            # verificando se o arquivo tem extensão .grib
            if file_name.endswith('.grib2'):
                for h in hora:
                    if f"{str(h).zfill(2)}" in file_name:
                        file_url = url_full + file_name
                        print(f"Baixando {file_url}")
                        file_data = req.get(file_url)  # fazendo download
                        local_file_name = os.path.join(output_dir, file_name)
                        with open(local_file_name, 'wb') as file:
                            file.write(file_data.content)  # salvando

    ############### LEITURA E MANIPULAÇÃO DOS DADOS ###############
        
    datas = [dia.replace('/', '') for dia in dias]  # retirando a barra das datas

    # Iterar sobre os dias, sempre indo de 12Z de um dia até 12Z do próximo
    for i in range(0, len(datas)-1):
       precip_dia = 0  # Inicializa o acumulado diário

       # Lista de horas entre 12Z do primeiro dia até 11Z do próximo dia
       horas = list(np.arange(12, 24)) + list(np.arange(0, 12))  # [12-23] + [00-11]

       # Iterar sobre as horas entre os dois arquivos
       for h in horas:
           # Ajustar a mudança de data (arquivos após meia-noite estão no próximo dia)
           if h >= 12:
               filename = f'MERGE_CPTEC_{datas[i]}{h:02d}.grib2'
           else:
               filename = f'MERGE_CPTEC_{datas[i+1]}{h:02d}.grib2'
          
           local_filename = os.path.join(output_dir, filename)  # Criando o caminho completo
            
           # Verifica se o arquivo existe antes de tentar carregá-lo
           if os.path.exists(local_filename):
               print(f"Lendo {filename}")
               ds = xr.load_dataset(local_filename, engine="cfgrib")
               precip = ds['prec']
               precip_dia += precip  # Acumula a precipitação
           else:
               print(f"Arquivo {filename} não encontrado.")

        # Salvando o arquivo em netcdf

       # Salvando o arquivo em netcdf
       precip_dia.to_netcdf(os.path.join(output_dir, f'acumulado_precip_{datas[i]}.nc'))

       print(f"Acumulado de precipitação {datas[i]} foi salvo")
    
    print("Todos os acumulados diários foram salvos no formato NetCDF.")

if __name__ == "__main__":
    main(output_dir)
