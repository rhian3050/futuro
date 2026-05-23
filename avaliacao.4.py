# Avaliação Continuada 4 - 1 ponto
# PROJETO DE VENDAS - parte 2
# Exercicios de CRUD completo (Produtos, Vendedores e Vendas)
# Entrega - dia 24/05/2026


# PRODUTOS

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="projeto_vendas_eletronicos_unifecaf"
)

cursor = conn.cursor()


# PRODUTOS

def criar_produto():

    descricao = input("Digite a descricao: ")
    preco = float(input("Digite o preco: "))

    sql = "INSERT INTO produtos(descricao,preco) VALUES(%s,%s)"

    cursor.execute(sql, (descricao, preco))
    conn.commit()

    print("Produto cadastrado")


def listar_produtos():

    cursor.execute("SELECT * FROM produtos")

    dados = cursor.fetchall()

    for i in dados:
        print(i)


def atualizar_produto():

    id_produto = int(input("Digite o id: "))

    descricao = input("Nova descricao: ")
    preco = float(input("Novo preco: "))

    sql = """
    UPDATE produtos
    SET descricao=%s, preco=%s
    WHERE id=%s
    """

    cursor.execute(sql, (descricao, preco, id_produto))
    conn.commit()

    print("Produto atualizado")


def excluir_produto():

    id_produto = int(input("Digite o id: "))

    cursor.execute(
        "DELETE FROM vendas_produtos WHERE id_produto=%s",
        (id_produto,)
    )

    cursor.execute(
        "DELETE FROM produtos WHERE id=%s",
        (id_produto,)
    )

    conn.commit()

    print("Produto excluido")


# VENDEDORES

def criar_vendedor():

    nome = input("Nome do vendedor: ")

    cursor.execute(
        "INSERT INTO vendedores(nome) VALUES(%s)",
        (nome,)
    )

    conn.commit()

    print("Vendedor cadastrado")


def listar_vendedores():

    cursor.execute("SELECT * FROM vendedores")

    dados = cursor.fetchall()

    for i in dados:
        print(i)


def atualizar_vendedor():

    id_vendedor = int(input("Digite o id: "))

    nome = input("Novo nome: ")

    cursor.execute(
        "UPDATE vendedores SET nome=%s WHERE id=%s",
        (nome, id_vendedor)
    )

    conn.commit()

    print("Atualizado")


def excluir_vendedor():

    id_vendedor = int(input("Digite o id: "))

    cursor.execute(
        "SELECT * FROM vendas WHERE id_vendedor=%s",
        (id_vendedor,)
    )

    resultado = cursor.fetchall()

    if len(resultado) > 0:
        print("Esse vendedor tem vendas")
    else:

        cursor.execute(
            "DELETE FROM vendedores WHERE id=%s",
            (id_vendedor,)
        )

        conn.commit()

        print("Excluido")


# VENDAS

def criar_venda_com_itens():

    id_vendedor = int(input("Id vendedor: "))
    desconto = float(input("Desconto: "))
    data = input("Data e hora (AAAA-MM-DD HH:MM:SS): ")

    cursor.execute(
        """
        INSERT INTO vendas
        (id_vendedor,data_e_hora,desconto,valor_final)
        VALUES(%s,%s,%s,%s)
        """,
        (id_vendedor, data, desconto, 0)
    )

    conn.commit()

    id_venda = cursor.lastrowid

    total = 0

    while True:

        id_produto = int(input("Id produto: "))
        qtd = int(input("Quantidade: "))

        cursor.execute(
            "SELECT preco FROM produtos WHERE id=%s",
            (id_produto,)
        )

        preco = cursor.fetchone()

        if preco == None:
            print("Produto nao encontrado")
            continue

        valor_unitario = float(preco[0])

        valor_total = qtd * valor_unitario

        total = total + valor_total

        cursor.execute(
            """
            INSERT INTO vendas_produtos
            (id_venda,id_produto,quantidade,
            valor_unitario,valor_total)
            VALUES(%s,%s,%s,%s,%s)
            """,
            (
                id_venda,
                id_produto,
                qtd,
                valor_unitario,
                valor_total
            )
        )

        conn.commit()

        resp = input("Adicionar mais produto? (s/n): ")

        if resp.lower() != "s":
            break

    valor_final = total - desconto

    cursor.execute(
        """
        UPDATE vendas
        SET valor_final=%s
        WHERE id=%s
        """,
        (valor_final, id_venda)
    )

    conn.commit()

    print("Venda cadastrada")


def listar_vendas_completas():

    sql = """
    SELECT
    vendas.id,
    vendedores.nome,
    produtos.descricao,
    vendas_produtos.quantidade,
    vendas_produtos.valor_unitario,
    vendas_produtos.valor_total

    FROM vendas

    INNER JOIN vendedores
    ON vendas.id_vendedor = vendedores.id

    INNER JOIN vendas_produtos
    ON vendas.id = vendas_produtos.id_venda

    INNER JOIN produtos
    ON produtos.id = vendas_produtos.id_produto
    """

    cursor.execute(sql)

    dados = cursor.fetchall()

    for i in dados:
        print(i)


def atualizar_venda_e_itens():

    id_venda = int(input("Id da venda: "))

    desconto = float(input("Novo desconto: "))
    valor_final = float(input("Novo valor final: "))

    cursor.execute(
        """
        UPDATE vendas
        SET desconto=%s,
        valor_final=%s
        WHERE id=%s
        """,
        (desconto, valor_final, id_venda)
    )

    conn.commit()

    print("Venda atualizada")


def excluir_venda():

    id_venda = int(input("Digite o id da venda: "))

    cursor.execute(
        "DELETE FROM vendas_produtos WHERE id_venda=%s",
        (id_venda,)
    )

    cursor.execute(
        "DELETE FROM vendas WHERE id=%s",
        (id_venda,)
    )

    conn.commit()

    print("Venda excluida")


# MENU

def menu():

    while True:

        print("\n===== MENU =====")
        print("1 - Criar produto")
        print("2 - Listar produtos")
        print("3 - Atualizar produto")
        print("4 - Excluir produto")
        print("5 - Criar vendedor")
        print("6 - Listar vendedores")
        print("7 - Atualizar vendedor")
        print("8 - Excluir vendedor")
        print("9 - Criar venda")
        print("10 - Listar vendas")
        print("11 - Atualizar venda")
        print("12 - Excluir venda")
        print("0 - Sair")

        op = input("Escolha uma opcao: ")

        if op == "1":
            criar_produto()

        elif op == "2":
            listar_produtos()

        elif op == "3":
            atualizar_produto()

        elif op == "4":
            excluir_produto()

        elif op == "5":
            criar_vendedor()

        elif op == "6":
            listar_vendedores()

        elif op == "7":
            atualizar_vendedor()

        elif op == "8":
            excluir_vendedor()

        elif op == "9":
            criar_venda_com_itens()

        elif op == "10":
            listar_vendas_completas()

        elif op == "11":
            atualizar_venda_e_itens()

        elif op == "12":
            excluir_venda()

        elif op == "0":
            print("Fim do programa")
            break

        else:
            print("Opcao invalida")


menu()

cursor.close()
conn.close()