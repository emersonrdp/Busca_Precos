import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from datetime import datetime

item_busca = 'smartphone'
url = f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit'
headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0'}


#def coleta_magazine_luiza(url):
""" Raspagem de dados - Magazine Luiza """
resposta = requests.get(url, headers=headers)


# TESTE - vai para dentro do IF

soup = bs(resposta.text, 'html.parser')

# listas que vão receber os resultados
itens = []
dados_itens_nome = []
dados_itens_avaliacao = []
dados_itens_link = []
dados_itens_preco_antigo = []
dados_itens_preco_parcelado = []
dados_itens_preco_avista = []

# Coletando Nome e Avaliação
for item in soup.find_all("div", attrs={"class": "sc-gQSkpc jTodsw"}):
    dados_itens_nome.append( item.h2.text ) # nome
    dados_itens_avaliacao.append( item.span.text ) # avaliacao

# Coletando Link
for item in soup.find_all("li", attrs={"class": "sc-iNIeMn bDaikj"}):
    dados_itens_link.append( 'https://www.magazineluiza.com.br' + item.a.get('href') ) # link
    #print('https://www.magazineluiza.com.br'+item.a.get('href'))

# Coletando Preço Antigo
for item in soup.find_all("p", attrs={"class": "sc-dcJsrY lmAmKF sc-fyVfxW egCHto"}):
    dados_itens_preco_antigo.append( item.text )

# Coletando Preço Parcelado
for item in soup.find_all("p", attrs={"class": "sc-dcJsrY dpUJi sc-empnci JKjlB"}):
    dados_itens_preco_parcelado.append( item.text )
    
# Coletando Preço A Vista
for item in soup.find_all("p", attrs={"class": "sc-dcJsrY eLxcFM sc-jdkBTo etFOes"}):
    dados_itens_preco_avista.append( item.text )

itens.append( list(zip(dados_itens_nome, dados_itens_link, dados_itens_avaliacao, dados_itens_preco_antigo, dados_itens_preco_parcelado, dados_itens_preco_avista)) )

itens[0]
len(itens[0])


# fim do TESTE


if (resposta.status_code == 200):
    # implementar a coleta com beratufulsoup

    print('OK')
else:
    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Erro ao fazer requisição da página: {resposta.status_code}')

