from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DB_PATH = 'banco.db'

def get_filtros():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(banco)") 
    colunas = [col[1] for col in cur.fetchall()]
    conn.close()
    return colunas

@app.route('/', methods=['GET', 'POST'])
def index():
    filtros = ['ano', 'edicao', 'cidade_sede', 'pais', 'delegacao', 'equipe', 'id_atleta',
               'nome_atleta', 'sexo', 'idade', 'altura', 'peso', 'esporte', 'evento', 'medalha']
    resultados = []

    if request.method == 'POST':
        query = "SELECT * FROM banco WHERE 1=1" 
        params = []

        for filtro in filtros:
            valor = request.form.get(filtro)
            if valor:
                query += f" AND {filtro} = ?"
                params.append(valor)

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(query, params)
        resultados = cur.fetchall()
        conn.close()

    return render_template('index.html', filtros=filtros, resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
