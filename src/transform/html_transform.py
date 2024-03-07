"""
Módulo html_transform: Fornece uma classe para transformar os dados obtidos das páginas HTML.

Classes:
    HtmlTransform: Classe para transformar os dados obtidos das páginas HTML.

"""

from dao.dao_get_html import DaoGetHtml
from extract.html_extract import HtmlExtractor

class HtmlTransform():
    """
    Classe HtmlTransform: Fornece métodos para transformar os dados obtidos das páginas HTML.

    Attributes:
        request (DaoGetHtml): Instância de DaoGetHtml para fazer solicitações HTTP e interagir com as páginas HTML.
        extractor (HtmlExtractor): Instância de HtmlExtractor para extrair informações das páginas HTML.
        list_game_best_sellers_page (Dict): Dicionário contendo os URLs das páginas dos jogos mais vendidos por ano.
        list_game_best_releases_page (Dict): Dicionário contendo os URLs das páginas dos melhores lançamentos por ano.
        list_game_most_played_page (Dict): Dicionário contendo os URLs das páginas dos jogos mais jogados por ano.
        lists_games (Dict): Dicionário para armazenar as listas de jogos por categoria e ano.

    Methods:
        get_lists_per_year: Obtém as listas de jogos para cada ano e categoria.
        fill_list_game_information_best_sellers: Preenche as informações dos jogos mais vendidos.
        fill_list_game_information_best_releases: Preenche as informações dos melhores lançamentos.
        fill_list_game_information_more_played: Preenche as informações dos jogos mais jogados.
        fill_lists_with_game_information: Preenche todas as listas com as informações dos jogos.
        return_set_data: Retorna os dados transformados em um conjunto.
        quit_transform: Encerra o processo de transformação.
    """
    def __init__(self) -> None:
        """
        Construtor da classe HtmlTransform.
        """
        self.request = DaoGetHtml()
        self.extractor = HtmlExtractor()
        self.list_game_best_sellers_page = {
                                            '2020': 'https://store.steampowered.com/sale/BestOf2020?tab=4', 
                                            '2021': 'https://store.steampowered.com/sale/BestOf2021?tab=1', 
                                            '2022': 'https://store.steampowered.com/sale/BestOf2022?tab=1', 
                                            '2023': 'https://store.steampowered.com/sale/BestOf2023?l=brazilian&tab=1'
                                            }
        self.list_game_best_releases_page = {
                                            '2020': 'https://store.steampowered.com/sale/BestOf2020?tab=2', 
                                            '2021': 'https://store.steampowered.com/sale/BestOf2021?tab=2', 
                                            '2022': 'https://store.steampowered.com/sale/BestOf2022?tab=2', 
                                            '2023': 'https://store.steampowered.com/sale/BestOf2023?l=brazilian&tab=2'
                                            }

        self.list_game_most_played_page = {
                                            '2020': 'https://store.steampowered.com/sale/BestOf2020?tab=1', 
                                            '2021': 'https://store.steampowered.com/sale/BestOf2021?tab=3', 
                                            '2022': 'https://store.steampowered.com/sale/BestOf2022?tab=3', 
                                            '2023': 'https://store.steampowered.com/sale/BestOf2023?l=brazilian&tab=3'
                                            }
        self.lists_games = {
            "list_game_best_sellers_per_year" : {},
            "list_game_best_releases_per_year" : {},
            "list_game_most_played_per_year" : {}
            }

    def get_lists_per_year(self):
        """
        Obtém as listas de jogos para cada ano e categoria.
        """
        for year, url in self.list_game_best_sellers_page.items():
            response =  self.request.get_html(url)
            self.lists_games['list_game_best_sellers_per_year'][year] =  self.extractor.extract_games_best_sellers(response['content_html'])
        for year, url in  self.list_game_best_releases_page.items():
            response =  self.request.get_html(url)
            self.lists_games['list_game_best_releases_per_year'][year] =  self.extractor.extract_games_best_releases(response['content_html'], year)
        for year, url in  self.list_game_most_played_page.items():
            response =  self.request.get_html(url)
            self.lists_games['list_game_most_played_per_year'][year] =  self.extractor.extract_games_most_played(response['content_html'])

    def fill_list_game_information_best_sellers(self):
        """
        Preenche as informações dos jogos mais vendidos.
        """
        for year, games_group_dic in self.lists_games['list_game_best_sellers_per_year'].items():
            for name_group, games in games_group_dic.items():
                for name_game, url in games.items():
                    response = self.request.get_html(url)
                    pagina_do_jogo = self.extractor.verify_page_game(response['content_html'])
                    if pagina_do_jogo:
                        resultado = self.extractor.extract_game_information(response['content_html'])
                        self.list_game_best_sellers_per_year[year][name_group][name_game] = {"genre" : resultado}
                    else:
                        # Ir para a página do jogo com selenium
                        response = self.request.go_page_of_game_when_warning_age()
                        resultado = self.extractor.extract_game_information(response['content_html'])
                        self.lists_games['list_game_best_sellers_per_year'][year][name_group][name_game] = {"genre" : resultado}

    def fill_list_game_information_best_releases(self):
        """
        Preenche as informações dos melhores lançamentos.
        """
        for year, games_group_dic in self.lists_games['list_game_best_releases_per_year'].items():
            for name_group, games in games_group_dic.items():
                for name_game, url in games.items():
                    response = self.request.get_html(url)
                    pagina_do_jogo = self.extractor.verify_page_game(response['content_html'])
                    if pagina_do_jogo:
                        resultado = self.extractor.extract_game_information(response['content_html'])
                        self.list_game_best_releases_per_year[year][name_group][name_game] = {"genre" : resultado}
                    else:
                        # Ir para a página do jogo com selenium
                        response = self.request.go_page_of_game_when_warning_age()
                        resultado = self.extractor.extract_game_information(response['content_html'])
                        self.lists_games['list_game_best_releases_per_year'][year][name_group][name_game] = {"genre" : resultado}

    def fill_list_game_information_more_played(self):
        """
        Preenche as informações dos jogos mais jogados.
        """
        for year, games_group_dic in self.lists_games['list_game_most_played_per_year'].items():
            for name_group, games in games_group_dic.items():
                for name_game, url in games.items():
                    response = self.request.get_html(url)
                    pagina_do_jogo = self.extractor.verify_page_game(response['content_html'])
                    if pagina_do_jogo:
                        resultado = self.extractor.extract_game_information(response['content_html'])
                        self.list_game_most_played_per_year[year][name_group][name_game] = {"genre" : resultado}
                    else:
                        # Ir para a página do jogo com selenium
                        response = self.request.go_page_of_game_when_warning_age()
                        resultado = self.extractor.extract_game_information(response['content_html'])
                        self.lists_games['list_game_most_played_per_year'][year][name_group][name_game] = {"genre" : resultado}

    def fill_lists_with_game_information(self):
        """
        Preenche todas as listas com as informações dos jogos.
        """
        self.fill_list_game_information_best_sellers()
        self.fill_list_game_information_best_releases()
        self.fill_list_game_information_more_played()

    def return_set_data(self):
        """
        Retorna os dados transformados em um conjunto.

        Returns:
            Dict: Dicionário contendo os dados transformados.
        """
        return {
                "best sellers" : self.lists_games['list_game_best_sellers_per_year'], 
                "best releases" : self.lists_games['list_game_best_releases_per_year'], 
                "most played" : self.lists_games['list_game_most_played_per_year']
            }

    def quit_transform(self):
        """
        Encerra o processo de transformação.
        """
        self.request.quit_navegador()
