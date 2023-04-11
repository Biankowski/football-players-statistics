import requests
from bs4 import BeautifulSoup
import re
import csv
from selenium.webdriver import Chrome


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
    driver = Chrome(
        executable_path="C:\\Users\\Biankovsky\\Downloads\\chromedriver\\chromedriver.exe")

    driver.get("https://www.sofascore.com/player/giorgian-de-arrascaeta/333587")

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    spans = soup.find_all('span', {'class': 'sc-bqWxrE hVYPTT'})

    data = []
    for span in spans:
        data.append(span.text)

    final_data = data[:100]

    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(final_data[::2])
        writer.writerow(final_data[1::2])

    driver.quit()


dynamic_scrap()
