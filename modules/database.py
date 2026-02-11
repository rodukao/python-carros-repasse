import os
import sqlite3

# caminhos
caminho_projeto = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))
caminho_banco = os.path.join(caminho_projeto, "data")


def conecta_banco():

    # cria diretório do banco caso não exista
    try:
        if not os.path.exists(caminho_banco):
            os.mkdir(caminho_banco)
            print("Diretório criado com sucesso!")
        else:
            print("O diretório já existe.")
    except Exception as e:
        print("Falha ao criar diretório: ", e)

    try:
        with sqlite3.connect(os.path.join(caminho_banco, "monitor_repasse.db")) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS veiculos (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, preco_brl REAL, quilometragem REAL, ano INTEGER, link TEXT UNIQUE)")
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS moedas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, valor_brl REAL, data_consulta DATETIME DEFAULT (DATETIME('now', 'localtime')))")
            conexao.commit()
    except Exception as e:
        print("Falha ao criar tabelas no banco de dados: ", e)


def salva_veiculos(lista_veiculos):

    try:
        with sqlite3.connect(os.path.join(caminho_banco, "monitor_repasse.db")) as conexao:
            cursor = conexao.cursor()
            sql = "INSERT OR IGNORE INTO veiculos (titulo, preco_brl, quilometragem, ano, link) VALUES (?, ?, ?, ?, ?)"
            lista_formatada = [
                (v['titulo'], v['preco'], v['km'], v['ano'], v['link']) for v in lista_veiculos]
            cursor.executemany(sql, lista_formatada)
            conexao.commit()

            print(f"Sucesso! {cursor.rowcount} novos registros processados.")

    except Exception as e:
        print("Erro ao inserir veículo: ", e)


def salva_moedas(moedas: dict):

    try:
        with sqlite3.connect(os.path.join(caminho_banco, "monitor_repasse.db")) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO moedas (nome, valor_brl) VALUES (?, ?)", ('bitcoin', moedas['bitcoin']))
            cursor.execute(
                "INSERT INTO moedas (nome, valor_brl) VALUES (?, ?)", ('dolar', moedas['dolar']))
            conexao.commit()
            print("Cotação do dia inserida com sucesso!")
    except Exception as e:
        print("Erro ao inserir as cotações diárias: ", e)


if __name__ == "__main__":
    conecta_banco()
