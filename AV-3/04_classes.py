import sqlite3
import os

class ConexaoBanco:
    def __init__(self, db_name="schulz_metrologia.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def conectar(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            # Habilita o uso de chaves estrangeiras no SQLite
            self.cursor.execute("PRAGMA foreign_keys = ON;")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def desconectar(self):
        if self.conn:
            self.conn.close()

    def criar_tabelas(self):
        """Cria as tabelas automaticamente se não existirem (DDL SQLite)"""
        try:
            self.cursor.executescript("""
                CREATE TABLE IF NOT EXISTS tecnicos (
                    id_tecnico INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cargo TEXT,
                    turno INTEGER
                );

                CREATE TABLE IF NOT EXISTS equipamentos (
                    id_equipamento INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo_tag TEXT NOT NULL UNIQUE,
                    descricao TEXT NOT NULL,
                    fabricante TEXT
                );

                CREATE TABLE IF NOT EXISTS medicoes (
                    id_medicao INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_equipamento INTEGER,
                    id_tecnico INTEGER,
                    nome_parametro TEXT NOT NULL,
                    valor_nominal REAL,
                    tol_positiva REAL,
                    tol_negativa REAL,
                    medicao_1 REAL,
                    medicao_2 REAL,
                    valor_obtido REAL,
                    erro REAL,
                    status TEXT,
                    FOREIGN KEY(id_equipamento) REFERENCES equipamentos(id_equipamento),
                    FOREIGN KEY(id_tecnico) REFERENCES tecnicos(id_tecnico)
                );
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {e}")

class Tecnico:
    def __init__(self, nome, cargo, turno):
        self.nome = nome
        self.cargo = cargo
        self.turno = turno

    def salvar(self, db: ConexaoBanco):
        try:
            db.cursor.execute(
                "INSERT INTO tecnicos (nome, cargo, turno) VALUES (?, ?, ?)",
                (self.nome, self.cargo, self.turno)
            )
            db.conn.commit()
            return db.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao salvar técnico {self.nome}: {e}")

class Equipamento:
    def __init__(self, codigo_tag, descricao, fabricante):
        self.codigo_tag = codigo_tag
        self.descricao = descricao
        self.fabricante = fabricante

    def salvar(self, db: ConexaoBanco):
        try:
            db.cursor.execute(
                "INSERT OR IGNORE INTO equipamentos (codigo_tag, descricao, fabricante) VALUES (?, ?, ?)",
                (self.codigo_tag, self.descricao, self.fabricante)
            )
            db.conn.commit()
            
            # Retorna o ID (caso tenha acabado de inserir ou caso já exista)
            db.cursor.execute("SELECT id_equipamento FROM equipamentos WHERE codigo_tag = ?", (self.codigo_tag,))
            return db.cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Erro ao salvar equipamento {self.codigo_tag}: {e}")

class Medicao:
    def __init__(self, id_equipamento, id_tecnico, nome_parametro, valor_nominal, tol_pos, tol_neg, med_1, med_2):
        self.id_equipamento = id_equipamento
        self.id_tecnico = id_tecnico
        self.nome_parametro = nome_parametro
        self.valor_nominal = valor_nominal
        self.tol_pos = tol_pos
        self.tol_neg = tol_neg
        self.med_1 = med_1
        self.med_2 = med_2
        
        # Métodos internos rodam na instânciação encapsulando a regra de negócio metrológica
        self.valor_obtido = self.__calcular_media()
        self.erro = self.__calcular_erro()
        self.status = self.__avaliar_status()

    def __calcular_media(self):
        """Calcula a média das duas leituras da MMC"""
        return round((self.med_1 + self.med_2) / 2, 6)

    def __calcular_erro(self):
        """Calcula o erro em relação ao valor nominal (Erro = Valor Obtido - Nominal)"""
        return round(self.valor_obtido - self.valor_nominal, 6)

    def __avaliar_status(self):
        """Avalia se a cota está aprovada baseada na tolerância (RN-04)"""
        limite_sup = self.valor_nominal + self.tol_pos
        limite_inf = self.valor_nominal + self.tol_neg
        
        if limite_inf <= self.valor_obtido <= limite_sup:
            return "APROVADO"
        return "REPROVADO"

    def salvar(self, db: ConexaoBanco):
        try:
            db.cursor.execute("""
                INSERT INTO medicoes 
                (id_equipamento, id_tecnico, nome_parametro, valor_nominal, tol_positiva, tol_negativa, 
                medicao_1, medicao_2, valor_obtido, erro, status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.id_equipamento, self.id_tecnico, self.nome_parametro, self.valor_nominal, 
                  self.tol_pos, self.tol_neg, self.med_1, self.med_2, self.valor_obtido, self.erro, self.status))
            db.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao salvar medição {self.nome_parametro}: {e}")