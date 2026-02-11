import requests


def busca_moedas():
    moedas = {
        'bitcoin': None,
        'dolar': None
    }

    try:
        request_bitcoin = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?vs_currencies=brl&ids=bitcoin")
        valor_bitcoin = request_bitcoin.json()['bitcoin']['brl']
        moedas['bitcoin'] = float(valor_bitcoin)
    except Exception as e:
        print("Não foi possível obter o preço do bitcoin: ", e)

    try:
        request_dolar = requests.get(
            "https://economia.awesomeapi.com.br/last/USD")
        valor_dolar = request_dolar.json()['USDBRL']['bid']
        moedas['dolar'] = float(valor_dolar)
    except Exception as e:
        print("Não foi possível obter o valor do dólar: ", e)

    return moedas


if __name__ == "__main__":
    valor_moedas = busca_moedas()
    print(valor_moedas)
