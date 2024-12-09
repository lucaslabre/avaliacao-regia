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

# Tecnologias utilizadas

* flask 
* pandas 
* requests
* sqlalchemy