import requests
from pprint import pprint

# Structure payload.
payload = {
   'source': 'amazon',
   'url': 'https://www.amazon.com.br/s?k=smartphone',
   #'locale': 'pt-br',     # esse parametro deu erro na requisição
   #'geo_location': 'BR',  # esse parametro deu erro na requisição
   'user_agent_type': 'desktop_chrome',
   'parse': True
}

# Get response.
response = requests.request(
    'POST',
    'https://realtime.oxylabs.io/v1/queries',
    auth=('YOUR_USERNAME', 'YOUR_PASSWORD'), #Your credentials go here
    json=payload,
)

# Instead of response with job status and results url, this will return the
# JSON response with results.
pprint(response.json())


############# Gerado pela IA OxyLabs

import requests
from pprint import pprint

# Structure payload.
payload = {
   'source': 'amazon_search',
   'user_agent_type': 'desktop',
   'query': 'smartphone',
   'domain': 'com.br',
   'parse': True
}

# Get response.
response = requests.request(
    'POST',
    'https://realtime.oxylabs.io/v1/queries',
    auth=('emersonrdp', 'YOUR_PASSWORD'), #Your credentials go here
    json=payload,
)

# Instead of response with job status and results url, this will return the
# JSON response with results.
pprint(response.json())