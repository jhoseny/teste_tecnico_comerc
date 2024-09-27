Este repositório contém os seguintes arquivos:
1) Dockerfile
3) precip_accumulation_v4.py
O script precip_accumulation_v4 faz o download dos dados diários do produto MERGE do CPTEC. Algumas instruções:
- Altere o a variável 'output_dir' para onde desejar salvar os dados MERGE e arquivos .nc;
- É preciso que o usuário escolha os dias de sua preferência e altere as variáveis yy (ano), mm (mês), dd_ini (dia inicial) e dd_end (dia final);
4) requirements.txt
  Esse arquivo contém as bibliotecas utilizadas dentro do script precip_accumulation_v4.py.
5) api_teste_v2.py
  Esse script cria uma API com três endpoints nas rotas: / (homepage), /teste-tecnico/datas-limite e /teste-tecnico/media-bacia/obter. Algumas instruções:
  - Altere o a variável path_arquivos adicionando o caminho dos dados .nc e contornos de bacia (devem estar na mesma pasta);
  - Escolha a bacia e o dia para obter a média, alterando as variáveis bacia_gdf e data;
  - Certifique-se que as libs flask, os, geopandas, rasterstats e rasterio estejam instaladas.

Os três primeiros são necessários para rodar o exercício 1 do teste e o último usado para o exercício 2. 
