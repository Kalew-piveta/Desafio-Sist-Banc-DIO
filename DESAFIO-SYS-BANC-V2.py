import time as t

menu = """
Bem vindo!
Selecione uma opção:

[u] Criar usuário
[c] Criar conta
[s] Saque
[d] Deposito
[e] Extrato
[q] Sair do Sistema

--> """

def auth_usuario(cpf, lista_usuarios):
    usuario = [usuario for usuario in lista_usuarios if usuario["cpf"] == cpf]
    return usuario[0] if usuario else None

def criar_usuario(lista_usuarios):
    cpf = input("Digite seu CPF (Somente números): ")
    usuario = auth_usuario(cpf, lista_usuarios)

    if usuario:
        print("\n### Esse usuário já existe!! ###\n")
        return lista_usuarios
    nome = input("Digite seu nome: ")
    data_nasc = input("Digite sua data de nascimento (dd-mm-aaaa): ")
    endereco = input("Digite seu endereço (logradouro, numero - bairro - cidade/sigla do estado): ")
    lista_usuarios.append({"nome": nome, "data_nascimento": data_nasc, "cpf": cpf, "endereco": endereco})

    print("\n### Usuário criado com sucesso! ###\n")
    return lista_usuarios

def criar_conta(lista_contas, numero_contas, agencia):
    cpf = input("Digite seu CPF (Somente números): ")
    usuario = auth_usuario(cpf, lista_usuarios)
    
    if usuario:
        numero_contas += 1
        lista_contas.append({"agencia": agencia, "numero_conta": numero_contas, "cpf_usuario": cpf})
        print("\n### Sua conta foi criada com sucesso! ###\n")
        return lista_contas, numero_contas
    
    print("\n### Usuário não encontrado. Crie um primeiramente! ###\n")
    return lista_contas, numero_contas

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > 0:
        if numero_saques < limite_saques:
            if valor <= limite: 
                if valor <= saldo:
                    print("\n### Seu Saque foi efetuado com sucesso! ###\n") 
                    saldo -= valor
                    extrato += f"\nSaque feito no valor de R${valor:.2f}\n"
                    numero_saques += 1
                    return saldo, extrato, numero_saques
                else:
                    print("\n### Não há saldo suficiente na sua conta para essa operação ###\n### Refaça a operação! ###\n")    
            else:
                print(f"\n### Seu valor máximo de saque permitido é de R${limite:.2f} ###\n### Refaça a operação! ###\n")
        else:
            print(F"\n### O limite máximo de saque diário foi excedido, valor máximo diário são 3 ###\n")
    else:
        print("\n### Opção inválida! ###\n### Refaça a operação! ###\n")
    return saldo, extrato, numero_saques


def deposito(saldo, valor, extrato, /):
    if valor > 0.0:
        print("\n### Seu deposito foi efetuado com sucesso! ###\n") 
        saldo += valor
        extrato += f"\nDeposito feito no valor de R${valor:.2f}\n"
        return saldo, extrato
    else:
        print("\n### Esse valor é inválido! ###\n### Refaça a operação! ###\n")
    return saldo, extrato
    

def Extrato(saldo, /, *, extrato):
    print(extrato, f"\n\nSaldo final na conta R${saldo:.2f}\n##########################")



saldo = 0.0
limite = 500
extrato = "#### EXTRATO DA CONTA ####\n\n"
LIMITE_SAQUE = 3
AGENCIA = "0001"
count = 0
lista_usuarios = []
lista_contas = []
numero_contas = 0

while True:
    
    opcao = input(menu)

    if opcao == "s":
        valor = float(input("Digite o valor que deseja efetuar o saque: "))
        saldo, extrato, count = saque(saldo=saldo, 
                                      valor=valor, 
                                      extrato=extrato, 
                                      limite=limite, 
                                      numero_saques=count, 
                                      limite_saques=LIMITE_SAQUE)

    elif opcao == "d":
        valor_deposito = float(input("Digite o valor que deseja depositar: "))
        saldo, extrato = deposito(saldo, valor_deposito, extrato)

    elif opcao == "e":
        Extrato(saldo, extrato=extrato)

    elif opcao == "c":
        lista_contas, numero_contas = criar_conta(lista_contas, numero_contas, AGENCIA)

    elif opcao == "u":
        lista_usuarios = criar_usuario(lista_usuarios)

    elif opcao == "q":
        print("\nObrigado!\nVolte Sempre!")
        break

    else:
        print("Opção inválida. Por favor tente novamente uma opção válida!")
        
        
        