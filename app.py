import streamlit as st
import pandas as pd
import coleta
import warnings 

# Ignorar todos os warnings 
warnings.filterwarnings("ignore")


# Magazine Luiza
#url = f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit'
#url_proxima_pagina = f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit&page={pagina}'

# Mercado Livre
#url = f'https://lista.mercadolivre.com.br/{item_busca}'

# Amazon
#url = f'https://www.amazon.com.br/s?k={item_busca}'
#item_busca = 'smartphone'
#item_busca = 'moto g54 256gb'






#df_coleta = pd.DataFrame()

#item_busca = item_busca.replace(' ', '+') # Substituição dos espaços de acordo com o site
#df_coleta_MagazineLuiza = coleta.coleta_magazine_luiza(f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit', item_busca)
#
#item_busca = item_busca.replace(' ', '-') # Substituição dos espaços de acordo com o site
#df_coleta_MecadoLivre = coleta.coleta_mercado_livre(f'https://lista.mercadolivre.com.br/{item_busca}', item_busca)
#
#item_busca = item_busca.replace(' ', '+') # Substituição dos espaços de acordo com o site
#df_coleta_Amazon = coleta.coleta_amazon(f'https://www.amazon.com.br/s?k={item_busca}', item_busca)
#
#df_coleta = pd.concat( [df_coleta_MagazineLuiza, df_coleta_MecadoLivre, df_coleta_Amazon], axis=0) # axis=0 (linhas)
#
## Exportando DataFrame para arquivo CSV
#df_coleta.to_csv('coleta.csv', sep=';', index=False, decimal=',' )

#df_coleta_MagazineLuiza


def main():

    df_coleta = pd.DataFrame()

    ##### Menu lateral para pesquisa #####
    item_busca = st.sidebar.text_input('Informe o produto que você deseja pesquisar: ')

    st.sidebar.write('Marque os sites que você deseja pesquisar:')
    checkbox_MagazineLuiza = st.sidebar.checkbox('Magazine Luiza')
    checkbox_MwecadoLivre = st.sidebar.checkbox('Mercado Livre')
    checkbox_Amazon = st.sidebar.checkbox('Amazon')


    ##### Conteúdo da página #####
    st.title('Aplicativo Pesquisa de Preços')
    # Mostrar os dados carregados
    st.subheader('Dados dos produtos coleletados nos sites selecionados')


    ##### Menu lateral para pesquisa #####
    if st.sidebar.button('Fazer a pesquisa'):

        # Monstrando botão agaurde enquanto faz a coleta dos dados
        with st.spinner('Aguarde...'):

            if checkbox_MagazineLuiza:
                item_busca = item_busca.replace(' ', '+') # Substituição dos espaços de acordo com o site
                df_coleta_MagazineLuiza = coleta.coleta_magazine_luiza(f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit', item_busca)
            else:
                df_coleta_MagazineLuiza = pd.DataFrame()

            if checkbox_MwecadoLivre:
                item_busca = item_busca.replace(' ', '-') # Substituição dos espaços de acordo com o site
                df_coleta_MecadoLivre = coleta.coleta_mercado_livre(f'https://lista.mercadolivre.com.br/{item_busca}', item_busca)
            else:
                df_coleta_MecadoLivre = pd.DataFrame()

            if checkbox_Amazon:
                item_busca = item_busca.replace(' ', '+') # Substituição dos espaços de acordo com o site
                df_coleta_Amazon = coleta.coleta_amazon(f'https://www.amazon.com.br/s?k={item_busca}', item_busca)
            else:
                df_coleta_Amazon = pd.DataFrame()
            
            df_coleta = pd.concat( [df_coleta_MagazineLuiza, df_coleta_MecadoLivre, df_coleta_Amazon], axis=0) # axis=0 (linhas)


    ##### Conteúdo da página #####
    if df_coleta.empty:
        st.write('Selecione os dados no menu à esquerda para fazer a pesquisa...')
    else:
        st.write(df_coleta.head())

        df_coleta.to_csv('coleta.csv', sep=';', index=False, decimal=',')

        # Abrindo o arquivo binário (substitua pelo caminho do seu arquivo)
        with open("coleta.csv", "rb") as file:
            csv = file.read()

        # Botão de download do arquivo em formato CSV
        st.download_button( label="Baixar dados em formato CSV", data=csv, file_name="dados_busca_preco.csv", mime="text/csv" )

        #if st.button('Clique aqui apra baixar os dados no formato CSV'):
        #if st.download_button('Download CSV', text_contents):

            # ******** Implementar uma opção de baixar o arquivo **********

            # Exportando DataFrame para arquivo CSV
            #st.download_button('Download CSV', df_coleta.to_csv('coleta.csv', sep=';', index=False, decimal=',' ))
            #csv = df_coleta.to_csv('coleta.csv', sep=';', index=False, decimal=',' )

        #if st.button('Clique aqui apra baixar os dados no formato XLS'):
        #    # Exportando DataFrame para arquivo CSV
        #    df_coleta.to_excel('coleta.xlsx', sheet_name='Coleta')
        #
        #if st.button('Clique aqui apra baixar os dados no formato JSON'):
        #    # Exportando DataFrame para arquivo CSV
        #    df_coleta.to_json('coleta.json')

    



main()