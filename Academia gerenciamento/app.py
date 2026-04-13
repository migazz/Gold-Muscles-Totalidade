from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
# Chave secreta para manter a sessão (Login) segura
app.secret_key = 'chave_secreta_muito_segura_da_gold_muscles'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/gold_muscles'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== M O D E L O S (Mesmos do site original) ====================
class Plano(db.Model):
    __tablename__ = 'planos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    beneficios = db.Column(db.Text, nullable=False)

class Personal(db.Model):
    __tablename__ = 'personais'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    horarios = db.Column(db.String(255), nullable=False)
    dias = db.Column(db.String(255), nullable=False)
    imagem_url = db.Column(db.String(255), nullable=False)

class Matricula(db.Model):
    __tablename__ = 'matriculas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(20), nullable=False)
    metodo_pagamento = db.Column(db.String(50), nullable=False)
    cartao_final = db.Column(db.String(4), nullable=True) # Apenas os últimos 4 dígitos
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id'), nullable=False)
    status = db.Column(db.String(20), default="Pendente") # Novo campo!
    data_matricula = db.Column(db.DateTime, default=datetime.utcnow)
    
    plano = db.relationship('Plano', backref='matriculas')

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'dono' ou 'funcionario'

class FichaTreino(db.Model):
    __tablename__ = 'fichas_treino'
    id = db.Column(db.Integer, primary_key=True)
    matricula_id = db.Column(db.Integer, db.ForeignKey('matriculas.id'), nullable=False)
    personal_id = db.Column(db.Integer, db.ForeignKey('personais.id'), nullable=False)
    texto_treino = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    matricula = db.relationship('Matricula', backref='fichas')
    personal = db.relationship('Personal')


# ==================== L O G I N   E   S E S S Ã O ====================

def require_login():
    if 'user_id' not in session:
        return False
    return True

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        # Busca o usuário no banco
        db_user = Usuario.query.filter_by(username=user, password=pw).first()
        if db_user:
            session['user_id'] = db_user.id
            session['username'] = db_user.username
            session['role'] = db_user.role
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ==================== R O T A S   P R I N C I P A I S ====================

@app.route('/')
def dashboard():
    if not require_login(): return redirect(url_for('login'))
    
    total_alunos = Matricula.query.count()
    total_personais = Personal.query.count()
    fichas_criadas = FichaTreino.query.count()
    
    # Busca 5 alunos mais recentes
    alunos_recentes = Matricula.query.order_by(Matricula.data_matricula.desc()).limit(5).all()

    return render_template('dashboard.html', 
        total=total_alunos, p_total=total_personais, f_total=fichas_criadas, recentes=alunos_recentes)

@app.route('/alunos')
def alunos():
    if not require_login(): return redirect(url_for('login'))
    todos = Matricula.query.all()
    return render_template('alunos.html', alunos=todos)

@app.route('/alunos/aprovar/<int:id>')
def aprovar_aluno(id):
    if not require_login(): return redirect(url_for('login'))
    # Apenas o dono pode aprovar matrícula
    if session.get('role') != 'dono':
        flash('Acesso negado. Apenas diretores aprovam matrículas.', 'error')
        return redirect(url_for('alunos'))
        
    aluno = Matricula.query.get(id)
    if aluno:
        aluno.status = 'Ativo'
        db.session.commit()
        flash('Aluno aprovado e ativado!', 'success')
    return redirect(url_for('alunos'))

@app.route('/alunos/inativar/<int:id>')
def inativar_aluno(id):
    if not require_login(): return redirect(url_for('login'))
    if session.get('role') != 'dono':
        flash('Acesso negado. Apenas diretores inativam alunos.', 'error')
        return redirect(url_for('alunos'))
        
    aluno = Matricula.query.get(id)
    if aluno:
        aluno.status = 'Inativo'
        db.session.commit()
        flash(f'Aluno {aluno.nome} desativado.', 'success')
    return redirect(url_for('alunos'))

@app.route('/alunos/deletar/<int:id>')
def deletar_aluno(id):
    if not require_login(): return redirect(url_for('login'))
    if session.get('role') != 'dono':
        flash('Acesso negado.', 'error')
        return redirect(url_for('alunos'))
        
    aluno = Matricula.query.get(id)
    if aluno:
        try:
            # Primeiro, removemos todas as fichas de treino vinculadas a este aluno
            # Isso evita o erro de "IntegrityError" (chave estrangeira)
            FichaTreino.query.filter_by(matricula_id=id).delete()
            
            # Agora sim, deletamos o aluno
            db.session.delete(aluno)
            db.session.commit()
            flash('Aluno e todo o seu histórico de treinos foram removidos permanentemente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao deletar: {str(e)}', 'error')
            
    return redirect(url_for('alunos'))



