
# ---------------- ARQUIVOS ----------------

def ler_arquivo(nome):
    arquivo = open(nome, "r")
    texto = arquivo.read()
    arquivo.close()

    lista = []

    linhas = texto.split("\n")

    for linha in linhas:
        if linha != "":
            lista.append(linha.split(";"))

    return lista


def gravar_arquivo(nome, lista):
    arquivo = open(nome, "w")

    for item in lista:
        arquivo.write(";".join(item) + "\n")

    arquivo.close()


def registrar(usuario, descricao):
    extratos.append([usuario[1], descricao])
    gravar_arquivo("extratos.txt", extratos)


# ---------------- USUARIOS ----------------

def procurar_usuario(cpf):
    for usuario in usuarios:
        if usuario[1] == cpf:
            return usuario

    return None


def cadastrar_investidor():
    nome = input("Nome: ")
    cpf = input("CPF: ")
    senha = input("Senha: ")

    if procurar_usuario(cpf) != None:
        print("CPF ja cadastrado.")
        return

    novo = [nome, cpf, senha, "0"]

    for cripto in criptomoedas:
        novo.append("0")

    usuarios.append(novo)

    gravar_arquivo("usuarios.txt", usuarios)

    print("Investidor cadastrado!")


def excluir_investidor():
    cpf = input("CPF do investidor: ")
    usuario = procurar_usuario(cpf)

    if usuario == None:
        print("Investidor nao encontrado.")
    else:
        usuarios.remove(usuario)
        gravar_arquivo("usuarios.txt", usuarios)
        print("Investidor excluido!")


def login():
    cpf = input("CPF: ")
    senha = input("Senha: ")

    if cpf == "11111111111" and senha == "123456":
        menu_admin()
    else:
        usuario = procurar_usuario(cpf)

        if usuario != None and usuario[2] == senha:
            menu_investidor(usuario)
        else:
            print("CPF ou senha incorretos.")


# ---------------- CONSULTAS ----------------

def consultar_saldo(usuario):
    print("\nNome:", usuario[0])
    print("CPF:", usuario[1])
    print("Reais: R$", usuario[3])

    i = 0

    for cripto in criptomoedas:
        print(cripto[0], ":", usuario[4 + i])
        i = i + 1


def consultar_extrato(usuario):
    print("\n===== EXTRATO =====")

    for item in extratos:
        if item[0] == usuario[1]:
            print(item[1])


def saldo_de_investidor():
    cpf = input("CPF: ")
    usuario = procurar_usuario(cpf)

    if usuario == None:
        print("Usuario nao encontrado.")
    else:
        consultar_saldo(usuario)


def extrato_de_investidor():
    cpf = input("CPF: ")
    usuario = procurar_usuario(cpf)

    if usuario == None:
        print("Usuario nao encontrado.")
    else:
        consultar_extrato(usuario)


# ---------------- DEPOSITO E SAQUE ----------------

def depositar(usuario):
    valor = float(input("Valor do deposito: "))

    if valor > 0:
        usuario[3] = str(float(usuario[3]) + valor)

        gravar_arquivo("usuarios.txt", usuarios)

        registrar(usuario, "Deposito: R$ " + str(valor))

        print("Deposito realizado!")
    else:
        print("Valor invalido.")


def sacar(usuario):
    valor = float(input("Valor do saque: "))

    if valor > 0:
        if valor <= float(usuario[3]):
            usuario[3] = str(float(usuario[3]) - valor)

            gravar_arquivo("usuarios.txt", usuarios)

            registrar(usuario, "Saque: R$ " + str(valor))

            print("Saque realizado!")
        else:
            print("Saldo insuficiente.")
    else:
        print("Valor invalido.")


# ---------------- CRIPTOMOEDAS ----------------

def escolher_cripto():
    print("\n===== CRIPTOMOEDAS =====")

    i = 0

    for cripto in criptomoedas:
        print(i + 1, "-", cripto[0], "- R$", cripto[1])
        i = i + 1

    escolha = int(input("Escolha: "))

    i = 1

    for cripto in criptomoedas:
        if escolha == i:
            return i - 1

        i = i + 1

    print("Opcao invalida.")
    return -1


def comprar(usuario):
    i = escolher_cripto()

    if i == -1:
        return

    valor = float(input("Valor da compra: R$ "))

    cotacao = float(criptomoedas[i][1])
    taxa = float(criptomoedas[i][2])

    total = valor + (valor * taxa / 100)

    if valor > 0:
        if total <= float(usuario[3]):
            quantidade = valor / cotacao

            usuario[3] = str(float(usuario[3]) - total)

            usuario[4 + i] = str(float(usuario[4 + i]) + quantidade)

            gravar_arquivo("usuarios.txt", usuarios)

            registrar(usuario, "Compra de " + criptomoedas[i][0])

            print("Compra realizada!")
        else:
            print("Saldo insuficiente.")
    else:
        print("Valor invalido.")


