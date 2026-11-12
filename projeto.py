from random import random

ARQ_USUARIOS = "usuarios.txt"
ARQ_CRIPTOS = "cripto.txt"
ARQ_EXTRATOS = "arquivos.txt"

ADMIN_CPF = "11111111111"
ADMIN_SENHA = "123456"


def ler_linhas(caminho):
    arq = open(caminho, "r", encoding="utf-8")
    todas = arq.readlines()
    arq.close()

    linhas = []
    for linha in todas:
        if linha.strip() != "":
            linhas.append(linha.strip())
    return linhas


def gravar_linhas(caminho, linhas):
    arq = open(caminho, "w", encoding="utf-8")
    for linha in linhas:
        arq.write(linha + "\n")
    arq.close()


def juntar(partes):

    texto = partes[0]
    for i in range(1, len(partes)):
        texto = texto + ";" + partes[i]
    return texto


def preparar():

    for nome in [ARQ_USUARIOS, ARQ_CRIPTOS, ARQ_EXTRATOS]:
        arq = open(nome, "a", encoding="utf-8")
        arq.close()

    if len(ler_linhas(ARQ_CRIPTOS)) == 0:
        gravar_linhas(ARQ_CRIPTOS, ["Bitcoin;350000.00;2;3", "Ethereum;15000.00;1;2", "Ripple;2.50;1;1"])


def buscar_usuario(cpf):

    for linha in ler_linhas(ARQ_USUARIOS):
        u = linha.split(";")
        if u[1] == cpf:
            return u
    return []


def salvar_usuario(u):

    linhas = ler_linhas(ARQ_USUARIOS)
    for i in range(len(linhas)):
        if linhas[i].split(";")[1] == u[1]:
            linhas[i] = juntar(u)
    gravar_linhas(ARQ_USUARIOS, linhas)


def registrar(u, texto):
    criptos = ler_linhas(ARQ_CRIPTOS)

    saldos = "REAL: " + u[3]
    for i in range(len(criptos)):
        saldos = saldos + " " + criptos[i].split(";")[0] + ": " + u[4 + i]

    arq = open(ARQ_EXTRATOS, "a", encoding="utf-8")
    arq.write(u[1] + ";" + texto + " " + saldos + "\n")
    arq.close()

def senha(u):
    if input("Senha (6 digitos): ") == u[2]:
        return True
    print("Senha incorreta.")
    return False


def mostrar_saldo(u):
    criptos = ler_linhas(ARQ_CRIPTOS)
    print("Nome:", u[0])
    print("CPF:", u[1])
    print("Reais: %.2f" % float(u[3]))
    for i in range(len(criptos)):
        print(criptos[i].split(";")[0] + ":", u[4 + i])


def mostrar_extrato(u):
    print("Nome:", u[0])
    print("CPF:", u[1])
    for linha in ler_linhas(ARQ_EXTRATOS):
        partes = linha.split(";")
        if partes[0] == u[1]:
            print(partes[1])


def escolher_cripto():
   
    criptos = ler_linhas(ARQ_CRIPTOS)
    for i in range(len(criptos)):
        c = criptos[i].split(";")
        print(i + 1, "-", c[0], "- R$", c[1])

    escolha = input("Escolha o numero da criptomoeda: ")
    if escolha.isdigit() and int(escolha) >= 1 and int(escolha) <= len(criptos):
        return int(escolha) - 1

    print("Opcao invalida.")
    return -1


def atualizar_cotacao():
    criptos = ler_linhas(ARQ_CRIPTOS)

    for i in range(len(criptos)):
        c = criptos[i].split(";")
        cotacao = float(c[1])
        variacao = random() * 10 - 5
        nova_cotacao = cotacao + cotacao * variacao / 100
        c[1] = "%.2f" % nova_cotacao
        criptos[i] = juntar(c)
        print(c[0], "- R$", c[1])

    gravar_linhas(ARQ_CRIPTOS, criptos)
    print("Cotacoes atualizadas!")

def consultar_saldo(cpf):
    u = buscar_usuario(cpf)
    if senha(u):
        mostrar_saldo(u)


def consultar_extrato(cpf):
    u = buscar_usuario(cpf)
    if senha(u):
        mostrar_extrato(u)


def depositar(cpf):
    valor = float(input("Valor do deposito: R$ "))
    if valor <= 0:
        print("Valor invalido.")
        return

    u = buscar_usuario(cpf)
    reais = float(u[3])

    u[3] = "%.2f" % (reais + valor)
    salvar_usuario(u)
    registrar(u, "+ %.2f REAL CT: 0.0 TX: 0.00" % valor)
    mostrar_saldo(u)


