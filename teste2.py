import os
import math
import random
from datetime import datetime

ARQ_USUARIOS = "dados/usuarios.txt"
ARQ_CRIPTOS = "dados/criptos.txt"
ARQ_EXTRATOS = "dados/extratos.txt"

# Formato das linhas de cada arquivo (campos separados por ";"):
#   usuarios.txt -> cpf;nome;senha;tipo;reais;carteira
#                   tipo = "admin" ou "investidor"
#                   carteira = "Bitcoin:0.0025,Ethereum:0.5" (vazia se não tem cripto)
#   criptos.txt  -> nome;cotacao;taxa_compra(%);taxa_venda(%)
#   extratos.txt -> cpf;data;sinal;valor;moeda;cotacao;taxa;saldos


# Leitura e gravação de arquivos
def ler_arquivo(arquivos):
    arq = open(arquivos, "r", encoding="utf-8")
    linhas = arq.readlines()
    arq.close()

    registrar = []
    for linha in linhas:
        if linha.strip() != "":
            registrar.append(linha.strip().split(";"))

    return registrar


def gravar_arquivo(arquivos, registrar):
    arq = open(arquivos, "w", encoding="utf-8")
    for r in registrar:
        linha = ";".join(r)
        arq.write(linha + "\n")
    arq.close()


def adicionar_arquivo(arquivos, registro):
    arq = open(arquivos, "a", encoding="utf-8")
    arq.write(";".join(registro) + "\n")
    arq.close()


def preparar_dados():
    os.makedirs("dados", exist_ok=True)

    if not os.path.exists(ARQ_USUARIOS):
        gravar_arquivo(ARQ_USUARIOS, [
            ["12345678900", "Administrador", "123456", "admin", "0.00", ""]
        ])
    if not os.path.exists(ARQ_CRIPTOS):
        gravar_arquivo(ARQ_CRIPTOS, [
            ["Bitcoin", "400000.00", "2", "3"],
            ["Ethereum", "16108.00", "1", "2"],
            ["Ripple", "2.57", "1", "1"],
        ])
    if not os.path.exists(ARQ_EXTRATOS):
        gravar_arquivo(ARQ_EXTRATOS, [])


# Funções
def formatar_reais(valor):
    return f"{valor:.2f}".replace(".", ",")


def texto_qtd(valor):
    texto = f"{valor:.8f}".rstrip("0")
    if texto.endswith("."):
        texto = texto + "0"
    return texto


def formatar_qtd(valor):
    return texto_qtd(valor).replace(".", ",")


def ler_cpf(mensagem="CPF (somente números, sem pontos e sem traços): "):
    while True:
        cpf = input(mensagem).strip()
        if len(cpf) == 11 and cpf.isdigit():
            return cpf
        print("CPF inválido: informe 11 dígitos, sem pontos e sem traços.")


def ler_senha():
    while True:
        senha = input("Senha (6 dígitos numéricos): ").strip()
        if len(senha) == 6 and senha.isdigit():
            return senha
        print("Senha inválida: use exatamente 6 dígitos numéricos.")


def ler_nome(mensagem):
    while True:
        nome = input(mensagem).strip()
        if nome != "" and nome.replace(" ", "").isalnum():
            return nome
        print("Nome inválido: use apenas letras, números e espaços.")


def ler_valor(mensagem, permitir_zero=False):
    while True:
        texto = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(texto)
        except ValueError:
            print("Valor inválido. Digite um número.")
            continue
        if not math.isfinite(valor) or valor < 0 or (valor == 0 and not permitir_zero):
            print("Valor inválido. Digite um número positivo.")
            continue
        return valor


def confirmar(mensagem):
    while True:
        resposta = input(mensagem + " (S/N): ").strip().upper()
        if resposta == "S":
            return True
        if resposta == "N":
            return False
        print("Responda S ou N.")


def confirmar_senha(registro):
    if ler_senha() == registro[2]:
        return True
    print("Senha incorreta.")
    return False


def buscar_usuario(cpf):
    for registro in ler_arquivo(ARQ_USUARIOS):
        if registro[0] == cpf:
            return registro
    return None


def salvar_usuario(usuario_novo):
    registros = ler_arquivo(ARQ_USUARIOS)
    for i in range(len(registros)):
        if registros[i][0] == usuario_novo[0]:
            registros[i] = usuario_novo
    gravar_arquivo(ARQ_USUARIOS, registros)


def buscar_cripto(nome):
    for cripto in ler_arquivo(ARQ_CRIPTOS):
        if cripto[0].lower() == nome.lower():
            return cripto
    return None


def carteira_para_dict(texto):
    carteira = {}
    if texto != "":
        for item in texto.split(","):
            nome, quantidade = item.split(":")
            carteira[nome] = float(quantidade)
    return carteira


