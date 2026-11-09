import random

ARQ_USUARIOS = "dados/usuarios.txt"
ARQ_CRIPTOS = "dados/criptomoedas.txt"
ARQ_EXTRATOS = "dados/extratos.txt"

def limpar_campo(texto):
    return texto.replace(";", ",").replace("\n", " ").strip()


def ler_arquivo(caminho):
    arq = open(caminho, "r", encoding="utf-8")
    linhas = arq.readlines()
    arq.close()

    registros = []

    for linha in linhas:
        if linha.strip() != "":
            registros.append(linha.strip().split(";"))

    return registros


def gravar_arquivo(caminho, registros):
    arq = open(caminho, "w", encoding="utf-8")

    for reg in registros:
        linha = ";".join(reg)
        arq.write(linha + "\n")

    arq.close()


def entrada_texto(msg):
    valor = input(msg).strip()

    while valor == "":
        print("Campo nao pode ser vazio.")
        valor = input(msg).strip()

    return limpar_campo(valor)


def entrada_numero(msg):
    valor = input(msg).strip()

    while not valor.isdigit():
        print("Digite apenas numeros.")
        valor = input(msg).strip()

    return valor


def pausa():
    input("\nPressione ENTER para continuar...")


def preparar_dados():
    for arq in [ARQ_USUARIOS, ARQ_CRIPTOS, ARQ_EXTRATOS]:
        arquivo = open(arq, "a", encoding="utf-8")
        arquivo.close()

    if len(ler_arquivo(ARQ_CRIPTOS)) == 0:
        criptos = [
            ["Bitcoin", "350000.00", "2", "3"],
            ["Ethereum", "15000.00", "1", "2"],
            ["Ripple", "2.50", "1", "1"]
        ]

        gravar_arquivo(ARQ_CRIPTOS, criptos)


def achar_usuario(cpf):
    usuarios = ler_arquivo(ARQ_USUARIOS)

    for usuario in usuarios:
        if usuario[1] == cpf:
            return usuario

    return []


def achar_cripto(nome):
    criptos = ler_arquivo(ARQ_CRIPTOS)

    for cripto in criptos:
        if cripto[0].lower() == nome.lower():
            return cripto

    return []


def login():
    print("\n--- LOGIN ---")

    cpf = entrada_numero("CPF: ")
    senha = entrada_numero("Senha: ")

    usuario = achar_usuario(cpf)

    if usuario == []:
        print("Usuario nao encontrado.")
        return []

    if usuario[2] == senha:
        print("Login realizado com sucesso!")
        return usuario
    else:
        print("Senha incorreta.")
        return []


def consultar_saldo(usuario):
    print("\n--- SALDO ---")
    print("Nome:", usuario[0])
    print("CPF:", usuario[1])
    print("Reais: R$", usuario[3])
    print("Bitcoin:", usuario[4])
    print("Ethereum:", usuario[5])
    print("Ripple:", usuario[6])

    pausa()


def consultar_extrato(usuario):
    extratos = ler_arquivo(ARQ_EXTRATOS)

    print("\n--- EXTRATO ---")

    encontrou = False

    for registro in extratos:
        if registro[0] == usuario[1]:
            print(registro[1], "-", registro[2], "- R$", registro[3])
            encontrou = True

    if encontrou == False:
        print("Nenhuma operacao encontrada.")

    pausa()


def depositar(usuario):
    valor = float(input("Valor do deposito: R$ "))

    if valor <= 0:
        print("Valor invalido.")
        pausa()
        return

    usuarios = ler_arquivo(ARQ_USUARIOS)

    for u in usuarios:
        if u[1] == usuario[1]:
            u[3] = str(float(u[3]) + valor)

    gravar_arquivo(ARQ_USUARIOS, usuarios)

    usuario[3] = str(float(usuario[3]) + valor)

    pausa()


def sacar(usuario):
    valor = float(input("Valor do saque: R$ "))

    saldo = float(usuario[3])

    if valor <= 0:
        print("Valor invalido.")
        pausa()
        return

    if valor > saldo:
        print("Saldo insuficiente.")
        pausa()
        return

    usuarios = ler_arquivo(ARQ_USUARIOS)

    for u in usuarios:
        if u[1] == usuario[1]:
            u[3] = str(float(u[3]) - valor)

    gravar_arquivo(ARQ_USUARIOS, usuarios)

    usuario[3] = str(float(usuario[3]) - valor)

    pausa()


