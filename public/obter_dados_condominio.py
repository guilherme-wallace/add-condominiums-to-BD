import requests
import base64
import json
from route.dadosDeconexao import hostIntranet, urlIXC, tokenIXC

def obter_dados_condominio(arquivo_saida_pega):
    host = hostIntranet
    url = urlIXC.format(host)
    token = tokenIXC

    payload = {
        'qtype': 'cliente_condominio.id',
        'query': '0',
        'oper': '>',
        'page': '1',
        'rp': '10000',
        'sortname': 'cliente_condominio.id',
        'sortorder': 'asc'
    }

    headers = {
        'ixcsoft': 'listar',
        'Authorization': 'Basic {}'.format(base64.b64encode(token).decode('utf-8')),
        'Content-Type': 'application/json'
    }

    response = requests.get(url, data=json.dumps(payload), headers=headers)

    with open(arquivo_saida_pega, 'w', encoding='utf-8') as f:
        f.write(response.text)

    print(f"A resposta foi salva no arquivo '{arquivo_saida_pega}'.")
    