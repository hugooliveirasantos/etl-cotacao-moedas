import pandas as pd
from datetime import datetime
from extract import get_currency_data

def transform_data(currency_pair="USD-BRL", days=30):
    """
    Transforma os dados extraídos, calculando médias diárias e semanais.
    
    :param currency_pair: Par de moedas (ex: USD-BRL, EUR-BRL)
    :param days: Número de dias para buscar cotações históricas
    :return: DataFrame transformado com médias diárias e semanais
    """
    
    # Extrair os dados da API
    raw_data = get_currency_data(currency_pair, days)
    if not raw_data:
        print("Nenhum dado foi extraído.")
        return None
    
    # Criar um DataFrame a partir dos dados extraídos
    df = pd.DataFrame(raw_data)
    
    # Converter colunas para numérico
    df["high"] = pd.to_numeric(df["high"])
    df["low"] = pd.to_numeric(df["low"])
    df["bid"] = pd.to_numeric(df["bid"])
    df["ask"] = pd.to_numeric(df["ask"])
    
    # Converter a coluna de data para formato datetime
    df["date"] = pd.to_datetime(df["date"])
    
    # Calcular média diária
    df_daily = df.groupby("date").agg({
        "high": "mean",
        "low": "mean",
        "bid": "mean",
        "ask": "mean",
    }).reset_index()
    
     # Calcular média semanal
    df["week"] = df["date"].dt.strftime("%Y-%U")  # Criar coluna com ano-semana
    df_weekly = df.groupby("week").agg({
        "high": "mean",
        "low": "mean",
        "bid": "mean",
        "ask": "mean"
    }).reset_index()
    
    return df_daily, df_weekly

if __name__ == "__main__":
    daily, weekly = transform_data()
    print("Média Diária:")
    print(daily.head())  # Exibir apenas as primeiras linhas
    print("\nMédia Semanal:")
    print(weekly.head())