def dict_para_carteira(carteira):
    itens = []
    for nome in carteira:
        if carteira[nome] > 0:
            itens.append(nome + ":" + texto_qtd(carteira[nome]))
    return ",".join(itens)


def mostrar_cotacoes():
    print("\n--- Cotações atuais ---")
    for cripto in ler_arquivo(ARQ_CRIPTOS):
        print(f"{cripto[0]}: R$ {formatar_reais(float(cripto[1]))} "
              f"(taxa compra {cripto[2]}% | taxa venda {cripto[3]}%)")


def mostrar_saldo(registro):
    carteira = carteira_para_dict(registro[5])
    print("\nNome:", registro[1])
    print("CPF:", registro[0])
    print("Reais:", formatar_reais(float(registro[4])))
    for cripto in ler_arquivo(ARQ_CRIPTOS):
        print(f"{cripto[0]}: {formatar_qtd(carteira.get(cripto[0], 0.0))}")


def registrar_extrato(registro, sinal, valor, moeda, cotacao, taxa):
    carteira = carteira_para_dict(registro[5])
    saldos = ["REAL:" + f"{float(registro[4]):.2f}"]
    for cripto in ler_arquivo(ARQ_CRIPTOS):
        saldos.append(cripto[0] + ":" + texto_qtd(carteira.get(cripto[0], 0.0)))

# compras e movimentos (R$)
    if moeda == "REAL" or sinal == "+":
        texto_valor = f"{valor:.2f}"
    else:
        texto_valor = texto_qtd(valor)

    data = datetime.now().strftime("%d-%m-%Y %H:%M")
    adicionar_arquivo(ARQ_EXTRATOS, [
        registro[0], data, sinal, texto_valor, moeda,
        f"{cotacao:.2f}", f"{taxa:g}", "|".join(saldos),
    ])


def mostrar_extrato(registro):
    print("\nNome:", registro[1])
    print("CPF:", registro[0])
    achou = False
    for linha in ler_arquivo(ARQ_EXTRATOS):
        if linha[0] == registro[0]:
            achou = True
            saldos = linha[7].replace("|", " ").replace(":", ": ")
            print(f"{linha[1]} {linha[2]} {linha[3]} {linha[4]} "
                  f"CT: {linha[5]} TX: {linha[6]} {saldos}")
    if not achou:
        print("Nenhuma operação registrada.")

# Login
def login():
    print("\n--- Login ---")
    cpf = ler_cpf()
    senha = ler_senha()
    usuario = buscar_usuario(cpf)
    if usuario is not None and usuario[2] == senha:
        print("Bem-vindo(a),", usuario[1] + "!")
        return cpf
    print("CPF ou senha incorretos.")
    return None

# Funções do investidor
def consultar_saldo(usuario):
    registro = buscar_usuario(usuario)
    if confirmar_senha(registro):
        mostrar_saldo(registro)


def consultar_extrato(usuario):
    registro = buscar_usuario(usuario)
    if confirmar_senha(registro):
        mostrar_extrato(registro)


def depositar(usuario):
    registro = buscar_usuario(usuario)
    valor = ler_valor("Valor do depósito (R$): ")
    reais = round(float(registro[4]) + valor, 2)
    registro[4] = f"{reais:.2f}"
    salvar_usuario(registro)
    registrar_extrato(registro, "+", valor, "REAL", 0.0, 0.0)
    print("Depósito realizado!")
    mostrar_saldo(registro)


def sacar(usuario):
    registro = buscar_usuario(usuario)
    valor = ler_valor("Valor do saque (R$): ")
    reais = float(registro[4])
    if valor > reais:
        print("Saldo insuficiente. O saldo não pode ficar negativo.")
        return
    reais = round(reais - valor, 2)
    registro[4] = f"{reais:.2f}"
    salvar_usuario(registro)
    registrar_extrato(registro, "-", valor, "REAL", 0.0, 0.0)
    print("Saque realizado!")
    mostrar_saldo(registro)


