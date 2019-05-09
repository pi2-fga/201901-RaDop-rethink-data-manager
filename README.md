# Rethink Data Manager

O **RDM (Rethink Data Manager)** é o serviço responsável por comunicar sistemas com o banco de dados RethinkDB do projeto, além de suprir, via websocket, um servidor com informação de mensagens de atualização da execução (Status) dos sistemas e subsistemas da Folha de Pagamento.

## Parâmetro

O **RDM** roda no formato [websocket](https://tools.ietf.org/html/rfc6455), dessa forma ele espera uma mensagem no canal de comunicação, a mensagem inicial deve ser um __JSON__ no seguinte formato:

```json
{
    "message": ""
}
```

## Tecnologia Utilizada

- [Websockets (Python)](https://websockets.readthedocs.io/en/stable/index.html)
- [E/S Assíncronos (Python)](https://docs.python.org/3/library/asyncio.html)
- [RethinkDB (Python)](https://rethinkdb.com/)
- Python 3

## Ambiente de Desenvolvimento

Para evoluções e desenvolvimento basta ter instalado em sua máquina o Python 3 e as demais dependências do projeto (que são explicadas logo a baixo), além do seu editor de texto de preferência.

## Ambiente de testes local

Antes da instalação das ferramentas de ambiente, certifique-se de que você tem um banco de dados [RethinkDB](https://www.rethinkdb.com/) rodando para a realização dos testes. O **RDM** ainda precisa que exista o _database_ **pytest_schema**, com as _tables_ **pytest_empty_table** e **pytest_table** para que os testes possam ser executados.

Recomendados a utilização de um ambiente virtual criado pelo módulo `virtualenvwrapper`.
Existe um sítio virtual com instruções em inglês para a instalação que pode ser acessado [aqui](https://virtualenvwrapper.readthedocs.io/en/latest/install.html). Mas você pode também seguir o roteiro abaixo para a instalação do ambiente:

```shell
sudo python3 -m pip install -U pip             # Faz a atualização do pip
sudo python3 -m pip install virtualenvwrapper  # Caso queira instalar apenas para o usuário use a opt --user
```

Agora configure o seu shell para utilizar o virtualenvwrapper, adicionando essas duas linhas ao arquivo de inicialização do seu shell (`.bashrc`, `.profile`, etc.)

```shell
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```

Caso queira adicionar um local específico de projeto basta adicionar uma terceira linha com o seguinte `export`:

```shell
export PROJECT_HOME=/path/to/project
```

Execute o arquivo de inicialização do shell para que as mudanças surtam efeito, por exemplo:

```shell
source ~/.bashrc
```

Agora crie um ambiente virtual com o seguinte comando (colocando o nome que deseja para o ambiente), neste exemplo usarei o nome composta:

```shell
mkvirtualenv rethink-data
```

Para utilizá-lo:

```shell
workon rethink-data
pip install -r requirements.txt   # Irá instalar todas as dependências usadas no projeto
```

## Configurando as variáveis de ambiente

O **RDM** permite uma configuração dinâmica a partir de algumas variáveis de ambiente, elas visam agilizar algumas mudanças e são usadas bastante no serviço, abaixo uma lista das variáveis e qual seu papel no **RDM**:

- ReDB_HOST: O endereço do host do banco de dados Rethink no qual o **RDM** deve se conectar. O padrão é `rethink`, que é o nome da rede docker para o funcionamento do serviço **RDM**, para realizar os testes o recomendado é usar `localhost`;
- ReDB_PORT: A porta no qual o banco de dados Rethink está operando. O padrão do RethinkDB é a porta `28015`, mas caso o seu banco esteja configurado diferente, indique nesta variável;
- ReDB_DEFAULT_DB: Define o _database_ padrão em que o serviço deve trabalhar. O padrão é `STATUS`, que deve ser o banco configurado para o envio de status, mas caso deseje transmitir status de outra _database_ indique nesta variável;
- WS_HOST: Indica em qual endereço o servidor WebSocket será servido. O padrão é `0.0.0.0`, que equivale ao localhost;
- WS_PORT: Indica em qual porta o servidor WebSocket será servido. O padrão é `8765`;

Exemplo de configuração de uma variável de ambiente:

```shell
export ReDB_HOST='0.0.0.0'
```

Caso o comando acima for executado no terminal ele valerá apenas enquanto a sessão desse terminal estiver viva, para uma configuração mais duradoura edite o `.bashrc` ou o `.profile` da sua máquina, assim as variáveis de ambiente configuradas sempre estarão disponíveis no sistema.

## Deploy local para desenvolvimento

Para deploy do servidor, basta seguir o roteiro abaixo:

```shell
python3 src/main.py
```

Esse comando irá subir o servidor RDM e após alguns instantes ele estará pronto para o uso.

Para testar a comunicação com um _client_ basta rodar em um outro terminal o código, também presente no projeto:

```shell
python3 src/client.py
```

Dessa forma é possível fazer testes.

Garanta que o RethinkDB esteja rodando e acessível, e, se for necessário, configure as demais variáveis dentro de `service/service.py`

## Execução do ambiente de testes

Para executar os testes do __RDM__ siga o roteiro abaixo:

```shell
pip install -r requirements.txt
sudo python3 -m pip install -r requirements.txt   # Ou caso não esteja trabalhando com uma virtualenv
```

**OBS**: Caso queria instalar apenas para o usuário e não no sistema use a opt `--user` ao final do comando pip.

Após a instalação das dependências basta rodar:

### Testes

```shell
pytest
```

### Cobertura de Código

```shell
pytest --cov=src src/tests/ --cov-report xml
pytest --cov=src src/tests/ --cov-report html:docs/html
```

### Linter

```shell
flake8 .
```

## _Build_

Para construir e rodar o container do microsserviço basta rodar os seguintes comandos:

```shell
docker build -t rethink-data-manager:latest .
docker run -d --name rethink-data-manager -p 8765:8765 --net=host rethink-data-manager
```