def comprar_cripto(usuario):
    criptos = ler_arquivo(ARQ_CRIPTOS)

    print("\n--- COTACOES ---")

    for cripto in criptos:
        print(cripto[0], "- R$", cripto[1])

    nome = entrada_texto("\nQual criptomoeda deseja comprar? ")

    cripto = achar_cripto(nome)

    if cripto == []:
        print("Criptomoeda nao encontrada.")
        pausa()
        return

    valor = float(input("Valor da compra em reais: R$ "))

    cotacao = float(cripto[1])
    taxa = float(cripto[2])

    total = valor + (valor * taxa / 100)

    if valor <= 0:
        print("Valor invalido.")
        pausa()
        return

    if total > float(usuario[3]):
        print("Saldo insuficiente.")
        pausa()
        return

    indice = criptos.index(cripto) + 4
    quantidade = valor / cotacao

    usuarios = ler_arquivo(ARQ_USUARIOS)

    for u in usuarios:
        if u[1] == usuario[1]:
            u[3] = str(float(u[3]) - total)
            u[indice] = str(float(u[indice]) + quantidade)

    gravar_arquivo(ARQ_USUARIOS, usuarios)

    usuario[3] = str(float(usuario[3]) - total)
    usuario[indice] = str(float(usuario[indice]) + quantidade)

    pausa()


def vender_cripto(usuario):
    criptos = ler_arquivo(ARQ_CRIPTOS)

    print("\n--- COTACOES ---")

    for cripto in criptos:
        print(cripto[0], "- R$", cripto[1])

    nome = entrada_texto("\nQual criptomoeda deseja vender? ")

    cripto = achar_cripto(nome)

    if cripto == []:
        print("Criptomoeda nao encontrada.")
        pausa()
        return

    valor = float(input("Quantidade de criptomoeda que deseja vender: "))

    indice = criptos.index(cripto) + 4

    cotacao = float(cripto[1])
    taxa = float(cripto[3])

    quantidade_disponivel = float(usuario[indice])

    if valor <= 0 or valor > quantidade_disponivel:
        print("Quantidade invalida ou saldo insuficiente.")
        pausa()
        return

    bruto = valor * cotacao
    recebido = bruto - (bruto * taxa / 100)

    usuarios = ler_arquivo(ARQ_USUARIOS)

    for u in usuarios:
        if u[1] == usuario[1]:
            u[indice] = str(float(u[indice]) - valor)
            u[3] = str(float(u[3]) + recebido)

    gravar_arquivo(ARQ_USUARIOS, usuarios)

    usuario[indice] = str(float(usuario[indice]) - valor)
    usuario[3] = str(float(usuario[3]) + recebido)

    pausa()


def atualizar_cotacao():
    criptos = ler_arquivo(ARQ_CRIPTOS)

    for cripto in criptos:
        variacao = random.uniform(-5, 5)

        cotacao = float(cripto[1])

        cotacao = cotacao + (cotacao * variacao / 100)

        cripto[1] = str(round(cotacao, 2))

    gravar_arquivo(ARQ_CRIPTOS, criptos)

    print("Cotacoes atualizadas!")

    pausa()


def menu_usuario(usuario):
    opcao = ""

    while opcao != "8":
        print("\n===== EXCHANGE DE CRIPTOMOEDAS =====")
        print("1 - Consultar saldo")
        print("2 - Consultar extrato")
        print("3 - Depositar reais")
        print("4 - Sacar reais")
        print("5 - Comprar criptomoeda")
        print("6 - Vender criptomoeda")
        print("7 - Atualizar cotacoes")
        print("8 - Sair")

        opcao = input("\nEscolha uma opcao: ")

        if opcao == "1":
            consultar_saldo(usuario)

        elif opcao == "2":
            consultar_extrato(usuario)

        elif opcao == "3":
            depositar(usuario)

        elif opcao == "4":
            sacar(usuario)

        elif opcao == "5":
            comprar_cripto(usuario)

        elif opcao == "6":
            vender_cripto(usuario)

        elif opcao == "7":
            atualizar_cotacao()

        elif opcao == "8":
            print("Saindo da Exchange...")

        else:
            print("Opcao invalida.")


def cadastrar_usuario():
    print("\n--- CADASTRO DE INVESTIDOR ---")

    nome = entrada_texto("Nome: ")
    cpf = entrada_numero("CPF: ")

    if achar_usuario(cpf) != []:
        print("CPF ja cadastrado.")
        pausa()
        return

    senha = entrada_numero("Senha de 6 digitos: ")

    while len(senha) != 6:
        print("A senha deve ter 6 digitos.")
        senha = entrada_numero("Senha: ")

    usuario = [nome, cpf, senha, "0.00", "0.0", "0.0", "0.0"]

    usuarios = ler_arquivo(ARQ_USUARIOS)
    usuarios.append(usuario)

    gravar_arquivo(ARQ_USUARIOS, usuarios)

    print("Cadastro realizado com sucesso!")

    pausa()

def inicio():
    preparar_dados()

    opcao = ""

    while opcao != "3":
        print("\n===== EXCHANGE =====")
        print("1 - Login")
        print("2 - Cadastrar investidor")
        print("3 - Sair")

        opcao = input("\nEscolha uma opcao: ")

        if opcao == "1":
            usuario = login()

            if usuario != []:
                menu_usuario(usuario)

        elif opcao == "2":
            cadastrar_usuario()

        elif opcao == "3":
            print("Encerrando programa...")

        else:
            print("Opcao invalida.")


inicio()
