import requests
from bs4 import BeautifulSoup
import re
import csv
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


def jogadores_flamengo_url():
    url_flamengo = "https://www.sofascore.com/team/football/flamengo/5981"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

    response = requests.get(url_flamengo, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    jogadores = []

    elements = soup.find_all(class_="sc-hLBbgP dRtNhU")
    for element in elements:
        for a_tag in element.find_all('a'):
            texto_do_link = a_tag.text
            regex = re.compile(r'/(player|manager)/\S+?/(\d+)$')
            match = regex.match(a_tag['href'])
            if match:
                url = match.group()
                jogadores.append(url)

    with open('jogadores_flamengo.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['URL'])
        for jogador in jogadores:
            writer.writerow([jogador])


def dynamic_scrap():
    first_line = True
    # Abrir o arquivo CSV com as URLs
    with open('mock.csv', mode='r') as arquivo_urls:
        leitor = csv.DictReader(arquivo_urls)
        # Inicializar o driver do Selenium
        driver = webdriver.Chrome(
            executable_path="C:\\Users\\Biankovsky\\Downloads\\chromedriver\\chromedriver.exe")

        # Loop pelas URLs do arquivo CSV
        for linha in leitor:
            url = linha['URL']
            driver.get("https://www.sofascore.com" + url)
            #driver.get(                "https://www.sofascore.com/player/gabriel-barbosa/358554")
            data = []

            time.sleep(10)
            btn = driver.find_element(
                By.XPATH, '//*[@id = "downshift-0-toggle-button"]')
            time.sleep(10)
            btn.click()
            time.sleep(3)

            # Recupera a string com todas as opções do menu
            menu = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'downshift-0-menu')))

            # Splita e joga os itens em um array
            menu_items = []
            for line in menu.text.split('\n'):
                menu_items.append([line])

            element_index = 0
            for i, item in enumerate(menu_items):
                if item == ['Brasileiro Série A']:
                    element_index = i
                    break

            time.sleep(5)
            element = driver.find_element(By.XPATH,
                                          '//*[@aria-activedescendant]')
            element_id = element.get_attribute('aria-activedescendant')
            item = driver.find_element(
                By.ID, element_id + f'downshift-0-item-{element_index}')
            time.sleep(5)
            item.click()

            time.sleep(10)
            # Extrair os dados da página
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # classe pode mudar depois de um tempo??
            spans = soup.find_all('span', {'class': 'sc-bqWxrE kAIqxV'})
            for span in spans:
                data.append(span.text)

            final_data = data[:100]
            pairs = [(final_data[i], final_data[i+1])
                     for i in range(0, len(final_data), 2)]
            dicionario = dict(pairs)
            colunas = list(dicionario.keys())
            valores = list(dicionario.values())

            # Escrever os dados no arquivo CSV
            with open('dados.csv', mode='a', newline='') as arquivo_dados:
                escritor = csv.writer(arquivo_dados)
                if first_line:
                    escritor.writerow(colunas)
                    first_line = False
                escritor.writerow(valores)

    # Fechar o driver do Selenium
    driver.quit()


dynamic_scrap()