def comprar_cripto(usuario):
    registro = buscar_usuario(usuario)
    if not confirmar_senha(registro):
        return

    mostrar_cotacoes()
    cripto = buscar_cripto(input("\nQual criptomoeda deseja comprar? "))
    if cripto is None:
        print("Criptomoeda não encontrada.")
        return

    reais = float(registro[4])
    print("Saldo em reais: R$", formatar_reais(reais))
    valor = ler_valor("Quanto deseja comprar (em R$, sem contar a taxa)? ")

    cotacao = float(cripto[1])
    taxa_percentual = float(cripto[2])
    taxa = round(valor * taxa_percentual / 100, 2)
    total = round(valor + taxa, 2)
    quantidade = round(valor / cotacao, 8)

    if total > reais:
        print("Saldo insuficiente. Custo total: R$", formatar_reais(total))
        return

    print(f"\nResumo: {formatar_qtd(quantidade)} {cripto[0]} por R$ {formatar_reais(valor)} "
          f"+ taxa R$ {formatar_reais(taxa)} = R$ {formatar_reais(total)}")
    if not confirmar("Confirmar compra?"):
        print("Compra cancelada.")
        return

    carteira = carteira_para_dict(registro[5])
    carteira[cripto[0]] = carteira.get(cripto[0], 0.0) + quantidade
    registro[4] = f"{round(reais - total, 2):.2f}"
    registro[5] = dict_para_carteira(carteira)
    salvar_usuario(registro)
    registrar_extrato(registro, "+", valor, cripto[0], cotacao, taxa_percentual / 100)
    print("Compra realizada!")
    mostrar_saldo(registro)


def vender_cripto(usuario):
    registro = buscar_usuario(usuario)
    if not confirmar_senha(registro):
        return

    mostrar_cotacoes()
    cripto = buscar_cripto(input("\nQual criptomoeda deseja vender? "))
    if cripto is None:
        print("Criptomoeda não encontrada.")
        return

    carteira = carteira_para_dict(registro[5])
    disponivel = carteira.get(cripto[0], 0.0)
    print(f"Você possui {formatar_qtd(disponivel)} {cripto[0]}.")
    quantidade = ler_valor(f"Quantidade de {cripto[0]} a vender: ")
    if quantidade > disponivel + 0.000000001:
        print("Quantidade insuficiente. O saldo não pode ficar negativo.")
        return
    quantidade = min(quantidade, disponivel)

    cotacao = float(cripto[1])
    taxa_percentual = float(cripto[3])
    bruto = round(quantidade * cotacao, 2)
    taxa = round(bruto * taxa_percentual / 100, 2)
    liquido = round(bruto - taxa, 2)

    print(f"\nResumo: {formatar_qtd(quantidade)} {cripto[0]} = R$ {formatar_reais(bruto)} "
          f"- taxa R$ {formatar_reais(taxa)} = R$ {formatar_reais(liquido)}")
    if not confirmar("Confirmar venda?"):
        print("Venda cancelada.")
        return

    carteira[cripto[0]] = disponivel - quantidade
    registro[4] = f"{round(float(registro[4]) + liquido, 2):.2f}"
    registro[5] = dict_para_carteira(carteira)
    salvar_usuario(registro)
    registrar_extrato(registro, "-", quantidade, cripto[0], cotacao, taxa_percentual / 100)
    print("Venda realizada!")
    mostrar_saldo(registro)


def atualizar_cotacao(nome=None):
    criptos = ler_arquivo(ARQ_CRIPTOS)
    for cripto in criptos:
        if nome is None or cripto[0].lower() == nome.lower():
            antiga = float(cripto[1])
            nova = round(antiga * random.uniform(0.95, 1.05), 2)
            minimo = math.ceil(antiga * 0.95 * 100) / 100
            maximo = math.floor(antiga * 1.05 * 100) / 100
            nova = max(min(nova, maximo), minimo, 0.01)
            cripto[1] = f"{nova:.2f}"
    gravar_arquivo(ARQ_CRIPTOS, criptos)
    print("Cotações atualizadas!")
    mostrar_cotacoes()


# Funções do administrador
def cadastrar_investidor():
    nome = ler_nome("Nome do investidor: ")
    cpf = ler_cpf()
    if buscar_usuario(cpf) is not None:
        print("Já existe um usuário com esse CPF.")
        return
    senha = ler_senha()
    adicionar_arquivo(ARQ_USUARIOS, [cpf, nome, senha, "investidor", "0.00", ""])
    print("Investidor cadastrado com sucesso!")


def buscar_investidor_admin():
    registro = buscar_usuario(ler_cpf("CPF do investidor: "))
    if registro is None or registro[3] != "investidor":
        print("CPF não encontrado.")
        return None
    return registro


def excluir_investidor():
    registro = buscar_investidor_admin()
    if registro is None:
        return
    mostrar_saldo(registro)
    if not confirmar("\nTem certeza que deseja excluir este investidor (extrato também)?"):
        print("Exclusão cancelada.")
        return

    usuarios = []
    for r in ler_arquivo(ARQ_USUARIOS):
        if r[0] != registro[0]:
            usuarios.append(r)
    gravar_arquivo(ARQ_USUARIOS, usuarios)

    extratos = []
    for linha in ler_arquivo(ARQ_EXTRATOS):
        if linha[0] != registro[0]:
            extratos.append(linha)
    gravar_arquivo(ARQ_EXTRATOS, extratos)
    print("Investidor excluído.")


