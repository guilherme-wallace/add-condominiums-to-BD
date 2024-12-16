import json
import csv

def processar_dados_condominios(pegacondsResultado, condsRegistrados, dadosFiltradosArquivo, arquivo_saida_formata):
    
    with open(pegacondsResultado, 'r', encoding='utf-8') as arquivo:
        pegacondsResultadoConteudo = arquivo.read()

    respostaPegacondsResultado = f'{pegacondsResultadoConteudo}'
    dados = json.loads(respostaPegacondsResultado)
    registros = dados.get('registros', [])

    registros_json = json.dumps(registros, indent=4, ensure_ascii=False)
    with open(condsRegistrados, 'w', encoding='utf-8') as arquivo:
        arquivo.write(registros_json)
    print(f"Os registros foram salvos em {condsRegistrados}.")

    with open(condsRegistrados, 'r', encoding='utf-8') as arquivo:
        dados_json = json.load(arquivo)

    dadosFiltrados = [
        {
            "id": registro["id"],
            "condominio": registro["condominio"],
            "id_cidade": registro["id_cidade"],
            "endereco": registro["endereco"],
            "numero": registro["numero"],
            "cep": registro["cep"],
            "bairro": registro["bairro"]
        }
        for registro in dados_json
    ]

    dadosFiltrados_json = json.dumps(dadosFiltrados, indent=4, ensure_ascii=False)
    with open(dadosFiltradosArquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(dadosFiltrados_json)
    print(f"Os dados filtrados foram salvos em {dadosFiltradosArquivo}.")

    with open(dadosFiltradosArquivo, 'r', encoding='utf-8') as arquivo:
        dados_json = json.load(arquivo)

    campos = ["id", "condominio", "id_cidade", "endereco", "numero", "cep", "bairro"]

    with open(arquivo_saida_formata, 'w', newline='', encoding='utf-8') as csvfile:
        escritor_csv = csv.DictWriter(csvfile, fieldnames=campos)

        escritor_csv.writeheader()
        for registro in dados_json:
            escritor_csv.writerow({campo: registro[campo] for campo in campos})

    print(f"Os dados foram convertidos e salvos em {arquivo_saida_formata}.")

