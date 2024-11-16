import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import re
from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0'}
item_busca = 'smartphone'

# Magazine Luiza
#url = f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit'
#url_proxima_pagina = f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit&page={pagina}'

# Mercado Livre
#url = f'https://lista.mercadolivre.com.br/{item_busca}'


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
                print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Chegamos na ultima página. Fim da coleta de dados.')
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



def coleta_mercado_livre(url):
    """ Raspagem de dados - Mercado Livre """

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
    pagina = 0

    while True:
        pagina += 1
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Coletando os dados da página {pagina}: {url}')
        resposta = requests.get(url, headers=headers)

        if (resposta.status_code == 200):
            soup = BeautifulSoup(resposta.text, 'html.parser')

            for item in soup.find_all("div", attrs={"class": "poly-card__content"}):
                dados_itens_nome.append( item.h2.text ) # nome

                # Verificação se o item tem Avaliação
                if item.find("span", class_="poly-reviews__rating"):
                    dados_itens_avaliacao.append( item.find("span", class_="poly-reviews__rating").text + ' ' + item.find("span", class_="poly-reviews__total").text ) # avaliacao
                else:
                    dados_itens_avaliacao.append( 0 )
                
                dados_itens_link.append( item.a['href'] ) # Link

                dados_itens_preco_avista.append( item.find("span", class_="andes-money-amount andes-money-amount--cents-superscript").text.replace('.','').replace(',','.').replace('R$','') ) # Preço a Vista

                # Verificação se o item tem Preço Parcelado
                # A função regex re.findall faz uma busca pegando o número decimal após o primeiro R$. Como em alguns campos tem o preço total e o preço da parcela, pegamos apenas o primeiro item "[0]"
                if item.find("span", class_=["poly-price__installments poly-text-positive","poly-price__installments poly-text-primary"] ):
                    dados_itens_texto_preco_parcelado.append( item.find("span", class_=["poly-price__installments poly-text-positive","poly-price__installments poly-text-primary"]).text ) # Texto Preço Parcelado
                    dados_itens_preco_parcelado.append( re.findall(r"R\$\s?(\d+[\.,]?\d*)",  item.find("span", class_=["poly-price__installments poly-text-positive","poly-price__installments poly-text-primary"]).text.replace('.','').replace(',','.'))[0] ) # Preço Parcelado
                else:
                    dados_itens_texto_preco_parcelado.append("Esse item não tem opção de parcelamento") # Texto Preço Parcelado
                    dados_itens_preco_parcelado.append(0) # Preço Parcelado

            # Verifica se existe próxima página, se não existir sai do while
            #   Se o botão de próxima página estiver deaabilitado vai sair do loop (verifica pela classe de botão "Seguinte" desabilitado)
            #   Caso contrario atualizará a variável url com o link da próxima página
            botao_proxima_pagina = soup.find("li", attrs={"class": "andes-pagination__button andes-pagination__button--next"})

            if soup.find("li", attrs={"class": "andes-pagination__button andes-pagination__button--next andes-pagination__button--disabled"}):
                print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Chegamos na ultima página. Fim da coleta de dados.')
                break
            else:
                #print(f'    Chamando a próxima página: {pagina}')
                url = botao_proxima_pagina.a['href'] # link da proxima página
                sleep(2)
        else:
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Erro ao fazer requisição da página {pagina}: {resposta.status_code}')
            break

    # Criando uma lista única com todos os produtos
    itens.append( list(zip(dados_itens_nome, dados_itens_link, dados_itens_avaliacao, dados_itens_texto_preco_parcelado, dados_itens_preco_parcelado, dados_itens_preco_avista)) )

    item_df = pd.DataFrame(itens[0], columns=['Nome','Link','Avaliacao','Parcelas','Preço Parcelado','Preço a Vista'])

    #len(itens[0])
    #len(item_df)
    #item_df.head()
    item_df.info()


    ####################################### TRATAMENTOS #######################################
    # Site coletado
    item_df['Site'] = 'Mercado Livre'

    # Data da Coleta
    item_df['Data da Coleta'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    #Alterando so campos de preço para float
    #item_df['Preço Antigo'] = item_df['Preço Antigo'].fillna(0).astype(float)
    item_df['Preço Parcelado'] = item_df['Preço Parcelado'].fillna(0).astype(float)
    item_df['Preço a Vista'] = item_df['Preço a Vista'].fillna(0).astype(float)

    # Corrigindo campos sem avaliação
    #item_df['Avaliacao'] = item_df['Avaliacao'].str.replace('ou', '').replace('no Pix', '')

    ################################### FIM DOS TRATAMENTOS ###################################


    # Exportando DataFrame para arquivo CSV
    item_df.to_csv('coletaMercadolivre.csv', sep=';', index=False, decimal=',' )

    #print('\n'+item_df)
    #item_df.info()
    #item_df.sort_values(by='Preço a Vista', ascending=True)




url = f'https://www.amazon.com.br/s?k={item_busca}'

"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    'DNT': '1',  # Do Not Track
}"""


####
# Foi necessário utilizar a biblioteca Seleniun para conseguir fazer a requisição de página da Amazon
# A Amazon retornava 503 nas tentativas de requisição da página de pesquisa de produtos.
# Mesmo tentando algumas técnicas como colocar mais oingormações no headers ou abrir uma sessão para utilizar cookies não surtiram efeito.
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')

#service = Service(executable_path='caminho/para/chromedriver')
#driver = webdriver.Chrome(service=service, options=options)
driver = webdriver.Chrome(options=options)

driver.get(url)
html = driver.page_source
#print(html[:500])

driver.quit()

soup = BeautifulSoup(html, 'html.parser')

####


#def coleta_mercado_livre(url):
#    """ Raspagem de dados - Amazon """

# listas que vão receber os resultados
itens = []
dados_itens_nome = []
dados_itens_avaliacao = []
dados_itens_qtd_avaliacao = []
dados_itens_link = []
dados_itens_preco_parcelado = []
dados_itens_texto_preco_parcelado = []
dados_itens_preco_avista = []

# Foi necessário utilizar a biblioteca Seleniun para conseguir fazer a requisição de página da Amazon
# A Amazon retornava 503 nas tentativas de requisição da página de pesquisa de produtos.
# Mesmo tentando algumas técnicas como colocar mais oingormações no headers ou abrir uma sessão para utilizar cookies não surtiram efeito.
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')

#service = Service(executable_path='caminho/para/chromedriver')
#driver = webdriver.Chrome(service=service, options=options)
driver = webdriver.Chrome(options=options)

pagina = 0

#while True:
pagina += 1
print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Coletando os dados da página {pagina}: {url}')

# Fazendo a requisição da página via Selenium
driver.get(url)
html = driver.page_source

#if (resposta.status_code == 200):
soup = BeautifulSoup(html, 'html.parser')

a = soup.find_all("div", attrs={"class": "a-section a-spacing-none a-spacing-top-small s-price-instructions-style"})
a
a.find("span", class_="a-size-base a-color-secondary")

for i in a:
    spans = i.find_all('span', class_='a-size-base a-color-secondary')

    # Coletando o texto dos spans encontrados
    spans_text = [span.get_text(strip=True) for span in spans]

    #print(type(spans_text[0]))
    if len(spans_text) == 4:
        print( spans_text[0] + ' ' + spans_text[1] + ' ' + spans_text[2] + ' ' + i.find('span', class_='a-offscreen').text + ' ' + spans_text[3])
    elif len(spans_text) == 3:
        print(spans_text[1] + ' ' + i.find('span', class_='a-offscreen').text + ' ' + spans_text[2])
    elif len(spans_text) == 2:
        print(spans_text[0] + ' ' + i.find('span', class_='a-offscreen').text + ' ' + spans_text[1])
    #print ( i.find(text="ou") )
    print ( i.find('span', class_='a-offscreen').text )

for item in soup.find_all("div", attrs={"class": "a-section a-spacing-small puis-padding-left-small puis-padding-right-small"}):
    #print ( re.findall(r"R\$\s?(\d+[\.,]?\d*)", item.find("span", class_="a-price a-text-price").text)[0] )
    
    if item.find("span", class_="a-price a-text-price"):
        print( item.find("span", class_="a-size-base a-color-secondary").text + ' ' + item.find("span", class_="a-offscreen").text + ' ' + item.find("span", class_="a-size-base a-color-secondary").text ) 
        print( re.findall(r"R\$\s?(\d+[\.,]?\d*)",  item.find("span", class_="a-price a-text-price").text.replace('.','').replace(',','.'))[0] )
    else:
        print("Esse item não tem opção de parcelamento")
        print( 0 )

    
    dados_itens_nome.append( item.h2.text ) # nome

    # Verificação se o item tem Avaliação
    if item.find("span", class_="poly-reviews__rating"):
        dados_itens_avaliacao.append( item.find("span", class_="a-icon-alt").text ) # avaliacao
        dados_itens_qtd_avaliacao.append( item.find("span", class_="poly-reviews__total").text ) # quantidade de avaliações
    else:
        dados_itens_avaliacao.append( 0 )
        dados_itens_qtd_avaliacao.append( 0 )
    
    dados_itens_link.append( 'https://www.amazon.com.br' + item.a['href'] ) # Link

    dados_itens_preco_avista.append( (item.find("span", class_="a-price-whole").text + item.find("span", class_="a-price-fraction").text).text.replace('.','').replace(',','.') ) # Preço a Vista

    # Verificação se o item tem Preço Parcelado
    # A função regex re.findall faz uma busca pegando o número decimal após o primeiro R$. Como em alguns campos tem o preço total e o preço da parcela, pegamos apenas o primeiro item "[0]"
    if item.find("span", class_=["poly-price__installments poly-text-positive","poly-price__installments poly-text-primary"] ):
        dados_itens_texto_preco_parcelado.append( item.find("span", class_=["poly-price__installments poly-text-positive","poly-price__installments poly-text-primary"]).text ) # Texto Preço Parcelado
        dados_itens_preco_parcelado.append( re.findall(r"R\$\s?(\d+[\.,]?\d*)",  item.find("span", class_="a-price a-text-price").text.replace('.','').replace(',','.'))[0] ) # Preço Parcelado
    else:
        dados_itens_texto_preco_parcelado.append("Esse item não tem opção de parcelamento") # Texto Preço Parcelado
        dados_itens_preco_parcelado.append(0) # Preço Parcelado

driver.quit()

# Verifica se existe próxima página, se não existir sai do while
#   Se o botão de próxima página estiver deaabilitado vai sair do loop (verifica pela classe de botão "Seguinte" desabilitado)
#   Caso contrario atualizará a variável url com o link da próxima página
#botao_proxima_pagina = soup.find("li", attrs={"class": "andes-pagination__button andes-pagination__button--next"})
#
#if soup.find("li", attrs={"class": "andes-pagination__button andes-pagination__button--next andes-pagination__button--disabled"}):
#    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Chegamos na ultima página. Fim da coleta de dados.')
#    break
#else:
#    #print(f'    Chamando a próxima página: {pagina}')
#    url = botao_proxima_pagina.a['href'] # link da proxima página
#    sleep(5)
#else:
#    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Erro ao fazer requisição da página {pagina}: {resposta.status_code}')
#    break

# Criando uma lista única com todos os produtos
itens.append( list(zip(dados_itens_nome, dados_itens_link, dados_itens_avaliacao, dados_itens_texto_preco_parcelado, dados_itens_preco_parcelado, dados_itens_preco_avista)) )

item_df = pd.DataFrame(itens[0], columns=['Nome','Link','Avaliacao','Parcelas','Preço Parcelado','Preço a Vista'])

#len(itens[0])
#len(item_df)
#item_df.head()
item_df.info()


####################################### TRATAMENTOS #######################################
# Site coletado
item_df['Site'] = 'Mercado Livre'

# Data da Coleta
item_df['Data da Coleta'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

#Alterando so campos de preço para float
#item_df['Preço Antigo'] = item_df['Preço Antigo'].fillna(0).astype(float)
item_df['Preço Parcelado'] = item_df['Preço Parcelado'].fillna(0).astype(float)
item_df['Preço a Vista'] = item_df['Preço a Vista'].fillna(0).astype(float)

# Corrigindo campos sem avaliação
#item_df['Avaliacao'] = item_df['Avaliacao'].str.replace('ou', '').replace('no Pix', '')

################################### FIM DOS TRATAMENTOS ###################################


# Exportando DataFrame para arquivo CSV
item_df.to_csv('coletaMercadolivre.csv', sep=';', index=False, decimal=',' )

#print('\n'+item_df)
#item_df.info()
#item_df.sort_values(by='Preço a Vista', ascending=True)
