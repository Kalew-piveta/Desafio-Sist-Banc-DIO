from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("\n### Você não tem saldo suficiente! ###\n")
        elif valor > 0:
            self._saldo -= valor
            print("\n### Saque realizado com sucesso! ###\n")
            return True
        else:
            print("\n### Valor informado inválido! ###\n")
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n### Depósito realizado com sucesso! ###\n")
        else:
            print("\n### O valor informado é inválido! ###\n")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n### O valor desejado excedeu o limite. ###\n")
        elif excedeu_saques:
            print("\n### Excedeu o numero máximo de saques. ###\n")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}

"""

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%D-%m-%Y %H:%M:%D"),
            }
        )

def menu():
    menu = """
    Bem vindo!
    Selecione uma opção:

    [u] Criar usuário
    [c] Criar conta
    [l] Listar contas
    [s] Saque
    [d] Deposito
    [e] Extrato
    [q] Sair do Sistema

    --> """
    return input(textwrap.dedent(menu))

def auth_usuario(cpf, lista_usuarios):
    usuario = [usuario for usuario in lista_usuarios if usuario.cpf == cpf]
    return usuario[0] if usuario else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n### Cliente não possui contas! ###\n")
        return
    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = auth_usuario(cpf, clientes)

    if not cliente:
        print("\n### Cliente não encontrado! ###\n")
        return
    valor = float(input("Informado o valor a ser depositado: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = auth_usuario(cpf, clientes)

    if not cliente:
        print("\n### Cliente não foi encontrado! ###\n")
        return
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def Extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = auth_usuario(cpf, clientes)

    if not cliente:
        print("\n### Cliente não encontrado ###\n")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print("\n############### EXTRATO ###############")
    transacoes = conta.historico.transacoes

    extrato =''
    if not transacoes:
        extrato = "Não houve transações."
    else:
        for transacao in transacoes:
            extrato += f'\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}'
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("########################################")

def criar_conta(numero_conta, clientes, contas):    
    cpf = input("Informe o CPF do cliente: ")
    cliente = auth_usuario(cpf, clientes)

    if not cliente:
        print("\n### Cliente não encontrado. Fluxo encerrado! ###\n")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\n### Conta criada com sucesso! ###\n")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def criar_usuario(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = auth_usuario(cpf, clientes)

    if cliente:
        print("\n### Já existe cliente com esse CPF cadastrado! ###\n")
        return
    nome = input("Informa o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, numero - bairro - cidade/sigla do estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento,cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n### Cliente criado com sucesso! ###\n")

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        
        if opcao == 'd':
            depositar(clientes)

        elif opcao == 's':
            sacar(clientes)
        elif opcao == 'e':
            Extrato(clientes)
        elif opcao == 'c':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == 'u':
            criar_usuario(clientes)
        elif opcao == 'l':
            listar_contas(contas)
        elif opcao == "q":
            break
        else:
            print("\n### Opção inválida! Tente novamente! ###\n")

if __name__ == "__main__":
    main()