from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Profissional(db.Model):
    __tablename__ = 'profissionais'
    profissional_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(80))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    agendamentos = db.relationship('Agendamento', backref='profissional')
    
    def __repr__(self):
        return f'<Profissional {self.nome}>'

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    paciente_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    agendamentos = db.relationship('Agendamento', backref='paciente')
    
    def __repr__(self):
        return f'<Paciente {self.nome}>'

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    agendamento_id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.paciente_id'), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.profissional_id'))
    data_consulta = db.Column(db.Date, nullable=False)
    hora_consulta = db.Column(db.Time, nullable=False)
    observacao = db.Column(db.Text)
    status = db.Column(db.String(20), default='pendente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Agendamento {self.paciente_id} - {self.data_consulta}>'
