# Organização dos Dados — Modelo Conceitual

A gente decidiu dividir o banco em três partes: **Técnico/Solicitante**, **Equipamento** e **Medição**. Não foi só porque o roteiro pede exatamente três tabelas, na verdade, quando fomos olhar de novo pro processo da Schulz que mapeamos na Entrega 01, essas três partes já apareciam naturalmente separadas: tem quem faz a calibração, tem o que está sendo calibrado, e tem o resultado da calibração em si. Só formalizamos isso em tabela.

A entidade **Técnico/Solicitante** ficou meio "genérica" de propósito. Ela guarda tanto os metrologistas (o José, que executa as medições, e o João, que assina o certificado) quanto os setores que pedem a calibração, tipo Usinagem I, Compressores e Pintura. No modelo completo que a gente fez antes disso eram duas tabelas separadas. Mas pra esse formato de 3 entidades deu pra juntar em uma só, incluindo um campo que indica se aquela linha é um técnico, um signatário ou um setor.

Já a tabela **Equipamento** guarda o instrumento que passa pela calibração: código, nome e fabricante. 

O motivo de isolar isso em uma tabela própria é bem prático: se a gente deixasse essas informações espalhadas dentro de cada linha de medição, qualquer erro de digitação (por exemplo, escrever "703.1208" em uma calibração e "703.1208 " com espaço no fim em outra) faria o sistema achar que existem dois instrumentos diferentes. E isso realmente aconteceu nas planilhas reais que a Schulz nos passou, vários instrumentos apareciam cadastrados mais de uma vez só porque alguém digitou o código de um jeito ligeiramente diferente.

Por fim, em **Medição** entra tudo que muda de uma calibração pra outra: 

* Qual cota foi medida;
* O valor nominal e a tolerância dessa cota (que vêm do desenho técnico do instrumento);
* As duas leituras feitas na máquina;
* A média, o erro e se aprovou ou não.

Separar isso do cadastro do Equipamento é o que permite o mesmo instrumento ser calibrado várias vezes ao longo dos anos sem precisar recadastrar ele toda vez, cada calibração nova só gera linhas novas em Medição, apontando pro mesmo equipamento.

Se o nome de um fabricante estiver escrito errado ou repetido de formas diferentes espalhado em várias linhas, corrigir isso depois fica inviavel, pois é um trabalho manual e cansativo. Com a estrutura separada, corrige uma vez só no cadastro do Equipamento, ou do Técnico/Solicitante e pronto, todo o histórico de medições continua apontando para o registro certo.