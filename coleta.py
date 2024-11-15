import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import re

headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0'}
item_busca = 'smartphone'
url = f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit&page={pagina}'
#url_proxima_pagina = f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit&page={pagina}'



def coleta_magazine_luiza(url):
    """ Raspagem de dados - Magazine Luiza """

    def proxima_pagina(pagina, item_busca):
        """Verificar se existe próxima página e retorna a requisição da próxima página"""
        if soup.find("button", attrs={"aria-label": "Go to next page"}):
            pagina += 1
            url = f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit&page={pagina}'
            #print(f'    Proxima página: {url} \n    Pagina: {pagina}')
            sleep(3)
            return pagina, url
    
    pagina = 1

    # listas que vão receber os resultados
    itens = []
    dados_itens_nome = []
    dados_itens_avaliacao = []
    dados_itens_link = []
    #dados_itens_preco_antigo = []
    dados_itens_preco_parcelado = []
    dados_itens_texto_preco_parcelado = []
    dados_itens_preco_avista = []

    while True:
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Coletando os dados da página {pagina}: {url}')
        resposta = requests.get(url, headers=headers)
        
        if (resposta.status_code == 200):
            soup = BeautifulSoup(resposta.text, 'html.parser')

            # Coletando Nome e Avaliação
            for item in soup.find_all("div", attrs={"class": "sc-gQSkpc jTodsw"}):
                dados_itens_nome.append( item.h2.text ) # nome
                dados_itens_avaliacao.append( item.span.text ) # avaliacao

            # Coletando Link
            for item in soup.find_all("li", attrs={"class": "sc-iNIeMn bDaikj"}):
                dados_itens_link.append( 'https://www.magazineluiza.com.br' + item.a.get('href') ) # link
                #print('https://www.magazineluiza.com.br'+item.a.get('href'))

            # Coletando Preço Antigo
            #for item in soup.find_all("p", attrs={"class": "sc-dcJsrY lmAmKF sc-fyVfxW egCHto"}):
            #    dados_itens_preco_antigo.append( item.text.replace('.','').replace(',','.').replace('R$\xa0','') )
                
            # Coletando Preço Parcelado
            for item in soup.find_all("p", attrs={"class": "sc-dcJsrY dpUJi sc-empnci JKjlB"}):
                dados_itens_texto_preco_parcelado.append( item.text.replace('\xa0',' ') )
                dados_itens_preco_parcelado.append( item.text.replace('.','').replace(',','.').replace('R$\xa0','').split(" em ")[0] )
                    
            # Coletando Preço A Vista
            for item in soup.find_all("p", attrs={"class": "sc-dcJsrY eLxcFM sc-jdkBTo etFOes"}):
                dados_itens_preco_avista.append( item.text.replace('.','').replace(',','.').replace('ou R$\xa0','').replace('R$\xa0','') )

            # Verifica se existe próxima página, se não existir sai do while
            #   Se o botão de próxima páfina estiver deaabilitado vai sair do loop
            #   Caso contrario chamará a fução que retornará a requisição da próxima página
            botao_proxima_pagina = soup.find("button", attrs={"aria-label": "Go to next page"})
            if botao_proxima_pagina.has_attr('disabled'):
                break
            else:
                #print(f'    Chamando a próxima página: {pagina}')
                pagina, url = proxima_pagina(pagina, item_busca)
        else:
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Erro ao fazer requisição da página {pagina}: {resposta.status_code}')
            break

    # Criando uma lista única com todos os produtos
    itens.append( list(zip(dados_itens_nome, dados_itens_link, dados_itens_avaliacao, dados_itens_texto_preco_parcelado, dados_itens_preco_parcelado, dados_itens_preco_avista)) )

    item_df = pd.DataFrame(itens[0], columns=['Nome','Link','Avaliacao','Parcelas','Preço Parcelado','Preço a Vista'])


    ####################################### TRATAMENTOS #######################################
    # Site coletado
    item_df['Site'] = 'Magazine Luiza'

    # Data da Coleta
    item_df['Data da Coleta'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    #Alterando so campos de preço para float
    #item_df['Preço Antigo'] = item_df['Preço Antigo'].fillna(0).astype(float)
    item_df['Preço Parcelado'] = item_df['Preço Parcelado'].fillna(0).astype(float)
    item_df['Preço a Vista'] = item_df['Preço a Vista'].fillna(0).astype(float)

    # Corrigindo campos sem avaliação
    item_df['Avaliacao'] = item_df['Avaliacao'].str.replace('ou', '').replace('no Pix', '')

    ################################### FIM DOS TRATAMENTOS ###################################


    # Exportando DataFrame para arquivo CSV
    item_df.to_csv('coletaMagazineLuiza.csv', sep=';', index=False, decimal=',' )

    return item_df




#url = f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit&page={pagina}'
url = f'https://lista.mercadolivre.com.br/{item_busca}'
https://lista.mercadolivre.com.br/smartphone#D[A:smartphone]
https://lista.mercadolivre.com.br/celulares-telefones/celulares-smartphones/smartphone_Desde_51_NoIndex_True
https://lista.mercadolivre.com.br/celulares-telefones/celulares-smartphones/smartphone_Desde_101_NoIndex_True
https://lista.mercadolivre.com.br/celulares-telefones/celulares-smartphones/smartphone_Desde_151_NoIndex_True
https://lista.mercadolivre.com.br/celulares-telefones/celulares-smartphones/smartphone_Desde_201_NoIndex_True

#def coleta_mercado_livre(url):
""" Raspagem de dados - Mercado Livre """

def proxima_pagina(pagina, item_busca):
        """Verificar se existe próxima página e retorna a requisição da próxima página"""
        if soup.find("button", attrs={"aria-label": "Go to next page"}):
            pagina += 1
            url = f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit&page={pagina}'
            #print(f'    Proxima página: {url} \n    Pagina: {pagina}')
            sleep(3)
            return pagina, url

# listas que vão receber os resultados
itens = []
dados_itens_nome = []
dados_itens_avaliacao = []
dados_itens_link = []
dados_itens_preco_parcelado = []
dados_itens_texto_preco_parcelado = []
dados_itens_preco_avista = []

"""
itemDicionario = {
    'Nome': dados_itens_nome,
    'Link': dados_itens_link,
    'Avaliação': dados_itens_avaliacao,
    'Preço_Antigo': dados_itens_preco_antigo,
    'Preço_Parcelado': dados_itens_preco_parcelado,
    'Preço_Parcelado_Texto': dados_itens_texto_preco_parcelado,
    'Preço_AVista': dados_itens_preco_avista
}

item_df_dict = pd.DataFrame(itemDicionario)
"""

#while True:
print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Coletando os dados da página {pagina}: {url}')
resposta = requests.get(url, headers=headers)

#if (resposta.status_code == 200):
soup = BeautifulSoup(resposta.text, 'html.parser')
# Coletando Nome e Avaliação

a = soup.find_all("div", attrs={"class": "poly-card__content"})
preco = soup.find_all("div", attrs={"class": "poly-price__current"})
preco.span.text
soup

for item in soup.find_all("div", attrs={"class": "poly-component__reviews"}):
    print ( item.text )


for item in soup.find_all("div", attrs={"class": "poly-card__content"}):
    # fazer testes para capturar a avaliação, não consegui pegar o texto da tag span
    print ( item.find("div", class_="poly-component__reviews").text )
    
    print ( item.find("span", class_="poly-reviews__rating") )
    print ( item.find("span", class_="poly-reviews__total").text )

    dados_itens_nome.append( item.h2.text ) # nome
    dados_itens_avaliacao.append( item.a['href'] ) # avaliacao

    dados_itens_link.append( item.a['href'] ) # Link
    dados_itens_preco_avista.append( item.find("span", class_="andes-money-amount andes-money-amount--cents-superscript").text.replace('.','').replace(',','.').replace('R$','') ) # Preço a Vista
    # A função regex re.search faz uma busca pegando o número decimal após o primeiro R$
    if item.find("span", class_=["poly-price__installments poly-text-positive","poly-price__installments poly-text-primary"] ):
        dados_itens_texto_preco_parcelado.append( item.find("span", class_=["poly-price__installments poly-text-positive","poly-price__installments poly-text-primary"]).text ) # Texto Preço Parcelado
        dados_itens_preco_parcelado.append( re.search(r"R\$\s?(\d+[\.,]?\d*)",  item.find("span", class_=["poly-price__installments poly-text-positive","poly-price__installments poly-text-primary"]).text ) ) # Preço Parcelado
    else:
        dados_itens_texto_preco_parcelado.append("Esse item não tem opção de parcelamento") # Texto Preço Parcelado
        dados_itens_preco_parcelado.append(0) # Preço Parcelado

len(dados_itens_nome)
len(dados_itens_avaliacao)
len(dados_itens_preco_avista)
len(dados_itens_texto_preco_parcelado)
len(dados_itens_preco_parcelado)

soup.find_all("span", attrs={"class": "andes-money-amount andes-money-amount--cents-superscript"})

for item in soup.find_all("span", attrs={"class": "andes-money-amount andes-money-amount--cents-superscript"}):
    print(item.text)
    type(preco)
    poly-price__current

for item in soup.find_all("div", attrs={"class": "poly-price__current"}):
    print(item.span.text)

###############

for item in soup.find_all("h2", attrs={"class": "poly-box poly-component__title"}):
    print(item.text)
    #dados_itens_nome.append( item.h2.text ) # nome
    #dados_itens_avaliacao.append( item.span.text ) # avaliacao
# Coletando Link
for item in soup.find_all("li", attrs={"class": "sc-iNIeMn bDaikj"}):
    dados_itens_link.append( 'https://www.magazineluiza.com.br' + item.a.get('href') ) # link
    #print('https://www.magazineluiza.com.br'+item.a.get('href'))
# Coletando Preço Antigo
#for item in soup.find_all("p", attrs={"class": "sc-dcJsrY lmAmKF sc-fyVfxW egCHto"}):
#    dados_itens_preco_antigo.append( item.text.replace('.','').replace(',','.').replace('R$\xa0','') )
    
# Coletando Preço Parcelado
for item in soup.find_all("p", attrs={"class": "sc-dcJsrY dpUJi sc-empnci JKjlB"}):
    dados_itens_texto_preco_parcelado.append( item.text.replace('\xa0',' ') )
    dados_itens_preco_parcelado.append( item.text.replace('.','').replace(',','.').replace('R$\xa0','').split(" em ")[0] )
        
# Coletando Preço A Vista
for item in soup.find_all("p", attrs={"class": "sc-dcJsrY eLxcFM sc-jdkBTo etFOes"}):
    dados_itens_preco_avista.append( item.text.replace('.','').replace(',','.').replace('ou R$\xa0','').replace('R$\xa0','') )
# Verifica se existe próxima página, se não existir sai do while
#   Se o botão de próxima páfina estiver deaabilitado vai sair do loop
#   Caso contrario chamará a fução que retornará a requisição da próxima página
botao_proxima_pagina = soup.find("button", attrs={"aria-label": "Go to next page"})
if botao_proxima_pagina.has_attr('disabled'):
    #break
#else:
    #print(f'    Chamando a próxima página: {pagina}')
    #pagina, url = proxima_pagina(pagina, item_busca)
#else:
    #print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Erro ao fazer requisição da página {pagina}: {resposta.status_code}')
    #break

# Criando uma lista única com todos os produtos
itens.append( list(zip(dados_itens_nome, dados_itens_link, dados_itens_avaliacao, dados_itens_texto_preco_parcelado, dados_itens_preco_parcelado, dados_itens_preco_avista)) )

item_df = pd.DataFrame(itens[0], columns=['Nome','Link','Avaliacao','Parcelas','Preço Parcelado','Preço a Vista'])


####################################### TRATAMENTOS #######################################
# Site coletado
item_df['Site'] = 'Magazine Luiza'

# Data da Coleta
item_df['Data da Coleta'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

#Alterando so campos de preço para float
#item_df['Preço Antigo'] = item_df['Preço Antigo'].fillna(0).astype(float)
item_df['Preço Parcelado'] = item_df['Preço Parcelado'].fillna(0).astype(float)
item_df['Preço a Vista'] = item_df['Preço a Vista'].fillna(0).astype(float)

# Corrigindo campos sem avaliação
item_df['Avaliacao'] = item_df['Avaliacao'].str.replace('ou', '').replace('no Pix', '')

################################### FIM DOS TRATAMENTOS ###################################


# Exportando DataFrame para arquivo CSV
item_df.to_csv('coletaMagazineLuiza.csv', sep=';', index=False, decimal=',' )

#print('\n'+item_df)
#item_df.info()
#item_df.sort_values(by='Preço a Vista', ascending=True)