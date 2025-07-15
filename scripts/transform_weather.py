# Importa a biblioteca openmeteo_requests, que serve para acessar dados de clima da API Open-Meteo
import openmeteo_requests

# Importa a biblioteca pandas, usada para manipular tabelas de dados (DataFrames)
import pandas as pd
# Importa requests_cache, que permite guardar respostas da internet para não precisar baixar de novo
import requests_cache
# Importa retry, que tenta novamente caso uma requisição falhe
from retry_requests import retry

# Configura o cache para guardar respostas por 1 hora (3600 segundos)
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
# Configura para tentar até 5 vezes caso a requisição falhe, esperando um pouco entre as tentativas
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
# Cria o cliente da API Open-Meteo usando as configurações acima
openmeteo = openmeteo_requests.Client(session = retry_session)

# Define a URL da API e os parâmetros do que queremos buscar (latitude, longitude, variáveis diárias, horárias e atuais)
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": -14.8661,  # Latitude do local
    "longitude": -40.8394, # Longitude do local
    # Lista de variáveis diárias que queremos buscar
    "daily": ["temperature_2m_max", "temperature_2m_min", "apparent_temperature_min", "apparent_temperature_max", "sunset", "daylight_duration", "sunshine_duration", "sunrise", "uv_index_max"],
    # Lista de variáveis horárias que queremos buscar
    "hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation_probability", "rain"],
    # Lista de variáveis atuais que queremos buscar
    "current": ["temperature_2m", "apparent_temperature", "relative_humidity_2m", "is_day", "rain"],
    "timezone": "America/Sao_Paulo" # Fuso horário
}
# Faz a requisição para a API e guarda a resposta
responses = openmeteo.weather_api(url, params=params)

# Pega a resposta do primeiro local (caso tivesse mais de um)
response = responses[0]
# Imprime informações básicas do local consultado
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Pega os dados atuais (do momento) e guarda cada variável em uma variável do Python
current = response.Current()
current_temperature_2m = current.Variables(0).Value()         # Temperatura atual
current_apparent_temperature = current.Variables(1).Value()   # Sensação térmica atual
current_relative_humidity_2m = current.Variables(2).Value()   # Umidade relativa atual
current_is_day = current.Variables(3).Value()                 # Se é dia (1) ou noite (0)
current_rain = current.Variables(4).Value()                   # Chuva atual

# Imprime os dados atuais
print(f"Current time {current.Time()}")
print(f"Current temperature_2m {current_temperature_2m}")
print(f"Current apparent_temperature {current_apparent_temperature}")
print(f"Current relative_humidity_2m {current_relative_humidity_2m}")
print(f"Current is_day {current_is_day}")
print(f"Current rain {current_rain}")

# Pega os dados por hora (horários)
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()           # Temperatura por hora
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()     # Umidade por hora
hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()     # Sensação térmica por hora
hourly_precipitation_probability = hourly.Variables(3).ValuesAsNumpy()# Probabilidade de chuva por hora
hourly_rain = hourly.Variables(4).ValuesAsNumpy()                     # Chuva por hora

# Cria uma tabela (DataFrame) com as datas e os dados horários
hourly_data = {"date": pd.date_range(
    start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),      # Data/hora inicial
    end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),     # Data/hora final
    freq = pd.Timedelta(seconds = hourly.Interval()),                   # Intervalo entre dados
    inclusive = "left"                                                  # Inclui a data inicial, exclui a final
)}
# Adiciona cada variável à tabela
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["apparent_temperature"] = hourly_apparent_temperature
hourly_data["precipitation_probability"] = hourly_precipitation_probability
hourly_data["rain"] = hourly_rain

# Cria o DataFrame (tabela) com os dados horários
hourly_dataframe = pd.DataFrame(data = hourly_data)
# Mostra a tabela na tela
print(hourly_dataframe)

# Pega os dados diários (um valor por dia)
daily = response.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()         # Temperatura máxima do dia
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()         # Temperatura mínima do dia
daily_apparent_temperature_min = daily.Variables(2).ValuesAsNumpy()   # Sensação térmica mínima do dia
daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()   # Sensação térmica máxima do dia
daily_sunset = daily.Variables(4).ValuesInt64AsNumpy()                # Horário do pôr do sol
daily_daylight_duration = daily.Variables(5).ValuesAsNumpy()          # Duração do dia (em segundos)
daily_sunshine_duration = daily.Variables(6).ValuesAsNumpy()          # Duração do sol (em segundos)
daily_sunrise = daily.Variables(7).ValuesInt64AsNumpy()               # Horário do nascer do sol
daily_uv_index_max = daily.Variables(8).ValuesAsNumpy()               # Índice UV máximo do dia

# Cria uma tabela (DataFrame) com as datas e os dados diários
daily_data = {"date": pd.date_range(
    start = pd.to_datetime(daily.Time(), unit = "s", utc = True),       # Data inicial
    end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),      # Data final
    freq = pd.Timedelta(seconds = daily.Interval()),                    # Intervalo entre dados (1 dia)
    inclusive = "left"                                                  # Inclui a data inicial, exclui a final
)}
# Adiciona cada variável à tabela
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
daily_data["sunset"] = daily_sunset
daily_data["daylight_duration"] = daily_daylight_duration
daily_data["sunshine_duration"] = daily_sunshine_duration
daily_data["sunrise"] = daily_sunrise
daily_data["uv_index_max"] = daily_uv_index_max

# Cria o DataFrame (tabela) com os dados diários
daily_dataframe = pd.DataFrame(data = daily_data)
# Mostra a tabela na tela
print(daily_dataframe)