def sacar(cpf):
    valor = float(input("Valor do saque: R$ "))
    u = buscar_usuario(cpf)
    reais = float(u[3])

    if valor <= 0:
        print("Valor invalido.")
        return
    if valor > reais:
        print("Saldo insuficiente.")
        return

    u[3] = "%.2f" % (reais - valor)
    salvar_usuario(u)
    registrar(u, "- %.2f REAL CT: 0.0 TX: 0.00" % valor)
    mostrar_saldo(u)


def comprar(cpf):
    u = buscar_usuario(cpf)
    if not senha(u):
        return
    i = escolher_cripto()
    if i == -1:
        return

    c = ler_linhas(ARQ_CRIPTOS)[i].split(";")
    cotacao = float(c[1])
    taxa = float(c[2]) / 100

    valor = float(input("Quanto deseja comprar (em reais): R$ "))
    total = valor + valor * taxa         
    quantidade = valor / cotacao         

    reais = float(u[3])
    saldo_cripto = float(u[4 + i])

    if valor <= 0:
        print("Valor invalido.")
        return
    if total > reais:
        print("Saldo insuficiente.")
        return

    u[3] = "%.2f" % (reais - total)
    u[4 + i] = "%.8f" % (saldo_cripto + quantidade)
    salvar_usuario(u)
    registrar(u, "+ %.2f %s CT: %s TX: %.2f" % (valor, c[0], c[1], taxa))
    mostrar_saldo(u)


def vender(cpf):
    u = buscar_usuario(cpf)
    if not senha(u):
        return
    i = escolher_cripto()
    if i == -1:
        return

    c = ler_linhas(ARQ_CRIPTOS)[i].split(";")
    cotacao = float(c[1])
    taxa = float(c[3]) / 100

    quantidade = float(input("Quanto deseja vender (quantidade de criptomoeda): "))
    bruto = quantidade * cotacao
    recebido = bruto - bruto * taxa      

    reais = float(u[3])
    saldo_cripto = float(u[4 + i])

    if quantidade <= 0:
        print("Quantidade invalida.")
        return
    if quantidade > saldo_cripto:
        print("Saldo de criptomoeda insuficiente.")
        return

    u[4 + i] = "%.8f" % (saldo_cripto - quantidade)
    u[3] = "%.2f" % (reais + recebido)
    salvar_usuario(u)
    registrar(u, "- %.2f %s CT: %s TX: %.2f" % (bruto, c[0], c[1], taxa))
    mostrar_saldo(u)

def cadastrar_investidor():
    linhas = ler_linhas(ARQ_USUARIOS)
    criptos = ler_linhas(ARQ_CRIPTOS)

    nome = input("Nome: ")
    cpf = input("CPF: ")
    senha = input("Senha (6 digitos): ")

    if not cpf.isdigit() or len(cpf) != 11 or len(senha) != 6 or not senha.isdigit():
        print("CPF ou senha invalidos.")
        return
    if buscar_usuario(cpf) != []:
        print("CPF ja cadastrado.")
        return

    novo = nome + ";" + cpf + ";" + senha + ";0.00"
    for c in criptos:
        novo = novo + ";0.00000000"

    linhas.append(novo)
    gravar_linhas(ARQ_USUARIOS, linhas)
    print("Investidor cadastrado!")


def excluir_investidor():
    cpf = input("CPF do investidor que deseja excluir: ")
    u = buscar_usuario(cpf)
    if u == []:
        print("CPF nao encontrado.")
        return

    mostrar_saldo(u)
    resposta = input("Deseja realmente excluir? (s/n): ")

    if resposta == "s":
        restantes = []
        for linha in ler_linhas(ARQ_USUARIOS):
            if linha.split(";")[1] != cpf:
                restantes.append(linha)
        gravar_linhas(ARQ_USUARIOS, restantes)

    extratos_novos = []
    for linha in ler_linhas(ARQ_EXTRATOS):
        partes = linha.split(";")
        if partes[0] != cpf:
                extratos_novos.append(linha)
        gravar_linhas(ARQ_EXTRATOS, extratos_novos)

        print("Investidor excluido!")
    else:
        print("Exclusao cancelada.")

