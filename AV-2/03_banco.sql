-- Banco de calibração da Schulz
-- 3 tabelas: tecnico_solicitante, equipamento e medicao

PRAGMA foreign_keys = ON;

-- Guarda tanto os metrologistas quanto os setores que pedem calibração. No modelo completo isso era duas tabelas, mas juntamos aqui pra manter só 3 entidades, como pede o roteiro.
CREATE TABLE IF NOT EXISTS tecnico_solicitante (
    id_pessoa     INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          TEXT NOT NULL,
    tipo          TEXT NOT NULL,   -- Técnico Executante / Signatário / Setor Solicitante
    setor         TEXT,
    cargo_funcao  TEXT,
    turno         INTEGER
);

-- Cadastro do instrumento calibrado. Separado da medição pra não repetircódigo/fabricante toda vez que o mesmo instrumento for calibrado de novo.
CREATE TABLE IF NOT EXISTS equipamento (
    id_equipamento INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo         TEXT NOT NULL UNIQUE,
    denominacao    TEXT NOT NULL,
    fabricante     TEXT,
    id_setor       INTEGER,
    FOREIGN KEY (id_setor) REFERENCES tecnico_solicitante (id_pessoa)
);

-- Cada linha aqui é uma cota medida dentro de um certificado. Um mesmo certificado gera várias linhas (uma por cota avaliada).
CREATE TABLE IF NOT EXISTS medicao (
    id_medicao          INTEGER PRIMARY KEY AUTOINCREMENT,
    id_equipamento      INTEGER NOT NULL,
    id_tecnico          INTEGER NOT NULL,
    numero_certificado  TEXT NOT NULL,
    data_emissao        TEXT NOT NULL,
    parametro           TEXT NOT NULL,
    valor_nominal       REAL NOT NULL,
    tolerancia_positiva REAL NOT NULL,
    tolerancia_negativa REAL NOT NULL,
    medicao_1           REAL NOT NULL,
    medicao_2           REAL NOT NULL,
    valor_obtido        REAL NOT NULL,
    erro                REAL NOT NULL,
    status              TEXT NOT NULL,
    FOREIGN KEY (id_equipamento) REFERENCES equipamento (id_equipamento),
    FOREIGN KEY (id_tecnico) REFERENCES tecnico_solicitante (id_pessoa)
);

-- Teste com dados reais do certificado 00091/2026, pra confirmar que as FKs estão funcionando antes de subir no repositório.
INSERT INTO tecnico_solicitante (nome, tipo, setor, cargo_funcao, turno) VALUES
    ('Usinagem I', 'Setor Solicitante', NULL, NULL, NULL),
    ('Jose Alcides Rosa Junior', 'Técnico Executante', 'Usinagem I', 'Técnico executante', 2),
    ('João Carlos Gomes de Oliveira', 'Signatário', NULL, 'Signatário Autorizado', NULL);

INSERT INTO equipamento (codigo, denominacao, fabricante, id_setor) VALUES
    ('703.1208', 'Dispositivo de controle', 'Não consta', 1);

INSERT INTO medicao (id_equipamento, id_tecnico, numero_certificado, data_emissao, parametro, valor_nominal, tolerancia_positiva, tolerancia_negativa, medicao_1, medicao_2, valor_obtido, erro, status) VALUES
    (1, 2, '00091/2026', '2026-08-26', '62P_DIAMETRO 1', 6.075, 0.010, -0.010, 6.078730, 6.078730, 6.078730, 0.003730, 'APROVADO');