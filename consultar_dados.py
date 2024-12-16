import mysql.connector
import json
from route.dadosDeconexao import configuracao_dbIntranet

tecnologia_id = 4
arquivo_saida='resultadoConsultaBanco.json'

def consultar_dados(arquivo_saida, tecnologia_id):
    configuracao_db = configuracao_dbIntranet
    conn = mysql.connector.connect(**configuracao_db)
    cursor = conn.cursor(dictionary=True)

    query = f"""
    SELECT DISTINCT
        c.condominioId,
        c.condominio,
        c.cidadeId,
        c.endereco,
        c.numero,
        c.cep,
        c.bairro,
        t.technology
    FROM 
        condominio c
    JOIN 
        `group` g ON g.groupId = c.condominioId
    JOIN 
        block b ON b.groupId = g.groupId
    JOIN 
        technology t ON t.technologyId = b.technologyId
    WHERE 
        t.technologyId = {tecnologia_id};
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    with open(arquivo_saida, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

    print(f"Consulta realizada e resultado salvo em '{arquivo_saida}'.")

consultar_dados(arquivo_saida, tecnologia_id)
