"""
Módulo load_dados: Fornece métodos para carregar dados em formato CSV.

Este módulo contém a classe LoadDados, que oferece métodos para carregar dados de jogos em formato CSV.

Classes:
    LoadDados: Uma classe que fornece métodos para carregar dados de jogos em formato CSV.
"""
from typing import Dict

class LoadDados():
    """
    Classe LoadDados: Fornece métodos para carregar dados em formato CSV.

    Methods:
        load_data_best_sellers_csv: Carrega dados dos jogos mais vendidos em formato CSV.
        load_data_best_releases_csv: Carrega dados dos jogos com melhores lançamentos em formato CSV.
        load_data_most_played_csv: Carrega dados dos jogos mais jogados em formato CSV.

    """

    def __init__(self) -> None:
        """
        Construtor da classe LoadDados.

        Inicializa as strings que representam as primeiras linhas dos arquivos CSV.
        """
        self.first_row_best_sellers_and_best_releases = "year;rank;game;genre;is_indie\n"
        self.first_row_most_played = "year;simultaneous_players;game;genre;is_indie\n"

    def load_data_best_sellers_csv(self, best_sellers : Dict) -> str:
        """
        Carrega dados dos jogos mais vendidos em formato CSV.

        Args:
            best_sellers (Dict): Dicionário contendo dados dos jogos mais vendidos no formato JSON:
            {
                "2020": {
                    "Platinum": {
                        "game": {
                            "genre": [
                                "genre 1",
                                ...
                            ]
                        },
                        "game 2" ...
                    },
                    "Gold" ...
                },
                "2021" ...
            }

        Returns:
            str: String contendo os dados formatados em CSV.
        """
        genres_remove = ["Animation & Modeling", "Design & Illustration", "Photo Editing", "Utilities"]
        string_csv = self.first_row_best_sellers_and_best_releases
        for ano, games_per_rank in best_sellers.items():
            for rank, games in games_per_rank.items():
                for game, genres in games.items():
                    for genre in genres['genre']:
                        if genre in genres_remove:
                            continue
                        if "Indie" in genres['genre']:
                            row = f"{ano};{rank};{game};{genre};True\n"
                        else:
                            row = f"{ano};{rank};{game};{genre};False\n"
                        string_csv += row
                        row = None
        return string_csv

    def load_data_best_releases_csv(self, best_releases : Dict) -> str:
        """
        Carrega dados dos jogos com melhores lançamentos em formato CSV.

        Args:
            best_releases (Dict): Dicionário contendo dados dos jogos com melhores lançamentos no formato JSON.
            {
                "2020": {
                    "Platinum": {
                        "game": {
                            "genre": [
                                "genre 1",
                                ...
                            ]
                        },
                        "game 2" ...
                    },
                    "Gold" ...
                },
                "2021" ...
            }

        Returns:
            str: String contendo os dados formatados em CSV.
        """
        # Best releases csv
        genres_remove = ["Animation & Modeling", "Design & Illustration", "Photo Editing", "Utilities"]
        string_csv = self.first_row_best_sellers_and_best_releases
        for ano, games_per_rank in best_releases.items():
            for rank, games in games_per_rank.items():
                for game, genres in games.items():
                    for genre in genres['genre']:
                        if genre in genres_remove:
                            continue
                        if "Indie" in genres['genre']:
                            row = f"{ano};{rank};{game};{genre};True\n"
                        else:
                            row = f"{ano};{rank};{game};{genre};False\n"
                        string_csv += row
                        row = None
        return string_csv

    def load_data_most_played_csv(self, most_played : Dict) -> str:
        """
        Carrega dados dos jogos mais jogados em formato CSV.

        Args:
            most_played (Dict): Dicionário contendo dados dos jogos mais jogados no formato JSON.
            {
                "2020": {
                    "qtd jogadores simultaneos": {
                        "game": {
                            "genre": [
                                "genre 1",
                                ...
                            ]
                        },
                        "game 2" ...
                    },
                    "qtd jogadores simultaneos 2" ...
                },
                "2021" ...
            }

        Returns:
            str: String contendo os dados formatados em CSV.
        """
        # most played csv
        genres_remove = ["Animation & Modeling", "Design & Illustration", "Photo Editing", "Utilities"]
        string_csv = self.first_row_most_played
        for ano, games_per_rank in most_played.items():
            for rank, games in games_per_rank.items():
                for game, genres in games.items():
                    for genre in genres['genre']:
                        if genre in genres_remove:
                            continue
                        if "Indie" in genres['genre']:
                            row = f"{ano};{rank};{game};{genre};True\n"
                        else:
                            row = f"{ano};{rank};{game};{genre};False\n"
                        string_csv += row
                        row = None
        return string_csv
