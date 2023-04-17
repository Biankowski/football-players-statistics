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
        driver = webdriver.Chrome(executable_path="C:\\Users\\rodri\Downloads\\chromedriver_win32\\chromedriver.exe")
        driver.maximize_window()
        wait = WebDriverWait(driver, 5)

        # Loop pelas URLs do arquivo CSV
        for linha in leitor:
            url = linha['URL']
            driver.get("https://www.sofascore.com" + url)
            #driver.get("https://www.sofascore.com/player/cleiton-santana/1134199")

            data = []

            try:
                # Recupera a competição desejada
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id = "downshift-0-toggle-button"]')))
                btn = driver.find_element(By.XPATH, '//*[@id = "downshift-0-toggle-button"]')
                driver.execute_script('arguments[0].click()', btn)

                # Recupera a string com todas as opções do menu
                wait.until(EC.presence_of_element_located((By.ID, 'downshift-0-menu')))
                menu = driver.find_element(By.ID, 'downshift-0-menu')

                # Splita e joga os itens em um array
                menu_items = []
                for line in menu.text.split('\n'):
                    menu_items.append([line])

                element_index = 0
                for i, item in enumerate(menu_items):
                    if item == ['Brasileiro Série A']:
                        element_index = i
                        break

                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@aria-activedescendant]')))
                element = driver.find_element(By.XPATH, '//*[@aria-activedescendant]')
                element_id = element.get_attribute('aria-activedescendant')
                wait.until(EC.presence_of_element_located((By.ID, element_id + f'downshift-0-item-{element_index}')))
                time.sleep(3)
                item = driver.find_element(By.ID, element_id + f'downshift-0-item-{element_index}')
                item.location_once_scrolled_into_view
                driver.execute_script('arguments[0].click()', item)
                time.sleep(5)
                
                # Recupera o ano da competição desejada
                wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="downshift-1-toggle-button"]')))
                btn_ano = driver.find_elements(By.XPATH, '//*[@id="downshift-1-toggle-button"]')
                driver.execute_script('arguments[0].click()', btn_ano[1])
                
                wait.until(EC.presence_of_all_elements_located((By.ID, 'downshift-1-menu')))
                menu_ano = driver.find_elements(By.ID, 'downshift-1-menu')
                
                menu_de_anos = []
                for line in menu_ano[1].text.split('\n'):
                    menu_de_anos.append([line])
                    
                element_index = 0
                for i, item in enumerate(menu_de_anos):
                    if item == ['2021']:
                        element_index = i
                        break
                    
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@aria-activedescendant]')))
                element_ano = driver.find_element(By.XPATH, '//*[@aria-activedescendant]')
                element_id_ano = element_ano.get_attribute('aria-activedescendant')
                wait.until(EC.presence_of_element_located((By.ID, element_id_ano + f'downshift-1-item-{element_index}')))
                time.sleep(3)
                item_ano = driver.find_element(By.ID, element_id + f'downshift-1-item-{element_index}')
                item_ano.location_once_scrolled_into_view
                driver.execute_script('arguments[0].click()', item_ano)
                time.sleep(5)
                
                
                
                # Extrair os dados da página
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # classe pode mudar depois de um tempo??
                #wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-bqWxrE kAIqxV')))
                spans = soup.find_all('span', {'class': 'sc-bqWxrE kAIqxV'})
                start_adding = False
                for span in spans:
                    if span.text == '':
                        pass
                    elif span.text == 'Brasileiro Série A':
                        start_adding = True
                        data.append(span.text)
                    elif start_adding:
                        data.append(span.text)

                # Extrair nome do jogador
                nomes = soup.find_all('h2', {'class': 'sc-bqWxrE eNZjKc'})
                for elemento in nomes:
                    nome_jogador = elemento.text

                # Extrair informações dos jogadores
                informacoes_jogador = soup.find_all(
                    'div', {'class': 'sc-hLBbgP sc-eDvSVe gjJmZQ lXUNw'})
                for elemento in informacoes_jogador:
                    informacoes = elemento.text

                salario = soup.find_all('div', {'class': 'sc-bqWxrE gsYByW'})
                for elemento in salario:
                    salary = elemento.text

                # Extrai as informações relevantes da string usando regex
                nationality = re.findall(r'Nationality(\w{3})', informacoes)[0]
                birth_date = re.findall(r'(\d{1,2}\s\w{3}\s\d{4})', informacoes)[0]
                height = re.findall(r'Height(\d{3}\s\w{2})', informacoes)[0]
                preferred_foot = re.findall(r'Preferred foot(\w+)', informacoes)[0]
                position = re.findall(r'Position(\w)', informacoes)[0]
                shirt_number = re.findall(r'Shirt number(\d+)', informacoes)[0]

                match = re.search(r'(Left|Right)', preferred_foot)
                if match:
                    preferred_foot = match.group(1)
                else:
                    preferred_foot = None

                final_data = data[:100]
                pairs = [(final_data[i], final_data[i+1])
                        for i in range(0, len(final_data), 2)]
                dicionario = dict(pairs)
                dicionario.update({'Nome do Jogador': nome_jogador,
                                'Nationality': nationality,
                                'Birth date': birth_date,
                                'Height': height,
                                'Preferred foot': preferred_foot,
                                'Position': position,
                                'Shirt number': shirt_number,
                                'Salary': salary})
                colunas = list(dicionario.keys())
                valores = list(dicionario.values())

                # Escrever os dados no arquivo CSV
                with open('dados.csv', mode='a', newline='') as arquivo_dados:
                    escritor = csv.writer(arquivo_dados)
                    if first_line:
                        escritor.writerow(colunas)
                        first_line = False
                    escritor.writerow(valores)
            except Exception as e:
                print(e)
                # nome_jogador = url.split('/')[2]
                # with open('dados.csv', mode='a', newline='') as arquivo_dados:
                #     escritor = csv.writer(arquivo_dados)
                #     escritor.writerow([nome_jogador])

    # Fechar o driver do Selenium
    driver.quit()


dynamic_scrap()