def cadastrar_cripto():
    usuarios = ler_linhas(ARQ_USUARIOS)
    criptos = ler_linhas(ARQ_CRIPTOS)

    nome = input("Nome da criptomoeda: ")
    cotacao = float(input("Cotacao: R$ "))
    taxa_compra = float(input("Taxa de compra (%): "))
    taxa_venda = float(input("Taxa de venda (%): "))

    if cotacao <= 0:
        print("A cotacao precisa ser maior que zero.")
        return

    if taxa_compra < 0 or taxa_venda < 0:
        print("As taxas nao podem ser negativas.")
        return

    for linha in criptos:
        dados = linha.split(";")
        if dados[0].lower() == nome.lower():
            print("Essa criptomoeda ja esta cadastrada.")
            return

    criptos.append("%s;%.2f;%.2f;%.2f" %
                   (nome, cotacao, taxa_compra, taxa_venda))

    for i in range(len(usuarios)):
        usuarios[i] = usuarios[i] + ";0.00000000"

    gravar_linhas(ARQ_CRIPTOS, criptos)
    gravar_linhas(ARQ_USUARIOS, usuarios)
    print("Criptomoeda cadastrada!")


def excluir_cripto():
    usuarios = ler_linhas(ARQ_USUARIOS)
    criptos = ler_linhas(ARQ_CRIPTOS)

    nome = input("Nome da criptomoeda que deseja excluir: ")

    pos = -1
    for i in range(len(criptos)):
        if criptos[i].split(";")[0] == nome:
            pos = i

    if pos == -1:
        print("Criptomoeda nao encontrada.")
        return

    c = criptos[pos].split(";")
    print("Nome:", c[0])
    print("Cotacao: R$", c[1])
    print("Taxa de compra:", c[2], "%")
    print("Taxa de venda:", c[3], "%")
    resposta = input("Deseja realmente excluir? (s/n): ")

    if resposta == "s":
        criptos.pop(pos)

        for i in range(len(usuarios)):
            u = usuarios[i].split(";")
            u.pop(4 + pos)
            usuarios[i] = juntar(u)

        gravar_linhas(ARQ_CRIPTOS, criptos)
        gravar_linhas(ARQ_USUARIOS, usuarios)
        print("Criptomoeda excluida!")
    else:
        print("Exclusao cancelada.")


def saldo_de_investidor():
    u = buscar_usuario(input("CPF do investidor: "))
    if u == []:
        print("CPF nao encontrado.")
    else:
        mostrar_saldo(u)


def extrato_de_investidor():
    u = buscar_usuario(input("CPF do investidor: "))
    if u == []:
        print("CPF nao encontrado.")
    else:
        mostrar_extrato(u)

def menu_investidor(cpf):
    opcao = ""

    while opcao != "8":
        print("\n===== MENU DO INVESTIDOR =====")
        print("1 - Consultar saldo")
        print("2 - Consultar extrato")
        print("3 - Depositar")
        print("4 - Sacar")
        print("5 - Comprar criptomoedas")
        print("6 - Vender criptomoedas")
        print("7 - Atualizar cotacao")
        print("8 - Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            consultar_saldo(cpf)
        elif opcao == "2":
            consultar_extrato(cpf)
        elif opcao == "3":
            depositar(cpf)
        elif opcao == "4":
            sacar(cpf)
        elif opcao == "5":
            comprar(cpf)
        elif opcao == "6":
            vender(cpf)
        elif opcao == "7":
            atualizar_cotacao()
        elif opcao != "8":
            print("Opcao invalida.")


def menu_admin():
    opcao = ""

    while opcao != "8":
        print("\n===== MENU DO ADMINISTRADOR =====")
        print("1 - Cadastrar novo investidor")
        print("2 - Excluir investidor")
        print("3 - Cadastrar nova criptomoeda")
        print("4 - Excluir criptomoeda")
        print("5 - Consultar saldo de um investidor")
        print("6 - Consultar extrato de um investidor")
        print("7 - Atualizar cotacao das criptomoedas")
        print("8 - Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_investidor()
        elif opcao == "2":
            excluir_investidor()
        elif opcao == "3":
            cadastrar_cripto()
        elif opcao == "4":
            excluir_cripto()
        elif opcao == "5":
            saldo_de_investidor()
        elif opcao == "6":
            extrato_de_investidor()
        elif opcao == "7":
            atualizar_cotacao()
        elif opcao != "8":
            print("Opcao invalida.")


def login():
    cpf = input("CPF (sem pontos e sem tracos): ")


    if not cpf.isdigit() or len(cpf) != 11:
        print("CPF invalido. Digite 11 numeros.")
        return

    senha = input("Senha (6 digitos): ")

    if cpf == ADMIN_CPF and senha == ADMIN_SENHA:
        menu_admin()
    else:
        u = buscar_usuario(cpf)
        if u != [] and u[2] == senha:
            menu_investidor(cpf)
        else:
            print("CPF ou senha incorretos.")

preparar()
opcao = ""

while opcao != "2":
    print("\n===== EXCHANGE DE CRIPTOMOEDAS =====")
    print("1 - Login")
    print("2 - Sair")
    opcao = input("Escolha: ")

    if opcao == "1":
        login()
    elif opcao != "2":
        print("Opcao invalida.")
