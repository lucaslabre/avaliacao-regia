import sqlite3
from flask import Blueprint, redirect, render_template, request, url_for
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
        query = "SELECT * FROM cad_cia_aberta limit 3"
        df = pd.read_sql_query(query, conn)
        conn.close()
    
        return render_template("view_companhias_abertas_b3.html", table=df)

    except Exception as e:
        return render_template("view_companhias_abertas_b3.html", error="Erro ao estabelecer conexão com banco de dados.")


@main.route("/update_table/<name_table>/<int:row_id>", methods=["POST"])
def update_table(name_table, row_id):

    dict_request = dict(request.form)

    key_value = ""
    for key, value in dict_request.items():
        if key != 'index':
            key_value += f"{key} = '{value}',"
    
    # Remove a última vírgula 
    key_value = key_value[:-1]
    query = f'UPDATE {name_table} SET {key_value} WHERE "index" = {row_id}'

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

    return redirect(url_for('main.view_companhias_abertas_b3'))






















# @main.route('/update', methods=['POST'])
# def update():
#     if request.method == 'POST':
#         record_id = request.form['id']
#         name = request.form['name']
#         value = request.form['value']

#         record = Record.query.get(record_id)
#         if record:
#             record.name = name
#             record.value = float(value)
#             db.session.commit()
#             flash('Registro atualizado com sucesso!', 'success')
#         else:
#             flash('Registro não encontrado.', 'danger')

#     return redirect(url_for('index'))
   