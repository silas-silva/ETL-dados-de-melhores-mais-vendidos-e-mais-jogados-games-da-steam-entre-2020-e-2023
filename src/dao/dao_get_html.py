"""
Módulo dao_get_html: Uma interface para realizar requisições web de forma simplificada.

Este módulo oferece a classe DaoGetHtml, que abstrai o uso de bibliotecas externas para facilitar a
manutenção e a troca da implementação de requisições web, se necessário.

Exemplo de uso:
    >>> from dao_get_html import DaoGetHtml
    >>> dao_get_html = DaoGetHtml()
    >>> response = dao_get_html.get_html("https://example.com")
    >>> print(response)
    {'content_html': '<html>...</html>'}

Classes:
    DaoGetHtml: Uma classe que oferece uma interface para realizar requisições web.
"""

import time
from typing import Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



class DaoGetHtml:
    """
    Classe DaoGetHtml: Uma interface para realizar requisições web de forma simplificada.
    Esta classe abstrai o uso de bibliotecas externas para facilitar a manutenção.
    
    Attributes:
        navegador (WebDriver): Instância do WebDriver do Selenium para interagir com o navegador.
    
    Methods:
        get_html: Realiza uma requisição HTTP GET para a URL fornecida e retorna o conteúdo HTML.
        go_page_of_game_when_warning_age: Navega para a página do jogo quando há um aviso de idade.
        scroll_page: Rola a página até o final para garantir o carregamento completo do conteúdo.
        quit_navegador: Fecha o navegador e encerra a instância do WebDriver.
    """

    def __init__(self) -> None:
        """
        Construtor da classe HttpRequester.
        
        Inicializa o WebDriver do Selenium e abre o navegador.
        """
        # Criar navegador
        servico = Service(ChromeDriverManager().install())
        ## Configurar as opções do Chrome para executar em segundo plano
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        #navegador = webdriver.Chrome(service=servico, options=chrome_options) # Deixar invisivel
        #navegador = webdriver.Chrome(service=servico)  # Deixar visivel
        self.navegador = webdriver.Chrome(service=servico, options=chrome_options)

    def get_html(self, url : str) -> Dict[int, str]:
        """
        Realiza uma requisição HTTP GET para a URL fornecida e retorna o conteúdo HTML.

        Args:
            url (str): A URL da página da qual se deseja obter o conteúdo HTML.

        Returns:
            Dict: Um dicionário contendo o conteúdo HTML.
                Exemplo:
                {
                    "content_html": "<html>...</html>",
                }
        """
        self.navegador.get(url) # Abra a página desejada
        time.sleep(0.2) # Esperar pagina carregar
        self.scroll_page() # Scroll até o final da página
        time.sleep(0.5)
        html_content = self.navegador.page_source
        return {
            "content_html": html_content
        }

    def go_page_of_game_when_warning_age(self):
        """
        Navega para a página do jogo quando há um aviso de idade.
        
        Returns:
            Returns:
            Dict: Um dicionário contendo o conteúdo HTML.
                Exemplo:
                {
                    "content_html": "<html>...</html>",
                }
        """
        # Encontrar o elemento select
        xpath_element = '/html/body/div[1]/div[7]/div[6]/div/div[2]/div/div[1]/div[2]/select[3]'
        select_element = self.navegador.find_element(By.XPATH ,xpath_element)
        select = Select(select_element)
        select.select_by_value("2000") # Selecionar o ano de 2000 no select
        # Clicar no botão para ir para a poagina do jogo
        select_button = self.navegador.find_element(By.XPATH ,'//*[@id="view_product_page_btn"]')
        select_button.click()
        time.sleep(0.2)
        self.scroll_page()
        html_content = self.navegador.page_source
        time.sleep(0.5)
        return {
            "content_html": html_content
        }

    def scroll_page(self):
        """
        Rola a página até o final para garantir o carregamento completo do conteúdo.
        """
        intervalo = 0.1  # Intervalo de 0.2 segundo entre cada rolagem
        incremento = 500  # Quantidade de pixels a rolar a cada vez
        posicao_anterior = -1 # Defina a posição inicial da barra de rolagem
        while True:
            # Execute o script JavaScript para rolar a página em incrementos de 500 pixels
            self.navegador.execute_script(f"window.scrollBy(0, {incremento});")
            time.sleep(intervalo)
            # Obtenha a posição atual da barra de rolagem
            posicao_atual = self.navegador.execute_script("return window.scrollY")
            if posicao_atual == posicao_anterior:
                break
            posicao_anterior = posicao_atual

    def quit_navegador(self):
        """
        Fecha o navegador e encerra a instância do WebDriver.
        """
        self.navegador.quit()
