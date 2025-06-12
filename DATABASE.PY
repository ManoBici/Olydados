import sqlite3
import csv

# Abrir o CSV primeiro pra pegar os campos
with open('banco.csv', newline='', encoding='utf-8') as csvfile:
    leitor = csv.DictReader(csvfile)
    campos = leitor.fieldnames  # isso pega os nomes das colunas (ex: ['ano', 'edicao', 'cidade_sede', ...])

# Agora conecta no banco
conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()

# Criar a tabela dinamicamente
colunas = ', '.join([f"{campo} TEXT" for campo in campos])  # tudo como texto por simplicidade
cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS banco (
        {colunas}
    )
''')

# Agora reabrimos o CSV para inserir os dados
with open('banco.csv', newline='', encoding='utf-8') as csvfile:
    leitor = csv.DictReader(csvfile)
    for linha in leitor:
        valores = tuple(linha[campo] for campo in campos)
        placeholders = ', '.join(['?'] * len(campos))
        cursor.execute(f'''
            INSERT INTO banco ({', '.join(campos)})
            VALUES ({placeholders})
        ''', valores)

# Finaliza
conexao.commit()
conexao.close()
