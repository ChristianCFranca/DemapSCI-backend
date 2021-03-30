# DemapSCI-backend
Implementação da API do servidor do Sistema de cadastro de infraestrutura não oficial do Departamento de Infraestrutura e Gestão Patrimonial do Banco Central do Brasil. O sistema é uma REST API implementada em Python utilizando o framework [FastAPI](https://fastapi.tiangolo.com/).

![FastAPI Logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

Este serviço foi construído para ser utilizado em um container [Docker](https://www.docker.com/). O banco de dados atualmente utilizado é o [PostgreSQL](https://www.postgresql.org/) (alterar dados de login no arquivo `database.py`). Caso o PostgreSQL não esteja disponível na máquina host, o banco de dados será alterado para o SQLite e um arquivo local será criado no diretório raíz do projeto.

O serviço já está disponível utilizando a plataforma [Heroku](https://miro.medium.com/max/1838/1*fIjRtO5P8zc3pjs0E5hYkw.png) na URL https://demap-sci-backend.herokuapp.com/. 

Para acessar a documentação criada dinamicamente pelo FastAPI, acessar o endpoint `/docs`: https://demap-sci-backend.herokuapp.com/docs

## Instalação e Execução

Caso deseje rodar este projeto localmente, aqui estão apresentadas as soluções com ou sem o uso do `Docker`.

### Python
1 - Clone este repositório localmente:
> git clone https://github.com/ChristianCFranca/DemapSCI-backend.git

2 - Instale as dependências utilizando o gerenciador de pacotes python `pip` (sugiro criar um ambiente virtual antes: https://docs.python.org/3/library/venv.html):
> pip install -r requirements.txt

3.1 - Rode a API utilizando o comando (necessário python 3 funcional na máquina em questão):

`python main.py`
>INFO:     Started server process [12852] \
>INFO:     Waiting for application startup. \
>INFO:     Application startup complete. \
>INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit) \


3.2 - Também é possível rodar utilizando diretamente o `uvicorn`:

`uvicorn main:app`
>INFO:     Started server process [12852] \
>INFO:     Waiting for application startup. \
>INFO:     Application startup complete. \
>INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit) \

4 - Acesse o endereço fornecido pela API (geralmente http://localhost/8000/docs) e verifique o correto funcionamento.

### Docker
1 - Construa a imagem docker:
> docker build -t NOME_DA_IMAGEM .

2 - Rode o container a partir da imagem criada:
> docker run -t NOME_DO_CONTAINER NOME_DA_IMAGEM

3 - Acesse o endereço da API em http://localhost/80/docs e verifique o correto funcionamento.