# Rethink Data Manager

[![Continuous Integration](https://travis-ci.org/radar-pi/rethink-data-manager.svg?branch=develop)](https://travis-ci.org/radar-pi/rethink-data-manager)
[![Maintainability](https://api.codeclimate.com/v1/badges/3e7d48b6113707baa23d/maintainability)](https://codeclimate.com/github/radar-pi/rethink-data-manager/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/3e7d48b6113707baa23d/test_coverage)](https://codeclimate.com/github/radar-pi/rethink-data-manager/test_coverage)

O **RDM (Rethink Data Manager)** é o serviço responsável por comunicar sistemas com o banco de dados RethinkDB do projeto, além de suprir, via websocket, um servidor com informação de mensagens de atualização da execução (Status) dos sistemas e subsistemas da Folha de Pagamento.

## Parâmetro

O **RDM** roda no formato [websocket](https://tools.ietf.org/html/rfc6455), dessa forma ele espera uma mensagem no canal de comunicação, a mensagem inicial deve ser um __JSON__ no seguinte formato:

```shell
{
    "id": "4bb803f2-68d8-4464-879f-3bf65aa9cc9f", # UUID identificador do pacote
    "type": "rethink-manager-call", # Tipo de chamada esperado para o RDM, chamadas diferentes serão ignoradas
    "payload": { # Dentro do payload vai ter os dados que serão usados para as operações de banco. Vão variar de acordo com a chamada
        "database": "test", # O esquema do banco da operação (mandatório)
        "table": "test", # A tabala do banco da operação (mandatório)
        "data": { # Objeto JSON da operação (inserção e atualização)
            "key": "value",
            "other_key":  2
        },
        "identifier": "a02263d6-fb4e-4cc0-ab81-0684fbe72df8" # Identificador da operação (seleção ou deleção)
    },
    "time": "2019-05-18T20:59:26.346996Z" # Data e hora da requisição no formato RFC3339
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

- `ReDB_HOST`: O endereço do host do banco de dados Rethink no qual o **RDM** deve se conectar. O padrão é `rethink`, que é o nome da rede docker para o funcionamento do serviço **RDM**, para realizar os testes o recomendado é usar `localhost`;
- `ReDB_PORT`: A porta no qual o banco de dados Rethink está operando. O padrão do RethinkDB é a porta `28015`, mas caso o seu banco esteja configurado diferente, indique nesta variável;
- `ReDB_DEFAULT_DB`: Define o _database_ padrão em que o serviço deve trabalhar. O padrão é `test`, que deve ser o banco configurado para o envio de status, mas caso deseje transmitir status de outra _database_ indique nesta variável;
- `ReDB_USER`: O usuário para autenticação no banco de dados RethinkDB. O padrão do RethinkDB é `admin`, mas caso tenha usuários diferentes para as operações basta indicar;
- `ReDB_PASS`: A senha do usuário para autenticação no banco de dados RethinkDB. O padrão é uma _string_ vazia, caso sua configuração esteja diferente basta indicar;
- `ReDB_AUDIT_DB`: Define o _database_ padrão para os arquivos de auditoria. Nesse _database_ devem haver as tabelas para salvar os dados recebidos dos serviços para auditoria. O _database_ padrão é chamado `AUDIT`;
- `ReDB_AUDIT_TABLE`: Define a tabela no qual o própio serviço do RDM salvará os dados recebidos por ele. O padrão é a tabela `rethink_data_manager` (nome do serviço). Caso queira indicar em outro formato para salvar basta configurar esta variável;
- `WS_HOST`: Indica em qual endereço o servidor WebSocket será servido. O padrão é `0.0.0.0`, que equivale ao localhost;
- `WS_PORT`: Indica em qual porta o servidor WebSocket será servido. O padrão é `8765`;

Exemplo de configuração de uma variável de ambiente:

```shell
export ReDB_HOST='0.0.0.0'
```

Caso o comando acima for executado no terminal ele valerá apenas enquanto a sessão desse terminal estiver viva, para uma configuração mais duradoura edite o `.bashrc` ou o `.profile` da sua máquina, assim as variáveis de ambiente configuradas sempre estarão disponíveis no sistema.

## Operações do RDM

O serviço do RDM oferece algumas operações do banco de dados RethinkDB, sendo grande parte deles relacionado com operações comuns com o _CRUD_ (_Create_, _Read_, _Update_ e _Delete_) de objetos. Abaixo estão listados as operações que o _websocket_ oferece a partir da URL do seu endereço:

- `/health`

Operação usada para verificar a saúde do serviço RDM. Não é preciso fazer envio de nenhum dado, apenas uma chamada e o serviço deve retornar a mensagem:

```text
Server Up and Running!
```

A URL de chamada vai depender da configuração do _host_ e da porta do _webscoket_, mas o exemplo em testes locais seria `localhost:8765/health`

- `/insert`

Operação usada para fazer inserção de dados no banco de dados. O modelo de mensagem para envio e para garantir o funcionamento da operação é:

```shell
{
    "id": "df03c48c-62fb-4f07-8a4b-7610fbe3adca",
    "type": "rethink-data-call",
    "payload": {
        "database": "database", # Nome do esquema que será usado
        "table": "table", # Nome da tabela que será usada
        "data": { # Objeto JSON que vai ser inserido
            "key": 1
        }
    },
    "time": "2019-05-18T22:34:52.490439Z"
}
```

Logo para a inserção, no `payload` deve haver as informações do `database`, `table` e o `data` (Objeto JSON).

A URL de chamada vai depender da configuração do _host_ e da porta do _webscoket_, mas o exemplo em testes locais seria `localhost:8765/insert`

- `/get`

Operação para fazer a busca de um único objeto no banco de dados. O modelo de mensagem para envio e para garantir o funcionamento da operação é:

```shell
{
    "id": "929b113d-91ab-41ab-87ca-7bc0e704fc7f",
    "type": "rethink-data-call",
    "payload": {
        "database": "database", # Nome do esquema que será usado
        "table": "table", # Nome da tabela que será usada
        "identifier": "2a33eda5-040c-40dc-ba1e-dcb8d2f5b140" # Identificador do objeto que se deseja recuperar
    },
    "time": "2019-05-18T22:40:20.755916Z"
}
```

Logo para a seleção, no `payload` deve haver as informações do `database`, `table` e o `identifier`. Sendo o `identifier` a chave do objeto que se deseja recuperar dentro do RethinkDB.

A URL de chamada vai depender da configuração do _host_ e da porta do _webscoket_, mas o exemplo em testes locais seria `localhost:8765/get`

- `/get_all`

Operação para listar todos os objetos de uma tabela no banco de dados. O modelo de mensagem para envio e para garantir o funcionamento da operação é:

```shell
{
    "id": "a5093f52-bde6-4c74-8989-c36d00e7d7b5",
    "type": "rethink-data-call",
    "payload": {
        "database": "database", # Nome do esquema que será usado
        "table": "table" # Nome da tabela que será usada
    },
    "time": "2019-05-18T22:42:35.267029Z"
}
```

Logo para a listagem, no `payload` deve haver as informações do `database` e a `table`.

A URL de chamada vai depender da configuração do _host_ e da porta do _webscoket_, mas o exemplo em testes locais seria `localhost:8765/get_all`

- `/update`

Operação para atualizar algum objeto do banco de dados. O modelo de mensagem para envio e para garantir o funcionamento da operação é:

```shell
{
    "id": "1174969a-c838-49cb-9751-66bb1be22af9",
    "type": "rethink-data-call",
    "payload": {
        "database": "database", # Nome do esquema que está o objeto
        "table": "table", # Nome da tabela que está o objeto
        "identifier": "23af3f1e-ee59-462a-bf41-abbb974ae3ea", # ID do objeto que se deseja atualizar (os IDs gerados pelo RethinkDB para os objetos também usa o formato UUID)
        "data": { # Declaração de atualização (as chaves e valores que estiverem na declaração serão atualizados ou adicionados), sendo um objeto JSON
            "key": 1
        }
    },
    "time": "2019-05-18T22:34:52.490439Z"
}
```

Logo para atualização, no `payload` deve haver as informações do `database`, `table`, `identifier` (aqui deve constar o ID do objeto que deseja se atualizar, pode ser recuperado pela operação `get` ou `get_all`) e `data` (aqui deve constar a declaração de atualização, logo o objeto JSON que constar nessa chave vai atualizar as chaves e valores que existirem no objeto, caso alguma chave não exista ela será incluída).

A URL de chamada vai depender da configuração do _host_ e da porta do _webscoket_, mas o exemplo em testes locais seria `localhost:8765/update`

- `/delete`

Operação para deletar algum objeto no banco de dados. O modelo de mensagem para envio e para garantir o funcionamento da operação é:

```shell
{
    "id": "f2da2d37-01c7-4a42-b681-dc4dfa3dc225",
    "type": "rethink-data-call",
    "payload": {
        "database": "database", # Nome do esquema que está o objeto
        "table": "table", # Nome da tabela que está o objeto
        "identifier": "efa67d0b-0d63-4962-b7a7-440ae2ee0848" # ID do objeto que se deseja deletar (os IDs gerados pelo RethinkDB para os objetos também usa o formato UUID)
    },
    "time": "2019-05-18T22:53:13.594738Z"
}
```

Logo para deleção, no `payload` deve haver as informações do `database`, `table` e `identifier` (aqui deve constar o ID do objeto que deseja se deletar, pode ser recuperado pela operação `get` ou `get_all`). Lembre-se que essa ação deletará o objeto e não pode ser desfeita.

A URL de chamada vai depender da configuração do _host_ e da porta do _webscoket_, mas o exemplo em testes locais seria `localhost:8765/delete`

- `delete_all`

Operação para deletar todos os objetos de uma tabela no banco de dados. O modelo de mensagem para envio e para garantir o funcionamento da operação é:

```shell
{
    "id": "b991a2c2-c4c9-4e69-a760-aebb173fcafe",
    "type": "rethink-data-call",
    "payload": {
        "database": "database", # Nome do esquema que deseja fazer a deleção
        "table": "table" # Nome da tabela onde se deseja deletar todos os objetos
    },
    "time": "2019-05-18T22:57:42.552426Z"
}
```

Logo para deleção de todos os objetos, no `payload` deve haver as informações do `database` e `table`. Lembre-se que essa ação deletará todos os objetos e não pode ser desfeita.

A URL de chamada vai depender da configuração do _host_ e da porta do _webscoket_, mas o exemplo em testes locais seria `localhost:8765/delete_all`

- `/create_table`

Operação para criar uma nova tabela no esquema do banco de dados. O modelo de mensagem para envio e para garantir o funcionamento da operação é:

```shell
{
    "id": "026b20aa-5fa1-4c28-b506-2ee24096fb74",
    "type": "rethink-data-call",
    "payload": {
        "database": "database", # Nome do esquema onde será criada a nova tabela
        "table": "new_table" # Nome da nova tabela
    },
    "time": "2019-05-18T23:01:41.355693Z"
}
```

Logo para a criação da tabela, no `payload` deve haver as informações do `database` e `table` (os nomes das tabelas só podem ter caracteres alfanuméricos, não pode começar em digitos e o único caractere aceito para separar palavras é o sublinhado `_`, do inglês _underscore_).

A URL de chamada vai depender da configuração do _host_ e da porta do _webscoket_, mas o exemplo em testes locais seria `localhost:8765/create_table`

__OBS__: Qualquer erro que ocorra nas operações o pacote _response_ deverá enviar uma mensagem. Para informações mais completas basta verificar os _logs_ do RDM.

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