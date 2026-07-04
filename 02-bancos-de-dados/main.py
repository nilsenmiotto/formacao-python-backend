import sqlite3
from sqlite import criar_conexao, remover_banco


def main():

    banco = "meu_banco.db"
    remover_banco(banco)
    conexao = criar_conexao(banco)

    if conexao:
        print("Conectado")
    else:
        print("Não foi possível conectar no banco.")
        exit(0)

    cursor = conexao.cursor()
    criar_tabela(cursor)

    nome = "Nilsen"
    email = "meu@email.com"
    dados = (nome, email)
    inserir_registros(conexao, cursor, dados)

    email = "novo@email.com"
    dados = (nome, email, 1)
    atualizar_registros(conexao, cursor, dados)

    dados = (1,)
    remover_registros(conexao, cursor, dados)

    lista_dados = [("joão", "joao@email.com"), ("maria", "maria@email.com")]
    inserir_varios_registros(conexao, cursor, lista_dados)

    print("Recuperando um registro")
    cliente = recuperar_registro(cursor, 2)
    print(cliente)

    print("Recuperando todos os registros")
    clientes = recuperar_todos_registros(cursor)
    for cliente in clientes:
        print(cliente)

    print("Recuperando um registro em dicionario")
    cliente = recuperar_dicionario(cursor, 3)
    print(cliente)

    print("Inserindo registros com rollback")
    try:
        cursor.execute(
            "INSERT INTO Clientes (nome, email) VALUES(?, ?);",
            ("sabrina", "sabrina@email.com"),
        )
        cursor.execute(
            "INSERT INTO Clientes (nome, email) VALUES(?, ?, ?);",
            (2, "ana", "ana@email.com"),
        )
        conexao.commit()
    except Exception as exc:
        print(f"Ocorreu um erro nos insert {exc}")
        conexao.rollback()

    conexao.close()


def criar_tabela(cursor):
    cursor.execute(
        "CREATE TABLE Clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100), email VARCHAR(50));"
    )


def inserir_registros(conexao, cursor, dados):
    cursor.execute("INSERT INTO Clientes (nome, email) VALUES(?, ?);", dados)
    conexao.commit()


def inserir_varios_registros(conexao, cursor, lista_dados):
    cursor.executemany("INSERT INTO Clientes (nome, email) VALUES(?, ?);", lista_dados)
    conexao.commit()


def atualizar_registros(conexao, cursor, dados):
    cursor.execute("UPDATE Clientes SET nome=?, email=? WHERE id=?;", dados)
    conexao.commit()


def remover_registros(conexao, cursor, dados):
    cursor.execute("DELETE FROM Clientes WHERE id=?;", dados)
    conexao.commit()


def recuperar_registro(cursor, id):
    cursor.execute("SELECT * FROM Clientes WHERE id=?;", (id,))
    return cursor.fetchone()


def recuperar_dicionario(cursor, id):
    cursor.row_factory = sqlite3.Row
    cursor.execute("SELECT * FROM Clientes WHERE id=?;", (id,))
    return dict(cursor.fetchone())


def recuperar_todos_registros(cursor):
    return cursor.execute("SELECT * FROM Clientes ORDER BY nome;")


main()
