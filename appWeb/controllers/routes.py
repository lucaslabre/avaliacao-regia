import sqlite3
from flask import Blueprint, render_template
import pandas as pd

main = Blueprint('main', __name__)


# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.bd')  
    conn.row_factory = sqlite3.Row        # Permite acessar os dados como dicionário
    return conn


# Rota inicial
@main.route('/')
def index():
    return render_template('index.html')


# Rota de visualização dos dados das companhias abertas B3
@main.route('/view_companhias_abertas_b3')
def view_companhias_abertas_b3():
    try:
        # Estabelece uma conexão com o banco de dados e realiza a query
        conn = get_db_connection()
        query = "SELECT * FROM cad_cia_aberta LIMIT 10"
        df = pd.read_sql_query(query, conn)
        conn.close()

        # Converte o DataFrame para uma tabela HTML
        table_html = df.to_html(classes="table table-bordered", index=False)
        return render_template("view_companhias_abertas_b3.html", table=table_html)

    except Exception as e:
        return render_template("view_companhias_abertas_b3.html", error="A tabela está vazia. Primeiro importe os dados")


    # conn = get_db_connection()
    # rows = conn.execute('select * from cad_cia_aberta limit 10').fetchall()
    # conn.close()
    # return render_template('/view_companhias_abertas_b3.html', reows=rows)
   