
# Projeto - Modelando o Sistema Bancário em POO com Python

 Realização do desafio proposto pela instrutor Guilherme da Digital Innovation One.  
 Foi feito um sistema bancário para efetuar operações de depósito, saque e visualização de extrato com o histórico das movimentações de diversas contas e clientes cadastrados.


### Escopo do Projeto
**Objetivo**
* Criar/aprimorar um sistema bancário;
* Alterar o modelo anterior para o modelo de programação orientada a Objeto (POO), mudando as funções existentes do projeto, para classes e objetos;
**Desafio extra:**
- Fazer as funções funcionarem de acordo com o proposto;
- Melhorar o código se puder;
- FIXME: Resolver problema de seleção de contas de um cliente.


**Diretrizes para elaboração do projeto**
- O programa deve estar separado em classes ao invés de dicionários;
- O código deve seguir o modelo UML apresentado pelo instrutor.

**Diretrizes para elaboração do projetos anteriores**
- O programa deve armazenar os clientes em lista com as seguintes informações: nome, CPF, data de nascimento e endereço;
- Não podemos cadastrar 2 clientes com o mesmo CPF;
- A conta deve ser composta por agência, número de conta e usuário;
- Número da conta deve ser sequencial, começando com 1 e a agência tem um número fixo, "0001".
- Um cliente pode ter mais de uma conta, mas uma conta deve ser criado por apenas um cliente
- O sistema deverá atender uma única conta, realizando as seguintes operação: depósito, saque, extrato;
- Juntamente com o Guilherme, foi iniciado a construção do sistema bancário;
- Cada depósito e cada saque deverá ser exibido no extrato;
- O valor de saque não pode exceder o saldo;
- O valor máximo de cada saque será de R$ 500,00;
- O limite máximo de saques será de 3 saques diários;

### Desafio Realizado
O código foi reescrito com toda definição de classes e funções para o código atenda o paradigma POO.

**Desafio extra realizado**

Sistema foi codificado para todo o sistema acima funcione.\
Foram criadas no menu, mais duas opções: uma para listar todas as contas criadas, e outra para listar todos os clientes cadastrados.\
No extrato, foi adicionado o saldo após cada operação para facilitar o acompanhamento das movimentações do usuário. Também foi destacado os dados da conta/cliente para facilitar a identificação.\
Foi trabalhado o menu inicial para melhor a visualização.\
Após cada operação, o sistema retorna uma mensagem com a confirmação da operação, o valor movimentado e o Saldo resultante.\
**FIXME RESOLVIDO:** Para clientes com mais de uma conta, é possível selecionar a conta que será feita a operação.

