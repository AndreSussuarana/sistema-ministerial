import datetime as dt
import sqlite3 as sql
from typing import Any


class GerenciadorBancoFornecedor:
    def __init__(self, banco_nome: str = "BancoFornecedor.db") -> None:
        self.banco_nome = banco_nome
        self.ativar_banco()

    def conectar(self):
        return sql.connect(self.banco_nome)

    def ativar_banco(self):

        with self.conectar() as conecte:
            cursor = conecte.cursor()

            cursor.execute("PRAGMA foreign_keys = ON;")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contratacoes (
                    id TEXT PRIMARY KEY,
                    orgao TEXT,
                    objeto TEXT,
                    valor_estimado REAL,
                    data_abertura TEXT,
                    link_edital TEXT,
                    status TEXT,
                    atualizado_em TIMESTAMP
                );
            """)
            conecte.commit()
            print("Parabéns, banco ativado")

    def salvar_contratacao(self, dados: dict[str, Any]):

        def as_str(valor: Any) -> str:
            return str(valor) if valor is not None else ""

        def as_float(valor: Any) -> float:
            try:
                return float(valor) if valor is not None else 0.0
            except (ValueError, TypeError):
                return 0.0

        with self.conectar() as conecte:
            cursor = conecte.cursor()

            params: tuple[Any, ...] = (
                as_str(dados.get("id")),
                as_str(dados.get("orgao")),
                as_str(dados.get("objeto")),
                as_float(dados.get("valor_estimado")),
                as_str(dados.get("data_abertura")),
                as_str(dados.get("link_edital")),
                as_str(dados.get("status")),
                str(dt.datetime.now()),  # noqa: DTZ005
            )

            cursor.execute(
                """
                INSERT OR REPLACE INTO contratacoes 
                (id, orgao, objeto, valor_estimado, data_abertura, link_edital, status, atualizado_em)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                params,
            )

            conecte.commit()


if __name__ == "__main__":
    gerenciador = GerenciadorBancoFornecedor()
