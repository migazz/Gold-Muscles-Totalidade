from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Configuração da conexão com o banco de dados MySQL (XAMPP root sem senha)
# 'mysql+pymysql://usuário:senha@host/nome_do_banco'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/gold_muscles'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy para lidar com o banco de dados
db = SQLAlchemy(app)

# Classe (Modelo) para a tabela de Planos
class Plano(db.Model):
    __tablename__ = 'planos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    beneficios = db.Column(db.Text, nullable=False)

    def get_beneficios_list(self):
        """Retorna os benefícios como uma lista para facilitar no HTML"""
        return self.beneficios.split(';')

# Classe (Modelo) para a tabela de Personais
class Personal(db.Model):
    __tablename__ = 'personais'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    horarios = db.Column(db.String(255), nullable=False)
    dias = db.Column(db.String(255), nullable=False)
    imagem_url = db.Column(db.String(255), nullable=False)

# Classe (Modelo) para a tabela de Matriculas recebidas via Modal
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
    data_matricula = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="Pendente") # Novo campo para o gerenciamento

# --- Novos modelos para o Sistema de Gerenciamento ---

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


@app.route('/')
def index():
    """
    Função principal que renderiza a página inicial.
    Ela busca todos os planos e personais no banco de dados e os envia para o template.
    """
    try:
        # Busca todas as linhas das tabelas planos e personais
        todos_planos = Plano.query.all()
        todos_personais = Personal.query.all()
        
        # Renderiza o arquivo templates/index.html passando os dados do banco
        return render_template('index.html', planos=todos_planos, personais=todos_personais)
    except Exception as e:
        # Caso o banco de dados ainda não tenha sido configurado no XAMPP, mostra uma mensagem amigável
        return f"Erro ao conectar ao banco de dados: {e}. Certifique-se de rodar o arquivo database.sql no seu HeidiSQL e que o MySQL do XAMPP esteja ligado."

@app.route('/api/matricular', methods=['POST'])
def api_matricular():
    """
    Rota invocada pelo Javascript sem recarregar a página (AJAX).
    Recebe os dados do modal e cria uma nova matrícula no banco.
    """
    try:
        dados = request.get_json()
        
        # Lógica de Segurança: Se for cartão, salva apenas o final
        final_cartao = None
        if dados.get('numero_cartao'):
            # Pega apenas os últimos 4 dígitos e limpa espaços
            limpo = str(dados['numero_cartao']).replace(" ", "")
            final_cartao = limpo[-4:]

        nova_matricula = Matricula(
            nome=dados['nome'],
            email=dados['email'],
            telefone=dados['telefone'],
            cpf=dados['cpf'],
            metodo_pagamento=dados['metodo_pagamento'],
            cartao_final=final_cartao,
            plano_id=int(dados['plano_id'])
        )
        db.session.add(nova_matricula)
        db.session.commit()
        return jsonify({"success": True, "message": "Matrícula pré-aprovada! Compareça à recepção."}), 200
    except Exception as e:

        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    # Cria as tabelas automaticamente (se ainda não existirem no BD)
    with app.app_context():
        # db.drop_all()  <- REMOVIDO para que o site gerencial não se perca
        db.create_all()

        
        # Reinserindo dados iniciais (já que demos drop_all)
        if not Plano.query.first():
            p1 = Plano(nome='Plano Silver', valor=89.90, beneficios='Acesso à musculação; Armário rotativo; App de treino')
            p2 = Plano(nome='Plano Gold', valor=129.90, beneficios='Musculação total; Aulas coletivas; Leve um amigo 4x/mês; Área VIP')
            p3 = Plano(nome='Plano Muscle VIP', valor=199.90, beneficios='Personal trainer 1x semana; Avaliação física mensal; Brinde exclusivo; Acesso ilimitado')
            db.session.add_all([p1, p2, p3])
            
            per1 = Personal(nome='Ricardo Silva', descricao='Especialista em hipertrofia.', horarios='06:00 - 12:00', dias='Seg, Qua, Sex', imagem_url='ricardo.jpg')
            per2 = Personal(nome='Elize Santos', descricao='Especialista em funcional.', horarios='14:00 - 20:00', dias='Ter, Qui, Sáb', imagem_url='elize.webp')
            db.session.add_all([per1, per2])
            db.session.commit()
        
    # Roda o servidor web na porta 5000 em modo debug para facilitar o desenvolvimento
    app.run(debug=True)

