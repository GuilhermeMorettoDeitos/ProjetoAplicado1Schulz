import os
from importlib import import_module

_classes = import_module("04_classes")
ConexaoBanco = _classes.ConexaoBanco
Tecnico = _classes.Tecnico
Equipamento = _classes.Equipamento
Medicao = _classes.Medicao

def limpar_banco(db_name="schulz_metrologia.db"):
    """essa função remove o banco antigo para garantir uma demonstração limpa do zero"""
    if os.path.exists(db_name):
        os.remove(db_name)

def main():
    limpar_banco()
    
    # 1. Inicializando e conectando ao Banco
    db = ConexaoBanco()
    db.conectar()
    db.criar_tabelas()

    # 2. Instanciando e persistindo Técnicos (POO)
    tecnico_exec = Tecnico("Jose Alcides Rosa Junior", "Técnico executante", 2)
    id_tecnico = tecnico_exec.salvar(db)

    # 3. Instanciando e persistindo o Equipamento
    equipamento = Equipamento("703.1208", "Dispositivo de controle", "Não consta")
    id_equip = equipamento.salvar(db)

    # 4. Inserindo as Medições Brutas (simulando a leitura do Calypso do arquivo .txt/.xlsx)
    # A classe Medicao vai calcular a média, o erro e o status automaticamente na instanciação.
    dados_brutos = [
        # Parametro, Nominal, Tol+, Tol-, Medida 1, Medida 2
        ("PLANICIDADE_REF", 0.000, 0.050, 0.000, 0.002167, 0.002267),
        ("ENTRE CENTROS_REF", 0.000, 0.040, 0.000, 0.027415, 0.027415),
        ("62P_DIAMETRO 1", 6.075, 0.010, -0.010, 6.078730, 6.078730),
        ("62P_POSIÇÃO 1", 0.000, 0.100, 0.000, 0.429552, 0.429552),
        ("62P_DIAMETRO 2", 6.075, 0.010, -0.010, 6.078131, 6.078031),
        ("62P_POSIÇÃO 2", 0.000, 0.100, 0.000, 0.244611, 0.244611),
        ("13P_DIAMETRO 1", 16.964, 0.010, -0.010, 16.968448, 16.968448)
    ]

    for dado in dados_brutos:
        medicao = Medicao(
            id_equipamento=id_equip,
            id_tecnico=id_tecnico,
            nome_parametro=dado[0],
            valor_nominal=dado[1],
            tol_pos=dado[2],
            tol_neg=dado[3],
            med_1=dado[4],
            med_2=dado[5]
        )
        medicao.salvar(db)

    # 5. Executando Consulta Relacional (JOIN) para Relatório
    query = """
        SELECT 
            e.descricao, e.codigo_tag, t.nome, 
            m.nome_parametro, m.valor_nominal, m.tol_positiva, m.tol_negativa, 
            m.valor_obtido, m.erro, m.status
        FROM medicoes m
        JOIN equipamentos e ON m.id_equipamento = e.id_equipamento
        JOIN tecnicos t ON m.id_tecnico = t.id_tecnico
    """
    db.cursor.execute(query)
    resultados = db.cursor.fetchall()

    # 6. Exibição simulada do Relatório por meio do terminal
    if resultados:
        print("="*85)
        print(" " * 25 + "CERTIFICADO DE CALIBRAÇÃO - SCHULZ")
        print("="*85)
        print(f"Denominação: {resultados[0][0]} | Código: {resultados[0][1]}")
        print(f"Técnico Executante: {resultados[0][2]}")
        print("-" * 85)
        print(f"{'Parâmetro':<20} | {'Nominal':<8} | {'Tol+':<6} | {'Tol-':<7} | {'Obtido':<8} | {'Erro':<8} | {'Status':<10}")
        print("-" * 85)

        for r in resultados:
            param, nom, tolp, toln, obt, erro, status = r[3], r[4], r[5], r[6], r[7], r[8], r[9]
            # Formatando para exibição em 3 casas decimais conforme o PDF original
            print(f"{param:<20} | {nom:>8.3f} | {tolp:>6.3f} | {toln:>7.3f} | {obt:>8.3f} | {erro:>8.3f} | {status:<10}")
        
        print("="*85)
    
    db.desconectar()

if __name__ == "__main__":
    main()