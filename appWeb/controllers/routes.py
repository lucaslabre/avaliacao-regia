import sqlite3
from flask import Blueprint, redirect, render_template, request, url_for
import pandas as pd

main = Blueprint('main', __name__)

TABLE_NAMES_TITLE_PAGES = {
    "cad_cia_aberta" : "Companhias Abertas (B3)",
    "fre_cia_aberta_empregado_local_faixa_etaria_2024" : "Companhia Aberta Empregado Local Faixa Etária",
    "fre_cia_aberta_empregado_local_declaracao_raca_2024" : "Companhia Aberta Empregado Local Declaração Raça",
    "fre_cia_aberta_empregado_local_declaracao_genero_2024" : "Companhia Aberta Empregado Local Declaração Gênero"
}

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.bd')  
    conn.row_factory = sqlite3.Row        # Permite acessar os dados como dicionário
    return conn


# Rota inicial
@main.route('/')
def index():
    return render_template('index.html')


# Rota de visualização dos dados 
@main.route('/view_data/<string:table_name>')
def view_data(table_name):
    try:
    # Estabelece uma conexão com o banco de dados e realiza a query
        conn = get_db_connection()
        query = f"SELECT * FROM {table_name} limit 3"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return render_template("view_companhias_abertas_b3.html", table=df, table_name=table_name, title_page=TABLE_NAMES_TITLE_PAGES[table_name])

    except Exception as e:
        return render_template("view_companhias_abertas_b3.html", error="Erro ao estabelecer conexão com banco de dados.")


@main.route('/form_ref_cvm')
def form_ref_cvm():
    title_page = 'Formulário de Referência (CVM)'
    return render_template("form_ref_cvm.html", title_page=title_page)


@main.route("/update_table/<table_name>/<int:row_id>", methods=["POST"])
def update_table(table_name, row_id):

    dict_request = dict(request.form)

    key_value = ""
    for key, value in dict_request.items():
        if key != 'index':
            key_value += f"{key} = '{value}',"
    
    # Remove a última vírgula 
    key_value = key_value[:-1]
    query = f'UPDATE {table_name} SET {key_value} WHERE "index" = {row_id}'

    # Executar a query
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()  # Confirmar a execução da query

        print("UPDATE realizado com sucesso!")
    except Exception as e:
        conn.rollback()  # Reverter em caso de erro
        print(f"Erro ao atualizar: {e}")
    finally:
        # Fechar a conexão
        conn.close()

    return redirect(url_for(f'main.view_data',table_name=table_name))
   