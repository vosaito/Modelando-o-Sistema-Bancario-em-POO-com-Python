from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime, date
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacoes(self, conta, transacao):
            transacao.registrar(conta)

    def adicionar_conta(self, conta):
            self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

    def __str__(self):
        return f"""\
            Nome:\t{self.nome}
            CPF:\t{self.cpf}
            Data de Nascimento:\t{self.data_nascimento}
            Endereço:\t{self.endereco}
        """

class Conta:
    def __init__(self, cliente, numero_conta, AGENCIA):
         self._AGENCIA = "0001"
         self._numero_conta = numero_conta
         self._saldo = 0
         self._cliente = cliente
         self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero_conta, AGENCIA):
        return cls(cliente, numero_conta, AGENCIA)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero_conta(self):
        return self._numero_conta

    @property
    def AGENCIA(self):
        return self._AGENCIA

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = (valor > saldo)

        if excedeu_saldo:
         print("Falha na operação! Saldo insuficiente.")

        elif valor > 0:
            self._saldo -= valor
            print(f"Saque realizado com sucesso de R$ {valor:.2f}! Saldo:R$ {self._saldo:.2f}")
            return True

        else:
            print("Falha na operação! Valor informado não é válido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito realizado com sucesso de R$ {valor:.2f}! Saldo:R$ {self._saldo:.2f}")
            return True

        else:
            print("Falha na operação! Valor informado não é válido.")

        return False
        
class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, AGENCIA, limite = 500, limite_saques = 3):
        super().__init__(numero_conta, cliente, AGENCIA)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico._transacoes 
             if transacao["tipo"] == Saque.__name__ and transacao["date"] == date.today()]
            )
        excedeu_limite = (valor > self.limite)
        excedeu_saques = (numero_saques >= self.limite_saques)

        if excedeu_limite:
            print("Falha na operação! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Falha na operação! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False
     
    def __str__(self):
        return f"""\
            Agência:\t{self.AGENCIA}
            Cc:\t\t{self.numero_conta}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao, conta):
        self._transacoes.append(
            {
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "date": date.today(),
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "saldo": conta.saldo,
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self, conta)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self, conta)

def menu():
    menu = """\n
    #########################################
            Bem vindo ao serviço de 
            autoatendimento do Banco
        
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo usuário
    [nc]\tNova conta
    [lc]\tLista de contas
    [lu]\tLista de usuários
    [q]\tSair

    #########################################
    Favor selecionar a operação que deseja:
    """
    return input(textwrap.dedent(menu))

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado. Favor verificar o cpf ou cadastrar novo cliente.")
        return

    valor = float(input("Informe o valor do depósito:"))    
    
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacoes(conta, transacao)
        
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado. Favor verificar o cpf ou cadastrar novo cliente.")
        return
    
    valor = float(input("Informe o valor do saque:"))

    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacoes(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado. Favor verificar o cpf ou cadastrar novo cliente.")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n################################ EXTRATO ################################\n")
    print(str(conta))
    transacoes = conta.historico._transacoes
    extrato = ""
    if not transacoes:
            print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            extrato += f"{transacao['data']}\t-- {transacao['tipo']}\t-- R$ {transacao['valor']:.2f}\t-- Saldo: R$ {transacao['saldo']:.2f}\n"
    print(extrato)
    print(f"\nSaldo Atual: R$ {conta.saldo:.2f}")
    print("\n#########################################################################")

def criar_clientes(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
            print("\nCPF já cadastrado!")
            return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (Logradouro, no - bairro - cidade/Estado): ")
    
    cliente = PessoaFisica(nome = nome, cpf = cpf, data_nascimento = data_nascimento, endereco = endereco)

    clientes.append(cliente)

    print("\nCliente cadastrado com sucesso!")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta cadastrada.")
        return
    
    if len(cliente.contas) > 1:
        print("\nCliente possui mais de uma conta cadastrada. Contas disponíveis: ")
        for conta in cliente.contas:
            print(f"Conta: {conta.numero_conta}")
        num_conta = input("Informe o número da conta: ")
        conta = [conta for conta in cliente.contas if str(conta.numero_conta) == num_conta]
        return conta[0]
    return cliente.contas[0]
       
def criar_conta(AGENCIA, numero_conta, clientes, contas):
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado. Favor verificar o cpf ou cadastrar novo cliente.")

    conta = ContaCorrente.nova_conta(cliente = cliente, numero_conta = numero_conta, AGENCIA = AGENCIA)
    contas.append(conta)
    cliente.contas.append(conta)
    print(f"\nConta criada com sucesso!\nAgência: {conta.AGENCIA}  Cc: {numero_conta}\nUsuário: {cliente.nome}  CPF: {cliente.cpf}")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def listar_clientes(clientes):
    for cliente in clientes:
        print("=" * 100)
        print(textwrap.dedent(str(cliente)))

def main():
    clientes = []
    contas = []
    
    while True: # loop infinito
    
        opção = menu()

        if opção == "d":
            depositar(clientes)

        elif opção == "s":
            sacar(clientes)

        elif opção == "e":
            exibir_extrato(clientes)

        elif opção == "nu":
            criar_clientes(clientes)

        elif opção == "nc":
            numero_conta = len(contas) + 1
            criar_conta(Conta.AGENCIA, numero_conta, clientes, contas)      
     
        elif opção == "lc":
            listar_contas(contas)

        elif opção == "lu":
            listar_clientes(clientes)

        elif opção =="q":
            print("\nObrigado por utilizar nossos serviços!")
            break

        else:
            print("\nOperação inválida.  Por favor selecione novamente a operação desejada.")

main ()