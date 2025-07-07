# 🌤️ Weather Data Pipeline com Apache Airflow

Este projeto implementa um pipeline de dados automatizado usando **Apache Airflow**, que coleta dados de previsão do tempo de uma API pública, processa essas informações e armazena em um banco de dados **PostgreSQL**.

O objetivo é demonstrar habilidades essenciais para a área de **Engenharia de Dados**, como orquestração de workflows, integração com APIs, ETL com Python e persistência de dados em banco relacional.

---

## 🧰 Tecnologias Utilizadas

- [Apache Airflow](https://airflow.apache.org/)
- [Python 3.9+](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker & Docker Compose](https://www.docker.com/)
- [OpenWeather API](https://openweathermap.org/api)

---

## 🛠️ Funcionalidades

- ⏱️ Pipeline agendado com Airflow
- 🌐 Coleta de dados via API pública
- 🧹 Transformação e limpeza dos dados com Python
- 🗃️ Armazenamento dos dados no PostgreSQL
- 📧 (Opcional) Envio de alerta por e-mail caso previsão seja de chuva

---

## ⚙️ Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/weather-data-pipeline-airflow.git
cd weather-data-pipeline-airflow

2. Configure o arquivo .env

Crie um arquivo .env na raiz com o seguinte conteúdo:

WEATHER_API_KEY=sua_api_key_aqui
CITY=São Paulo

    🔑 Para obter a API Key, cadastre-se gratuitamente em https://openweathermap.org/api

3. Suba os containers com Docker

docker-compose up -d

    Airflow Web UI: http://localhost:8080
    Login padrão:

        Usuário: admin

        Senha: admin

    PostgreSQL rodando na porta 5432

📂 Estrutura do Projeto

weather-data-pipeline-airflow/
├── dags/                    # Arquivos da DAG do Airflow
│   └── weather_dag.py
├── scripts/                 # Scripts Python de ETL
│   ├── fetch_weather.py
│   ├── transform_weather.py
│   └── load_to_postgres.py
├── data/                    # (opcional) backups locais
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
