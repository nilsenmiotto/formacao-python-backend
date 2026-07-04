import sqlite3
from pathlib import Path

DIRETORIO_BANCO = Path(__file__).parent


def criar_conexao(base_dados: str) -> sqlite3.Connection:
    """Cria uma conexão com o banco de dados SQLite."""
    try:
        conexao = sqlite3.connect(DIRETORIO_BANCO / base_dados)
        return conexao
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


def remover_banco(base_dados: str):
    Path(DIRETORIO_BANCO / base_dados).unlink()
