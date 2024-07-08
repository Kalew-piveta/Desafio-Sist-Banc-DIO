from abc import ABC, abstractmethod
from datetime import datetime, timezone
import textwrap
import functools

class ContaIterador:
    def __init__(self, contas: list):
        self.contas = contas
        self.count = 0
    def __iter__(self):
        return self
    def __next__(self):
        try: 
            conta = self.contas[self.count]
            self.count += 1
            return f"{conta.__str__()}\nSaldo:\t\tR$ {conta.saldo:.2f}"
        except IndexError:
            raise StopIteration

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) > 2:
            print("\n ### Você excedeu o número máximo de transações do dia. ###")
            return
        
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
                "data": datetime.now().strftime("%d-%m-%y %H:%M:%S"),
            }
        )
    
    def gerar_relatorio(self, tipo_transacao = None):        
        if tipo_transacao is None:
            for transacao in self.transacoes:
                yield f'\n{transacao['data']}\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}'
        else:
            for transacao in self.transacoes:
                    if transacao["tipo"] == tipo_transacao:
                        yield f'\n{transacao['data']}\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}'
    
    def transacoes_do_dia(self):
        data_atual = datetime.now().date()
        transacoes = []
        for transacao in self.transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes

def log_transacao(func):
    @functools.wraps(func)
    def printar(*args, **kwargs):
        retorno = func(*args, **kwargs)
        if retorno == True:
            print(f"Transação do tipo {func.__name__.upper()} foi feita em: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}")
        else:
            return
    return printar

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

@log_transacao
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
    return True

@log_transacao
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
    return True

@log_transacao
def Extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = auth_usuario(cpf, clientes)

    if not cliente:
        print("\n### Cliente não encontrado ###\n")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    tipo_trans = input("Selecione qual o filtro de transações deseja (saque/deposito). Caso não queira digite (n): ")
    print("\n############### EXTRATO ###############")
    # TODO: atualizar a implementação para utilizar o gerador definido na classe Histórico.
    extrato = ''
    if tipo_trans == "saque":
        for transacoes in conta.historico.gerar_relatorio(tipo_transacao = Saque.__name__):
            extrato += f'{transacoes}'
    elif tipo_trans == "deposito":
        for transacoes in conta.historico.gerar_relatorio(tipo_transacao = Deposito.__name__):
            extrato += f'{transacoes}'
    else:
        for transacoes in conta.historico.gerar_relatorio():
            extrato += f'{transacoes}'
    if extrato == '':     
        extrato += "Não houve transações."

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("########################################")
    return True

@log_transacao
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
    return True

@log_transacao
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
    return True

def listar_contas(contas):
    # TODO: implemetar utilizando a classe iteradora
    for conta in ContaIterador(contas=contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
        print("=" * 100)

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