## cria uma versão do banco
flask --app app db migrate -m "Base inicial"

## atualiza a base de dados
flask db upgrade

## desatualiza a base de dados
flask db downgrade