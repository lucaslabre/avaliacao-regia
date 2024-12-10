import io
import os
import zipfile
import requests
import pandas as pd
import sqlite3

from sqlalchemy import create_engine

# URL do arquivo CSV
CSV_URL  = "https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv"

#  URL do arquivo zip
ZIP_URL_META_FRE_CIA_ABERTA = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FRE/DADOS/fre_cia_aberta_2024.zip"

# Tabelas que queremos extrair do ZIP
TARGET_FILES = [
    "fre_cia_aberta_empregado_local_faixa_etaria_2024.csv",
    "fre_cia_aberta_empregado_local_declaracao_raca_2024.csv",
    "fre_cia_aberta_empregado_local_declaracao_genero_2024.csv"
]

# Banco de dados SQLite
DB_FILE = "database.bd"

# Configuração do banco de dados SQLite
DATABASE_URI = "sqlite:///database.bd"
engine = create_engine(DATABASE_URI)

def importar_dados_companhias_abertas():
    # Baixa o CSV
    response = requests.get(CSV_URL)
    response.raise_for_status()
    
    # Lê o conteúdo do CSV em um DataFrame
    csv_content = io.StringIO(response.content.decode("latin1"))
    df = pd.read_csv(csv_content, sep=";", encoding="latin1")

    # Conecta ao banco de dados SQLite
    conn = sqlite3.connect(DB_FILE)
    df.to_sql("cad_cia_aberta", conn, if_exists="replace", index=True)
    conn.close()
    print("Dados das Companhias Abertas importados e salvos no banco de dados com sucesso.")


def importar_dados_formulario_referencia():
    zip_path = "meta_fre_cia_aberta.zip"
    extract_path = "extracted_data"

    try:
        # Baixar o arquivo ZIP
        response = requests.get(ZIP_URL_META_FRE_CIA_ABERTA)
        
        if response.status_code != 200:
            print("Não foi possível baixar o arquivo ZIP.")
            return 

        with open(zip_path, 'wb') as f:
            f.write(response.content)

        # Extrair os arquivos necessários
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Processar e armazenar os dados no banco de dados SQLite
        for target_file in TARGET_FILES:
            file_path = os.path.join(extract_path, target_file)
            if os.path.exists(file_path):
                # Ler os dados com pandas
                df = pd.read_csv(file_path, sep=';', encoding='latin1')
                table_name = os.path.splitext(target_file)[0]  # Nome da tabela baseado no nome do arquivo
                df.to_sql(table_name, con=engine, if_exists='replace', index=True)
            else:
                return print(f"Arquivo {target_file} não encontrado no ZIP extraído.")

        return print("Dados do Formulário de Referência importados e salvos no banco de dados com sucesso.")

    except Exception as e:
        return print("Erro ao importar arquivos.")
    finally:
        # Limpar arquivos temporários
        if os.path.exists(zip_path):
            os.remove(zip_path)
        if os.path.exists(extract_path):
            import shutil
            shutil.rmtree(extract_path)

if __name__ == "__main__":
    print("Início da importação dos dados")

    importar_dados_companhias_abertas()
    importar_dados_formulario_referencia()

    print("Todos os dados foram importados com sucesso!")
