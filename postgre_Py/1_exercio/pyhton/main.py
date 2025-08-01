import psycopg2
from datetime import datetime

def calcular_idade(data_nasc):
    hoje = datetime.now()
    return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))

def calcular_imc(peso, altura):
    return peso / (altura ** 2)

try:
    id_desejado = int(input("Digite o ID da pessoa: "))

    conn = psycopg2.connect(
        host="localhost",
        database="peso",
        user="vitor",
        password="133122"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT nome, nasc, peso, altura FROM paciente WHERE id = %s", (id_desejado,))
    pessoa = cursor.fetchone()

    if pessoa:
        nome, nasc, peso, altura = pessoa
        idade = calcular_idade(nasc)
        imc = calcular_imc(peso, altura)

        print("\nRELATÓRIO DE SAÚDE")
        print("=" * 50)
        print(f"\nNome: {nome}")
        print(f"Idade: {idade} anos")
        print(f"Peso: {peso} kg | Altura: {altura} m")
        print(f"IMC: {imc:.2f} - ", end="")

        if imc < 18.5:
            print("Abaixo do peso")
        elif 18.5 <= imc < 25:
            print("Peso normal")
        elif 25 <= imc < 30:
            print("Sobrepeso")
        else:
            print("Obesidade")
        print("\n" + "=" * 50)
    else:
        print(f"Nenhuma pessoa encontrada com o ID {id_desejado}")

except psycopg2.Error as err:
    print(f"Erro de conexão ou consulta: {err}")

except ValueError:
    print("ID inválido. Por favor, digite um número inteiro.")

finally:
    try:
        if conn:
            cursor.close()
            conn.close()
            print("Conexão encerrada.")
    except NameError:
        pass
