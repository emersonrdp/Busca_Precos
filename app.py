import coleta


# Magazine Luiza
#url = f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit'
#url_proxima_pagina = f'https://www.magazineluiza.com.br/busca/{item_busca}/?from=submit&page={pagina}'

# Mercado Livre
#url = f'https://lista.mercadolivre.com.br/{item_busca}'

# Amazon
#url = f'https://www.amazon.com.br/s?k={item_busca}'
item_busca = 'smartphone'


coleta.coleta_amazon(f'https://www.amazon.com.br/s?k={item_busca}')