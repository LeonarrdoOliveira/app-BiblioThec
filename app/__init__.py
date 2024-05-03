from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bibliotech.db'  # Configuração do banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa o rastreamento de modificações
db = SQLAlchemy(app)

# Importa as rotas da aplicação
from app import routes

# Criar uma instância do Flask-Mail
mail = Mail(app)

# Cria as tabelas do banco de dados (apenas para desenvolvimento)
db.create_all()
