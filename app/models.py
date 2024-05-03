from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    editora = db.Column(db.String(100))
    num_paginas = db.Column(db.Integer)
    categoria = db.Column(db.String(100))

from datetime import datetime  # Adicione esta linha para corrigir o erro

class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=False)
    data_emprestimo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_devolucao = db.Column(db.DateTime)

    usuario = db.relationship('Usuario', backref=db.backref('emprestimos', lazy=True))
    livro = db.relationship('Livro', backref=db.backref('emprestimos', lazy=True))


from app import db

class MaterialAvariado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_avaria = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"MaterialAvariado('{self.titulo}', '{self.data_avaria}')"

# No arquivo app/models.py

from app import db

class PedidoRecurso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_pedido = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pendente')

    def __repr__(self):
        return f"PedidoRecurso('{self.titulo}', '{self.descricao}', '{self.data_pedido}', '{self.status}')"

from app import db

class Aviso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Aviso('{self.titulo}', '{self.conteudo}')"

from app import db

class LivroDoacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    editora = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"LivroDoacao('{self.titulo}', '{self.autor}', '{self.editora}', '{self.status}')"

from app import db

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=False)
    data_reserva = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Reserva('{self.usuario_id}', '{self.livro_id}', '{self.data_reserva}')"

from app import db

class UsuarioLeitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    data_suspensao = db.Column(db.DateTime)

    def __repr__(self):
        return f"UsuarioLeitor('{self.nome}', '{self.cpf}', '{self.email}')"

from app.models import Funcionario

@app.route('/excluir_funcionario/<int:user_id>', methods=['POST'])
def excluir_funcionario(user_id):
    funcionario = Funcionario.query.get(user_id)
    if not funcionario:
        return jsonify({'error': 'Funcionário não encontrado'}), 404
    
    db.session.delete(funcionario)
    db.session.commit()
    
    return jsonify({'message': f'Funcionário {funcionario.nome} excluído com sucesso'}), 200

from app import db

class PrazoReserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prazo = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"PrazoReserva('{self.prazo}')"

from app import db

class EventoLeitura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"EventoLeitura('{self.titulo}', '{self.descricao}', '{self.data}')"


#Gerar imagens e QRCode para carteirinhas

from PIL import Image, ImageDraw, ImageFont
import qrcode

def gerar_carteirinha(usuario):
    # Lógica para gerar a carteirinha com foto e QR code
    # Aqui você pode usar bibliotecas como Pillow para manipulação de imagens e qrcode para gerar QR codes
    # Este é apenas um exemplo simples, você precisará adaptá-lo de acordo com suas necessidades
    
    # Cria uma nova imagem em branco
    img = Image.new('RGB', (600, 400), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    
    # Adiciona texto e imagem (exemplo)
    font = ImageFont.truetype("arial.ttf", 36)
    d.text((10,10), f"Nome: {usuario.nome}", fill=(0,0,0), font=font)
    d.text((10,60), f"CPF: {usuario.cpf}", fill=(0,0,0), font=font)
    # Adiciona a foto do usuário (exemplo)
    # d.text((10,110), "Foto:", fill=(0,0,0), font=font)
    # img.paste(usuario.foto, (10, 160))  # Exemplo: usuário.foto é a imagem da foto do usuário
    
    # Gera um QR code com o ID do usuário (exemplo)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"http://example.com/user/{usuario.id}")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    img.paste(qr_img, (400, 10))
    
    # Salva a imagem gerada
    img.save(f"carteirinha_{usuario.id}.png")
