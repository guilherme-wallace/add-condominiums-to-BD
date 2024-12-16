import csv
import pymysql
from route.dadosDeconexao import configuracao_dbIntranet

def inserir_dados_no_banco(arquivo_csv, nome_da_tabela):
    configuracao_db = configuracao_dbIntranet
    conexao = pymysql.connect(**configuracao_db)

    condominios_processados = {"inseridos": [], "atualizados": []}

    try:
        with conexao.cursor() as cursor:
            with open(arquivo_csv, 'r', encoding='utf-8') as csvfile:
                leitor_csv = csv.DictReader(csvfile)

                for linha in leitor_csv:
                    query_verificacao = f"SELECT condominio, cidadeId, endereco, numero, cep, bairro FROM {nome_da_tabela} WHERE condominioId = %s"
                    cursor.execute(query_verificacao, (linha['id'],))
                    resultado = cursor.fetchone()

                    if not resultado:
                        query_insercao = f"""
                        INSERT INTO {nome_da_tabela} (condominioId, condominio, cidadeId, endereco, numero, cep, bairro)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(query_insercao, (
                            linha['id'],
                            linha['condominio'],
                            linha['id_cidade'],
                            linha['endereco'],
                            linha['numero'],
                            linha['cep'],
                            linha['bairro']
                        ))
                        condominios_processados["inseridos"].append(linha['condominio'])
                    else:
                        dados_banco = dict(zip(["condominio", "cidadeId", "endereco", "numero", "cep", "bairro"], resultado))
                        dados_csv = {
                            "condominio": linha["condominio"],
                            "cidadeId": linha["id_cidade"],
                            "endereco": linha["endereco"],
                            "numero": linha["numero"],
                            "cep": linha["cep"],
                            "bairro": linha["bairro"]
                        }

                        if dados_banco != dados_csv:
                            query_atualizacao = f"""
                            UPDATE {nome_da_tabela}
                            SET condominio = %s, cidadeId = %s, endereco = %s, numero = %s, cep = %s, bairro = %s
                            WHERE condominioId = %s
                            """
                            cursor.execute(query_atualizacao, (
                                linha['condominio'],
                                linha['id_cidade'],
                                linha['endereco'],
                                linha['numero'],
                                linha['cep'],
                                linha['bairro'],
                                linha['id']
                            ))
                            condominios_processados["atualizados"].append(linha['condominio'])

            conexao.commit()

    except Exception as e:
        print(f"Erro ao inserir ou atualizar dados: {e}")

    finally:
        conexao.close()

    resposta_for_log = ""
    if condominios_processados["inseridos"]:
        resposta_for_log += "Condomínios inseridos no banco de dados:\n"
        resposta_for_log += "\n".join(f"- {condominio}" for condominio in condominios_processados["inseridos"])
    if condominios_processados["atualizados"]:
        if resposta_for_log:
            resposta_for_log += "\n\n"
        resposta_for_log += "Condomínios atualizados no banco de dados:\n"
        resposta_for_log += "\n".join(f"- {condominio}" for condominio in condominios_processados["atualizados"])
    if not resposta_for_log:
        resposta_for_log = "Nenhum novo condomínio foi inserido ou atualizado."

    print(resposta_for_log)
    return resposta_for_log
