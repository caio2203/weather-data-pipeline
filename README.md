# 🌤️ Weather Data Pipeline

Este projeto implementa um pipeline de dados utilizando **Python**, que coleta dados de previsão do tempo de uma API pública, processa essas informações e armazena em arquivos **JSON** para posterior análise ou integração.

O objetivo é demonstrar habilidades essenciais para a área de **Engenharia de Dados**, como integração com APIs, ETL com Python e persistência de dados.

---

## 🧰 Tecnologias Utilizadas

- [Python 3.12+](https://www.python.org/)
- [Bibliotecas Python: requests, pandas, etc.]
- [OpenWeather API](https://openweathermap.org/api)

---

## 🛠️ Funcionalidades

- 🌐 Coleta de dados via API pública
- 🧹 Transformação e limpeza dos dados com Python
- 🗃️ Armazenamento dos dados em arquivos JSON

---

## ⚙️ Como Executar o Projeto

1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd weather-data-pipeline
```

2. (Opcional) Crie e ative um ambiente virtual Python

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências necessárias

```bash
pip install -r requirements.txt
```

4. Configure sua chave de API do OpenWeather em um arquivo `.env` ou diretamente nos scripts.

5. Execute os scripts conforme desejado:

```bash
python scripts/fetch_weather.py
python scripts/transform_weather.py
python scripts/load_to_db.py
```

---

## 📂 Estrutura do Projeto

```
weather-data-pipeline/
├── scripts/                 # Scripts Python de ETL
│   ├── fetch_weather.py
│   ├── transform_weather.py
│   └── load_to_db.py
├── data/                    # Arquivos JSON de dados coletados
├── README.md
└── ...                      # Outros arquivos e pastas
```

---

## 📌 Objetivo

Este projeto foi desenvolvido como parte do meu aprendizado prático para atuar como Engenheiro de Dados Júnior, com foco em pipelines de dados, automação e boas práticas em Python.

---

## ✨ Melhorias Futuras

- Dashboard com Streamlit para visualização dos dados
- Deploy em nuvem (ex: AWS EC2 + RDS)
- Adição de testes unitários nos scripts

---

## 👨‍💻 Autor

Caio
