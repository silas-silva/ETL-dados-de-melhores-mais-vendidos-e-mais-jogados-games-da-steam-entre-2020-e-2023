"""
Módulo principal: Fornece funcionalidades para extrair dados das páginas HTML, transformá-los e salvá-los em arquivos CSV.

Funções:
    extract_and_transform: Extrai dados das páginas HTML e os transforma, salvando-os em um arquivo JSON.
    get_csvs: Carrega os dados do arquivo JSON e os converte em strings formatadas em CSV.
    save_csv: Salva uma string formatada em CSV em um arquivo CSV.
    get_and_save_csv: Obtém os dados convertidos em CSV e os salva em arquivos CSV.
"""

import os
import json
import csv
from transform.html_transform import HtmlTransform
from load.load_dados import LoadDados


def extract_and_transform():
    """
    Extrai dados das páginas HTML e os transforma, salvando-os em um arquivo JSON.
    """
    transform = HtmlTransform()
    transform.get_lists_per_year()
    transform.fill_lists_with_game_information()
    # Salvando o dicionário como um arquivo JSON com codificação UTF-8
    with open("../arquivos/data.json", "w", encoding="utf-8") as arquivo:
        json.dump(transform.return_set_data(), arquivo, ensure_ascii=False, indent=4)
    transform.quit_transform()

def get_csvs():
    """
    Carrega os dados do arquivo JSON e os converte em strings formatadas em CSV.

    Returns:
        List[str]: Lista contendo as strings formatadas em CSV para os jogos mais vendidos, melhores lançamentos e mais jogados.
    """
    dados = {}
    with open('../arquivos/data.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    load_data = LoadDados()
    best_sellers_csv = load_data.load_data_best_sellers_csv(dados['best sellers'])
    best_releases_csv = load_data.load_data_best_releases_csv(dados['best releases'])
    most_played_csv = load_data.load_data_most_played_csv(dados['most played'])
    dados = None
    return [best_sellers_csv, best_releases_csv, most_played_csv]

def save_csv(name_csv, string_for_save):
    """
    Salva uma string formatada em CSV em um arquivo CSV.

    Args:
        name_csv (str): Nome do arquivo CSV a ser salvo.
        string_for_save (str): String formatada em CSV a ser salva no arquivo.
    """
    rows = string_for_save.split('\n') # Dividindo a string em linhas
    with open(f'../arquivos/{name_csv}.csv', 'w', newline='', encoding='utf-8') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv, delimiter=';')
        for row in rows:
            if row == "":
                continue
            colunas = row.split(';')
            escritor_csv.writerow(colunas)

def get_and_save_csv():
    """
    Obtém os dados convertidos em CSV e os salva em arquivos CSV.
    """
    csvs = get_csvs()
    #print(csvs)
    save_csv('best_sellers', csvs[0])
    save_csv('best_releases', csvs[1])
    save_csv('most_played', csvs[2])

# Verificar se o arquivo dados.json existe
if not os.path.exists('../arquivos/data.json'):
    # O arquivo dados.json não existe, extrai-lo
    extract_and_transform()
    get_and_save_csv()

else:
    # arquivo existente
    get_and_save_csv()
