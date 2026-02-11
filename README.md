# Monitor de Repasse de Veículos

Este projeto é um dashboard interativo desenvolvido em Python para monitorar anúncios de veículos em plataformas de repasse, integrando cotações de moedas (Bitcoin e Dólar) em tempo real para análise de poder de compra e precificação.

## Funcionalidades

**Scraping de Dados:** Coleta automática de informações como título, preço, quilometragem, ano e link de anúncios.
**Integração com API:** Busca cotações atualizadas de BTC e USD via API externa.
**Banco de Dados Local:** Armazenamento persistente utilizando SQLite para histórico de preços e veículos.
**Dashboard Interativo:** Interface desenvolvida em Streamlit com:
. Filtros de preço máximo e intervalo de anos.
. Conversão automática de valores para BTC e USD.
. Gráficos de dispersão para análise de distribuição de preços por ano.
. Sistema de fallback que utiliza a última cotação salva caso a API esteja indisponível.

## Tecnologias Utilizadas
Python 3.x
Streamlit (Interface do Dashboard)
Pandas (Processamento e análise de dados)
SQLite3 (Banco de dados relacional)
Selenium / Requests (Web Scraping)

## Como Instalar
1. Clone o repositório:
```git clone [https://github.com/rodukao/python-carros-repasse.git]```
```cd nome-do-repositorio```

2. Crie um ambiente virtual e ative-o:python -m venv .venv
No Windows:
```.venv\Scripts\activate```
No Linux/Mac:
```source .venv/bin/activate```

3. Instale as dependências:pip install -r requirements.txt

## Como Usar
### Executar o Scraper
Para atualizar o banco de dados com novos veículos e cotações manualmente via terminal:
```python main.py```

### Iniciar o Dashboard
Para visualizar os dados e interagir com os filtros:
```streamlit run dashboard.py```

## Estrutura do Projeto
- main.py: Script principal para execução do fluxo de coleta e salvamento.
- dashboard.py: Código fonte da interface Streamlit
    - modules/:
        - api_client.py: Lógica de consumo de APIs de moedas.
        - database.py: Funções de criação de tabelas e persistência de dados.
        - scraper.py: Lógica de extração de dados da web.
    - data/: Pasta destinada ao arquivo de banco de dados SQLite.
    
Projeto desenvolvido para fins de estudo e monitoramento de mercado.
