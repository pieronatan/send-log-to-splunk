# Projeto Splunk Log Manager

## Descrição

Este projeto é um gerenciador de logs para Splunk, desenvolvido em Python. Ele coleta logs, os formata e envia para o Splunk HTTP Event Collector (HEC) em lotes.

## Estrutura do Projeto

- `infra/`: Contém arquivos de configuração do Terraform para infraestrutura na AWS.
    - `cloudwatch.tf`: Configuração do grupo de logs do CloudWatch.
    - `backend.tf`: Configuração do backend do Terraform.
- `src/`: Contém o código-fonte do projeto.
    - `utils.py`: Funções utilitárias.
    - `splunk_manager.py`: Implementação do gerenciador de logs para Splunk.

## Pré-requisitos

- Python 3.6+
- Terraform
- AWS CLI configurado
- Variáveis de ambiente configuradas:
    - `SPLUNK_HEC_URL`: URL do Splunk HEC.
    - `SPLUNK_HEC_TOKEN`: Token de autenticação do Splunk HEC.
    - `SPLUNK_HEC_INDEX`: Índice do Splunk onde os logs serão armazenados.

## Instalação

1. Clone o repositório:
    ```sh
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_REPOSITORIO>
    ```

2. Crie um ambiente virtual e instale as dependências:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install urllib3
    ```

3. Configure a infraestrutura usando Terraform:
    ```sh
    cd infra
    terraform init
    terraform apply
    ```

## Contribuição

1. Faça um fork do projeto.
2. Crie uma nova branch (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça um push para a branch (`git push origin feature/nova-feature`).
5. Crie um novo Pull Request.
