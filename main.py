from modules.database import conecta_banco, salva_veiculos, salva_moedas
from modules.api_client import busca_moedas
from modules.scraper import busca_itens


def pipeline():
    conecta_banco()
    lista_veiculos = busca_itens()
    if lista_veiculos:
        salva_veiculos(lista_veiculos)
    else:
        print("Erro na operação de salvar veículos")

    cotacao_moedas = busca_moedas()
    if cotacao_moedas:
        salva_moedas(cotacao_moedas)
    else:
        print("Erro na operação de salvar moedas")


if __name__ == "__main__":
    pipeline()