def cadastrar_cripto():
    nome = ler_nome("Nome da criptomoeda: ")
    if buscar_cripto(nome) is not None:
        print("Essa criptomoeda já existe.")
        return
    cotacao = ler_valor("Cotação inicial (R$): ")
    taxa_compra = ler_valor("Taxa de compra (%): ", True)
    taxa_venda = ler_valor("Taxa de venda (%): ", True)
    adicionar_arquivo(ARQ_CRIPTOS, [nome, f"{cotacao:.2f}", f"{taxa_compra:g}", f"{taxa_venda:g}"])
    print("Criptomoeda cadastrada com sucesso!")


def excluir_cripto():
    cripto = buscar_cripto(input("Nome da criptomoeda a ser excluída: "))
    if cripto is None:
        print("Criptomoeda não encontrada.")
        return


    for usuario in ler_arquivo(ARQ_USUARIOS):
        if carteira_para_dict(usuario[5]).get(cripto[0], 0.0) > 0:
            print("Não é possível excluir: há investidores com saldo dessa criptomoeda.")
            return

    print("\nNome:", cripto[0])
    print("Cotação: R$", formatar_reais(float(cripto[1])))
    print("Taxa de compra:", cripto[2] + "%")
    print("Taxa de venda:", cripto[3] + "%")
    if not confirmar("\nTem certeza que deseja excluir esta criptomoeda?"):
        print("Exclusão cancelada.")
        return

    criptos = []
    for c in ler_arquivo(ARQ_CRIPTOS):
        if c[0] != cripto[0]:
            criptos.append(c)
    gravar_arquivo(ARQ_CRIPTOS, criptos)
    print("Criptomoeda excluída.")


def consultar_saldo_investidor():
    registro = buscar_investidor_admin()
    if registro is not None:
        mostrar_saldo(registro)


def consultar_extrato_investidor():
    registro = buscar_investidor_admin()
    if registro is not None:
        mostrar_extrato(registro)


def atualizar_cotacao_admin():
    print("1. Atualizar todas as criptomoedas")
    print("2. Atualizar uma criptomoeda específica")
    opcao = input("Escolha: ").strip()
    if opcao == "1":
        atualizar_cotacao()
    elif opcao == "2":
        mostrar_cotacoes()
        nome = input("\nQual criptomoeda deseja atualizar? ").strip()
        if buscar_cripto(nome) is None:
            print("Criptomoeda não encontrada.")
        else:
            atualizar_cotacao(nome)
    else:
        print("Opção inválida.")


# Menus
def menu_investidor(usuario):
    while True:
        nome = buscar_usuario(usuario)[1]
        print(f"\n=== MENU DO INVESTIDOR ({nome}) ===")
        print("[1.] Consultar saldo.")
        print("[2.] Consultar extrato.")
        print("[3.] Depositar.")
        print("[4.] Sacar.")
        print("[5.] Comprar criptomoedas.")
        print("[6.] Vender criptomoedas.")
        print("[7.] Atualizar cotação.")
        print("[8.] Sair.")
        opcao = input("Escolha: ").strip()

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
            print("Saindo da conta...")
            break
        else:
            print("Opção inválida.")


def menu_admin(usuario):
    while True:
        nome = buscar_usuario(usuario)[1]
        print(f"\n=== MENU DO ADMINISTRADOR ({nome}) ===")
        print("[1.] Cadastrar novo investidor.")
        print("[2.] Excluir investidor.")
        print("[3.] Cadastrar nova criptomoeda.")
        print("[4.] Excluir criptomoeda.")
        print("[5.] Consultar saldo de um investidor.")
        print("[6.] Consultar extrato de um investidor.")
        print("[7.] Atualizar cotação das criptomoedas.")
        print("[8.] Sair.")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_investidor()
        elif opcao == "2":
            excluir_investidor()
        elif opcao == "3":
            cadastrar_cripto()
        elif opcao == "4":
            excluir_cripto()
        elif opcao == "5":
            consultar_saldo_investidor()
        elif opcao == "6":
            consultar_extrato_investidor()
        elif opcao == "7":
            atualizar_cotacao_admin()
        elif opcao == "8":
            print("Saindo da conta de administrador...")
            break
        else:
            print("Opção inválida.")


def menu(usuario):
    if buscar_usuario(usuario)[3] == "admin":
        menu_admin(usuario)
    else:
        menu_investidor(usuario)


def inicio():
    preparar_dados()
    while True:
        print("\n=== EXCHANGE DE CRIPTOMOEDAS ===")
        print("1. Entrar")
        print("0. Encerrar programa")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            usuario = login()
            if usuario is not None:
                menu(usuario)
        elif opcao == "0":
            print("Programa encerrado. Seus dados estão salvos nos arquivos .txt.")
            break
        else:
            print("Opção inválida.")


inicio()