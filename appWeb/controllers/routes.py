from appWeb import app
import sqlite3
from flask import redirect, render_template, request, url_for
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px


TABLE_NAMES_TITLE_PAGES = {
    "cad_cia_aberta" : "Companhias Abertas (B3)",
    "fre_cia_aberta_empregado_local_faixa_etaria_2024" : "Companhia Aberta Empregado Local Faixa Etária",
    "fre_cia_aberta_empregado_local_declaracao_raca_2024" : "Companhia Aberta Empregado Local Declaração Raça",
    "fre_cia_aberta_empregado_local_declaracao_genero_2024" : "Companhia Aberta Empregado Local Declaração Gênero"
}


# Função para conectar ao banco de dados
def get_db_connection():
    return sqlite3.connect('database.db')  


# Rota inicial
@app.route('/')
def index():
    title_page = 'Teste de Avaliação Régia'
    return render_template('index.html', title_page=title_page)


# Rota de visualização dos dados 
@app.route('/view_data/<string:table_name>')
def view_data(table_name):
    # Estabelece uma conexão com o banco de dados e realiza a query
    conn = get_db_connection()
    query = f"SELECT * FROM {table_name} limit 50"
    df = pd.read_sql_query(query, conn)
    conn.close()
    print(df.head())

    return render_template("view_table_data.html", table=df, table_name=table_name, title_page=TABLE_NAMES_TITLE_PAGES[table_name])


@app.route('/form_ref_cvm')
def form_ref_cvm():
    title_page = 'Formulário de Referência (CVM)'
    return render_template("form_ref_cvm.html", title_page=title_page)


@app.route("/update_table/<table_name>/<int:row_id>", methods=["POST"])
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

    return redirect(url_for('view_data',table_name=table_name))
   




# Integrando Dash ao Flask
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/')

# Busca os dados das tabelas
conn = get_db_connection()
query_genero = '''
    select * from fre_cia_aberta_empregado_local_declaracao_genero_2024
'''
df_genero = pd.read_sql_query(query_genero, conn)

query_raca = '''
    select * from fre_cia_aberta_empregado_local_declaracao_raca_2024
'''
df_raca = pd.read_sql_query(query_raca, conn)

query_faixa_etaria = '''
    select * from fre_cia_aberta_empregado_local_faixa_etaria_2024
'''
df_faixa_etaria = pd.read_sql_query(query_faixa_etaria, conn)
conn.close()

# Configura o layout do dashboard
dash_app.layout = html.Div(
    [
        # Dash 1
        html.H1(children='Distribuição percentual de funcionários por gênero', style={'textAlign':'center'}),
        dcc.Dropdown(df_genero.Nome_Companhia.unique(), df_genero.Nome_Companhia[0], id='dropdown-companhia'),
        dcc.Graph(
            id='graph-content-companhia',
            figure={
                'data': [{'type': 'pie'}]
            }
        ),
        # Dash 2
        html.H1(children='Distribuição percentual de funcionários por raça', style={'textAlign':'center'}),
        dcc.Dropdown(df_raca.Nome_Companhia.unique(), df_raca.Nome_Companhia[0], id='dropdown-raca'),
        dcc.Graph(
            id='graph-content-raca',
            figure={
                'data': [{'type': 'bar'}]
            }
        ),
        # Dash 3
        html.H1(children='Distribuição percentual de funcionários por faixa etária', style={'textAlign':'center'}),
        dcc.Dropdown(df_raca.Nome_Companhia.unique(), df_raca.Nome_Companhia[0], id='dropdown-faixa-etaria'),
        dcc.Graph(
            id='graph-content-faixa-etaria',
            figure={
                'data': [{'type': 'bar'}]
            }
        )
    ]
)

# Função de callback para alteração da distribuição por gênero
@callback(
    Output('graph-content-companhia', 'figure'),
    Input('dropdown-companhia', 'value')
)
def update_graph(empresa_selecionada):
    # Faz o somatório das colunas de quantidade de todos os locais da companhia
    totais_df = df_genero.groupby('Nome_Companhia').agg({
        'Quantidade_Feminino' : 'sum',
        'Quantidade_Masculino' : 'sum',
        'Quantidade_Nao_Binario' : 'sum',
        'Quantidade_Outros' : 'sum',
        'Quantidade_Sem_Resposta' : 'sum'
    })
    
    # Pega os totais apenas da empresa selecionada e transforma em um Series
    total_empresa_selecionada = totais_df.loc[empresa_selecionada]
    
    # Reseta o index mudando de nome da companhia para sequencial
    total_empresa_selecionada_df = total_empresa_selecionada.reset_index()

    # Renomeia as colunas
    total_empresa_selecionada_df.columns = ['Gênero', 'Quantidade']

    dff = total_empresa_selecionada_df
    return px.pie(dff, names='Gênero', values='Quantidade')


# Função de callback para alteração da distribuição por raça
@callback(
    Output('graph-content-raca', 'figure'),
    Input('dropdown-raca', 'value')
)
def update_graph(empresa_selecionada):
    # Faz o somatório das colunas de quantidade de todos os locais da companhia
    totais_df = df_raca.groupby('Nome_Companhia').agg({
        'Quantidade_Amarelo' : 'sum',
        'Quantidade_Branco' : 'sum',
        'Quantidade_Preto' : 'sum',
        'Quantidade_Pardo' : 'sum',
        'Quantidade_Indigena' : 'sum',
        'Quantidade_Outros' : 'sum',
        'Quantidade_Sem_Resposta' : 'sum'
    })
    
    # Pega os totais apenas da empresa selecionada e transforma em um Series
    total_empresa_selecionada = totais_df.loc[empresa_selecionada]

    # Reseta o index mudando de nome da companhia para sequencial
    total_empresa_selecionada_df = total_empresa_selecionada.reset_index()

    # Renomeia as colunas
    total_empresa_selecionada_df.columns = ['Raça', 'Quantidade']

    dff = total_empresa_selecionada_df
    return px.bar(dff, x='Raça', y='Quantidade')


# Função de callback para alteração da distribuição por faixa etária
@callback(
    Output('graph-content-faixa-etaria', 'figure'),
    Input('dropdown-faixa-etaria', 'value')
)
def update_graph(empresa_selecionada):
    # Faz o somatório das colunas de quantidade de todos os locais da companhia
    totais_df = df_faixa_etaria.groupby('Nome_Companhia').agg({
        'Quantidade_Ate30Anos' : 'sum',
        'Quantidade_30a50Anos' : 'sum',
        'Quantidade_Acima50Anos' : 'sum'
    })

    # Pega os totais apenas da empresa selecionada e transforma em um Series
    total_empresa_selecionada = totais_df.loc[empresa_selecionada]

    # Reseta o index mudando de nome da companhia para sequencial
    total_empresa_selecionada_df = total_empresa_selecionada.reset_index()

    # Renomeia as colunas
    total_empresa_selecionada_df.columns = ['Faixa Etaria', 'Quantidade']

    dff = total_empresa_selecionada_df
    return px.bar(dff, x='Faixa Etaria', y='Quantidade')