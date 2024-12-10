from flask import Flask


def create_app():
    app = Flask(__name__)

    #Importa as rotas
    from .controllers.routes import main 
    app.register_blueprint(main)

    return app