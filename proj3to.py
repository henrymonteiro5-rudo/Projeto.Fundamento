import os

ARQ_USUARIOS = "dados/usuarios.txt"
ARQ_CRIPTOS = "dados/criptos.txt"
ARQ_EXTRATOS = "dados/extratos.txt"


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


def preparar_dados():
    pass


def login():
    ...


def consultar_saldo(usuario):
    ...


def consultar_extrato(usuario):
    ...


def depositar(usuario):
    ...


def sacar(usuario):
    ...


def comprar_cripto(usuario):
    ...


def vender_cripto(usuario):
    ...


def atualizar_cotacao():
    ...


def menu(usuario):
    ...


def inicio():
    ...