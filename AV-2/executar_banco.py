# ==============================================================================
# SCRIPT DE TESTE DO BANCO DE DADOS - PROJETO APLICADO I (SCHULZ S.A.)
#
# O que ele faz:
#   1. Apaga o banco de teste antigo (o 03_banco.sql tem INSERTs de exemplo, então
#      cada execução precisa começar do zero)
#   2. Conecta ao SQLite e ativa as chaves estrangeiras (PRAGMA foreign_keys)
#   3. Executa o arquivo 03_banco.sql (tabelas + dados de teste)
#   4. Confere se as 3 tabelas e as chaves estrangeiras existem
#   5. Testa a integridade referencial (inserir medição com técnico/equipamento
#      inexistente DEVE ser recusado pelo banco)
#   6. Mostra os dados de teste com um JOIN entre as 3 tabelas
#
# Como rodar (na pasta do projeto):  python executar_banco.py
# ==============================================================================
import os
import sqlite3
import sys

PASTA = os.path.dirname(os.path.abspath(__file__))
NOME_BANCO = os.path.join(PASTA, "schulz_calibracao.db")
ARQUIVO_SQL = os.path.join(PASTA, "03_banco.sql")
TABELAS_ESPERADAS = ("tecnico_solicitante", "equipamento", "medicao")


def executar_script_sql(conexao):
    """Lê o 03_banco.sql e executa todas as instruções (DDL + INSERTs de teste)."""
    with open(ARQUIVO_SQL, "r", encoding="utf-8") as f:
        script_sql = f.read()
    conexao.executescript(script_sql)
    conexao.commit()


def listar_tabelas(cursor):
    """Retorna os nomes das tabelas criadas (ignora tabelas internas do SQLite)."""
    cursor.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )
    return [linha[0] for linha in cursor.fetchall()]


def colunas_da_tabela(cursor, tabela):
    cursor.execute(f"PRAGMA table_info({tabela})")
    return [linha[1] for linha in cursor.fetchall()]


def chaves_estrangeiras(cursor, tabela):
    """Retorna lista de (coluna_local, tabela_referenciada, coluna_referenciada)."""
    cursor.execute(f"PRAGMA foreign_key_list({tabela})")
    return [(linha[3], linha[2], linha[4]) for linha in cursor.fetchall()]


def testar_integridade(conexao):
    """
    Tenta inserir uma medição apontando para técnico e equipamento que não existem.
    Todas as colunas NOT NULL são preenchidas, para que o único motivo possível
    da recusa seja a chave estrangeira. Nada é gravado: a transação é desfeita.
    """
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO medicao (id_equipamento, id_tecnico, numero_certificado, "
            "data_emissao, parametro, valor_nominal, tolerancia_positiva, "
            "tolerancia_negativa, medicao_1, medicao_2, valor_obtido, erro, status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (9999, 9999, "TESTE/0000", "2026-01-01", "TESTE_INTEGRIDADE",
             0, 0, 0, 0, 0, 0, 0, "APROVADO"),
        )
        return False  # o banco aceitou: a integridade NÃO está funcionando
    except sqlite3.IntegrityError as e:
        return "FOREIGN KEY" in str(e).upper()
    finally:
        conexao.rollback()


def mostrar_dados_de_teste(cursor):
    """JOIN entre as 3 tabelas para provar que os relacionamentos funcionam."""
    cursor.execute(
        """
        SELECT m.numero_certificado, e.codigo, e.denominacao, t.nome,
               m.parametro, m.valor_obtido, m.erro, m.status
        FROM medicao m
        JOIN equipamento e ON m.id_equipamento = e.id_equipamento
        JOIN tecnico_solicitante t ON m.id_tecnico = t.id_pessoa
        ORDER BY m.id_medicao
        """
    )
    linhas = cursor.fetchall()
    print("Dados de teste (JOIN medicao + equipamento + tecnico_solicitante):")
    if not linhas:
        print("  (nenhuma medição encontrada)")
    for cert, cod, den, tec, par, obt, erro, status in linhas:
        print(f"  Cert. {cert} | {cod} ({den}) | {tec}")
        print(f"    {par}: obtido={obt:.3f} erro={erro:.3f} -> {status}")


def main():
    conexao = None
    try:
        # Começa sempre do zero, porque o 03_banco.sql insere dados de exemplo
        # (rodar duas vezes sem apagar quebraria na regra UNIQUE do codigo).
        if os.path.exists(NOME_BANCO):
            os.remove(NOME_BANCO)

        conexao = sqlite3.connect(NOME_BANCO)
        conexao.execute("PRAGMA foreign_keys = ON;")
        cursor = conexao.cursor()

        # 1. Cria as tabelas e insere os dados de teste do 03_banco.sql
        executar_script_sql(conexao)
        # Garante o PRAGMA ligado depois do executescript
        conexao.execute("PRAGMA foreign_keys = ON;")

        # 2. Confere se as tabelas esperadas existem
        tabelas = listar_tabelas(cursor)
        faltando = [t for t in TABELAS_ESPERADAS if t not in tabelas]

        print("=" * 70)
        print(f"Banco de dados: {os.path.basename(NOME_BANCO)}")
        print("=" * 70)
        for tabela in tabelas:
            print(f"Tabela '{tabela}': {', '.join(colunas_da_tabela(cursor, tabela))}")

        if faltando:
            print("-" * 70)
            print(f"ERRO: tabelas não encontradas: {', '.join(faltando)}")
            sys.exit(1)

        # 3. Mostra as chaves estrangeiras
        print("-" * 70)
        print("Chaves estrangeiras:")
        for tabela in ("equipamento", "medicao"):
            for coluna, tabela_ref, coluna_ref in chaves_estrangeiras(cursor, tabela):
                print(f"  {tabela}.{coluna} -> {tabela_ref}({coluna_ref})")

        # 4. Confere o PRAGMA e testa a integridade referencial
        cursor.execute("PRAGMA foreign_keys;")
        fk_ativo = cursor.fetchone()[0] == 1
        print("-" * 70)
        print(f"PRAGMA foreign_keys ativo: {'SIM' if fk_ativo else 'NÃO'}")

        integridade_ok = testar_integridade(conexao)
        print(
            "Teste de integridade referencial: "
            + ("OK (medição com técnico/equipamento inexistente foi recusada)"
               if integridade_ok else "FALHOU (o banco aceitou dados inválidos)")
        )

        # 5. Mostra os dados de teste
        print("-" * 70)
        mostrar_dados_de_teste(cursor)

        print("=" * 70)
        if fk_ativo and integridade_ok:
            print(f"SUCESSO: banco '{os.path.basename(NOME_BANCO)}' gerado e validado!")
            print("As tabelas 'tecnico_solicitante', 'equipamento' e 'medicao' foram criadas.")
        else:
            print("ATENÇÃO: o banco foi criado, mas a validação falhou.")
            sys.exit(1)
        print("=" * 70)

    except FileNotFoundError:
        print(f"ERRO: arquivo '{ARQUIVO_SQL}' não encontrado. Ele precisa estar na mesma pasta deste script.")
        sys.exit(1)
    except sqlite3.Error as e:
        print(f"ERRO ao executar o script SQL: {e}")
        sys.exit(1)
    finally:
        if conexao:
            conexao.close()


if __name__ == "__main__":
    main()