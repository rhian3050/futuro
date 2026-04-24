saldo = 0
extrato = []

op = 0

while op != 4:

    print("===== MENU =====")
    print("1 - Adicionar Dinheiro")
    print("2 - Sacar Dinheiro")
    print("3 - Mostrar Extrato")
    print("4 - Sair")

    op = int(input("Escolha: "))

    if op == 1:
        valor = float(input("Valor deposito: "))
        saldo += valor
        extrato.append("Deposito " + str(valor))
        print("ok deposito")

    if op == 2:
        valor = float(input("Valor saque: "))
        if valor > saldo:
            print("nao tem saldo")
        else:
            saldo = saldo - valor
            extrato.append("Saque " + str(valor))
            print("ok saque")

    if op == 3:
        print("EXTRATO:")
        for i in extrato:
            print(i)
        print("saldo =", saldo)

    if op == 4:
        print("fim")

print("programa acabou")