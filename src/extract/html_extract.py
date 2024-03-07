"""
Módulo html_extractor: Fornece métodos para extrair informações de páginas HTML.

Este módulo contém a classe HtmlExtractor, que oferece métodos para extrair informações específicas de páginas HTML, 
como os nomes e links dos jogos mais vendidos, mais jogados e melhores lançamentos, 
bem como os gêneros de um jogo específico e verificações de página de jogo.

Classes:
    HtmlExtractor: Uma classe que fornece métodos para extrair informações de páginas HTML.

"""
import re
from typing import Dict, List
from bs4 import BeautifulSoup


class HtmlExtractor:
    """
    Classe HtmlExtractor: Fornece métodos para extrair informações de páginas HTML.

    Methods:
        extract_games_best_sellers: Extrai nomes e links dos jogos mais vendidos em cada ano.
        extract_games_most_played: Extrai nomes e links dos jogos mais jogados em cada ano.
        extract_games_best_releases: Extrai nomes e links dos jogos que tiveram melhores lançamentos em cada ano.
        extract_game_information: Extrai os gêneros de um jogo a partir de sua página HTML.
        verify_page_game: Verifica se uma página de jogo contém uma mensagem de aviso de idade.
    """

    def extract_games_best_sellers(self, html : str) -> Dict[str, Dict]:
        """
        Extração dos nomes e links dos jogos mais vendidos em cada ano.

        Args:
            html (str): HTML para extração das informações.

        Returns:
            Dict: Dicionário contendo nomes e URLs dos jogos mais vendidos em cada ano.
                Exemplo:
                {
                    'Platinum': {'nome_game': 'url', ...},
                    ...
                }
        """
        # Pegar separado por platina, ouro, prata e bronze
        class_groups = {
            'class_groups': "_2NfLqUpH_h0Ba0jlv9M9ZE", 
            'class_name_group': "_3FRxVBrTtFQLhmHRstBbC_", 
            'class_game_card': "_2yyhUHhk3d1DRpG4Sx9_og",
            'class_game_image':  "cODQhXeXS-Yn-vLIBNwyW"
            }
        soup = BeautifulSoup(html, 'html.parser')
        groups_games_list = soup.find_all(class_=class_groups['class_groups'])
        groups_games_items = {}
        for group in groups_games_list:
            aux = group.find(class_=class_groups['class_name_group'])
            if aux:
                pass
            else:
                name_group = aux.text
                if name_group == "Platina":
                    name_group =  "Platinum"
                if name_group == "Ouro":
                    name_group =  "Gold"
                if name_group == "Prata":
                    name_group =  "Silver"
                if name_group == "Bronze":
                    name_group =  "Bronze"
                groups_games_items[name_group] = {}
                list_games = group.find_all(class_=class_groups['class_game_card'])
                # para cada game
                for game in list_games:
                    name_game = game.find(class_=class_groups['class_game_image']).get('alt')
                    link_game = game.find('a').get('href')
                    groups_games_items[name_group][name_game] = link_game
        return groups_games_items


    def extract_games_most_played(self, html : str) -> Dict[str, Dict]:
        """
        Extração dos nomes e links dos jogos mais jogados em cada ano.

        Args:
            html (str): HTML para extração das informações.

        Returns:
            Dict: Dicionário contendo nomes e URLs dos jogos mais jogados em cada ano.
                Exemplo:
                {
                    'Platinum': {'nome_game': 'url', ...},
                    ...
                }
        """
        # Pegar separado por quantidade de jogadores simultaneos
        class_groups = {
            'class_groups': "_2NfLqUpH_h0Ba0jlv9M9ZE", 
            'class_name_group': "_3FRxVBrTtFQLhmHRstBbC_", 
            'class_game_card': "_2yyhUHhk3d1DRpG4Sx9_og",
            'class_game_image':  "cODQhXeXS-Yn-vLIBNwyW"
            }
        soup = BeautifulSoup(html, 'html.parser')
        groups_games_list = soup.find_all(class_=class_groups)
        groups_games_items = {}
        for group in groups_games_list:
            aux = group.find(class_=class_groups['class_name_group'])
            if aux:
                pass
            else:
                name_group = aux.text
                # Usando expressão regular para encontrar o número na string
                match = re.search(r'\d+', name_group)
                if match:
                    # Extrair o número encontrado
                    number_str = match.group()
                    # Remover vírgulas se houver
                    name_group = f"{number_str.replace(',', '.')}000"
                groups_games_items[name_group] = {}
                list_games = group.find_all(class_=class_groups['class_game_card'])
                # para cada game
                for game in list_games:
                    name_game = game.find(class_=class_groups['class_game_image']).get('alt')
                    link_game = game.find('a').get('href')
                    groups_games_items[name_group][name_game] = link_game
        return groups_games_items

    def extract_games_best_releases(self, html : str, year : int) -> Dict[str, Dict]:
        """
        Extração dos nomes e links dos jogos que tiveram melhores lançamentos em um ano específico.

        Args:
            html (str): HTML para extração das informações.
            year (int): Ano referente à página HTML.

        Returns:
            Dict: Dicionário contendo nomes e URLs dos jogos que tiveram melhores lançamentos no ano especificado.
                Exemplo:
                {
                    'Platinum': {'nome_game': 'url', ...},
                    ...
                }
        """
        class_groups = {
            'class_groups': "_2NfLqUpH_h0Ba0jlv9M9ZE", 
            'class_name_group': "_3FRxVBrTtFQLhmHRstBbC_", 
            'class_game_card': "_2yyhUHhk3d1DRpG4Sx9_og",
            'class_game_image':  "cODQhXeXS-Yn-vLIBNwyW"
        }
        groups_remove = {
                    "grups_not_extract_2020": ["January", "February", "March", "April", "May", "June",
                             "July", "August", "September", "October", "November", "December", "Top New Releases By Month"],
                    "grups_not_extract_2021": ["Top New Releases By Month"]
        }
        soup = BeautifulSoup(html, 'html.parser')
        groups_games_list = soup.find_all(class_=class_groups['class_groups'])
        groups_games_items = {}
        for group in groups_games_list:
            aux = group.find(class_=class_groups['class_name_group'])
            if not aux:
                name_group = aux.text
                if year == "2020":
                    if name_group == "Top New Releases of 2020":
                        name_group = "Platinum"
                    if name_group in groups_remove['grups_not_extract_2020']:
                        continue
                if year == "2021":
                    if name_group in groups_remove['grups_not_extract_2021']:
                        continue
                if year == "2023":
                    if name_group == "Platina":
                        name_group =  "Platinum"
                    if name_group == "Ouro":
                        name_group =  "Gold"
                    if name_group == "Prata":
                        name_group =  "Silver"
                groups_games_items[name_group] = {}
                list_games = group.find_all(class_=class_groups['class_game_card'])
                # para cada game
                for game in list_games:
                    name_game = game.find(class_=class_groups['class_game_image']).get('alt')
                    link_game = game.find('a').get('href')
                    groups_games_items[name_group][name_game] = link_game
        return groups_games_items

    def extract_game_information(self, html: str) -> List[str]:
        """
        Extração dos gêneros de um jogo a partir de sua página HTML.

        Args:
            html (str): HTML da página do jogo.

        Returns:
            List[str]: Lista com os gêneros do jogo.
        """
        # Parse the HTML content
        soup = BeautifulSoup(html, 'html.parser')
        # Initialize an empty dictionary
        genres = []
        # Find the genre
        genre_element = soup.find('b', text='Genre:')
        if genre_element:
            genres_span = genre_element.find_next_sibling('span')
            #print(genres_span)
            genres = [genre.text.strip() for genre in genres_span.find_all('a')]
        return genres

    def verify_page_game(self, html: str) -> Dict:
        """
        Verifica se uma página de jogo contém uma mensagem de aviso.

        Args:
            html (str): HTML da página do jogo.

        Returns:
            bool: True se a página não contém mensagem de aviso, False caso contrário.
        """
        # Parse the HTML content
        soup = BeautifulSoup(html, 'html.parser')
        # Check if the message is present
        texto = 'Please enter your birth date to continue:'
        warning_message = soup.find('div', text=texto)
        if warning_message:
            return False
        return True
