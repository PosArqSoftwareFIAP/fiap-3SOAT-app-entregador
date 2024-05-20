from flask import Flask,jsonify,request
import mysql.connector
import os
import sys
from cliente import cliente_bp
from restaurante import restaurante_bp
from entregador import entregador_bp
from avaliacao import avaliacao_bp
from pedido import pedido_bp
from produto import produto_bp
from fatura import fatura_bp
from flask_restx import Api, Resource
from flasgger import Swagger
from functools import wraps
from db import db_mysql_class

   



   


def token_required(f):
    
    token = None

    if 'Authorization' in request.headers:
        if request.headers['Authorization']:
            token = request.headers['Authorization'].split(" ")[1]

    if not token:
        return jsonify({'message': 'Token is missing!'}), 403

    try:
        db_objt = db_mysql_class()
        connection = db_objt.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT user FROM bearer_token WHERE bearer_token = %s", (token,))
        user = cursor.fetchone()

        if not user:

            return jsonify({'message': 'Token is invalid!'}), 403
    finally:
        cursor.close()
        connection.close()

    return


#Criar uma instância do Flask
app = Flask(__name__)
swagger = Swagger(app)
api = Api(app, version='1.0', title='FIAP-FOOD', description='API sobre o entregavel da pós', doc='/swagger/')

@app.before_request
def before_request():
    if request.path == '/apidocs/' or '/flasgger_static/':
        return
    token_func = token_required(lambda: None)
    return token_func

app.register_blueprint(cliente_bp)
app.register_blueprint(restaurante_bp)
app.register_blueprint(entregador_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(pedido_bp)
app.register_blueprint(avaliacao_bp)
app.register_blueprint(fatura_bp)




#Definir uma rota para a página inicial
@app.route('/')
def hello_world():
    return 'Hello, World!'



#Iniciar o aplicativo se este arquivo for executado diretamente
if __name__ == '__main__':
    app.run()



