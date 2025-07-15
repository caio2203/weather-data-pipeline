# Importa as bibliotecas necessárias:
import openmeteo_requests  # Para acessar a API de clima Open-Meteo
import pandas as pd        # Para manipular tabelas de dados (DataFrames)
import requests_cache      # Para guardar respostas da internet e evitar baixar de novo
from retry_requests import retry  # Para tentar novamente caso uma requisição falhe
import os                  # Para lidar com pastas e arquivos no computador

# Função que busca os dados do clima
def fetch_weather():
    # Configura o cache para guardar respostas por 1 hora (3600 segundos)
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    # Configura para tentar até 3 vezes caso a requisição falhe, esperando um pouco entre as tentativas
    retry_session = retry(cache_session, retries=3, backoff_factor=0.2)
    # Cria o cliente da API Open-Meteo usando as configurações acima
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Define a URL da API e os parâmetros do que queremos buscar (latitude, longitude, variáveis diárias, horárias e atuais)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -14.8661,   # Latitude do local
        "longitude": -40.8394,  # Longitude do local
        # Lista de variáveis diárias que queremos buscar
        "daily": [
            "temperature_2m_max", "temperature_2m_min", "apparent_temperature_min",
            "apparent_temperature_max", "sunset", "daylight_duration",
            "sunshine_duration", "sunrise", "uv_index_max"
        ],
        # Lista de variáveis horárias que queremos buscar
        "hourly": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature",
            "precipitation_probability", "rain"
        ],
        # Lista de variáveis atuais que queremos buscar
        "current": [
            "temperature_2m", "apparent_temperature", "relative_humidity_2m",
            "is_day", "rain"
        ],
        "timezone": "America/Sao_Paulo"  # Fuso horário
    }

    # Faz a requisição para a API e guarda a resposta
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]  # Pega a resposta do primeiro local (caso tivesse mais de um)

    # --- DADOS ATUAIS ---
    current = response.Current()  # Pega os dados atuais (do momento)
    current_data = {
        "temperature_2m": current.Variables(0).Value(),         # Temperatura atual
        "apparent_temperature": current.Variables(1).Value(),   # Sensação térmica atual
        "relative_humidity_2m": current.Variables(2).Value(),   # Umidade relativa atual
        "is_day": current.Variables(3).Value(),                 # Se é dia (1) ou noite (0)
        "rain": current.Variables(4).Value(),                   # Chuva atual
        "timestamp": pd.to_datetime(current.Time(), unit="s")   # Momento da medição
    }

    # --- DADOS HORÁRIOS ---
    hourly = response.Hourly()  # Pega os dados por hora
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),          # Data/hora inicial
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),         # Data/hora final
            freq=pd.Timedelta(seconds=hourly.Interval()),           # Intervalo entre dados
            inclusive="left"                                        # Inclui a data inicial, exclui a final
        ),
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),      # Temperatura por hora
        "relative_humidity_2m": hourly.Variables(1).ValuesAsNumpy(),# Umidade por hora
        "apparent_temperature": hourly.Variables(2).ValuesAsNumpy(),# Sensação térmica por hora
        "precipitation_probability": hourly.Variables(3).ValuesAsNumpy(), # Probabilidade de chuva por hora
        "rain": hourly.Variables(4).ValuesAsNumpy()                 # Chuva por hora
    }
    hourly_df = pd.DataFrame(hourly_data)  # Cria uma tabela (DataFrame) com os dados horários

    # --- DADOS DIÁRIOS ---
    daily = response.Daily()  # Pega os dados diários (um valor por dia)
    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s"),           # Data inicial
            end=pd.to_datetime(daily.TimeEnd(), unit="s"),          # Data final
            freq=pd.Timedelta(seconds=daily.Interval()),            # Intervalo entre dados (1 dia)
            inclusive="left"                                        # Inclui a data inicial, exclui a final
        ),
        "temperature_2m_max": daily.Variables(0).ValuesAsNumpy(),   # Temperatura máxima do dia
        "temperature_2m_min": daily.Variables(1).ValuesAsNumpy(),   # Temperatura mínima do dia
        "apparent_temperature_min": daily.Variables(2).ValuesAsNumpy(), # Sensação térmica mínima do dia
        "apparent_temperature_max": daily.Variables(3).ValuesAsNumpy(), # Sensação térmica máxima do dia
        "sunset": daily.Variables(4).ValuesInt64AsNumpy(),          # Horário do pôr do sol
        "daylight_duration": daily.Variables(5).ValuesAsNumpy(),    # Duração do dia (em segundos)
        "sunshine_duration": daily.Variables(6).ValuesAsNumpy(),    # Duração do sol (em segundos)
        "sunrise": daily.Variables(7).ValuesInt64AsNumpy(),         # Horário do nascer do sol
        "uv_index_max": daily.Variables(8).ValuesAsNumpy(),         # Índice UV máximo do dia
    }
    daily_df = pd.DataFrame(daily_data)  # Cria uma tabela (DataFrame) com os dados diários

    # Retorna os dados atuais, horários e diários
    return current_data, hourly_df, daily_df

# Teste local: se rodar este arquivo diretamente, executa este bloco
if __name__ == "__main__":
    c, h, d = fetch_weather()  # Busca os dados do clima
    print("CURRENT:")          # Mostra os dados atuais
    print(c)
    print("HOURLY:")           # Mostra as primeiras linhas dos dados horários
    print(h.head())
    print("DAILY:")            # Mostra as primeiras linhas dos dados diários
    print(d.head())

# Função para salvar os dados em arquivos CSV
def save_to_csv(current_data, hourly_df, daily_df):
    os.makedirs("data", exist_ok=True)  # Cria a pasta 'data' se não existir

    # Salva os dados atuais em um arquivo CSV (apenas uma linha)
    pd.DataFrame([current_data]).to_csv("data/weather_current.csv", index=False)

    # Salva os dados horários em um arquivo CSV
    hourly_df.to_csv("data/weather_hourly.csv", index=False)

    # Salva os dados diários em um arquivo CSV
    daily_df.to_csv("data/weather_daily.csv", index=False)

    print("✔️ Arquivos CSV salvos em /data")  # Mensagem de sucesso

# Teste local: se rodar este arquivo diretamente, executa este bloco também
if __name__ == "__main__":
    c, h, d = fetch_weather()      # Busca os dados do clima
    save_to_csv(c, h, d)           # Salva os dados em arquivos CSV