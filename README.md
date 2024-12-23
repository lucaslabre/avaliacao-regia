# Passos para rodar os scripts de importação

1. Criar ambiente virtual
    - ```python -m venv venv```
2. Ativar virtual env
    - Windows: ```.\venv\Scripts\activate```
    - Linux: ```source venv/bin/activate```
3. Instalar requisitos da aplicação
    - ```pip install -r .\requirements.txt```
4. Inicializar a aplicação
    - ```python .\script_import\import_data.py```

# Passos para executar a aplicação web.

1. Executar a aplicação Flask
    - ```python .\run.py```

2. Abrir o navegador
    - http://127.0.0.1:5000

# Tecnologias utilizadas

* flask 
* pandas 
* requests
* dash