def vender(usuario):
    i = escolher_cripto()

    if i == -1:
        return

    quantidade = float(input("Quantidade para vender: "))

    if quantidade > 0:
        if quantidade <= float(usuario[4 + i]):

            cotacao = float(criptomoedas[i][1])
            taxa = float(criptomoedas[i][3])

            valor = quantidade * cotacao
            total = valor - (valor * taxa / 100)

            usuario[4 + i] = str(float(usuario[4 + i]) - quantidade)

            usuario[3] = str(float(usuario[3]) + total)

            gravar_arquivo("usuarios.txt", usuarios)

            registrar(usuario, "Venda de " + criptomoedas[i][0])

            print("Venda realizada!")
        else:
            print("Saldo de criptomoeda insuficiente.")
    else:
        print("Quantidade invalida.")


# ---------------- ADMINISTRADOR ----------------

def cadastrar_cripto():
    nome = input("Nome: ")
    cotacao = input("Cotacao: ")
    taxa_compra = input("Taxa de compra: ")
    taxa_venda = input("Taxa de venda: ")

    nova = [nome, cotacao, taxa_compra, taxa_venda]

    criptomoedas.append(nova)

    for usuario in usuarios:
        usuario.append("0")

    gravar_arquivo("criptomoedas.txt", criptomoedas)
    gravar_arquivo("usuarios.txt", usuarios)

    print("Criptomoeda cadastrada!")


def excluir_cripto():
    nome = input("Nome da criptomoeda: ")

    i = 0

    for cripto in criptomoedas:
        if cripto[0] == nome:
            criptomoedas.remove(cripto)

            for usuario in usuarios:
                usuario.remove(usuario[4 + i])

            gravar_arquivo("criptomoedas.txt", criptomoedas)
            gravar_arquivo("usuarios.txt", usuarios)

            print("Criptomoeda excluida!")
            return

        i = i + 1

    print("Criptomoeda nao encontrada.")


def atualizar_cotacao():
    for cripto in criptomoedas:
        print(cripto[0])
        cripto[1] = input("Nova cotacao: ")

    gravar_arquivo("criptomoedas.txt", criptomoedas)

    print("Cotacoes atualizadas!")


# ---------------- MENU INVESTIDOR ----------------

def menu_investidor(usuario):
    opcao = ""

    while opcao != "8":
        print("\n===== MENU INVESTIDOR =====")
        print("1 - Consultar saldo")
        print("2 - Consultar extrato")
        print("3 - Depositar")
        print("4 - Sacar")
        print("5 - Comprar criptomoedas")
        print("6 - Vender criptomoedas")
        print("7 - Atualizar cotacoes")
        print("8 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            consultar_saldo(usuario)

        elif opcao == "2":
            consultar_extrato(usuario)

        elif opcao == "3":
            depositar(usuario)

        elif opcao == "4":
            sacar(usuario)

        elif opcao == "5":
            comprar(usuario)

        elif opcao == "6":
            vender(usuario)

        elif opcao == "7":
            atualizar_cotacao()

        elif opcao != "8":
            print("Opcao invalida.")


# ---------------- MENU ADMINISTRADOR ----------------

def menu_admin():
    opcao = ""

    while opcao != "8":
        print("\n===== MENU ADMINISTRADOR =====")
        print("1 - Cadastrar investidor")
        print("2 - Excluir investidor")
        print("3 - Cadastrar criptomoeda")
        print("4 - Excluir criptomoeda")
        print("5 - Consultar saldo")
        print("6 - Consultar extrato")
        print("7 - Atualizar cotacoes")
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


# ---------------- PROGRAMA PRINCIPAL ----------------

arquivo = open("usuarios.txt", "a")
arquivo.close()

arquivo = open("criptomoedas.txt", "a")
arquivo.close()

arquivo = open("extratos.txt", "a")
arquivo.close()


usuarios = ler_arquivo("usuarios.txt")
criptomoedas = ler_arquivo("criptomoedas.txt")
extratos = ler_arquivo("extratos.txt")


if criptomoedas == []:
    criptomoedas = [
        ["Bitcoin", "350000", "2", "3"],
        ["Ethereum", "15000", "1", "2"],
        ["Ripple", "2.50", "1", "1"]
    ]

    gravar_arquivo("criptomoedas.txt", criptomoedas)


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

print("Programa encerrado!")
