import pandas as pd 
import plotly.express as px
import plotly


def criar_dash_funcionarios_genero(conn):
    print('Criando dash')

    tags_select = criar_tags_select(conn)

    return tags_select    


def criar_tags_select(conn):
    query = """SELECT
        g.Nome_Companhia,
        SUM(g.Quantidade_Feminino) AS Feminino,
        SUM(g.Quantidade_Masculino) AS Masculino,
        SUM(g.Quantidade_Nao_Binario) AS Nao_Binario,
        SUM(g.Quantidade_Outros) AS Outros,
        SUM(g.Quantidade_Sem_Resposta) AS Sem_Resposta,
        SUM(g.Quantidade_Feminino) + SUM(g.Quantidade_Masculino) + SUM(g.Quantidade_Nao_Binario) + SUM(g.Quantidade_Outros) + SUM(g.Quantidade_Sem_Resposta) TOTAL
        FROM
            fre_cia_aberta_empregado_local_declaracao_genero_2024 g
        GROUP BY
        g.Nome_Companhia
    """
    
    df = pd.read_sql_query(query, conn)

    unique_values = df['Nome_Companhia'].unique()
    options = ''.join(f'<option value="{value}">{value}</option>' for value in unique_values)
    select_html = f'<select>{options}</select>'
    return select_html

def exemplo_dash_generico_scatter():
    # Simulando dados
    df = px.data.iris()

    # Criando um gráfico de dispersão
    fig = px.scatter(df, x="sepal_length", y="sepal_width", color="species")

    # Convertendo o gráfico para HTML
    plot_div = plotly.offline.plot(fig, output_type='div')

    return plot_div


def exemplo_dash_generico_pie(conn):
    print('Criando dash')
    

    # Simulando dados de funcionários (adapte para sua fonte de dados)
    data = [
        {'Gênero': 'Masculino', 'Quantidade': 120},
        {'Gênero': 'Feminino', 'Quantidade': 80},
        {'Gênero': 'Não Binário', 'Quantidade': 10}
    ]
    
    # Criando um DataFrame do Pandas para facilitar a manipulação
    df = pd.DataFrame(data)
    
    # Criando um gráfico de pizza com as porcentagens
    # fig = px.pie(df, values='Quantidade', names='Gênero', title='Distribuição de Funcionários por Gênero')
    fig = px.pie(df, values='Quantidade', names='Gênero', title='Distribuição de Funcionários por Gênero',
             color_discrete_sequence=px.colors.qualitative.Pastel,
             hover_data=['Quantidade'],
             labels={'Quantidade': 'Número de Funcionários'},
             )

    # Convertendo o gráfico para HTML
    plot_div = plotly.offline.plot(fig, output_type='div')

    return plot_div


    




