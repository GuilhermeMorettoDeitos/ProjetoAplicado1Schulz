# Dicionário de Dados do Sistema

Campos usados no processo de calibração da Schulz, organizados nas três tabelas do banco.

| Tabela | Campo | Tipo | Descrição |
|---|---|---|---|
| tecnico_solicitante | id_pessoa | int | Chave primária da tabela |
| tecnico_solicitante | nome | text | Nome do técnico ou do setor |
| tecnico_solicitante | tipo | text | Diz se a linha é um técnico executante, um signatário ou um setor solicitante |
| tecnico_solicitante | setor | text | Setor a que a pessoa pertence, quando se aplica |
| tecnico_solicitante | cargo_funcao | text | Cargo/função dentro da Schulz |
| tecnico_solicitante | turno | int | Turno de trabalho (1 ou 2) — só faz sentido pra quem executa medição |
| equipamento | id_equipamento | int | Chave primária da tabela |
| equipamento | codigo | text | Código do instrumento, ex: 703.1208 |
| equipamento | denominacao | text | Nome do instrumento |
| equipamento | fabricante | text | Fabricante do instrumento |
| equipamento | id_setor | int | Aponta pro setor dono do instrumento |
| medicao | id_medicao | int | Chave primária da tabela |
| medicao | id_equipamento | int | Aponta pro instrumento calibrado |
| medicao | id_tecnico | int | Aponta pro técnico que fez a medição |
| medicao | numero_certificado | text | Número do certificado gerado, ex: 00091/2026 |
| medicao | data_emissao | text | Data em que o certificado foi emitido |
| medicao | parametro | text | Nome da cota medida, ex: 62P_DIAMETRO 1 |
| medicao | valor_nominal | Real | Valor esperado da cota, direto do desenho técnico |
| medicao | tolerancia_positiva | Real | Quanto a cota pode passar do nominal pra cima |
| medicao | tolerancia_negativa | Real | Quanto a cota pode passar do nominal pra baixo |
| medicao | medicao_1 | Real | Primeira leitura feita na máquina |
| medicao | medicao_2 | Real | Segunda leitura feita na máquina |
| medicao | valor_obtido | Real | Média das duas leituras |
| medicao | erro | Real | Valor obtido menos o valor nominal |
| medicao | status | text | APROVADO ou REPROVADO, calculado pela regra de tolerância |