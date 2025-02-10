import requests
import json
from datetime import datetime

def get_currency_data(currency_pair="USD-BRL", days=30):
    """
    Extrai os dados de cotação da moeda fornecida pela API AwesomeAPI.

    :param currency_pair: Par de moedas (ex: USD-BRL, EUR-BRL)
    :param days: Número de dias para buscar cotações históricas
    :return: Lista de dicionários com os dados de cotação
    """
    url = f"https://economia.awesomeapi.com.br/json/daily/{currency_pair}/{days}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança erro se a requisição falhar
        data = response.json()

        extracted_data = []
        for entry in data:
            extracted_data.append({
                "timestamp": int(entry["timestamp"]),
                "date": datetime.fromtimestamp(int(entry["timestamp"])).strftime("%Y-%m-%d"),
                "high": float(entry["high"]),
                "low": float(entry["low"]),
                "bid": float(entry["bid"]),
                "ask": float(entry["ask"]),
            })

        return extracted_data

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição da API: {e}")
        return None

# Teste rápido
if __name__ == "__main__":
    cotacoes = get_currency_data()
    print(json.dumps(cotacoes[:5], indent=4))  # Exibir apenas as 5 primeiras entradas
