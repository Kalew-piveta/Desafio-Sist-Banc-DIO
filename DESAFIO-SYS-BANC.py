import time as t

menu = """
Bem vindo!
Selecione uma opção:

[s] Saque
[d] Deposito
[e] Extrato
[q] Sair do Sistema

--> """
def saque():
    global saldo,extrato,limite,LIMITE_SAQUE

    valor_saque = float(input("Digite o valor que deseja efetuar o saque: "))
    count = 0
    
    if valor_saque < 0:
        if count < LIMITE_SAQUE:
            if valor_saque <= limite:
                if valor_saque <= saldo:
                    print("\n### Seu Saque foi efetuado com sucesso! ###\n") 
                    saldo -= valor_saque
                    extrato += f"\nSaque feito no valor de R${valor_saque:.2f}\n"
                    count += 1
                else:
                    print("\n### Não há saldo suficiente na sua conta para essa operação ###\n### Refaça a operação! ###\n")    
            else:
                print(f"\n### Seu valor máximo de saque permitido é de R${limite:.2f} ###\n### Refaça a operação! ###\n")
        else:
            print(F"\n### O limite máximo de saque diário foi excedido, valor máximo diário são 3 ###\n")
    else:
        print("\n### Opção inválida! ###\n### Refaça a operação! ###\n")

    t.sleep(2)

def deposito():
    global extrato, saldo
    valor_deposito = float(input("Digite o valor que deseja depositar: "))
    if valor_deposito > 0.0:
        print("\n### Seu deposito foi efetuado com sucesso! ###\n") 
        saldo += valor_deposito
        extrato += f"\nDeposito feito no valor de R${valor_deposito:.2f}\n"
    else:
        print("\n### Esse valor é inválido! ###\n### Refaça a operação! ###\n")
    
    t.sleep(2)

def Extrato():
    global extrato
    print(extrato, f"\n\nSaldo final na conta R${saldo:.2f}\n##########################")

saldo = 0.0
limite = 500
extrato = "#### EXTRATO DA CONTA ####\n\n"
LIMITE_SAQUE = 3

while True:
    opcao = input(menu)
    
    if opcao == "s":
        saque()
    elif opcao == "d":
        deposito()
    elif opcao == "e":
        Extrato()
    elif opcao == "q":
        print("\nObrigado!\nVolte Sempre!")
        break
    else:
        print("Opção inválida. Por favor tente novamente uma opção válida!")
        
        
        