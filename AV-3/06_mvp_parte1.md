# Projeto Aplicado I - AV03 (Parte 1 do MVP)
**Equipe:** Grupo 15
**Empresa Parceira:** Schulz S.A.
**Linguagem Utilizada:** Python 3.11 com SQLite3

## 1. Padrões de Programação Orientada a Objetos (POO) Utilizados

Neste MVP em Python, a gente procurou seguir os princípios básicos de Orientação a Objetos pra deixar o código mais organizado.

- **Encapsulamento de Regras de Negócio (RN-04):** A regra que calcula os erros de metrologia não fica solta no script principal. A gente colocou ela bem protegida dentro da classe `Medicao`. Os métodos que fazem os cálculos, tipo o `__calcular_media` e o `__avaliar_status`, são todos privados (usando os dois underlines `__` do Python). Isso garante que ninguem de fora consiga alterar o status da peça caso a matemática diga que ela foi reprovada. (Isso atende ao requisito RNF-02 de Integridade).
- **Separação de Responsabilidades (SRP):** Deixamos a classe `ConexaoBanco` cuidando só de lidar com o SQLite e criar as tabelas. Já as classes de domínio (`Tecnico`, `Equipamento`, `Medicao`) cuidam de guardar os próprios dados e cada uma tem seu método `.salvar()`, pra gravar no banco.
- **Tecnologia escolhida:** Usamos o Python justamente por lidar muito bem com números float de alta precisão que vêm da máquina, e também por ser mais simples de se trabalhar, em nossa opnião, em relação ao java. 

## 2. Tratamento de Erros e Banco de Dados (SQLite)

Como a gente migrou a ideia do MySQL da AV02 para o SQLite agora, resolvemos fazer o banco se configurar sozinho:

- **Tabelas Autogeridas:** Usando o comando `CREATE TABLE IF NOT EXISTS`, a nossa classe de conexão já roda o script DDL sozinha e prepara tudo na primeira vez que o código roda.
- **Tratamento de Exceções (`try/except`):** Colocamos tudo que é de banco de dados (`INSERT`, `SELECT`, `COMMIT`) dentro de blocos *try-except* pegando o `sqlite3.Error`. Isso evita que o programa feche do nada sem mostrar o erro de um jeito seguro no terminal.

## 3. Representação do Diagrama de Classes (UML Textual)

A estrutura do sistema ficou dividida nessas quatro classes principais: `ConexaoBanco`, `Tecnico`, `Equipamento` e `Medicao`. Cada uma tem seu papel no sistema.

### 3.1. Classe ConexaoBanco

**Responsabilidade:** abrir a conexão com o SQLite e criar as tabelas logo de cara.

**Atributos:**
- `db_name: String` — guarda o nome do arquivo do banco.
- `conn: Connection` — é a conexão ativa mesmo.
- `cursor: Cursor` — o que a gente usa pra rodar os SQLs.

**Métodos:**
- `conectar()` — liga o banco.
- `desconectar()` — desliga o banco.
- `criar_tabelas()` — cria as tabelas se elas não existirem ainda.

### 3.2. Classe Tecnico

**Responsabilidade:** guardar os dados do profissional que faz a calibração.

**Atributos:**
- `nome: String` — nome do técnico.
- `cargo: String` — o que ele faz.
- `turno: Integer` — qual o turno dele.

**Métodos:**
- `salvar(db: ConexaoBanco)` — manda os dados do técnico pro banco.

### 3.3. Classe Equipamento

**Responsabilidade:** representar o instrumento que tá sendo medido.

**Atributos:**
- `codigo_tag: String` — o código do equipamento.
- `descricao: String` — o que é o equipamento.
- `fabricante: String` — quem fabricou.

**Métodos:**
- `salvar(db: ConexaoBanco)` — salva o equipamento no SQLite.

### 3.4. Classe Medicao

**Responsabilidade:** é a classe mais importante. Ela guarda os dados do ensaio, faz a matemática e decide se a peça tá aprovada ou não de acordo com as tolerâncias.

**Atributos:**
- `valor_nominal: Float` — o valor que deveria ter.
- `tol_pos: Float` — o limite pra mais.
- `tol_neg: Float` — o limite pra menos.
- `med_1: Float` — primeira leitura da máquina.
- `med_2: Float` — segunda leitura da máquina.
- `valor_obtido: Float` — a média final.
- `erro: Float` — a diferença pro valor nominal.
- `status: String` — `APROVADO` ou `REPROVADO`.

**Métodos:**
- `__calcular_media(): Float` — tira a média das duas leituras.
- `__calcular_erro(): Float` — acha o erro pro nominal.
- `__avaliar_status(): String` — confere se bateu com as tolerâncias.
- `salvar(db: ConexaoBanco)` — grava a medição final no banco.

Esses métodos com underline `__` são internos da classe, o que deixa a lógica matemática bem fechadinha num lugar só.

### 3.5. Relacionamentos entre as classes

- **Tecnico e Medicao:** um mesmo técnico pode fazer várias medições.
- **Equipamento e Medicao:** um equipamento vai ter várias medições registradas com o passar do tempo.
- **ConexaoBanco e as outras:** as três classes de dados usam a `ConexaoBanco` na hora de rodar o `salvar()` no SQLite.

### 3.6. Fluxo de funcionamento

1. Primeiro a `ConexaoBanco` liga no SQLite e arruma as tabelas.
2. A gente cria as instâncias de `Tecnico` e `Equipamento` pra representar os dados do ensaio.
3. A classe `Medicao` recebe os números brutos, tira a média, descobre o erro e avalia se passou ou não.
4. Depois de tudo calculado, os dados vão todos pro banco com os métodos `salvar()`.
5. Por fim, o sistema faz um SELECT pra consultar tudo e mostrar o relatório final na tela.

## 4. Instruções para Execução do Projeto

Para facilitar a avaliação e o acesso do nosso MVP, deixamos o ambiente totalmente configurado. O professor pode escolher testar o sistema de duas formas: usando Docker (nossa recomendação, pois não exige configurar banco nem Python na máquina) ou rodando o script localmente.

### Opção A: Execução via Docker (Recomendado)
Se tiver o Docker Desktop instalado, basta abrir o terminal na pasta raiz do projeto e rodar dois comandos:

1. **Construir a imagem da aplicação:**
   `docker build -t mvp_schulz .`
2. **Rodar o container:**
   `docker run --rm mvp_schulz`

O sistema vai inicializar o SQLite isolado, realizar as validações e imprimir o relatório do certificado diretamente no terminal.

### Opção B: Execução Local (Python padrão)
Caso prefira rodar direto na máquina, você só vai precisar do Python 3 instalado. Como a gente usou só a biblioteca nativa `sqlite3`, não presisa instalar pacotes externos com o pip, mas a gente recomenda rodar dentro de um ambiente virtual (venv) por boas práticas de desenvolvimento.

1. Abra o terminal na pasta do projeto.
2. Crie e ative o ambiente virtual (opcional, mas recomendado):
   - No Windows: rode `python -m venv venv` e depois ative com `venv\Scripts\activate`
   - No Linux/Mac: rode `python3 -m venv venv` e depois ative com `source venv/bin/activate`
3. Execute o arquivo principal:
   `python 05_main.py` (ou `python3 05_main.py` dependendo do seu sistema).

Ao rodar o comando, o arquivo `schulz_metrologia.db` vai ser criado sozinho na pasta, as tabelas serão montadas e o relatório final vai aparecer direto no console.