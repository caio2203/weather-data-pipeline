# 🌤️ Weather Data Pipeline

Este projeto implementa um pipeline de dados automatizado usando **Python**, que coleta dados de previsão do tempo de uma API pública, processa essas informações e armazena em um arquivo **CSV**.

O objetivo é demonstrar habilidades essenciais para a área de **Engenharia de Dados**, como orquestração de workflows, integração com APIs, ETL com Python e persistência de dados em banco relacional.

---

## 🧰 Tecnologias Utilizadas

- [Python 3.9+](https://www.python.org/)
- [Docker & Docker Compose](https://www.docker.com/)
- [OpenWeather API](https://openweathermap.org/api)

---

## 🛠️ Funcionalidades

- 🌐 Coleta de dados via API pública
- 🧹 Transformação e limpeza dos dados com Python
- 🗃️ Armazenamento dos dados em CSV

---

## ⚙️ Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/weather-data-pipeline-airflow.git
cd weather-data-pipeline


    🔑 Para obter a API Key, cadastre-se gratuitamente em https://openweathermap.org/api

3. Suba os containers com Docker

docker-compose up -d

📂 Estrutura do Projeto

weather-data-pipeline/
├── scripts/                 # Scripts Python de ETL
│   ├── fetch_weather.py
│   ├── transform_weather.py
│   └── load_to_postgres.py
├── data/                    # arquivo CSV
├── .env                     # Variáveis de ambiente (não versionado)
├── docker-compose.yml       # Ambiente Docker
└── README.md

📌 Objetivo

Este projeto foi desenvolvido como parte do meu aprendizado prático para atuar como Engenheiro de Dados Júnior, com foco em pipelines de dados, automação e boas práticas de orquestração com Airflow.
✨ Melhorias Futuras

    Dashboard com Streamlit para visualização dos dados

    Deploy em nuvem (ex: AWS EC2 + RDS)

    Uso de Sensor no Airflow para aguardar condições específicas

    Adição de testes unitários nos scripts

👨‍💻 Autor

Caio
