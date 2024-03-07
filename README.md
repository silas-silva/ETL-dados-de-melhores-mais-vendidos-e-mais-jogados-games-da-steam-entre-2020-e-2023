# ETL de dados

## Objetivo
- Extrair dados de jogos da Steam entre os anos de 2020 e 2023
    - Extração dos jogos mais vendidos em cada ano
    - Extração dos jogos mais jogaddos em cada ano
    - Extração dos jogos que tiveram os melhores lançamentos em cada ano

## Principais Ferramentas utilizadas:
- Python 
- Pylint
- Selenium
- Git

## Descrição dos dados
- Pasta /src
    - Classes e modulos do ETL
    - Arquivo principal `main.py` para executar o ETL

- Pasta /arquivos
    - Contém um Json com dados da extração
    - Contém 3 arquivos `.csv`
        - best_sellers.csv
        - best_releases.csv
        - most_played.csv

## Como executar em sua Máquina
1. Crie um ambiente virtual
2. Entre no ambiente virtual
3. Execute `pip install -r requirements.txt` para instalar as dependências.
4. Execute o arquivo `src/main.py` para executar a automação.
