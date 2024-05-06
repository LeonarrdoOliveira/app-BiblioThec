from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify, send_file
from app import app, db
from app.models import Usuario, Livro, Emprestimo, Aviso, EventoLeitura, Funcionario, Reserva, PrazoReserva, LivroDoacao
import qrcode
from PIL import Image
from datetime import datetime, timedelta
from collections import Counter
from flask_login import current_user, login_required

# Rotas para usuários

@app.route('/listar_usuarios')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('listar_usuarios.html', usuarios=usuarios)

@app.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        
        novo_usuario = Usuario(nome=nome, cpf=cpf, email=email, telefone=telefone, endereco=endereco)
        db.session.add(novo_usuario)
        db.session.commit()
        
        return redirect(url_for('listar_usuarios'))
    
    return render_template('cadastrar_usuario.html')

@app.route('/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
def editar_usuario(user_id):
    usuario = Usuario.query.get(user_id)
    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.cpf = request.form['cpf']
        usuario.email = request.form['email']
        usuario.telefone = request.form['telefone']
        usuario.endereco = request.form['endereco']
        db.session.commit()
        return redirect(url_for('listar_usuarios'))
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/excluir_usuario/<int:user_id>', methods=['POST'])
def excluir_usuario(user_id):
    usuario = Usuario.query.get(user_id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('listar_usuarios'))

@app.route('/dados_pessoais')
@login_required
def dados_pessoais():
    return render_template('dados_pessoais.html', usuario=current_user)

# Rotas para empréstimos e devoluções

@app.route('/emprestar_livro/<int:livro_id>/<int:user_id>', methods=['POST'])
def emprestar_livro(livro_id, user_id):
    livro = Livro.query.get(livro_id)
    usuario = Usuario.query.get(user_id)
    
    if not livro or not usuario:
        return jsonify({'message': 'Livro ou usuário não encontrado'}), 404
    
    if livro.emprestado_para:
        return jsonify({'message': 'Livro já emprestado'}), 400
    
    emprestimo = Emprestimo(usuario_id=user_id, livro_id=livro_id, data_emprestimo=datetime.utcnow())
    livro.emprestado_para = usuario
    db.session.add(emprestimo)
    db.session.commit()
    
    return jsonify({'message': 'Livro emprestado com sucesso'}), 200

@app.route('/devolver_livro/<int:emprestimo_id>', methods=['POST'])
def devolver_livro(emprestimo_id):
    emprestimo = Emprestimo.query.get(emprestimo_id)
    
    if not emprestimo:
        return jsonify({'message': 'Empréstimo não encontrado'}), 404
    
    emprestimo.livro.emprestado_para = None
    emprestimo.data_devolucao = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Livro devolvido com sucesso'}), 200

# Rotas para avisos

@app.route('/criar_aviso', methods=['POST'])
def criar_aviso():
    titulo = request.form['titulo']
    mensagem = request.form['mensagem']
    
    aviso = Aviso(titulo=titulo, mensagem=mensagem)
    db.session.add(aviso)
    db.session.commit()
    
    return jsonify({'message': 'Aviso criado com sucesso'}), 200

@app.route('/listar_avisos')
def listar_avisos():
    avisos = Aviso.query.all()
    return render_template('listar_avisos.html', avisos=avisos)

# Rotas para eventos de leitura

@app.route('/promover_evento_leitura', methods=['POST'])
def promover_evento_leitura():
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    
    evento_leitura = EventoLeitura(titulo=titulo, descricao=descricao)
    db.session.add(evento_leitura)
    db.session.commit()
    
    return jsonify({'message': 'Evento de leitura promovido com sucesso'}), 200

@app.route('/listar_eventos_leitura')
def listar_eventos_leitura():
    eventos = EventoLeitura.query.all()
    return render_template('listar_eventos_leitura.html', eventos=eventos)

# Rotas para reservas

@app.route('/reservar_livro/<int:livro_id>/<int:user_id>', methods=['POST'])
def reservar_livro(livro_id, user_id):
    livro = Livro.query.get(livro_id)
    usuario = Usuario.query.get(user_id)
    
    if not livro or not usuario:
        return jsonify({'message': 'Livro ou usuário não encontrado'}), 404
    
    reserva = Reserva(usuario_id=user_id, livro_id=livro_id, data_reserva=datetime.utcnow())
    db.session.add(reserva)
    db.session.commit()
    
    return jsonify({'message': 'Livro reservado com sucesso'}), 200

@app.route('/listar_reservas')
def listar_reservas():
    reservas = Reserva.query.all()
    return render_template('listar_reservas.html', reservas=reservas)

# Rotas para doações

@app.route('/doar_livro', methods=['POST'])
def doar_livro():
    titulo = request.form['titulo']
    autor = request.form['autor']
    descricao = request.form['descricao']
    
    livro_doacao = LivroDoacao(titulo=titulo, autor=autor, descricao=descricao)
    db.session.add(livro_doacao)
    db.session.commit()
    
    return jsonify({'message': 'Livro doado com sucesso'}), 200

@app.route('/listar_livros_doacao')
def listar_livros_doacao():
    livros_doacao = LivroDoacao.query.all()
    return render_template('listar_livros_doacao.html', livros_doacao=livros_doacao)