@app.route('/personais', methods=['GET', 'POST'])
def personais():
    if not require_login(): return redirect(url_for('login'))
    
    if request.method == 'POST':
        if session.get('role') != 'dono':
            flash('Apenas donos podem cadastrar novos personais.', 'error')
        else:
            p = Personal(
                nome=request.form['nome'],
                descricao=request.form['descricao'],
                horarios=request.form['horarios'],
                dias=request.form['dias'],
                imagem_url=request.form['imagem_url'] # ex: lucas.jpg
            )
            db.session.add(p)
            db.session.commit()
            flash('Personal cadastrado. Já está visível no site principal!', 'success')
            return redirect(url_for('personais'))
            
    lista = Personal.query.all()
    return render_template('personais.html', personais=lista)

@app.route('/personais/deletar/<int:id>')
def deletar_personal(id):
    if not require_login(): return redirect(url_for('login'))
    if session.get('role') != 'dono':
        flash('Acesso negado.', 'error')
        return redirect(url_for('personais'))
        
    p = Personal.query.get(id)
    if p:
        # Verifica se o personal tem fichas de treino vinculadas antes de deletar
        # Caso tenha, a deleção falharia pelo banco de dados (chave estrangeira)
        # Vamos apenas deletar. Se falhar, avisamos.
        try:
            db.session.delete(p)
            db.session.commit()
            flash(f'Treinador {p.nome} removido do quadro de funcionários.', 'success')
        except:
            db.session.rollback()
            flash('Não é possível remover este personal pois ele possui fichas de treino ativas vinculadas a alunos.', 'error')
            
    return redirect(url_for('personais'))


@app.route('/fichas', methods=['GET', 'POST'])
def fichas():
    if not require_login(): return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Dono e Funcionário podem criar fichas
        nova_ficha = FichaTreino(
            matricula_id=request.form['matricula_id'],
            personal_id=request.form['personal_id'],
            texto_treino=request.form['texto_treino']
        )
        db.session.add(nova_ficha)
        db.session.commit()
        flash('Ficha de treino anexada ao aluno com sucesso!', 'success')
        return redirect(url_for('fichas'))
        
    todas_fichas = FichaTreino.query.order_by(FichaTreino.data_criacao.desc()).all()
    alunos = Matricula.query.filter_by(status='Ativo').all() # Só faz ficha pra ativo
    personais_list = Personal.query.all()
    
    return render_template('fichas.html', fichas=todas_fichas, alunos=alunos, personais=personais_list)

if __name__ == '__main__':
    # Roda o app de gerenciamento na porta 5001 para não bater com o 5000 do site dos alunos
    with app.app_context():
        # db.drop_all() # Comentado após a primeira execução bem sucedida
        db.create_all()

        
        # Re-insere dados iniciais (planos e personais do site)
        if not Plano.query.first():
            p1 = Plano(nome='Plano Silver', valor=89.90, beneficios='Acesso à musculação; Armário rotativo; App de treino')
            p2 = Plano(nome='Plano Gold', valor=129.90, beneficios='Musculação total; Aulas coletivas; Leve um amigo 4x/mês; Área VIP')
            p3 = Plano(nome='Plano Muscle VIP', valor=199.90, beneficios='Personal trainer 1x semana; Avaliação física mensal; Brinde exclusivo; Acesso ilimitado')
            db.session.add_all([p1, p2, p3])
            
            per1 = Personal(nome='Ricardo Silva', descricao='Especialista em hipertrofia.', horarios='06:00 - 12:00', dias='Seg, Qua, Sex', imagem_url='ricardo.jpg')
            per2 = Personal(nome='Elize Santos', descricao='Especialista em funcional.', horarios='14:00 - 20:00', dias='Ter, Qui, Sáb', imagem_url='elize.webp')
            db.session.add_all([per1, per2])
            db.session.commit()
        
        # Garante que os usuários existam
        if not Usuario.query.filter_by(username="dono").first():
            db.session.add(Usuario(username="dono", password="123", role="dono"))
        if not Usuario.query.filter_by(username="func").first():
            db.session.add(Usuario(username="func", password="123", role="funcionario"))
        if not Usuario.query.filter_by(username="colab").first():
            db.session.add(Usuario(username="colab", password="123", role="colaborador")) # Novo Usuário
        db.session.commit()



            
    app.run(port=5001, debug=True)
