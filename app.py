import pandas as pd
import coleta


# Magazine Luiza
#url = f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit'
#url_proxima_pagina = f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit&page={pagina}'

# Mercado Livre
#url = f'https://lista.mercadolivre.com.br/{item_busca}'

# Amazon
#url = f'https://www.amazon.com.br/s?k={item_busca}'
item_busca = 'smartphone'


df_coleta = pd.DataFrame()

df_coleta = pd.concat( df_coleta, coleta.coleta_magazine_luiza(f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit') )

df_coleta = pd.concat( df_coleta, coleta.coleta_mercado_livre(f'https://lista.mercadolivre.com.br/{item_busca}') )

df_coleta = pd.concat( df_coleta, coleta.coleta_amazon(f'https://www.amazon.com.br/s?k={item_busca}') )

# Exportando DataFrame para arquivo CSV
df_coleta.to_csv('coleta.csv', sep=';', index=False, decimal=',' )